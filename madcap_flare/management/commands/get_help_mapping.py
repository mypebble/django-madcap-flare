"""Turn the MCF .h file into a help mapping and print it out.
"""
from argparse import FileType
from pprint import pformat

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Run the command.
    """

    help = u'Parse an MCF .h file and output a dict.'

    def add_arguments(self, parser):
        """Parse.
        """
        parser.add_argument(
            'header', type=FileType('r'), help='Header file to read from.')

    def handle(self, *args, **options):
        """Run the command.
        """
        content = options['header'].read()

        lines = content.splitlines()
        data_dict = dict(line[1:3] for line in lines)
        self.stdout.write(pformat(data_dict))
