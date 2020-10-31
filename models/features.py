from django.db import models 
from django.utils.text import slugify

from box.core.helpers import get_admin_url 

from transliterate import translit


def generate_unique_slug(instance, slug):
	objects = instance._meta.model.objects.all()
	origin_slug = slug
	numb = 1
	while objects.filter(slug=slug).exclude(pk=instance.pk).exists():
		slug = f'{origin_slug}-{numb}'
		numb += 1
	return slug 


def trans_slug(instance, field_name):
	try:
		slug = slugify(translit(getattr(instance, field_name), reversed=True))
	except Exception as e:
		slug = slugify(getattr(instance, field_name))
	return slug 


def handle_slug(instance, field_name, *args, **kwargs):
	if instance.slug:
		slug = instance.slug 
	elif not instance.slug:
		slug = trans_slug(instance, field_name)
	instance.slug = generate_unique_slug(instance, slug)
	return instance


class FeatureCategory(models.Model):
    name = models.CharField(verbose_name="Назва", max_length=255)
    slug = models.SlugField(verbose_name="Слаг", unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        handle_slug(self, 'name')
        super().save(*args, **kwargs)

    def get_admin_url(self):
        return get_admin_url(self)

    @classmethod
    def modeltranslation_fields(self):
        return ['name']
    
    def get_item_features(self, item):
        return ItemFeature.objects.filter(item=item,category=self)

    class Meta:
        verbose_name = 'категорія характеристик'
        verbose_name_plural = 'категорії характеристик'

    def __str__(self):
        return f'{self.name}'


class FeatureValue(models.Model):
    value = models.CharField(verbose_name="Значення", max_length=255)
    code  = models.SlugField(verbose_name="Код", unique=True, null=True, blank=True)
    slug = models.SlugField(verbose_name="Слаг", unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        handle_slug(self, 'value')
        super().save(*args, **kwargs)

    def get_admin_url(self):
        return get_admin_url(self)

    def __str__(self):
        return f'{self.value}'

    @classmethod
    def modeltranslation_fields(self):
        return ['value']

    class Meta:
        verbose_name = 'значення характеристики'
        verbose_name_plural = 'значення характеристик'


class Feature(models.Model):
    name = models.CharField(verbose_name="Назва", max_length=255)
    code = models.SlugField(verbose_name='Код', blank=True, null=True, unique=True)
    slug = models.SlugField(verbose_name="Слаг", unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        handle_slug(self, 'name')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
    
    def get_admin_url(self):
        return get_admin_url(self)
        
    @classmethod
    def modeltranslation_fields(self):
        return ['name']
    
    def get_values(self, item=None):
        item_features = ItemFeature.objects.filter(name=self)
        if item:
            item_features = item_features.filter(item=item)
        features_value_ids = item_features.values_list('value__id', flat=True)
        values = FeatureValue.objects.filter(id__in=features_value_ids)
        return values
    

    class Meta:
        verbose_name = 'назва характеристики'
        verbose_name_plural = 'назви характеристик'


class ItemFeature(models.Model):
    # items = models.ManyToManyField(to="sw_catalog.Item", verbose_name="Товари", related_name="item_features", blank=)
    item      = models.ForeignKey(to="sw_catalog.Item", verbose_name="Товар", on_delete=models.CASCADE)
    name      = models.ForeignKey(to="sw_catalog.Feature", verbose_name="Назва характеристики", on_delete=models.CASCADE)
    value     = models.ForeignKey(to="sw_catalog.FeatureValue", verbose_name="Значення характеристики", on_delete=models.CASCADE)
    category  = models.ForeignKey(verbose_name='Категорія', to='sw_catalog.FeatureCategory', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Активність", default=True)
    code      = models.SlugField(verbose_name='Код', blank=True, null=True, unique=True)

    def get_admin_url(self):
        return get_admin_url(self)
        
    def __str__(self):
        return f'{self.name}:{self.value} - {self.item}'

    class Meta:
        verbose_name = 'характеристика товара'
        verbose_name_plural = 'характеристики товара'



