from django.utils.feedgenerator import (
  Atom1Feed,
  Rss201rev2Feed ,
  RssUserland091Feed ,
  Atom1Feed,
)
from django.contrib.syndication.views import Feed
from .models import Item
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import SyndicationFeed
from django.utils.xmlutils import SimplerXMLGenerator
import itertools
from django.contrib.syndication.views import Feed
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.html import strip_tags
from sorl.thumbnail.base import ThumbnailException
from store.models import Product, OptionItem, ProductCategory

SETTINGS = settings.FEEDS

current_site = Site.objects.get_current()
from django.utils.html import strip_tags

class GoogleProductsFeed(Rss201rev2Feed):
    """
    This class will output most of the non type-specific fields from the
    attribute list here:
    http://www.google.com/support/merchants/bin/answer.py?answer=160085&hl=en

    Note: the per-item shipping and tax fields are omitted as we don't
    currently need them.
    """

    PAYMENT_TYPES = ('Cash', 'Check', 'Visa', 'MasterCard', 'AmericanExpress', 'Discover', 'GoogleCheckout', 'wiretransfer',)
    PRICE_TYPES = ('negotiable', 'starting',)
    ONLINE_ONLY = ('y', 'n',)
    CONDITIONS = ('new', 'used', 'refurbished',)
    FREE_SHIPPING_PRICE = "0.00"

    def rss_attributes(self):
        attrs = super(GoogleProductsFeed, self).rss_attributes()
        attrs['xmlns:g'] = 'http://base.google.com/ns/1.0'
        attrs['xmlns:c'] = 'http://base.google.com/cns/1.0'
        return attrs

    def add_item_elements(self, handler, item):
        super(GoogleProductsFeed, self).add_item_elements(handler, item)

        # we only show in stock products
        handler.addQuickElement(u"g:availability", 'in stock')

        if item['google_category'] is not None:
            handler.addQuickElement(u"g:google_product_category", item['google_category'])

        if item['brand'] is not None:
            handler.addQuickElement(u"g:brand", item['brand'])

        if item['colors'] is not None:
            for color in item['colors']:
                handler.addQuickElement(u"g:color", color)

        if item['condition'] in self.CONDITIONS:
            handler.addQuickElement(u"g:condition", item['condition'])

        if item['ean'] is not None:
            handler.addQuickElement(u"g:ean", item['ean'])

        if item['features'] is not None:
            for feature in item['features']:
                handler.addQuickElement(u"g:feature", feature)

        # we don't want this since Django RSS feeds already have guid elements
        #handler.addQuickElement(u"g:id", item['id'])

        if item['image_links'] is not None:
            # 1st image is "image_link"
            # then up to 10 "additional_image_link"s maybe used
            key = u"g:image_link"
            for img in item['image_links']:
                handler.addQuickElement(key, img)
                key = u"g:additional_image_link"

        if item['made_in'] is not None:
            handler.addQuickElement(u"g:made_in", item['made_in'])

        if item['manufacturer'] is not None:
            handler.addQuickElement(u"g:manufacturer", item['manufacturer'])

        if item['materials'] is not None:
            for material in item['materials']:
                handler.addQuickElement(u"g:material", material)

        if item['model_number'] is not None:
            handler.addQuickElement(u"g:model_number", item['model_number'])

        if item['mpn'] is not None:
            handler.addQuickElement(u"g:mpn", item['mpn'])

        if item['online_only'] is not None and item['online_only'] in self.ONLINE_ONLY:
            handler.addQuickElement(u"g:online_only", item['online_only'])

        if item['payments_accepted'] is not None:
            for payment in item['payments_accepted']:
                if payment in self.PAYMENT_TYPES:
                    handler.addQuickElement(u"g:payment_accepted", payment)

        if item['payment_notes'] is not None:
            handler.addQuickElement(u"g:payment_notes", item['payment_notes'])

        handler.addQuickElement(u"g:price", '%(price)s %(currency)s' % item)

        if item['price_type'] is not None and item['price_type'] in self.PRICE_TYPES:
            handler.addQuickElement(u"g:price_type", item['price_type'])

        if item['product_types'] is not None:
            for type in item['product_types']:
                handler.addQuickElement(u"g:product_type", type)

        if item['quantity'] is not None:
            handler.addQuickElement(u"g:quantity", item['quantity'])

        if item['sizes'] is not None:
            for size in item['sizes']:
                handler.addQuickElement(u"g:size", size)

        if item['upc'] is not None:
            handler.addQuickElement(u"g:upc", item['upc'])

        if item['youtube_videos'] is not None:
            for video in item['youtube_videos']:
                handler.addQuickElement(u"g:youtube", video)

        handler.startElement(u'g:shipping', {})
        handler.addQuickElement(u"g:price", self.FREE_SHIPPING_PRICE)
        handler.endElement(u'g:shipping')


