


def generate_unique_slug(klass, field, item, *args, **kwargs):
	origin_slug = slugify(translit(field, reversed=True)) # slugify(field)
	unique_slug = origin_slug
	numb = 1
	obj = klass.objects.filter(slug=unique_slug)
	while obj.exists():
		obj = obj.first()
		unique_slug = f'{origin_slug}-{numb}'
		numb += 1
	return unique_slug


def item_image_folder(instance, full_filename):
	foldername   = instance.item.slug
	raw_filename = full_filename.strip().split('.')
	ext          = raw_filename[-1].strip()
	filename     = raw_filename[0].strip()
	filename     = f'{filename}.{ext}'
	path         = '/'.join(['shop', 'item', foldername, filename])
	return path 

def get_image_path(item, full_filename):
	foldername   = item.slug
	raw_filename = full_filename.strip().split('.')
	ext          = raw_filename[-1].strip()
	filename     = raw_filename[0].strip()
	filename     = f'{filename}.{ext}'
	path         = '/'.join(['shop', 'item', foldername, filename])
	return path 

