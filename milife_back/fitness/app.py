from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class FitnessConfig(AppConfig):
    name = 'milife_back.fitness'
    verbose_name = _('fitness')

    def ready(self):
        import milife_back.fitness.signals  # noqa
