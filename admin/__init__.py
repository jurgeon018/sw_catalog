from .item_related import * 
from .item import * 
from .item_category import * 
from .attribute import * 
from .features import * 
from .config import * 



admin.site.register(ItemStock, ItemStockAdmin)
admin.site.register(ItemCategory, ItemCategoryAdmin)
admin.site.register(ItemManufacturer, ItemManufacturerAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemImage, ItemImageAdmin)

admin.site.register(ItemBrand, ItemBrandAdmin)
admin.site.register(ItemUnit, ItemUnitAdmin)
admin.site.register(ItemReview, ItemReviewAdmin)
admin.site.register(CatalogueConfig, CatalogueConfigAdmin)
