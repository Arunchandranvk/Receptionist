from django import template

register = template.Library()

@register.filter
def filter_unread(enquiries):
    return [enquiry for enquiry in enquiries if not enquiry.is_read]