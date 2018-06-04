from django import template

register = template.Library()


@register.simple_tag
def get_stage_class(translation, stage):
    return translation.get_stage_class(stage)
