from django.utils.translation import gettext_lazy as _
from django.db import models 
from box.core.models import AbstractPage, BaseMixin
# from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline
# from adminsortable.fields import SortableForeignKey
from ..utils import generate_unique_slug, item_image_folder
from django.contrib.auth import get_user_model
from django.conf import settings 
from box.core import settings as core_settings
from colorfield.fields import ColorField
from django.utils import timezone 
from PIL import Image, ImageEnhance

from io import BytesIO
from django.core.files import File

User = get_user_model()

class ItemView(models.Model):
    sk   = models.CharField(verbose_name=_("Ключ сесії"), max_length=255)
    ip   = models.CharField(verbose_name=_("IP-адреса"), max_length=255)
    item = models.ForeignKey(
        verbose_name=_("Товар"), to="sw_catalog.Item", on_delete=models.CASCADE
    )
    def __str__(self):
        return f'{self.sk}: {self.item.title}'

class ItemUnit(models.Model):
    name = models.CharField(
        verbose_name=_("Назва"), unique=True, max_length=255,
    )

    def __str__(self):
        return f'{self.name}'
    
    @classmethod
    def modeltranslation_fields(self):
        return [
            'name',
        ]
    
    class Meta:
        verbose_name = _("одиниця вимірювання товарів")
        verbose_name_plural = _("одиниці вимірювання товарів")



class ItemBrand(AbstractPage):

    def get_absolute_url(self):
        try:
            return reverse("brand", kwargs={"slug": self.slug})
        except:
            return '' 
            
    class Meta:
        verbose_name = _('Бренд')
        verbose_name_plural = _("Бренди")
        ordering = ['order']


def compress(image):
    im = Image.open(image)
    im_io = BytesIO() 
    im.save(im_io, 'JPEG', quality=40) 
    name = image.name
    name = image.name.split('/')[-1]
    new_image = File(im_io, name=name)
    return new_image


# from filer.fields.image import FilerImageField
# from filer.fields.file import FilerFileField

class ItemImage(models.Model):
    order           = models.PositiveIntegerField(
        verbose_name=_("Порядок"), default=0, blank=False, null=False
    )
    # item      = SortableForeignKey(
    item      = models.ForeignKey(
        verbose_name=_("Товар"), to="sw_catalog.Item", 
        on_delete=models.SET_NULL, 
        related_name='images', null=True,
    )
    
    # image     = FilerImageField(
        # on_delete=models.CASCADE,
    image     = models.ImageField(
        verbose_name=_('Ссилка зображення'), 
        upload_to=item_image_folder, 
        blank=True, null=True, 
    )
    alt = models.CharField(
        verbose_name=_("Альт"), max_length=255, blank=True, null=True,
    )

    def __str__(self):
        return "%s" % self.image
    
    def save(self, *args, **kwargs):	
        # img = Image.open(self.image.path)
        # img = img.resize((400, 400), Image.ANTIALIAS)
        # img.save(self.image.path)
        # self.handle_image(*args, **kwargs)
        # new_image = compress(self.image)
        # self.image = new_image
        super().save(*args, **kwargs)

    def handle_image(self, *args, **kwargs):
        # image = Image.open('image.jpg')
        # watermark = Image.open('watermark.png')
        # image.paste(watermark, (x, y), watermark)
        # x = self.add_watermark(self.image, 'watermarks/sample.png')
        # self.image = x
        print(x)

    def add_watermark(self, image, watermark, opacity=1, wm_interval=0):
        assert opacity >= 0 and opacity <= 1
        if opacity < 1:
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')
            else:
                watermark = watermark.copy()
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark.putalpha(alpha)
        layer = Image.new('RGBA', (400,400), (0,0,0,0))
        # layer = Image.new('RGBA', image.size, (0,0,0,0))
        for y in range(0, image.size[1], watermark.size[1]+wm_interval):
            for x in range(0, image.size[0], watermark.size[0]+wm_interval):
                layer.paste(watermark, (x, y))
        return Image.composite(layer,  image,  layer)
        
    @classmethod
    def modeltranslation_fields(cls):
        fields = [
            'alt',
        ]
        return fields
    
    @property
    def image_url(self):
        image_url = core_settings.IMAGE_NOT_FOUND
        # if self.image: image_url = self.image.url 
        if self.image: 
            try:
                x = open(self.image.path)
                image_url = self.image.url 
            except:
                image_url = core_settings.IMAGE_NOT_FOUND
        return image_url

    class Meta: 
        verbose_name = _('зображення товару'); 
        verbose_name_plural = _('зображення товару'); 
        ordering = ['order',]



class ItemManufacturer(BaseMixin):
    name  = models.CharField(verbose_name=_('Назва'), max_length=255)

    @classmethod
    def modeltranslation_fields(cls):
        fields = [
            'name',
        ]
        return fields

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = _('виробник товарів')
        verbose_name_plural = _('виробники товарів')
        ordering = ['order']


class ItemReview(BaseMixin):
    item    = models.ForeignKey(verbose_name=_("Товар"),  blank=True, null=True, to="sw_catalog.Item", on_delete=models.SET_NULL, related_name="reviews",)
    user    = models.ForeignKey(verbose_name=_("Автор"),  blank=True, null=True, to=User, on_delete=models.SET_NULL, related_name="reviews",)
    text    = models.CharField(verbose_name=_("Текст"),  blank=True, null=True, max_length=255)
    phone   = models.CharField(verbose_name=_("Телефон"), blank=True, null=True, max_length=255)
    email   = models.CharField(verbose_name=_("E-mail"),  blank=True, null=True, max_length=255)
    name    = models.CharField(verbose_name=_("Ім'я"),    blank=True, null=True, max_length=255)
    rating  = models.CharField(verbose_name=_("Оцінка"),  blank=True, null=True, max_length=255)

    def __str__(self):
        return f"{self.text}{self.rating}"

    class Meta:
        verbose_name = _('Відгук')
        verbose_name_plural = _('Відгуки')
        ordering = ['order']


class ItemStock(models.Model):
    text         = models.CharField(verbose_name=_('Текст'), max_length=255, unique=True)
    availability = models.BooleanField(verbose_name=_('Можливість покупки'), default=True)
    colour       = ColorField(verbose_name=_('Колір'),  max_length=255)

    def __str__(self):
        return f"{self.text}"
    
    def save(self, *args, **kwargs):
        self.text = self.text.lower().strip()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('статус наявності')
        verbose_name_plural = _('статуси наявності')

    @classmethod
    def modeltranslation_fields(cls):
        fields = [
            'text',
        ]
        return fields




