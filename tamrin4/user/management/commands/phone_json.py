from django.conf import settings
from django.core.management import BaseCommand
from user.models import MyUser
from django.core import serializers


class Command(BaseCommand):
    help = "give phone numbers in json"

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)
        parser.add_argument('--name', type=str)

    def handle(self, *args, **options):
        qs = MyUser.objects.filter(user=options['user_id'])

        if qs:
            if options['name']:
                file_name = options['name']
            else:
                file_name = options["user_id"]
            qs_json = serializers.serialize('json', qs)
            with open(f'{file_name}.json', 'w') as file:
                file.write(qs_json)
        else:
            print('user not found.')
