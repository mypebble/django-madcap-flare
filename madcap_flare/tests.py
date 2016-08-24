"""Tests for Madcap Flare.
"""
from StringIO import StringIO
from os import path
from unittest import TestCase

from mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command

from madcap_flare.templatetags import madcap_flare_tags as tags


class TemplateTagTestCase(TestCase):
    """Test the template tags for the MCF integration.
    """

    def test_templatetag(self):
        """The template tag should load a URL with cshid.
        """
        output = tags.madcap_flare_help({'help_key': 'test-flare'})
        self.assertEqual(output, 'http://example.com/Default.htm#cshid=1011')

    def test_unset_key(self):
        """If the help_key isn't in settings, raise an error.
        """
        context = {'help_key': 'unused-key'}
        self.assertRaises(
            ImproperlyConfigured,
            tags.madcap_flare_help,
            context)

    @patch('madcap_flare.templatetags.madcap_flare_tags.settings')
    def test_missing_root_setting(self, settings):
        """MADCAP_FLARE_ROOT is missing, raise an error.
        """
        def _error(*args, **kwargs):
            raise AttributeError

        settings.MADCAP_FLARE_ROOT.side_effect = _error

        self.assertRaises(
            ImproperlyConfigured,
            tags.madcap_flare_help,
            {'help_key': 'test-flare'})

    @patch('madcap_flare.templatetags.madcap_flare_tags.settings')
    def test_missing_tags_settings(self, settings):
        """If MADCAP_FLARE_TAGS is missing, raise an error.
        """
        def _error(*args, **kwargs):
            raise AttributeError

        settings.MADCAP_FLARE_TAGS.side_effect = _error

        self.assertRaises(
            ImproperlyConfigured,
            tags.madcap_flare_help,
            {'help_key': 'test-flare'})


class CommandTestCase(TestCase):
    """Test the get_help_mapping management command.
    """

    def test_clean_file(self):
        """Get a clean .h file.
        """
        output = u"""{\n    'test-flare': '1011'\n}\n"""
        file_path = path.abspath(
            path.join(path.dirname(__file__), 'fixtures/madcap_flare/clean.h'))
        fake_stdout = StringIO()
        call_command('get_help_mapping', file_path, stdout=fake_stdout)
        self.assertEqual(fake_stdout.getvalue(), output)

    def test_get_dirty(self):
        """Still works even if tabs/spaces mixed up.
        """
        output = u"""{\n    'uses-tabs': '1011'\n}\n"""
        file_path = path.abspath(
            path.join(path.dirname(__file__), 'fixtures/madcap_flare/dirty.h'))
        fake_stdout = StringIO()
        call_command('get_help_mapping', file_path, stdout=fake_stdout)
        self.assertEqual(fake_stdout.getvalue(), output)
