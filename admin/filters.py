
from django.utils.translation import gettext_lazy as _

from mptt.admin import MPTTModelAdmin, TreeRelatedFieldListFilter
from admin_auto_filters.filters import AutocompleteFilter
from django.utils.translation import gettext_lazy as _


class CategoryFilter(AutocompleteFilter):
    title = _('категорією') 
    field_name = 'category' 

class MarkersFilter(AutocompleteFilter):
    title = _('маркерами') 
    field_name = 'markers' 

class BrandFilter(AutocompleteFilter):
    title = _('брендами')
    field_name = 'brand' 


class ItemStockFilter(AutocompleteFilter):
    title = _('наявністю')
    field_name = 'in_stock'


class ItemIsActiveFilter(AutocompleteFilter):
    title = _('активністю')
    field_name = 'is_active'


class ItemFilter(AutocompleteFilter):
    title = _('товаром')
    field_name = 'item'
class AttributeFilter(AutocompleteFilter):
    title = _('атрибутом')
    field_name = 'attribute'
class ItemAttributeFilter(AutocompleteFilter):
    title = _('атрибутом товару')
    field_name = 'item_attribute'


    
class ItemCategoryTreeRelatedFieldListFilter(TreeRelatedFieldListFilter):
    mptt_level_indent = 20

