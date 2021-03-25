from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Contact, Activity
from .models import Configuration, AvatarImage, Avatar, Industry, CustomerIndustries, Currency, CustomerCurrencies
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from api.models import *
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ContactInline(admin.StackedInline):
    model = Contact
    can_delete = False
    verbose_name_plural = 'contacts'


class ActivityInline(admin.StackedInline):
    model = Activity
    can_delete = False
    verbose_name_plural = 'activity'


class ConfigurationInline(admin.StackedInline):
    model = Configuration
    can_delete = False
    verbose_name_plural = 'configuration'


class IndustryInLine(admin.StackedInline):
    # class Media:
    #     js = (
    #         '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',      # project static folder
    #         'webapp/js/industries.js',   # app static folder
    #     )

    model = Industry
    can_delete = False
    verbose_name_plural = 'Industry'


class CurrencyInLine(admin.StackedInline):

    model = Currency
    can_delete = False
    verbose_name_plural = 'Currency'


class AvatarInline(admin.StackedInline):
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',      # project static folder
            'webapp/js/custom.js',   # app static folder
        )

    model = Avatar
    can_delete = False
    verbose_name_plural = 'avatar'
    readonly_fields = ["avatar_image"]

    def avatar_image(self, obj):
        img = ''
        av = AvatarImage.objects.get(images=img)
        return mark_safe('<img src="{}" width="100px" height="100" />'.format(av.images.url))


class AvatarImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'images', 'image_tag']
    readonly_fields = ["avatar_image"]

    def avatar_image(self, obj):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(obj.images.url))

    def image_tag(self, obj):
        print(obj.images)
        return format_html('<img src="{}" width="30" height="30" />'.format(obj.images.url))

    image_tag.short_description = 'image_tag'



# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (
                ContactInline,
                ActivityInline,
                ConfigurationInline,
                AvatarInline,
                IndustryInLine,
                CurrencyInLine
            )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(AvatarImage, AvatarImagesAdmin)
admin.site.register(Reports)
admin.site.register(CustomerIndustries)
admin.site.register(CustomerCurrencies)

