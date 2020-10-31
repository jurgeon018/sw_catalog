


def get_family_tree(child):
  subcategories = child.subcategories.all()
  if not subcategories:
      return {
        "title": child.title, 
        "slug":child.slug,
        'id':child.id,
        "items_count":"",
        "subcategories": []
      }
  return {
      "title": child.title,
      "slug":child.slug,
      'id':child.id,
      "subcategories": [get_family_tree(child) for child in subcategories],
  }

