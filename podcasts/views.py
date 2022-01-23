from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.template.loader import render_to_string

from .models import Episode, NewsItem
from .forms import NewsItemForm

# Create your views here.


class HomePageView(ListView):
    template_name = "homepage.html"
    model = Episode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["episodes"] = Episode.objects.filter().order_by("-pub_date")[:10]
        return context

class NewsView(ListView):
    """ Show a full list of all news items"""
    template_name = "news_home.html"
    model = NewsItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context["newsitems"] = NewsItem.objects.filter(status=3).order_by("-pub_date")[:10]
        context["newsitems"] = NewsItem.objects.filter().order_by("-pub_date")[:10]
        data = render(request, 'news_item.html', context)
        if b_is_saved_as_static:
            content = render_to_string('news_item.html', context)
            with open('your-list.html', 'w') as static_file:
                static_file.write(content)
        return context

# class NewsItemView(ListView):
#     """ Show a full list of all news items"""
#     template_name = "news_home.html"
#     model = NewsItem
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["newsitem"] = NewsItem.objects.filter().order_by("-pub_date")[:10]
#         return context

# def news_list_static(request):
#     """ Show all the news items tagged to publish"""
#     news_items = news_item.objects.order_by("-pub_date")[:10]


def news_item(request, news_item_id='1'):
    """ Show a single news item"""
    b_is_saved_as_static = True
    news_item = NewsItem.objects.get(id=news_item_id)
    context = {'news_item': news_item}
    data = render(request, 'news_item.html', context)
    if b_is_saved_as_static:
        content = render_to_string('news_item.html', context)
        with open('your-template-static.html', 'w') as static_file:
            static_file.write(content)
    """
    as_file = request.GET.get('as_file')
    context = {'some_key': 'some_value'}

    if as_file:
        content = render_to_string('your-template.html', context)                
        with open('path/to/your-template-static.html', 'w') as static_file:
            static_file.write(content)
    """


    return render(request, 'news_item.html', context)

def edit_news_item(request, news_item_id='1'):
    """ Edit an existing news item"""
    news_item = NewsItem.objects.get(id=news_item_id)

    if request.method != 'POST':
        # Initial request; pre-fill the form with the current entry
        form = NewsItemForm(instance=news_item)
    else:
        # POST data submitted; process data
        form = NewsItemForm(instance=news_item, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('podcasts:news_item', args=[news_item.id]))


    context = {'news_item': news_item, 'form': form}
    return render(request, 'edit_news_item.html', context)
