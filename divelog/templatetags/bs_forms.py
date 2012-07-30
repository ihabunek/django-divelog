from django import template
from django.utils.log import getLogger

register = template.Library()

@register.inclusion_tag('bootstrap/field.html')
def bs_field(field):
    "Renders a single form field with bootstrap styling."
    return { 'field': field }

@register.inclusion_tag('bootstrap/fields.html')
def bs_fields(fields):
    "Renders the form's fields with bootstrap styling."
    return { 'fields': fields }

@register.inclusion_tag('bootstrap/form.html')
def bs_form(form, submit_text="Submit"):
    "Renders a form with bootstrap styling."
    return { 
        'form': form,
        'submit_text': submit_text 
    }
