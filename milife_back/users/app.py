from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class UsersConfig(AppConfig):
    name = 'milife_back.users'
    verbose_name = _('Users')

    def ready(self):
        import milife_back.users.signals  # noqa
