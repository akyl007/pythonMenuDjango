from django import template
from django.utils.safestring import mark_safe

from ..models import MenuItem

register = template.Library()


def render_menu(menu_name, current_url):
    menu_items = MenuItem.objects.filter(menu__name=menu_name).select_related('parent')
    menu_dict = {}
    for item in menu_items:
        if item.parent:
            if item.parent not in menu_dict:
                menu_dict[item.parent] = []
            menu_dict[item.parent].append(item)
        else:
            if item not in menu_dict:
                menu_dict[item] = []

    def render_item(item, is_active):
        children = menu_dict.get(item, [])
        classes = 'active' if is_active else ''
        html = f'<li class="{classes}"><a href="{item.get_absolute_url()}">{item.title}</a>'
        if children:
            html += '<ul>'
            for child in children:
                html += render_item(child, child.get_absolute_url() == current_url)
            html += '</ul>'
        html += '</li>'
        return html

    # Determine the active URL
    active_url = current_url
    menu_html = '<ul>'
    for item in menu_items.filter(parent__isnull=True):
        menu_html += render_item(item, item.get_absolute_url() == active_url)
    menu_html += '</ul>'

    return mark_safe(menu_html)


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    return render_menu(menu_name, current_url)
