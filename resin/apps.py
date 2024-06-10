from django.contrib.admin.apps import AdminConfig


class ResinAdminConfig(AdminConfig):
    default_site = "resin.admin.ResinAdminSite"
