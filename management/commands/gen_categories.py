from django.core.management.base import BaseCommand
from box.apps.sw_shop.sw_catalog.models import (
  Item, ItemImage, ItemCategory, Attribute, AttributeValue, ItemAttribute, ItemAttributeValue
)
import random
import datetime 
import json 
import csv




class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    for i in range(1, 10):
      print(i)
      cat, _ = ItemCategory.objects.get_or_create(title=f'категорія {i}')
      print(cat)




