from django.contrib.sitemaps import Sitemap 
from .models import Item, ItemCategory


class ItemSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1
    protocol = 'https'
    i18n = True 

    def items(self):
        return Item.objects.all()
        
    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_absolute_url()

class ItemCategorySitemap(Sitemap):
    changefreq = 'never'
    priority = 1
    protocol = 'https'
    i18n = True

    def items(self):
        return ItemCategory.objects.all()

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_absolute_url()
