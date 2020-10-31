
from box.core.sw_solo.models import SingletonModel
from django.db import models 
from django.utils.translation import gettext_lazy as _ 



class CatalogueConfig(SingletonModel):
  PENNY_DIVIDER = (
    ('dot','.'),
    ('coma',','),
  )
  THOUSANDS_DIVIDER = (
    ("no","без роздільника: 1234567 грн"),
    ("space","пробіл: 1 234 456 грн "),
    ("coma","кома: 1,234,456"),
  )
  ABSENT_ITEMS_POSITION = (
    ("default","default"),
    ("end","end"),
    ("hide","hide"),
  )

  items_per_page               = models.PositiveIntegerField(verbose_name=_("Товарів на сторінці сайту"), null=True, default=24)
  posts_per_page               = models.PositiveIntegerField(verbose_name=_("Статей на сторінці блоґу"), default=50)
  # max_order_items              = models.PositiveIntegerField(verbose_name=_("Максимум товарів у замовленні"), default=24)
  # max_comparison_items         = models.PositiveIntegerField(verbose_name=_("Максимум товарів у порівнянні"), default=50)
  # item_measurment_unit         = models.CharField(verbose_name=_("Одиниці вимірювання товарів"), default="шт", max_length=255)
  # penny_divider                = models.CharField(verbose_name=_("Роздільник копійок"), choices=PENNY_DIVIDER, default=0, max_length=255)
  # thousands_divider            = models.CharField(verbose_name=_("Роздільник тисяч"), choices=THOUSANDS_DIVIDER, default=0, max_length=255)
  # absent_items_position        = models.CharField(verbose_name=_("Відсутні товари "), choices=ABSENT_ITEMS_POSITION, default=0, max_length=255)
  # absent_items_preorder        = models.BooleanField(verbose_name=_("Передзамовлення відсутніх товарів"), default=False)
  # empty_categories_visibility  = models.BooleanField(verbose_name=_("Відображати порожні категорії"), default=False)

  clear_catalogue              = models.BooleanField(verbose_name=_(" Очистити каталог товарів "), default=False)
  # https://stackoverflow.com/questions/849142/how-to-limit-the-maximum-value-of-a-numeric-field-in-a-django-model
  # watermark_horizontal         = models.PositiveIntegerField(verbose_name=_("Горизонтальне положення водяного знака (лівіше-правіше)"), blank=True, null=True)#, max_value=100, min_value=1)
  # watermark_vertical           = models.PositiveIntegerField(verbose_name=_("Вертикальне положення водяного знака (вижче-нижче)"), blank=True, null=True)#, max_value=100, min_value=1)

  def __str__(self):
    return f'{self.id}'
  
  def __save__(self, *args, **kwargs):
    if self.clear_catalogue:
      Item.objects.all().delete()
    super().save(*args, **kwargs)
  
  class Meta:
    verbose_name        = _('Налаштування каталогу')
    verbose_name_plural = _('Налаштування каталогу')



