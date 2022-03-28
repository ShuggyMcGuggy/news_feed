from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string

from dateutil import parser


from .models import Episode, NewsItem, Publication_Stories, Publication, Status
from .forms import NewsItemForm, ArticleForm

# Create your views here.

def home(request):
    """ Landing page for the published site"""
    return render(request, 'index.html')


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
        context["newsitems"] = NewsItem.objects.filter().order_by("-pub_date")[:20]
        return context

class NewsNewView(ListView):
    """ Show a full list of all news items"""
    template_name = "news_new.html"
    model = NewsItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_new = Status.objects.filter(state='New')
        context["newsitems"] = NewsItem.objects.filter(status=status_new[0].id).order_by("-pub_date")[:10]
        return context

class PubsView(ListView):
    """ Show a full list of all publication items"""
    template_name = "pubs_home.html"
    model = Publication

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pubitems"] = Publication.objects.all()
        return context

def pub_item(request, pub_item_id='1'):
    """ Show a single publication"""
    pub_item = Publication.objects.get(id=pub_item_id)
    l_linked_news = Publication_Stories.objects.filter(publication_id=pub_item_id)

    fd_static_website_root = 'static_website'
    fd_static_website_static = 'imgs'
    b_debug_mode = True

    l_stories = []
    for linked_news_item in l_linked_news:
        news_story = linked_news_item.news_item_id
        l_stories = l_stories + [news_story]

    context = {'pub_item': pub_item,
               'b_debug_mode': b_debug_mode,
               'fd_static_website_root': fd_static_website_root,
               'news_items': l_linked_news,
               'l_stories': l_stories}
    return render(request, 'pub_item.html', context)

# *************  View to publish a static version of the publication ******
def pub_item_static(request, pub_item_id='1'):
    """ Show a single publication"""
    pub_item = Publication.objects.get(id=pub_item_id)
    l_linked_news = Publication_Stories.objects.filter(publication_id=pub_item_id)

    fd_static_website_root = '/app/static_website'
    fd_static_website_static = 'imgs'
    b_debug_mode = True

    l_stories = []
    for linked_news_item in l_linked_news:
        news_story = linked_news_item.news_item_id
        l_stories = l_stories + [news_story]

    context = {'pub_item': pub_item,
               'b_debug_mode': b_debug_mode,
               'news_items': l_linked_news,
               'l_stories': l_stories,
               'static_website_root': fd_static_website_root,
               'static_website_static': fd_static_website_static}

    content = render_to_string('pub_item_static.html', context)
    with open(fd_static_website_root + '/publication_' + pub_item_id + '.html', 'w') as static_file:
        static_file.write(content)

    return HttpResponseRedirect(reverse('podcasts:pub_item', args=[pub_item_id]))

 # *****************************
def ArticleNewView(request):
    """ Create a New Publication"""

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ArticleForm()
    else:
        # POST data submitted ; process data.
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.save()
            return HttpResponseRedirect(reverse('podcasts:publications'))


    context = {'form': form}
    return render(request, 'article_new.html', context)

    #
    # l_stories = []
    # for linked_news_item in l_linked_news:
    #     news_story = linked_news_item.news_item_id
    #     l_stories = l_stories + [news_story]
    #
    # context = {'pub_item': pub_item,
    #            'news_items': l_linked_news,
    #            'l_stories': l_stories}
    # return render(request, 'pub_item.html', context)

def ArticleEditView(request, pub_item_id='1'):
    """ Edit an existing article"""
    """ Show a single publication"""
    pub_item = Publication.objects.get(id=pub_item_id)
    l_linked_news = Publication_Stories.objects.filter(publication_id=pub_item_id)

    if request.method != 'POST':
        form = ArticleForm(instance=pub_item )
    else:
        form = ArticleForm(instance=pub_item, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('podcasts:publications'))

    # context = {'pub_item': pub_item, 'form': form}
    # return render(request, 'article_edit.html', context)


    l_stories = []
    for linked_news_item in l_linked_news:
        news_story = linked_news_item.news_item_id
        l_stories = l_stories + [news_story]

    context = {'pub_item': pub_item,
               'news_items': l_linked_news,
               'l_stories': l_stories,
               'form': form
               }
    return render(request, 'article_edit.html', context)

def news_list_static(request):
    """ Show all the news items tagged to publish"""

    b_is_saved_as_static = True
    # filter the list by status of 3 ==
    news_items = NewsItem.objects.filter(status=3).order_by("-pub_date")[:10]

    context = {'news_items': news_items}
    # context["newsitems"] = NewsItem.objects.filter().order_by("-pub_date")[:10]
    if b_is_saved_as_static:
        content = render_to_string('news_list_static.html', context)
        with open('your_list.html', 'w') as static_file:
            static_file.write(content)
    return render(request, 'news_list_static.html', context)

# **************************
# New new item list ready for publishing with stars
def news_list_star_rating(request):
    """ Show all the news items tagged to publish"""

    b_is_saved_as_static = True
    # filter the list by status of 3 ==
    news_items = NewsItem.objects.filter(status=3).order_by("-pub_date")[:10]
    context = {'news_items': news_items,
               }
    # context["newsitems"] = NewsItem.objects.filter().order_by("-pub_date")[:10]
    if b_is_saved_as_static:
        content = render_to_string('news_list_static_out.html', context)
        with open('your_list.html', 'w') as static_file:
            static_file.write(content)
    return render(request, 'news_list_static.html', context)


# **************************
@login_required
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
@login_required
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


    context = {'news_item': news_item,
               'form': form}
    return render(request, 'edit_news_item.html', context)

# ***** Create a view to load a new story and test it works
def load_test_story(request):

    newsitem = NewsItem(
        source_name="My Source",
        title="My Title",
        description="Fabulous",
        pub_date=parser.parse("15/03/2022"),
        link="https://www.adoclib.com/blog/django-psycopg2-errors-stringdatarighttruncation-value-too-long-for-type-character-varying-200.html",
        image="https://frozen-brushlands-72168.herokuapp.com/staticfiles/imgs/agile_pm.png" ,
        guid="0001",
    )
    if not NewsItem.objects.filter(guid=item.guid).exists():
        newsitem.save()
    return render(request, 'load_test_story.html')

