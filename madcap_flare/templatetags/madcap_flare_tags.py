"""In-app support documentation-related template tags.
"""
from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

register = template.Library()


@register.simple_tag(takes_context=True)
def contextual_help_url(context):
    """Render the contextual help button.

    Using the given context key "help_key", determine the correct contextual
    help URL to render so the user can click on it. If this isn't given, or
    isn't available in the configured help, we just display the link for the
    menu to the user.
    """
    help_file = 'Default.htm'
    help_key = context.get('help_key')

    return '{root}{help_file}{help_id}'.format(
        root=settings.CONTEXTUAL_HELP_ROOT,
        help_file=help_file,
        help_id=_get_help_id(help_key))


def _get_help_id(help_key):
    """Return the hashcode referencing the contextual help document.

    If help_key is a falsy value, this returns an empty string.
    If the lookup can't find the help_key, this returns an empty string.
    """
    if not help_key:
        return ''
    if help_key not in help_mapping:
        raise ImproperlyConfigured(
            u'help_key: {key} must be one of:\n{allowed_keys}'.format(
                key=help_key, allowed_keys='\n'.join(sorted(
                    help_mapping.keys()))))

    return '#cshid={map}'.format(map=help_mapping[help_key])
