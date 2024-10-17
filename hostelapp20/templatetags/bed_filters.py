from django import template

register = template.Library()

@register.filter
def bed_color(bed):
    # Assuming bed has a related_name of tenant for the Tenant model
    if bed.tenant:
        return "fas fa-bed red" # Use Font Awesome class for bed icon with red color
    else:
        return "fas fa-bed" # Use Font Awesome class for bed icon with default color
