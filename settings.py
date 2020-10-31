from django.conf import settings 

def get(a, b):
    return getattr(settings, a, b) 

MULTIPLE_CATEGORY      = get('MULTIPLE_CATEGORY', False) 
ITEM_SEARCH_FIELDS     = get('ITEM_SEARCH_FIELDS', ['code',]) 
ITEM_URL_NAME          = get('ITEM_URL_NAME', "item")
ITEM_MEDIA_PATH        = get('ITEM_MEDIA_PATH',  '/')
ITEM_CATEGORY_URL_NAME = get('ITEM_CATEGORY_URL_NAME', 'item_category')
PAGINATE_AJAX          = get('PAGINATE_AJAX', True)


FILTER_BY_CATEGORY      = get('FILTER_BY_CATEGORY', True)
FILTER_BY_SUBCATEGORIES = get('FILTER_BY_SUBCATEGORIES', False)

if FILTER_BY_CATEGORY == FILTER_BY_SUBCATEGORIES:
    raise('FILTER_BY_CATEGORY and FILTER_BY_SUBCATEGORIES cant be equal')





ITEM_UPLOAD_TO = 'shop/item/'


