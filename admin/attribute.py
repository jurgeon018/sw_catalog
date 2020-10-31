from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.contrib import admin 
from django.shortcuts import reverse 
from django.utils.safestring import mark_safe
from django.urls import path 
from django.contrib import admin 
from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.shortcuts import reverse 
from django.utils.safestring import mark_safe
from django.urls import path 
from django.conf import settings
from django.forms import TextInput, Textarea, NumberInput
from django.utils.translation import gettext_lazy as _


from box.core.utils import (
    AdminImageWidget, show_admin_link, move_to, BaseAdmin,
    seo, base_main_info
)
from box.apps.sw_shop.sw_catalog.models import * 
from box.apps.sw_shop.sw_cart.models import * 
from box.apps.sw_shop.sw_catalog.models import * 
from box.apps.sw_shop.sw_cart.models import * 


import nested_admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin, TreeRelatedFieldListFilter
from modeltranslation.admin import *
from dal import autocomplete
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin


from .filters import ItemFilter, CategoryFilter
from .views import * 
from .item_inlines import * 
from ..resources import * 

zminna = True
# zminna = False


class AttrBaseMixin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    ):
    pass 

class ItemAttributeValueInline(nested_admin.NestedTabularInline):
    # if 'jet' not in settings.INSTALLED_APPS:
    if zminna:
        autocomplete_fields = [
            'value',
            'proposition',
        ]
    # fieldsets = (
    #     (None, {
    #         "fields": (
    #             'value',
    #             'price',
    #             'currency',
    #             'proposition',
    #             (
    #                 'amount',
    #                 'description',
    #             ),
    #         ),
    #     }),
    # )
    
    extra = 0
    classes = [
        'collapse',
    ]
    # sortable_field_name = "attribute"
    model = ItemAttributeValue
    formfield_overrides = {
        models.TextField:{'widget':forms.Textarea(attrs={'cols':'35', 'rows':'1'})}
    }


class ItemAttributeInline(nested_admin.NestedTabularInline):
    # if 'jet' not in settings.INSTALLED_APPS:
    if zminna:
        autocomplete_fields = [
            'attribute'
        ]

    extra = 0
    classes = [
        'collapse',
    ]
    # sortable_field_name = "product"
    model = ItemAttribute
    inlines = [ItemAttributeValueInline]


class ItemAttributeAdmin(
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    nested_admin.NestedModelAdmin,
    ):
    class Media:
        pass
    resource_class = ItemAttributeResource
    inlines = [
        ItemAttributeValueInline,
    ]
    if 'jet' not in settings.INSTALLED_APPS:
        autocomplete_fields = [
            'item',
            'attribute',
        ]
    list_filter = [
        'is_option',
        ItemFilter,
        AttributeFilter,
        # 'item',
    ]
    list_display = [
        'id',
        'is_option',
        'attribute',
        'item',
    ]
    list_display_links = [
        'id',
        'attribute',
        'item',
        'is_option',
    ]
    list_editable = [
        # 'is_option',
    ]
    search_fields = [
        'item',
    ]


class AttributeCategoryAdmin(AttrBaseMixin):
    resource_class = AttributeCategoryResource
    search_fields = [
        'name',
    ] 
    list_display = [
        'id',
        'name',
    ]
    list_display_links = [
        'id',
    ]
    list_editable = [
        'name',
    ]
    save_on_top = True 


class ItemAttributeValueAdmin(
    AttrBaseMixin,
    nested_admin.NestedModelAdmin,
    ):
    class Media:
        pass
    # def get_model_perms(self, request):
    #     return {}
    resource_class = ItemAttributeValueResource
    if 'jet' not in settings.INSTALLED_APPS:
        autocomplete_fields = [
            'item_attribute',
            'value',
        ] 
    list_display = [
        'id',
        'item_attribute',
        'price',
        'value',
    ]
    list_editable = [
        'value',
        'price',
    ]
    list_display_links = [
        'id',
        'item_attribute',
    ]
    list_filter = [
        ItemAttributeFilter,
    ]


class AttributeAdmin(AttrBaseMixin):
    def delete_queryset(self, request, queryset):
        queryset.filter(code__isnull=True).delete()
    
    def has_delete_permission(self, request, obj=None):
        return False if obj and obj.code else True 

    resource_class = AttributeResource
    # TODO: change category. проміжний action.
    search_fields = [
        'name'
    ]
    if 'jet' not in settings.INSTALLED_APPS:
        autocomplete_fields = [
            'category',
        ]
    list_display = [
        'id',
        'code',
        'category',
        'name',
    ]
    list_display_links = [
        'id',
    ]
    list_editable = [
        'category',
        'name',
    ]
    readonly_fields = [
        # 'code',
    ]
    list_filter = [
        CategoryFilter,

    ]

class AttributeValueAdmin(AttrBaseMixin):
    def delete_queryset(self, request, queryset):
        queryset.filter(code__isnull=True).delete()
    
    def has_delete_permission(self, request, obj=None):
        return False if obj and obj.code else True 
    autocomplete_fields = [
        'attribute',
    ]
    resource_class = AttributeValueResource
    readonly_fields = [
        # 'code',
    ]
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
    search_fields = [
        'value'
    ]



admin.site.register(ItemAttribute, ItemAttributeAdmin)
admin.site.register(ItemAttributeValue, ItemAttributeValueAdmin)
admin.site.register(AttributeValue, AttributeValueAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(AttributeCategory, AttributeCategoryAdmin)


