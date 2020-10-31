from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ItemConfig(AppConfig):
    name = 'box.apps.sw_shop.sw_catalog'
    verbose_name = _('каталог')
    verbose_name_plural = verbose_name


default_app_config = 'box.apps.sw_shop.sw_catalog.ItemConfig'
