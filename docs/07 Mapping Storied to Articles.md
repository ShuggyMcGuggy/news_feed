# Create a from to enable Articel to be mapped to Stories

## Useful Links
- [How to create a dynamic selection](https://samiddha99.medium.com/implement-dynamic-select-options-with-django-d04e791f0483)

## Steps

- Create a URL for mapping that passes the reerence ID for the article
- Create a view that passes the article detail and story objects in the context
- Create a page that shows:
  - Article: the article details 
  - Mapped Stories: the list of mapped stories from the look up table
- Change the view to be a form to take the selection of the story and create a new mapping tabel entry

## How to use mutiple filter criterions for django objects
the objects.filter(*query goes here*) can include mutiple query criteria.
The format is very specific.

for example I can filter using a match against several items using:

filtered_objects = objects.filter(attribute_id__in=[1,2,3])

Read the following link for more information:

- [Guide to filters available](https://pythonguides.com/python-django-filter/)