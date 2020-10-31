from import_export.resources import ModelResource
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from ..models import * 



class ItemImageResource(ModelResource):
    # item = Field(
    #     column_name='item',
    #     attribute="item",
    #     widget=ForeignKeyWidget(Item, field='id')
    # )

    class Meta:
        model = ItemImage
        exclude = [
            'order',
            'created',
            'updated',
        ]
    def before_import_row(self, row, **kwargs):
        row['image'] = f"shop/item/{row['image']}"


class ItemManufacturerResource(ModelResource):
    class Meta:
        model = ItemManufacturer
        exclude = []

    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None


class ItemUnitResource(ModelResource):
    class Meta:
        model = ItemUnit
        exclude = []

    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None


class ItemBrandResource(ModelResource):
    class Meta:
        model = ItemBrand
        exclude = []

    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None


class ItemStockResource(ModelResource):
    class Meta:
        model = ItemStock
        exclude = [
        ]




