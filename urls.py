from django.urls import path, include
from .views import GoogleMerchant, prom_export


urlpatterns = [
  path('api/', include('sw_catalog.api.urls')),
  path('google.xml/', GoogleMerchant()),
  path('prom.csv/', prom_export),
]



