from django import template
from ..models import *


register = template.Library()


@register.filter
def get_type(value):
    return type(value)


@register.simple_tag
def get_item_attribute_values(item, code):
    return item.get_item_attribute_values(code)


@register.simple_tag
def get_category_features(category, item):
    return category.get_item_features(item)


@register.simple_tag
def get_category_attributes(category, item=None):
    return category.get_category_attributes(item)


@register.simple_tag
def get_category_attribute_values(category, item=None):
    return category.get_category_attribute_values(item)


@register.simple_tag
def get_item_price(item, currency=None, price_type=None):
    return item.get_price(currency, price_type)


@register.simple_tag
def get_item_attribute_value_price(item_attribute_value, currency=None, price_type=None):
    return item_attribute_value.get_price(currency, price_type)























