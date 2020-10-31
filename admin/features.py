from django.contrib import admin
from django.conf import settings  
from ..models.features import * 

import nested_admin 


class ItemFeatureInline(nested_admin.NestedTabularInline):
    model = ItemFeature
    # model = ItemFeature.items.through
    extra = 0
    classes = ['collapse']
    if 'jet' not in settings.INSTALLED_APPS:
        autocomplete_fields = [
            'name',
            'value',
            'category',
        ]
    # classes 




@admin.register(ItemFeature)
class ItemFeatureAdmin(admin.ModelAdmin):
    pass


@admin.register(FeatureValue)
class FeatureValueAdmin(admin.ModelAdmin):
    search_fields = ['value']


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(FeatureCategory)
class FeatureCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']


    


































