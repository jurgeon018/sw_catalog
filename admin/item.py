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



from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin, TreeRelatedFieldListFilter
from modeltranslation.admin import *
from dal import autocomplete
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin


from .filters import * 
from .views import * 
from .item_inlines import * 
from .attribute import * 
from .features import * 
from ..resources import * 

import nested_admin



class SimilarInline(nested_admin.NestedTabularInline):
    model = Item.similars.through
    extra = 0 
    fk_name = 'from_item'
    if 'jet' not in settings.INSTALLED_APPS:
        autocomplete_fields = [
            'to_item',
        ]
    classes = ['collapse',]
    verbose_name = _('Схожий товар')
    verbose_name_plural = _('Схожі товари')
    
if 'jet' in settings.INSTALLED_APPS:
    from jet.filters import RelatedFieldAjaxListFilter
 
from importlib import import_module 

def gen_item_inlines():
    inlines = [
        SimilarInline,
        ItemImageInline,
        ItemFeatureInline,
        ItemAttributeInline,
        # ItemReviewInline, 
    ]  
    for item_additional_inline in item_settings.ITEM_ADDITIONAL_INLINE:
        module, klass = item_additional_inline.rsplit('.', 1)
        module = import_module(module)
        inline = getattr(module, klass)
        inlines.append(inline)
    return inlines


class ItemAdmin(
    BaseAdmin,
    TabbedTranslationAdmin, 
    nested_admin.NestedModelAdmin,
    ): 
    # changeform
    # change_form_template = 'item_change_form.html'
    # form = ItemForm
    resource_class = ItemResource
    # list_filter = [
    #     ('manufacturer', RelatedFieldAjaxListFilter),
    # ]

    if 'jet' in settings.INSTALLED_APPS:

        list_filter = [
            ('category', RelatedFieldAjaxListFilter),
            ('manufacturer', RelatedFieldAjaxListFilter),
            ('brand', RelatedFieldAjaxListFilter),
            ('markers', RelatedFieldAjaxListFilter),

        ]
    else:
        list_filter = [
            # "category",
            # ('category', ItemCategoryTreeRelatedFieldListFilter),
            CategoryFilter,
            MarkersFilter,
            BrandFilter,
        ]
    if not 'jet' in settings.INSTALLED_APPS:
        autocomplete_fields = [
            'similars',
            'markers',
            'labels',
            'manufacturer',
            'brand',
            'in_stock',
            'currency',
            'unit',
        ]
        if item_settings.MULTIPLE_CATEGORY:
            autocomplete_fields.append('categories')
        else:
            autocomplete_fields.append('category')
    prepopulated_fields = {
        "slug": ("title",),
        # "code": ("title",),
    }

    inlines = gen_item_inlines()
    item_fields = [
        'title',
        "brand",
        "manufacturer",
        "markers",   
        'currency',
        "labels",   
        # "similars",   
        'in_stock',
        (
        "unit",
        'amount',
        ),
        (
        'price',
        'discount',
        'discount_type',
        ),
        'is_active',
        'image',
    ]
    if item_settings .MULTIPLE_CATEGORY:
        item_fields.insert(2 ,'categories')
    else:
        item_fields.insert(2 ,'category')
    fieldsets = [
        [_("ОПИС"), {
            'fields':[
                'description',
                'created',
                'updated',
            ],
            'classes':[
                'collapse',
            ],
        }],
        seo,
        [_('ОСНОВНА ІНФОРМАЦІЯ'), {
            'fields':item_fields
        }],
    ]    
    # changelist  
    # TODO: Проміжна дія: встановити всім вибраним товарам валюту їхньої категорії
    # TODO: Проміжна дія: встановити всім вибраним товарам характеристики їхньої категорії
    # change_list_template = 'item_change_list.html'
    search_fields = [
        'title',
        'code',
    ]

    list_display = [
        'show_image',
        'title',
        'price',
        'discount',
        'discount_type',
        'category',
        # 'currency',
        'amount',
        # 'unit',
        'is_active',
        # "clone_link",
        'show_site_link',
        "show_edit_link",
        "show_delete_link",
    ]
    list_editable = [
        'price',
        # 'currency',
        'category',
        'discount',
        'discount_type',
        'amount',
        # 'unit',
        'is_active',
    ]
    list_display_links = [
        # 'order',
        'title',
    ]
    list_per_page = 40 
    def change_category(self, request, queryset):
        initial = {
            'model':ItemCategory,
            'attr':'category',
            'action_value':'change_category',
            'action_type':'add',
            'text':_('Нова категорія буде застосована для наступних позиций:'),
            'title':_("Зміна категорії"),
            'message':_('Категорія {0} була застосована до {1} товарів'),
        }
        return move_to(self, request, queryset, initial)

    def change_brand(self, request, queryset):
        initial = {
            'model':ItemBrand,
            'attr':'brand',
            'action_value':'change_brand',
            'action_type':'add',

            'text':_('Новий бренд буде застосований для наступних позиций:'),
            'title':_("Зміна бренду"),
            'message':_('Бренд {0} був застосований до {1} товарів'),
        }
        return move_to(self, request, queryset, initial)

    def add_markers(self, request, queryset):
        initial = {
            'model':GlobalMarker,
            'attr':'markers',
            'action_value':'add_markers',
            'action_type':'add',
            'text':_('Нові маркери будуть застосовані для наступних позиций:'),
            'title':_("Додавання маркерів"),
            'message':_('Маркери {0} були застосовані до {1} товарів'),
        }
        return move_to(self, request, queryset, initial)
    
    def remove_markers(self, request, queryset):
        initial = {
            'model':GlobalMarker,
            'attr':'markers',
            'action_value':'remove_markers',
            'action_type':'remove',
            'text':_('Нові маркери будуть забрані з наступних позиций:'),
            'title':_("Видалення маркерів з товарів"),
            'message':_('Маркери {0} були забрані з {1} товарів'),
        }
        return move_to(self, request, queryset, initial)

    change_category.short_description = _("Змінити категорію")
    add_markers.short_description     = _("Додати маркери")
    remove_markers.short_description  = _("Забрати маркери")
    change_brand.short_description    = _("Змінити бренд")
    actions = [
        "is_active_on",
        "is_active_off",
        "change_category",
        "change_brand",
        "add_markers",
        "remove_markers",
        'export_admin_action',
    ]
