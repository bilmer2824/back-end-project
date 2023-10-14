from django import template
from blog.models import Category
from django.db.models import Count

register = template.Library()



@register.simple_tag()
def get_all_categories():
    return Category.objects.annotate(Count('article'))