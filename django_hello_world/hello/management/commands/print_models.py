from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model_type in ContentType.objects.all():
            s = '%s_%s - %d\n' % (
                model_type.app_label,
                model_type.model,
                model_type.model_class().objects.count())
            self.stdout.write(s)
            self.stderr.write('Error: %s' % s)
