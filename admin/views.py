
from django.shortcuts import render 
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect 
from django.conf import settings 

# from box.apps.sw_shop.sw_catalog.parser.main import *
from box.core.sw_imp_exp.main import ExportMixin

from box.apps.sw_shop.sw_catalog.models import Item, ItemImage


@staff_member_required
def feed_items(request):
  if request.method == 'POST':
    f = request.FILES['file'] 
    status = read_items_from_xlsx(f)
    if status:
      messages.success(request, 'Товари були успішно завантажені')
    else:
      messages.warning(reqeust, 'Сталась помилка')
  return render(request, 'feed_items.html', locals())


@staff_member_required
def delete_item_photoes(request, slug):
  Item.objects.get(slug=slug).images.all().delete()
  return redirect(request.META.get('HTTP_REFERER', '/admin/'))


@staff_member_required
def delete_item_features(request, slug):
  Item.objects.get(slug=slug).features.all().delete()
  return redirect(request.META.get('HTTP_REFERER', '/admin/'))


@staff_member_required
def import_item_photoes(request, slug=None):
  from box.apps.sw_shop.sw_catalog.models import Item, ItemImage
  from django.core.files.base import ContentFile
  from PIL import Image 
  from django.utils import timezone 
  if slug:

    item = Item.objects.get(slug=slug)
    files = request.FILES.getlist('files', [])

    for f in files:
      img = ItemImage.objects.create(item=item)
      img.image.save(
        f'{timezone.now()}.png',
        ContentFile(f.read()),
      )
      img.save()
  return redirect(request.META.get('HTTP_REFERER', '/admin/'))


@staff_member_required
def export_item_photoes(request, slug=None):
  from box.imp_exp.main import ExportMixin
  export   = ExportMixin()
  queryset = Item.objects.filter(slug=slug)
  response = export.admin_export_items_photoes(request, queryset)
  return response





