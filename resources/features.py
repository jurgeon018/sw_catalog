from import_export.resources import ModelResource 
from ..models import * 


class FeatureCategoryResource(ModelResource):

    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None 

    class Meta:
        model = FeatureCategory
        exclude = []


class FeatureValueResource(ModelResource):

    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None 

    class Meta:
        model = FeatureValue
        exclude = []


class FeatureResource(ModelResource):

    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None 

    class Meta:
        model = Feature
        exclude = []


class ItemFeatureResource(ModelResource):

    def before_import_row(self, row, **kwargs):
        if row.get('code') == '': row['code'] = None 

    class Meta:
        model = ItemFeature
        exclude = []


