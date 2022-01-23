#Export Django page as HTML

## Useful Links
- [Link to stakoverlfow export instructions](https://stackoverflow.com/questions/22162027/how-do-i-generate-a-static-html-file-from-a-django-template/22162541)
- [Link use render_to_string to save static HTML](https://stackoverflow.com/questions/22162027/how-do-i-generate-a-static-html-file-from-a-django-template)

## Approach
- Create new url
- create new template 
- use the code to export template to static HTML
- Style the page with bootstrap 5

### Example : Use render_to_string to output static HTML
You can leverage Django's template loader to render your template, including whatever context you pass to it, as a string and then save that out to the filesystem. If you need to save that file on an external system, such as Amazon S3, you can use the Boto library.

Here's an example of how to render a view to a file, using an optional querystring parameter as the trigger...

from django.shortcuts import render
from django.template.loader import render_to_string

def my_view(request):
    as_file = request.GET.get('as_file')
    context = {'some_key': 'some_value'}

    if as_file:
        content = render_to_string('your-template.html', context)                
        with open('path/to/your-template-static.html', 'w') as static_file:
            static_file.write(content)

    return render('your-template.html', context)