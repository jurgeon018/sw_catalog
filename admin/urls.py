from django.urls import path 
from .views import * 


urlpatterns = [

  path('feed_items/', feed_items, name="feed_items"),
  path('export_item_photoes/<slug>/',  export_item_photoes,  name='export_item_photoes'),
  path('import_item_photoes/<slug>/',  import_item_photoes,  name='import_item_photoes'),
  path('delete_item_photoes/<slug>/',  delete_item_photoes,  name='delete_item_photoes'),
  path('delete_item_features/<slug>/', delete_item_features, name='delete_item_features'),

]
