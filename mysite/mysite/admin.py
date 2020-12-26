# from django.contrib.admin import AdminSite as admin
from django.contrib import admin
from django.contrib.admin import AdminSite


# reference on admin-site
# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#overriding-default-admin-site


# admin.site_header = 'Guardian BI Cards Portal admin'
# django.contrib.admin.AdminSite.site_header = 'sdkjfdsfgsdjhfghdsgh'

class MySiteAdmin(django.contrib.admin.AdminSite):
    site_header = 'Guardian BI Cards Portal admin 03'

# admin_site = MySiteAdmin()

