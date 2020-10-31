from django.conf import settings 
from box.apps.sw_shop.sw_catalog.models import *
from box.apps.sw_shop.sw_catalog import settings as item_settings
from modeltranslation.manager import get_translatable_fields_for_model
from rest_framework import serializers


class CurrencySerializer(serializers.ModelSerializer):
  class Meta:
    model = Currency
    exclude = []


class ItemReviewSerializer(serializers.ModelSerializer):
  created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
  updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

  class Meta:
    model = ItemReview
    exclude = [
    ]


class ItemImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = ItemImage
    exclude = [
      'item',
    ]


class AttributeValueSerializer(serializers.ModelSerializer):
  class Meta:
    model = AttributeValue 
    exclude = []


class AttributeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Attribute
    exclude = []


class ItemAttributeValueSerializer(serializers.ModelSerializer):
  value = AttributeValueSerializer(read_only=True)
  currency = CurrencySerializer(read_only=True)
  class Meta:
    model = ItemAttributeValue
    exclude = []


class ItemAttributeSerializer(serializers.ModelSerializer):
  # item_attribute_values = ItemAttributeValueSerializer(read_only=True, many=True)
  # item_attribute_values = serializers.ListSerializer()
  attribute = AttributeSerializer(read_only=True)
  class Meta:
    model = ItemAttribute
    exclude = []


class ItemSubcategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = ItemCategory
    exclude = []


class ItemCategorySerializer(serializers.ModelSerializer):
  parent = ItemSubcategorySerializer()
  class Meta:
    model = ItemCategory
    exclude = []

class ItemStockSerializer(serializers.ModelSerializer):
  class Meta:
    model = ItemStock 
    exclude = []


class ItemDetailSerializer(serializers.ModelSerializer):
  images   = ItemImageSerializer(many=True, read_only=True)
  # features = ItemFeatureSerializer(many=True)
  absolute_url = serializers.SerializerMethodField() 
  image_url = serializers.SerializerMethodField() 
  
  is_in_cart = serializers.SerializerMethodField()
  def get_is_in_cart(self, obj):
    request = self.context.get('request')
    if request:
      return obj.is_in_cart(request)

  def get_absolute_url(self, obj):
      return obj.get_absolute_url()

  def get_image_url(self, obj):
    return obj.image_url

  if item_settings.MULTIPLE_CATEGORY:
    categories = ItemCategorySerializer(many=True)
  else:
    category = ItemCategorySerializer()

  price    = serializers.ReadOnlyField()
  reviews  = ItemReviewSerializer(many=True)
  currency = CurrencySerializer()
  in_stock = ItemStockSerializer()

  class Meta:
    model = Item
    exclude = [
      'similars',
      # 'images',
    ]
from box.core.sw_global_config.models import GlobalMarker
class GlobalMarkerSerializer(serializers.ModelSerializer):
  class Meta:
    model = GlobalMarker
    exclude = []


class ItemListSerializer(serializers.ModelSerializer):
  price    = serializers.ReadOnlyField()
  currency = CurrencySerializer()
  in_stock = ItemStockSerializer()
  markers  = GlobalMarkerSerializer(many=True, read_only=True)
  absolute_url = serializers.SerializerMethodField() 
  def get_absolute_url(self, obj):
      return obj.get_absolute_url()

  image_url = serializers.SerializerMethodField() 
  def get_image_url(self, obj):
    return obj.image_url

  final_unconverted_price = serializers.SerializerMethodField() 
  def get_final_unconverted_price(self, obj):
    return obj.final_unconverted_price()
  
  is_in_cart = serializers.SerializerMethodField()
  def get_is_in_cart(self, obj):
    return obj.is_in_cart(self.context['request'])

  class Meta:
    model = Item
    exclude = [
    ]

  # def get_field_names(self, declared_fields, info):
  #   fields = super().get_field_names(declared_fields, info)
  #   trans_fields = get_translatable_fields_for_model(self.Meta.model)
  #   all_fields = []


  #   requested_langs = []
  #   if 'request' in self.context:
  #     lang_param = self.context['request'].query_params.get('lang', None)
  #     print("lang_param:", lang_param)
  #     requested_langs = lang_param.split(',') if lang_param else []
  #     print("requested_langs:", requested_langs)

  #   for f in fields:
  #     if f not in trans_fields:
  #         all_fields.append(f)
  #     else:
  #         for l in settings.LANGUAGES:
  #             if not requested_langs or l[0] in requested_langs:
  #                 all_fields.append("{}_{}".format(f, l[0]))
  #   print("all_fields:", all_fields)
  #   print()
  #   print("fields:", fields)
  #   print()
  #   print("trans_fields:", trans_fields)
  #   print()

  #   return all_fields

