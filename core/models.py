from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import Group

class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100, default='Not defined')
    department = models.CharField(max_length=100, default='Not defined')
    telephone = models.CharField(max_length=100, default='Not defined')
    address = models.CharField(max_length=100, default='Not defined')
    postcode = models.CharField(max_length=100, default='Not defined')
    city = models.CharField(max_length=100, default='Not defined')
    country = models.CharField(max_length=100, default='Not defined')
    vat = models.CharField(max_length=100, default='Not defined')


class Activity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastUpload = models.CharField(max_length=100, default='Not defined')
    lastFileUploaded = models.CharField(max_length=100, default='Not defined')


class Configuration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    ACCOUNT_TYPE = (
        ('admin', 'Administrator'),
        ('standard', 'Standard'),
        ('basic', 'Basic')
    )
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE, default='standard')

    LANGUAGES = (
        ('en', 'English'),
        ('de', 'Deutsch'),
    )
    language = models.CharField(max_length=2, choices=LANGUAGES, default='en')

    PLANS = (
        ('basic', 'Basic'),
        ('pro', 'Professional'),
        ('advanced', 'Advanced'),
        ('crm', 'CRM'),
        ('developer', 'Developer'),
        ('controller', 'Controller'),
    )
    plan = models.CharField(max_length=10, choices=PLANS, default='basic')

    token = models.CharField(max_length=100, default='Not defined')


class AvatarImage(models.Model):
    images = models.ImageField(null=True, blank=True, upload_to="images/avatar/")

    def __str__(self):
        img_data = str(self.images)
        img = img_data[14:]
        return img


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Avatar_image = models.ForeignKey(AvatarImage, on_delete=models.CASCADE)


class CustomerIndustries(models.Model):
    industries_name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.industries_name)
    
    class Meta:
        verbose_name_plural = "Customer Industries"


class Industry(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    industries_name = models.ForeignKey(CustomerIndustries, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.industries_name)

    class Meta:
        verbose_name_plural = "Industry"


class CustomerCurrencies(models.Model):
    currencies_name = models.CharField(max_length=350, default='€', null=False, blank=False)

    def __str__(self):
        return str(self.currencies_name)
    
    class Meta:
        verbose_name_plural = "Customer Currencies"



Group.add_to_class('industries_name', models.TextField(blank=True, null=True))
# Group.add_to_class('currencies', models.ManyToManyField(Currency, blank=True))


class Currency(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currencies_name = models.ForeignKey(CustomerCurrencies, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.currencies_name)

    class Meta:
        verbose_name_plural = "Currency"


CHOICE_LIST = (
    ('CHF', 'Swiss Franc'),
    ('€', 'Euro'),
    ('£', 'British Pound Sterling'),
    ('$', 'US Dollar'),
    ('RUB', 'Russian Ruble'),
    ('¥', 'Japanese Yen')
)

#     currency = models.CharField(
#         max_length=350, default='€', 
#         choices=CHOICE_LIST, verbose_name='currency'
#     )


Group.add_to_class('currencies_name', 
    models.CharField(
        max_length=350, default='€', 
        choices=CHOICE_LIST, verbose_name='currency'
    )
)

