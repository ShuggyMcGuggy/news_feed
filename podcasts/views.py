from django.shortcuts import render
from django.views.generic import ListView
from .models import Episode, NewsItem

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
        context["newsitems"] = NewsItem.objects.filter().order_by("-pub_date")[:10]
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

def news_item(request, news_item_id='1'):
    """ Show a single news item"""
    news_item = NewsItem.objects.get(id=news_item_id)
    context = {'news_item': news_item}
    return render(request, 'news_item.html', context)
