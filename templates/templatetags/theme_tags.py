from django import template

register = template.Library()

@register.simple_tag
def get_theme_variables():
    """Return theme variables"""
    return {
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
            'body': '#6D6777',
            'headingColor': '#433C50',
            'bodyBg': '#f4f5fa',
        }
    }
