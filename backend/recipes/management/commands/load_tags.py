from django.core.management.base import BaseCommand

import json
from pathlib import Path
from ...models import Tags


class Command(BaseCommand):
    '''Load data from csv file.'''
    def get_root_path(self):
        return Path(__file__).parent.parent.parent.parent.parent

    def handle(self, *args, **options):
        path = self.get_root_path()
        with open(str(path) + '/data/tags.json', encoding='utf-8') as f:
            json_data = json.loads(f.read())
        for tag in json_data:
            Tags.objects.create(**tag)
        self.stdout.write(self.style.SUCCESS(
            'Data in "tags" table is created.')
        )
