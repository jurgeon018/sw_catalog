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
    seo, base_main_info, ClonableModelAdmin
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

class ItemCategoryAdmin(
    BaseAdmin,
    ImportExportActionModelAdmin,
    ImportExportModelAdmin, 
    # ClonableModelAdmin, 
    # SortableAdminMixin,
    DraggableMPTTAdmin,
    TabbedTranslationAdmin,
    admin.ModelAdmin,
    ):
    # changelist
    # TODO: Проміжна дія : встановити всім товарам в вибраних категоріях валюту категорії.
    # TODO: Проміжна дія: встановити всім товарам в вибраних категоріях характеристику категорії.
    def delete_queryset(self, request, queryset):
        queryset.filter(code__isnull=True).delete()
    
    def has_delete_permission(self, request, obj=None):
        return False if obj and obj.code else True 

    def tree_title(self, obj):
        lvl = obj._mpttfield('level') * self.mptt_level_indent
        return mark_safe(f'<div style="text-indent:{lvl}px">{obj.tree_title}</div>')
    tree_title.short_description = _('Заголовок')
    expand_tree_by_default = False 
    mptt_level_indent = 20

    resource_class = ItemCategoryResource
    inlines = [
        ItemCategoryInline,
    ]
    actions = [
        # "is_active_on",
        # "is_active_off",
    ]
    # mptt_indent_field = "currency"
    list_display = [
        'tree_actions',
        "show_image",
        # 'indented_title',
        'tree_title',
        # 'title',
        'is_active',
        'show_site_link',
        'show_delete_link',
    ]
    search_fields = [
        'title',
    ]
    list_display_links = [
        # 'indented_title',
        'tree_title',
        # 'title',
    ]
    list_editable = [
        'is_active',
    ]
    list_filter = (
        # ('title', TreeRelatedFieldListFilter),
    )
    list_per_page = 200 

    # changeform
    formfield_overrides = {
        models.ImageField:{'widget': AdminImageWidget},
        models.CharField: {'widget': NumberInput(attrs={'size':'40'})},
        models.CharField: {'widget': TextInput(attrs={'size':'40'})},
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':20})},
    }
    prepopulated_fields = {
        "slug": ("title",),
    }
    fieldsets = [
        [_('ОСНОВНА ІНФОРМАЦІЯ'), {
            "fields":[
                "title",
                "currency",
                'parent',
                "image",
                'description',
                'is_active',
                "created",
                'updated',
            ]
        }],
        seo,
    ]
    if 'jet' not in settings.INSTALLED_APPS:
        autocomplete_fields = [
            'parent',
            'currency'
        ]
    
   