class GoogleProducts(Feed):
    feed_type = GoogleProductsFeed

    title = 'Products From Your Store'
    link = 'http://www.yoursite.com/'
    description = 'Google Product Search feed'

    DESC_LEN = 10000
    MAX_ATTRS = 10
    ROOT_CAT_TO_GCAT = {
        'Sneakers': 'Clothing & Accessories > Shoes',
        'Clothing': 'Clothing & Accessories > Clothing',
        }

    def __call__(self, request, *args, **kwargs):
        self.item_sizes = {}
        return super(GoogleProducts, self).__call__(request, *args, **kwargs)

    def body_func(self, item):
        return item.body

    def get_item_sizes(self, item):
        return self.item_sizes[item.pk]

    def item_title(self, item):
        return '%s %s, %s' % (item.brand.name, item.short_name, item.colour)

    def item_description(self, item):
        """
        We append the in-stock sizes to the end of the description because
        Google reject the product if > 10 sizes submitted in size attributes:
        http://www.google.com/support/forum/p/base/thread?tid=342324990311782f&hl=en
        """
        sizes_str = ' Sizes in stock: %s' % ','.join(self.get_item_sizes(item))
        return '%s%s' % (
            strip_tags(item.editors_notes)[:self.DESC_LEN - len(sizes_str)],# char limit
            sizes_str
        )

    def item_link(self, item):
        return "http://%s%s?utm_source=google_product_search&utm_medium=organic&utm_campaign=google_product_search" % (current_site.domain, item.get_absolute_url())

    def item_extra_kwargs(self, item):
        def filter_sizes(sizes):
            "trims the set of in-stock sizes down to 10 significant ones"
            surplus = len(sizes) - self.MAX_ATTRS
            # start by eliminating half-sizes
            i = 0
            while surplus > 0 and i < len(sizes):
                if str(sizes[i])[-2:] == '.5':
                    sizes.pop(i)
                    surplus -= 1
                i += 1
            # then chop sizes off the end
            while surplus > 0:
                sizes.pop()
                surplus -= 1
            return sizes

        def get_root_cat(item):
            try:
                cat = item.categories.all()[0]
            except ProductCategory.DoesNotExist, IndexError:
                return None
            root_category = cat.get_root()
            return self.ROOT_CAT_TO_GCAT.get(root_category.title, None)

        product_data = {
            'google_category': get_root_cat(item),
            'brand': item.brand.name,
            'colors': list(item.colour_tags.values_list('name', flat=True))[:self.MAX_ATTRS-1] + [item.colour],
            'condition': 'new',
            'ean': None,
            'features': None,
            'image_links': None,
            'made_in': None,
            'manufacturer': item.brand.name,
            'materials': None,
            'model_number': None, # this must be unique, not as important as below
            'mpn': item.manufacturer_product_code,
            'online_only': 'y',
            'payments_accepted': ['Visa', 'MasterCard', 'AmericanExpress', ],
            'payment_notes': 'PayPal',
            'price': str(item.get_prices()['selling']),
            'currency': 'GBP',
            'price_type': None,
            'product_types': list(set(itertools.chain.from_iterable([cat.google_taxonomy_list for cat in item.categories.all()])))[:self.MAX_ATTRS],
            'quantity': str(item.denorm_stock),
            'sizes': filter_sizes(list(self.get_item_sizes(item))),
            'upc': None,
            'youtube_videos': None,
        }

        # use 1 + self.MAX_ATTRS items, as [1:] images are put as 10 "additional" image links
        if item.gallery() is not None:
            try:
                product_data['image_links'] = ['http://%s%s' % \
                    (current_site.domain, img.image.extra_thumbnails['product_fullsize']) \
                    for img in item.gallery().images.all()[:1+self.MAX_ATTRS] \
                    if 'product_fullsize' in img.image.extra_thumbnails]
            except OverflowError:
                pass
            except ThumbnailException:
                pass

        return product_data

    def items(self):
        return Product.live_objects.all().select_related()















class CustomSyndicationFeed(SyndicationFeed):

    mime_type = 'application/xml'
    content_type = 'application/xml'

    def write(self, outfile, encoding):
        handler = SimplerXMLGenerator(outfile, encoding)
        handler.startDocument()
        handler.startElement("root", self.root_attributes())
        self.add_root_elements(handler)
        self.write_items(handler)
        handler.endElement("root")

    def add_root_elements(self, handler):
        # Add root elements here
        handler.addQuickElement("my_feed_title", self.feed['title'])
        handler.addQuickElement("my_feed_url", self.feed['link'])

    def write_items(self, handler):
        for item in self.items:
            handler.startElement('my_item', self.item_attributes(item))
            self.add_item_elements(handler, item)
            handler.endElement("my_item")

    @staticmethod
    def _safe_add_element(handler, item, attr):
        # Add attribute to xml only if it is present, no empty tags
        if item.get(attr):
            handler.addQuickElement(attr, item[attr])

    def add_item_elements(self, handler, item):
        # Handle each element that needs to be added to an xml item
        # 'item' is a dict of attributes
        handler.addQuickElement('title', item['title'])
        # handler.addQuickElement('date', item['date'])
        # handler.addQuickElement('link', item['link'])
        handler.addQuickElement('description', item['description'])

        self._safe_add_element(handler, item, 'city')
        self._safe_add_element(handler, item, 'postalcode')



