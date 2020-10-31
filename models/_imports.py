from django.db import models 
from django.contrib import admin 
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.db import models
from django.utils.html import mark_safe
from django.core.files.base import ContentFile
from django.conf import settings 
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models.signals import post_save, pre_save

from tinymce import HTMLField
from transliterate import translit, get_available_language_codes#, slugify
from adminsortable.fields import SortableForeignKey
# from mptt.models import MPTTModel, TreeForeignKey
from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline
from adminsortable.fields import SortableForeignKey
import os 
from PIL import Image

from box.core.managers import *
from box.core.models import AbstractPage, BaseMixin
from ..utils import generate_unique_slug, item_image_folder


User = get_user_model()

