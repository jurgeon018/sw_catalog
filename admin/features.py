from django.contrib import admin
from django.conf import settings  
from ..models.features import * 
from ..resources.features import * 
from modeltranslation.admin import TabbedTranslationAdmin
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
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



from .filters import * 

@admin.register(ItemFeature)
class ItemFeatureAdmin(admin.ModelAdmin):
    class Media:
        pass
    search_fields = [
        'name__name',
        'value__value',
        'item__title',
    ]
    list_display = [
        'id',
        'item',
        'name',
        'value',
        'category',
    ]
    list_display_links = [
        'id',
    ]
    list_filter = [
        # 'item',
        FeatureFilter,
        FeatureValueFilter,
        FeatureCategoryFilter,
    ]
    autocomplete_fields = [
        'item',
        'name',
        'value',
        'category',
    ]


@admin.register(FeatureValue)
class FeatureValueAdmin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    # admin.ModelAdmin
    ):
    resource_class = FeatureValueResource
    search_fields = ['value']
    list_display = [
        'id',
        'code',
        'value',
    ]
    list_editable = [
        'value',
    ]
    list_display_links = [
        'id',
    ]


@admin.register(Feature)
class FeatureAdmin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    # admin.ModelAdmin
    ):

    search_fields = ['name']
    list_display = [
        'id',
        'code',
        'name',
    ]
    list_display_links = [
        'id',
    ]
    list_editable = [
        # 'code',
        'name',
    ]
    autocomplete_fields = [
        # 'category',
    ]


@admin.register(FeatureCategory)
class FeatureCategoryAdmin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    # admin.ModelAdmin
    ):

    search_fields = ['name']


    


































