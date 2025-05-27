from django import template
import json

register = template.Library()

@register.simple_tag
def get_theme_variables():
    theme_vars = {
        'colors': {
            'primary': '#8c57ff',
            'secondary': '#8a8d93',
            'success': '#56ca00',
            'info': '#16b1ff',
            'warning': '#ffb400',
            'danger': '#ff4c51',
            'dark': '#4b4b4b',
            'black': '#2e263d',
            'white': '#fff',
            'bodyColor': '#6D6777',
            'headingColor': '#433C50',
            'bodyBg': '#f4f5fa',
        }
    }
    return json.dumps(theme_vars)
