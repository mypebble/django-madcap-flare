# Madcap Flare Integration

Simple integration tools to link to embedded Madcap Flare help


## Installation

Install the Madcap Flare integration from PyPi:

```
pip install django-madcap-flare
```

and add it to your settings.py:

```python
INSTALLED_APPS = [
    ...
    'madcap_flare',
    ...
]
```

You will also need to configure the
[`MADCAP_FLARE_ROOT` and `MADCAP_FLARE_TAGS`](#configuring)

## Usage

You can convert Madcap Flare header files into a Python dict with the
`get_help_mapping` command:

```
python manage.py get_help_mapping path_to_file.h
```

This will output a dict on the command line that you can copy into your
settings.py file.

### Configuring

To setup your template tags, take the output of `get_help_mapping` and set it to
the `MADCAP_FLARE_TAGS` in settings.py:

```python
MADCAP_FLARE_TAGS = {
  'my-help-topic': '1000',
  'other-help-topic': '2000',
}

MADCAP_FLARE_ROOT = 'https://www.example.com/help_topics/'
```

The `MADCAP_FLARE_ROOT` setting tells Django what to use for your host name and
default path.

### View Mixin

To inject your information into your templates, you can use the view mixin for
Madcap Flare:

```python
from django.views.generic import ListView

from madcap_flare.views import MadcapFlareMixin

from myproject.myapp.models import MyModel


class MyListView(MadcapFlareMixin, ListView):
    """Sample list view.
    """

    help_key = 'my-help-topic'
    queryset = MyModel.objects.all()
```

The MadcapFlareMixin injects the `help_key` object into your template context.

### Template Tag

The `madcap_flare_help` template tag outputs a Madcap Flare URL that can be
linked from your templates:

```html
{% load madcap_flare_tags %}

<p>To get more help on this feature, see our
  <a href="{% madcap_flare_help %}">documentation</a>
</p>
```

With the `help_key` set above, this will output:

```html
<p>To get more help on this feature, see our
  <a href="https://www.example.com/help_topics/Default.htm#cshid=1000">documentation</a>
</p>
```

## Developing

To test the integration just run:

```bash
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python setup.py develop
python tests/manage.py test
```

### Writing Docs for PyPI

To convert the docs to RST for PyPI:

```bash
pandoc --from=markdown --to=rst --output=README.txt README.md
```
