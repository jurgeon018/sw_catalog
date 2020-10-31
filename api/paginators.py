from rest_framework.pagination import BasePagination, LimitOffsetPagination, PageNumberPagination, CursorPagination


from box.apps.sw_shop.sw_cart.utils import get_cart


def get_items_in_favours(request, items):
  items_in_favours = []
  for item in items:
    cart = get_cart(request)
    # if cart.favour_items.all().exists():
    if cart.favour_items.filter(item=item).exists():
      items_in_favours.append(item.id)
  return items_in_favours


def get_items_in_cart(request, items):
  items_in_cart = []
  for item in items:
    cart = get_cart(request)
    if cart.items.filter(item=item).exists():
      items_in_cart.append(item.id)
  return items_in_cart


class StandardPageNumberPagination(PageNumberPagination):
    page_size              = 6
    max_page_size          = 1000
    page_query_param       = 'page_number'
    page_size_query_param  = 'per_page'
    
    def get_paginated_response(self, data):
        items = self.page.object_list
        response = super().get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['page_number'] = self.page.number
        response.data['items_in_cart'] = get_items_in_cart(self.request, items)
        response.data['items_in_favours'] = get_items_in_favours(self.request, items)
        return response

class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit      = 10
    max_limit          = 1000
    limit_query_param  = 'limit'
    offset_query_param = 'offset'


class StandardCursorPagination(CursorPagination):
    page_size = 10 
    cursor_query_param = 'cursor'
    ordering = '-id'
