from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from box.apps.sw_shop.sw_catalog import settings as item_settings


from box.apps.sw_shop.sw_catalog.models import Item, ItemCategory, ItemReview
from box.apps.sw_shop.sw_catalog.api.serializers import ItemDetailSerializer, ItemReviewSerializer
from box.apps.sw_shop.sw_cart.utils import get_cart
from box.core.utils import get_line
from box.apps.sw_shop.sw_catalog.api.search import filter_search
from box.core.mail import box_send_mail
from box.core.sw_global_config.models import GlobalConfig
from box.apps.sw_shop.sw_catalog.models import CatalogueConfig


from rest_framework import generics 
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import * 
from .paginators import * 

import json 

from ast import literal_eval

import logging

logger = logging.getLogger(__name__)



class ItemList(generics.ListCreateAPIView):
  queryset = Item.objects.all()
  serializer_class = ItemListSerializer
  pagination_class = StandardPageNumberPagination

  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)

  def get_queryset(self):
    '''
    :category_ids: айді категорІЙ(МАССИВ З ЦИФРАМИ)
    :max_price: максимальна ціна(цифра)
    :min_price: мінімальна ціна(цифра)
    :is_discount: true|false
    :ordering: -price | price 
    '''
    queryset     = super().get_queryset().filter(is_active=True).order_by('order')
    data         = self.request.query_params
    category_id  = data.get('category_id', None)
    max_price    = data.get('max_price', None)
    min_price    = data.get('min_price', None)
    is_discount  = data.get('is_discount', None)
    ordering     = data.get('ordering', None)
    category_ids = data.get('category_ids', [])
    attributes   = data.get('attributes', [])
    features     = data.get('features', [])
    brand_slugs  = data.get('brand_slugs','').split(',')

    if brand_slugs != ['']:
      queryset = queryset.filter(brand__slug__in=brand_slugs)
      
    if category_id is not None:
      cat = ItemCategory.objects.get(id=category_id)
      descentant_ids = list(cat.get_descendants().values_list('id', flat=True))
      descentant_ids.append(cat.id) 
      queryset = queryset.filter(category__id__in=descentant_ids)

      # if item_settings.FILTER_BY_CATEGORY
      #   queryset = queryset.filter(category__id=category_id)
      # elif item_settings.FILTER_BY_SUBCATEGORIES:
      #   descentant_ids = cat.get_descendants()
      #   queryset = queryset.filter(category__id__in=descentant_ids)
    if category_ids: category_ids = json.loads(category_ids)#; category_ids = literal_eval(category_ids)
    if category_ids:
      queryset = queryset.filter(category__id__in=category_ids)
    
    if max_price:
      queryset = queryset.filter(price__lte=max_price)
    
    if min_price:
      queryset = queryset.filter(price__gte=min_price)
    
    if is_discount == 'true' or is_discount is True:
      queryset = queryset.exclude(discount=0)

    if ordering is not None:
      queryset = queryset.order_by(ordering)

    if attributes: attributes = json.loads(attributes)
    for attribute in attributes:
      if attribute.get('attribute_id') and attribute.get('value_ids'):
        values = AttributeValue.objects.filter(id__in=attribute['value_ids'])
        attribute = Attribute.objects.get(id=attribute['attribute_id'])
        item_attributes = ItemAttribute.objects.filter(attribute=attribute)
        item_attribute_ids = ItemAttributeValue.objects.filter(
          item_attribute__in=item_attributes,
          value__in=values,
        ).values_list('item_attribute_id', flat=True)
        item_ids = ItemAttribute.objects.filter(
          id__in=item_attribute_ids,
        ).values_list('item', flat=True)
        queryset = queryset.filter(id__in=item_ids)

    if features: features = json.loads(features)
    for feature in features:
      if feature.get('feature_id') and feature.get('feature_value_id'):
        feature       = Feature.objects.get(id=feature['feature_id'])
        feature_value = FeatureValue.objects.get(id=feature['feature_value_id'])
        item_features = ItemFeature.objects.filter(value__id=feature_value.id)
        item_ids      = item_features.values_list('item__id', flat=True)
        queryset      = queryset.filter(id__in=item_ids)
      elif feature.get('feature_slug') and feature.get('feature_value_slug'):
        feature       = Feature.objects.get(id=feature['feature_slug'])
        feature_value = FeatureValue.objects.get(id=feature['feature_value_slug'])
        item_features = ItemFeature.objects.filter(value__slug=feature_value.id)
        item_ids      = item_features.values_list('item__id', flat=True)
        queryset      = queryset.filter(id__in=item_ids)

    feature_value_slugs = []
    for key, value in data.items():
      if value == "true" and key != 'is_discount':
        feature_value_slugs.append(key)

    if feature_value_slugs:
      item_features = ItemFeature.objects.filter(value__slug__in=feature_value_slugs)
      item_ids      = item_features.values_list('item__id', flat=True)
      queryset      = queryset.filter(id__in=item_ids)
    
    return queryset


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Item.objects.all()
  serializer_class = ItemDetailSerializer
  pagination_class = StandardPageNumberPagination


class ReviewViewSet(ModelViewSet):
  queryset = ItemReview.objects.all().filter(is_active=True)
  serializer_class = ItemReviewSerializer


from django.http import Http404
from rest_framework.decorators import api_view
from box.apps.sw_shop.sw_cart.models import CartItemAttribute


@api_view(['GET','POST','DELETE'])
def delete_option(request):
  if request.method == 'GET':
    data = request.query_params
  else:
    data = request.data
  cart_item_attribute_id   = data.get('cart_item_attribute_id')
  item_attribute_value_id  = data.get('item_attribute_value_id')
  cart_item_attribute      = CartItemAttribute.objects.get(pk=cart_item_attribute_id)
  item_attribute_value     = ItemAttributeValue.objects.get(pk=item_attribute_value_id)
  cart_item_attribute.values.remove(item_attribute_value)
  if cart_item_attribute.values.all().count == 0:
    cart_item_attribute.delete()
  response = {'status':'ok'}
  return Response(response)


from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
  page_size             = 100
  page_size_query_param = 'page_size'
  max_page_size         = 300
  page_query_param      = 'page_number'

class ItemAttributeList(generics.ListAPIView):
  queryset = ItemAttribute.objects.all()#.filter(is_active=True)
  serializer_class = ItemAttributeSerializer
  pagination_class = CustomPageNumberPagination
  
  def get_queryset(self):
    queryset     = super().get_queryset()
    request      = self.request 
    query_params = request.query_params
    item_id      = query_params.get('item_id')
    if item_id:
      queryset = queryset.filter(item__id=item_id)
    return queryset

class ItemAttributeRetrieve(generics.RetrieveAPIView):
  queryset = ItemAttribute.objects.all()#.filter(is_active=True)
  serializer_class = ItemAttributeSerializer

class ItemAttributeValueList(generics.ListAPIView):
  queryset = ItemAttributeValue.objects.all()#.filter(is_active=True)
  serializer_class = ItemAttributeValueSerializer
  pagination_class = CustomPageNumberPagination
  
  def get_queryset(self):
    queryset     = super().get_queryset()
    request      = self.request 
    query_params = request.query_params
    item_attribute_id      = query_params.get('item_attribute_id')
    if item_attribute_id:
      queryset = queryset.filter(item_attribute__id=item_attribute_id)
    return queryset


class ItemAttributeValueRetrieve(generics.RetrieveAPIView):
  queryset = ItemAttributeValue.objects.all()#.filter(is_active=True)
  serializer_class = ItemAttributeValueSerializer
  





@csrf_exempt
def create_review(request):
    item_id = request.POST['item_id']
    rating  = request.POST['product_rating']
    text    = request.POST.get('text', '---')
    name    = request.POST.get('name', '---')
    phone   = request.POST.get('phone', '---')
    email   = request.POST.get('email', '---')
    item    = Item.objects.get(id=item_id)
    review  = ItemReview.objects.create(
      item=item,
      text=text,
      phone=phone,
      email=email,
      name=name,
      rating=rating,
    )
    # if GlobalConfig.get_solo().auto_review_approval:
    #   review.is_active = True 
    #   review.save()
    json_review = ItemReviewSerializer(review).data
    response = {
      "review":json_review,
      "reviews_count":item.reviews.all().count(),
      "current_star":rating,
      "rounded_stars":item.rounded_stars,
      "stars":item.stars,
      "is_active":review.is_active,
      "status":"OK"
    }
    box_send_mail(
      subject=(f"Отримано відгук до товару {item.title}"),
      template='mail/item_review_mail.html', 
      email_config=CatalogRecipientEmail,
      model=review,
    )
    return JsonResponse(response)







# OLD 





def filter_category(items, query):
  category = query.get('category')
  if category:
    if item_settings.MULTIPLE_CATEGORY:
      cat1 = ItemCategory.objects.all().get(slug=category)
      cat2 = ItemCategory.objects.all().filter(parent__slug=category)
      categories = [
        cat1,
      ]
      for cat in cat2:
        categories.append(cat)
      items = Item.active_objects.all().filter(categories__in=categories)
    else:
      items = items.filter(
        Q(category__slug=category) |
        Q(category__parent__slug=category) |
        Q(category__parent__parent__slug=category)
      ).distinct()
  return items



def paginate(items, query):
  response     = {}
  page_number  = query.get('page', 1)
  per_page     = query.get('per_page', CatalogueConfig.get_solo().items_per_page)
  ordering     = query.get('sort', '-created')
  if not item_settings.PAGINATE_AJAX:
    page = items      
  else:
    page = Paginator(items, per_page=per_page).get_page(page_number)
    is_paginated = page.has_other_pages()
    current_page = page.number
    last_page    = page.paginator.num_pages
    page_range   = page.paginator.page_range
    has_prev     = page.has_previous()
    has_next     = page.has_next()
    next_url     = f'?page={page.next_page_number()}' if has_next else ''
    prev_url     = f'?page={page.previous_page_number()}' if has_prev else ''
    first_url    = f'?page=1'
    last_url     = f'?page={last_page}'
    response.update({
      'is_paginated':    is_paginated,
      'current_page':    current_page,
      'page_range':      list(page_range),
      'last_page':       last_page,
      'first_url':       first_url,
      'next_url':        next_url,
      'prev_url':        prev_url,
      'last_url':        last_url,
      'has_prev':        has_prev,
      'has_next':        has_next,
    })

  page_items = ItemDetailSerializer(page, many=True, read_only=True).data
  response = {
    'paginated_items': page_items,
  }
  return response


def make_ordering(items, query):
  ordering = query.get('sort', '-created')
  if ordering:
    items = items.order_by(ordering)
  return items

@csrf_exempt
def get_items(request):
  query = request.POST
  items = Item.active_objects.all()
  items = filter_search(items, query)
  items = filter_category(items, query)
  items = make_ordering(items, query)
  response = paginate(items, query)

  # items_in_favours = get_items_in_favours(request, items)
  # items_in_cart    = get_items_in_cart(request, items)
  # json_items   = ItemDetailSerializer(items, many=True, read_only=True).data
  # TODO: кешування. Коли на сайті 1000+ товарів, то вони серіалізуються 10 сеукнд
  response.update({
    # 'items_in_favours':items_in_favours,
    # 'items_in_cart':   items_in_cart,
    # 'json_items':      json_items,
  })
  return JsonResponse(response)




@csrf_exempt
def get_item(request):
  query   = request.POST or request.GET
  item_id = query.get('item_id', 1)
  item = Item.objects.get(id=item_id)
  item = ItemDetailSerializer(item).data
  response = item
  return JsonResponse(response)


