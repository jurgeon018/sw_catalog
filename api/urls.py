from django.urls import path, include 
from .views import * 


urlpatterns = [
  path('items/', ItemList.as_view()),
  path('items/<pk>/', ItemDetail.as_view()),
  path('item_attributes/', ItemAttributeList.as_view()),
  path('item_attributes/<pk>/', ItemAttributeRetrieve.as_view()),
  path('item_attribute_values/', ItemAttributeValueList.as_view()),
  path('item_attribute_values/<pk>/', ItemAttributeValueRetrieve.as_view()),
  path('delete_option/', delete_option),
  path('create_review/', create_review),
  path('get_items/', get_items, name='get_items'),
  path('get_item/', get_item, name='get_item'),
]





