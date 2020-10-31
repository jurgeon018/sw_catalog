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
from ..resources import * 


class ItemImageInline(
    SortableInlineAdminMixin,
    TranslationTabularInline,
    ):
    model = ItemImage
    extra = 0
    classes = ['collapse']
    # def get_fields(self, request, obj):
    #     fields = [
    #         'image',
    #         # 'order',
    #         'alt',
    #     ]
    #     return fields 
    fields = [
        'image',
        'alt',
    ]
    readonly_fields = [
        # 'order',
    ]
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}



class ItemReviewInline(admin.TabularInline):
    model = ItemReview
    extra = 0 
    classes = ['collapse']
    exclude = [
        
    ]


class ItemInline(TranslationTabularInline):
    def show_title(self, obj):
      option = "change" # "delete | history | change"
      massiv = []
      app   = obj._meta.app_label
      model = obj._meta.model_name
      url   = f'admin:{app}_{model}_{option}'
      href  = reverse(url, args=(obj.pk,))
      name  = f'{obj.title}'
      link  = mark_safe(f"<a href={href}>{name}</a>")
      return link
    show_title.short_description = 'Товар'
    model = Item 
    extra = 0
    fields = [
        'show_title',
        'old_price',
        'price',
        'currency',
    ]
    readonly_fields = [
        'show_title',
        'old_price',
        'price',
        'currency',
    ]
    classes = ['collapse']
    # if settings.MULTIPLE_CATEGORY:
    #     filter_horizontal = [
    #         'categories',
    #     ]
    # else:
    #     filter_horizontal = [
    #         'category',
    #     ]


class ItemCategoryInline(TranslationStackedInline):
    model = ItemCategory 
    extra = 0
    fields = [
        'title',
        'is_active',
        'image',
        'slug',
    ]
    classes = ['collapse']
    verbose_name = _("підкатегорія")
    verbose_name_plural = _("підкатегорії")
    prepopulated_fields = {
        "slug": ("title",), 
    }
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }
