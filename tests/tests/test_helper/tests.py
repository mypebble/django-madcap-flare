"""Tests for Madcap Flare.
"""
from unittest import TestCase

from django.core.exceptions import ImproperlyConfigured

from madcap_flare.templatetags import madcap_flare_tags as tags


class TemplateTagTestCase(TestCase):
    """Test the template tags for the MCF integration.
    """

    def test_templatetag(self):
        """The template tag should load a URL with cshid.
        """
        output = tags.madcap_flare_help({'help_key': 'test-flare'})
        self.assertEqual(output, 'http://example.com/Default.html#1011')

    def test_unset_key(self):
        """If the help_key isn't in settings, raise an error.
        """
        context = {'help_key': 'unused-key'}
        self.assertRaises(
            ImproperlyConfigured,
            tags.madcap_flare_help,
            context)
