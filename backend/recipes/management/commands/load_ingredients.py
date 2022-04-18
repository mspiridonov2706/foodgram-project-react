from django.core.management.base import BaseCommand

import json
from pathlib import Path
from ...models import Ingredients


class Command(BaseCommand):
    '''Load data from csv file.'''
    def get_root_path(self):
        return Path(__file__).parent.parent.parent.parent.parent

    def handle(self, *args, **options):
        path = self.get_root_path()
        with open(str(path) + '/data/ingredients.json', encoding='utf-8') as f:
            json_data = json.loads(f.read())
        for ingredient in json_data:
            Ingredients.objects.create(**ingredient)
        self.stdout.write(self.style.SUCCESS(
            'Data in "ingredients" table is created.')
        )
