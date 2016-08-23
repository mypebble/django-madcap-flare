"""Tests for Madcap Flare.
"""
from unittest import TestCase
from mock import patch

from django.core.exceptions import ImproperlyConfigured

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
