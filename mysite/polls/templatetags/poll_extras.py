# reference:
# https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#howto-writing-custom-template-tags


# in your template you would use the following:
# {% load poll_extras %}

import datetime
from django import template

register = template.Library()

#  in the filter {{ var|foo:"bar" }}, the filter foo would be passed the variable var and the argument "bar".

# example: {{ somevariable|cut:"0" }}
@register.filter(name='cut', is_safe=True)
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

# same as:
# register.filter('cut', cut)


@register.simple_tag(name='current_time')
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.inclusion_tag('results2.html')
def show_results(poll):
    choices = poll.choice_set.all()
    return {'choices': choices}


# from django.template.loader import get_template
# t = get_template('results2.html')
# register.inclusion_tag(t)(show_results)