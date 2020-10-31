from django.core.management.base import BaseCommand 
from box.apps.sw_shop.sw_catalog.models import Item, ItemCategory 
from random import choice 


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        categories = ItemCategory.objects.filter(parent__id__isnull=False).values_list('pk', flat=True)
        for item in Item.objects.all():
            category = ItemCategory.objects.get(pk=choice(categories))
            item.category = category
            item.save()
            print(item)

