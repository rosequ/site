from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from captcha.fields import ReCaptchaField

from prologin.models import Gender
from .widgets import PreviewFileInput

User = get_user_model()


class UserProfileForm(forms.ModelForm):
    readonly_during_contest = ('first_name', 'last_name', 'address', 'birthday',
                               'postal_code', 'city', 'country',)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'birthday',
                  'address', 'postal_code', 'city', 'country',
                  'phone', 'email', 'allow_mailing',
                  'preferred_language', 'school_stage', 'timezone',
                  'preferred_locale', 'avatar', 'picture',)
        widgets = {
            'avatar': PreviewFileInput(image_attrs={'style': 'max-width: 90px; max-height: 90px;'}),
            'picture': PreviewFileInput(image_attrs={'style': 'max-width: 90px; max-height: 90px;'}),
            'gender': forms.RadioSelect(),
            'address': forms.Textarea(attrs=dict(rows=2)),
        }

    def __init__(self, *args, **kwargs):
        self.is_contest = kwargs.pop('is_contest', False)
        super().__init__(*args, **kwargs)
        self.fields['gender'].required = False
        self.fields['gender'].label = _("How do you prefer to be described?")
        self.fields['gender'].choices = [
            (Gender.female.value, mark_safe(_("<em>She is writing code for the contest</em>"))),
            (Gender.male.value, mark_safe(_("<em>He is writing code for the contest</em>"))),
            ("", _("Other or prefer not to tell")),
        ]
        if self.is_contest:
            for field in self.readonly_during_contest:
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                self.fields[field].help_text = _("You can not change your details during the contest. If there is an "
                                                 "important change you want to make, please contact the staff.")

        if not self.instance.team_memberships.count():
            # If not part of any team, makes no sense to add a staff picture
            self.fields.pop('picture', None)

    def clean(self):
        if self.is_contest:
            for field in self.readonly_during_contest:
                self.cleaned_data.pop(field, None)
        return super().clean()


class RegisterForm(forms.ModelForm):
    captcha = ReCaptchaField(label="",
                             help_text='<small>{}</small>'.format(
                                 _("Please check the box above and complete the additional tasks if any. "
                                   "This is required to fight spamming bots on the website.")))

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'allow_mailing', 'captcha')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_username(self):
        if User.objects.filter(username__iexact=self.cleaned_data['username']):
            raise forms.ValidationError(_("This username is already in use. "
                                          "Please supply a different username."))
        return self.cleaned_data['username'].strip().lower()

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. "
                                          "Please supply a different email address."))
        return self.cleaned_data['email'].strip().lower()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254, required=True,
                             widget=forms.EmailInput(attrs={'placeholder': _("Your email address")}))


class ProloginAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _("Username or email")
        self.fields['username'].help_text = _("This field is case insensitive. It means capitals and small letters are "
                                              "considered to be equal.")
        self.error_messages['invalid_login'] = _("Please enter a correct username (or email) and password.")


class ImpersonateForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True, is_superuser=False),
                                  required=False, empty_label='', widget=forms.HiddenInput())
    username = forms.CharField(required=False)

    @classmethod
    def search_users(cls, query):
        """
        Token-based search of a user to impersonate.
        If there are users whose fields *starts with* query tokens, they are returned immediately.
        If there is no result, we try harder by searching fields that *contains* tokens.
        :type query: query string to search for
        :return a Queryset of matching users (can be empty)
        """
        from itertools import product, combinations, permutations

        qs = cls.base_fields['user'].queryset
        # limit to 4 tokens, as the combinatorics are explosive (24 clauses for 4 tokens, 60 for 5)
        tokens = [token for token in query.split() if len(token) >= 2][:4]
        if not tokens:
            return qs.none()

        fields = ('username', 'first_name', 'last_name', 'email')
        r = min(len(tokens), len(fields))

        def build(operator):
            q = Q()
            for keys, values in product(combinations(fields, r=r), permutations(tokens, r=r)):
                q |= Q(**{'{}__{}'.format(key, operator): value for key, value in zip(keys, values)})
            return q

        res = qs.filter(build('istartswith'))
        if res.exists():
            return res

        return qs.filter(build('icontains'))

    def clean(self):
        # provided by Javascript in the hidden field
        user = self.cleaned_data.get('user')
        if not user:
            # graceful degradation if no JS: use plain text input as query & take first result
            username = self.cleaned_data.get('username', '').strip()
            if not username:
                raise ValidationError(_("you must provide a username."))
            user = ImpersonateForm.search_users(username).first()
        if not user:
            raise ValidationError(_("no user matches your query."))
        self.cleaned_data['user'] = user
