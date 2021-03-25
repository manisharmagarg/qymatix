from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


class MyRegistrationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    # username = forms.CharField(\
    # label=_("Email"),
    # )

    username = forms.EmailField( \
        label=_("Email"),
        widget=forms.EmailInput \
        )

    first_name = forms.CharField( \
        label=_("first_name"),
    )

    last_name = forms.CharField( \
        label=_("last_name"),
    )

    # email = forms.EmailField(\
    # label=_("Email"),
    # widget=forms.PasswordInput\
    # )

    terms = forms.BooleanField( \
        error_messages={'required': 'You must accept the terms and conditions'}, \
        label="Terms&Conditions" \
        )

    password1 = forms.CharField( \
        label=_("Password"),
        widget=forms.HiddenInput,
        # widget=forms.PasswordInput\
    )

    password2 = forms.CharField( \
        label=_("Password confirmation"),
        # widget=forms.PasswordInput,
        widget=forms.HiddenInput,
        help_text=_("Enter the same password as above, for verification.") \
        )

    class Meta:
        model = User
        # exclude = ["password1", "password2"]
        exclude = ['email']
        fields = ("username", \
                  'first_name', \
                  'last_name', \
                  # "email",\
                  "password1", \
                  "password2", \
                  )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def password_match(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise Exception({'password_mismatch': True})
        return password2

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)

        # user.email = self.cleaned_data['email']
        user.email = user.username

        domains = [
            "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com",
            "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
            "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk",
            "email.com", "fastmail.fm", "games.com", "gmx.net", "hush.com", "hushmail.com", "icloud.com",
            "iname.com", "inbox.com", "lavabit.com", "love.com", "outlook.com", "pobox.com", "protonmail.com",
            "rocketmail.com", "safe-mail.net", "wow.com", "ygm.com",
            "ymail.com", "zoho.com", "yandex.com",
            "bellsouth.net", "charter.net", "cox.net", "earthlink.net", "juno.com",
            "btinternet.com", "virginmedia.com", "blueyonder.co.uk", "freeserve.co.uk", "live.co.uk",
            "ntlworld.com", "o2.co.uk", "orange.net", "sky.com", "talktalk.co.uk", "tiscali.co.uk",
            "virgin.net", "wanadoo.co.uk", "bt.com",
            "sina.com", "qq.com", "naver.com", "hanmail.net", "daum.net", "nate.com", "yahoo.co.jp", "yahoo.co.kr",
            "yahoo.co.id", "yahoo.co.in", "yahoo.com.sg", "yahoo.com.ph",
            "hotmail.fr", "live.fr", "laposte.net", "yahoo.fr", "wanadoo.fr", "orange.fr", "gmx.fr", "sfr.fr",
            "neuf.fr", "free.fr",
            "gmx.de", "hotmail.de", "live.de", "online.de", "t-online.de", "web.de", "yahoo.de",
            "libero.it", "virgilio.it", "hotmail.it", "aol.it", "tiscali.it", "alice.it", "live.it", "yahoo.it",
            "email.it", "tin.it", "poste.it", "teletu.it",
            "mail.ru", "rambler.ru", "yandex.ru", "ya.ru", "list.ru",
            "hotmail.be", "live.be", "skynet.be", "voo.be", "tvcablenet.be", "telenet.be",
            "hotmail.com.ar", "live.com.ar", "yahoo.com.ar", "fibertel.com.ar", "speedy.com.ar", "arnet.com.ar",
            "yahoo.com.mx", "live.com.mx", "hotmail.es", "hotmail.com.mx", "prodigy.net.mx",
            "yahoo.com.br", "hotmail.com.br", "outlook.com.br", "uol.com.br", "bol.com.br", "terra.com.br", "ig.com.br",
            "itelefonica.com.br", "r7.com", "zipmail.com.br", "globo.com", "globomail.com", "oi.com.br"
        ]

        if '@' not in user.email or any(d in user.email.split('@')[1] for d in domains):
            raise Exception({'invalid_email': True})

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise Exception({'password_mismatch': True})

        # userName = user.email.replace("@", "__")
        # user.username = userName.replace(".", "_")
        # username = user.email.split("@")[0]
        username = user.email.replace("@", "__")
        user.username = username.replace(".", "_").replace("-", "___")

        user.set_password(self.cleaned_data["password1"])

        # password = User.objects.make_random_password()
        # user.set_password(password)

        if commit:
            user.save()
        return user
