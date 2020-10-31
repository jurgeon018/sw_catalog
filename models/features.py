from django.db import models 


class FeatureCategory(models.Model):
    name = models.CharField(verbose_name="Назва", max_length=255)

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

    def __str__(self):
        return f'{self.name}'
    
    @classmethod
    def modeltranslation_fields(self):
        return ['name']

    class Meta:
        verbose_name = 'назва характеристики'
        verbose_name_plural = 'назви характеристик'


class ItemFeature(models.Model):
    # items = models.ManyToManyField(to="sw_catalog.Item", verbose_name="Товари")
    item      = models.ForeignKey(to="sw_catalog.Item", verbose_name="Товар", on_delete=models.CASCADE)
    name      = models.ForeignKey(to="sw_catalog.Feature", verbose_name="Назва характеристики", on_delete=models.CASCADE)
    value     = models.ForeignKey(to="sw_catalog.FeatureValue", verbose_name="Значення характеристики", on_delete=models.CASCADE)
    category  = models.ForeignKey(verbose_name='Категорія', to='sw_catalog.FeatureCategory', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Активність", default=True)
    code      = models.SlugField(verbose_name='Код', blank=True, null=True, unique=True)

    def __str__(self):
        return f'{self.name}:{self.value} - {self.item}'

    class Meta:
        verbose_name = 'характеристика товара'
        verbose_name_plural = 'характеристики товара'



