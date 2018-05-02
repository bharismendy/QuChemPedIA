from django.apps import AppConfig


class QuchempediaConfig(AppConfig):
    name = 'QuChemPedIA'

    def ready(self):
        import QuChemPedIA.signals
