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