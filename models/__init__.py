from .attribute import * 
from .features import * 
from .config import * 
from .category import * 
# from box.core.sw_currency.models import * 
from .item_related import * 
from .item import * 

from box.core.models import AbstractRecipientEmail

from django.utils.translation import ugettext_lazy as _


class CatalogConfig(SingletonModel):

  def __str__(self):
    return f'{self.id}'

  class Meta:
    verbose_name = _("Налаштування каталогу")
    verbose_name_plural = verbose_name
    

class CatalogRecipientEmail(AbstractRecipientEmail):
  config = models.ForeignKey(
    verbose_name=_("Налаштування"),to="sw_catalog.CatalogConfig", 
    on_delete=models.CASCADE, related_name='emails',
  )

  class Meta:
      verbose_name = _('емейл для сповіщень про товари')
      verbose_name_plural = _("емейли для сповіщень про товари")

