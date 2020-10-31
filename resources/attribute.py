from import_export.resources import ModelResource
from import_export.fields import Field 
from ..models import * 



class AttributeCategoryResource(ModelResource):
    class Meta:
        model = AttributeCategory
        exclude =  []


class AttributeResource(ModelResource):
    class Meta:
        model = Attribute
        exclude =  [
        ]

    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None 


class AttributeValueResource(ModelResource):
    class Meta:
        model = AttributeValue
        exclude =  []
    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None 


class ItemAttributeResource(ModelResource):
    class Meta:
        model = ItemAttribute
        exclude = [

        ]

    def dehydrate_attribute(self, item):
        attribute = None 
        try:
            if item.attribute: attribute = obj.attribute.name.lower().strip()
        except Exception as e:
            print('e:',e)
        return attribute
        
    def before_import_row(self, row, **kwargs):
        if row.get('attribute'):
            name = row['attribute'].lower().strip()
            row['attribute'] = Attribute.objects.get_or_create(name=name)[0].id


class ItemAttributeValueResource(ModelResource):
    itemid         = Field(attribute=None, column_name="itemid")
    attribute_name = Field(attribute=None, column_name="attribute_name")
    value_value    = Field(attribute=None, column_name="value_value")
    class Meta:
        model = ItemAttributeValue
        exclude =  [
        ]

    def dehydrate_itemid(self, obj):
        itemid = None
        if getattr(obj, 'item_attribute', None): itemid = obj.item_attribute.item.id
        return itemid 

    def dehydrate_attribute_name(self, obj):
        attribute_name = None 
        try:
            if obj.item_attribute: attribute_name = obj.item_attribute.attribute.name
        except Exception as e:
            print('e:', e)
        return attribute_name 
        
    def dehydrate_value_value(self, obj):
        value_value = None 
        try:
            if obj.value: value_value = obj.value.value
        except Exception as e:
            print('e:', e)
        return value_value 

    def dehydrate_currency(self, item):
        currency = None
        if getattr(item, 'currency', None): currency = item.currency.code 
        return currency

    def before_import_row(self, row, **kwargs):
        attribute_name = row['attribute_name'].lower().strip()
        value_value    = row['value_value'].lower().strip()
        item_attribute, _ = ItemAttribute.objects.get_or_create(
            item=Item.objects.get(id=row['itemid']),
            attribute=Attribute.objects.get_or_create(name=attribute_name)[0],
        )
        row['item_attribute'] = item_attribute.id
        row['value'] = AttributeValue.objects.get_or_create(value=value_value)[0].id
        row['currency'] = Currency.objects.get_or_create(code=row['currency'])[0].id
        if row.get('amount') == '':
            row['amount'] = None 




