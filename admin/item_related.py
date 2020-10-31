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


from box.core.utils import (
    AdminImageWidget, show_admin_link, move_to, BaseAdmin,
    seo, base_main_info
)
from box.apps.sw_shop.sw_catalog.models import * 
from box.apps.sw_shop.sw_cart.models import * 
from box.apps.sw_shop.sw_catalog.models import * 
from box.apps.sw_shop.sw_cart.models import * 



from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin, TreeRelatedFieldListFilter
from modeltranslation.admin import *
from dal import autocomplete
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin


from .filters import * 
from .views import * 
from .item_inlines import * 
from ..resources import * 



class ItemManufacturerAdmin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    ):
    resource_class = ItemManufacturerResource
    search_fields = [
        'name'
    ]


class ItemUnitAdmin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    ):
    list_display = [
        'id',
        'name',
    ]
    list_display_links = list_display
    search_fields = [
        'name',
    ]


class ItemImageAdmin(
    # nested_admin.NestedTabularInline,
    # BaseAdmin, 
    SortableAdminMixin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    ):
    # def get_model_perms(self, request):
    #     return {}

    def show_item(self, obj):
        return show_admin_link(obj=obj, obj_attr='item', obj_name='title')

    show_item.short_description = ('Товар')
    resource_class = ItemImageResource
    list_display = [
        'id',
        # 'show_image',
        'alt',
        'show_item',
    ]
    list_display_links = [
        'id',
        'alt',
    ]
    list_editable = []
    if 'jet' not in settings.INSTALLED_APPS:
        autocomplete_fields = [
            'item',
        ]


class ItemStockAdmin(
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
    ):
    # def get_model_perms(self, request):
    #     return {}

    # def has_add_permission(self, request, obj=None):
    #     return False 

    list_display = [
        'id',
        'text',
        'availability',
        'colour',
    ] 
    list_display_links = [
        'id',
        'text',
    ] 
    readonly_fields = [
        'availability',
    ]
    exclude = [
        'is_active',
    ]
    search_fields = [
        'text',
    ]



class ItemBrandAdmin(BaseAdmin, SortableAdminMixin, 
    TabbedTranslationAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin,
):
    # change_form
    fieldsets = [
        base_main_info,
        seo,
    ]
    prepopulated_fields = {
        'slug':('title',)
    }


class ItemReviewAdmin(
    BaseAdmin,
    # nested_admin.NestedTabularInline,
    ):
    list_display = [
        'id',
        'text',
        'phone',
        'email',
        'name',
        'is_active',
    ]
    list_display_links = [
        'id',
    ]
    list_filter = [
        'is_active',
    ]
    search_fields = [
        'text',
        'phone',
        'email',
        'name',
    ]


