from django.core.management.base import BaseCommand
from box.apps.sw_shop.sw_catalog.models import *
import random
import datetime 
import json 
import csv




class Command(BaseCommand):
  def handle(self, *args, **kwargs):
    ItemAttribute.objects.all().delete()
    ItemAttributeValue.objects.all().delete()




