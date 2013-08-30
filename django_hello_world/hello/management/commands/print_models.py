from django.core.management.base import BaseCommand
from django.db import models
import sys


class Command(BaseCommand):
    def handle(self, *args, **options):
        report = []
        models_dict = self.project_models()
        for key, value in models_dict.items():
            report.append("%s: %d\n" % (key.__name__, value))
        sys.stdout.write(''.join(report))
        sys.stderr.write(''.join(['error: ' + item for item in report]))

    def project_models(self):
        result = {}
        all_models = models.get_models()
        for model in all_models:
            result[model] = model.objects.count()
        return result
