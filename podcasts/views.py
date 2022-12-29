from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string


from dateutil import parser


from .models import Episode, NewsItem, Publication_Stories, Publication, Status, PageExport
from .forms import NewsItemForm, ArticleForm, PublicationStoryForm, NewsArticleMapForm, NewsLinkPubForm
from content_aggregator.settings import BASE_DIR

from src.html_export import export_page

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
# ***********************************

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
        # context["pubitems"] = Publication.objects.all()
        context["pubitems"] = Publication.objects.filter(owner=self.request.user).order_by('date_added')
        return context

# All users can read a published item if they have the link
def pub_item(request, pub_item_id='1'):
    """ Show a single publication"""
    pub_item = Publication.objects.get(id=pub_item_id)
    l_linked_news = Publication_Stories.objects.filter(publication_id=pub_item_id)

    fd_static_website_root = 'static_website'
    fd_static_website_static = 'imgs'
    b_debug_mode = False

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
    """
    Create a static page that can be saved to file and republished
    Key element is the need to change the hyperlinks to relative links for the website

    images to be held in ./imgs
    references to home page to be change to website

    This is handled by passing the links as context variables
    and loading them with the {{ }} template Construct

    """
    pub_item = Publication.objects.get(id=pub_item_id)
    l_linked_news = Publication_Stories.objects.filter(publication_id=pub_item_id)

    # fd_static_website_root = '/app/static_website'
    fd_static_website_root = str(BASE_DIR) + '//static_website'
    url_commentator = 'https://frozen-brushlands-72168.herokuapp.com/'

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
               'static_website_static': fd_static_website_static,
               'url_commentator': url_commentator
               }

    content = render_to_string('pub_item_static.html', context)
    # with open(fd_static_website_root + '/publication_' + pub_item_id + '.html', 'w') as static_file:
    #     static_file.write(content)

    # return HttpResponseRedirect(reverse('podcasts:pub_item', args=[pub_item_id]))
    return render(request, 'pub_item_static.html', context)

 # *****************************
@login_required
# Only registered users can create new articles
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
            new_article.owner = request.user
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

@login_required
def ArticleEditView(request, pub_item_id='1'):
    """ Edit an existing article
    Only the owner of the article can edit the article
    """
    """ Show a single publication"""
    pub_item = Publication.objects.get(id=pub_item_id)
    l_linked_news = Publication_Stories.objects.filter(publication_id=pub_item_id)
    if pub_item.owner != request.user:
        raise Http404

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

# *******************
@login_required
def ArticleMapStoriesView(request, pub_item_id='1'):
    """ Edit an existing article
    Only registed users can map stories to articles"""
    """ to enable the mapping of the article to stories"""
    pub_item = Publication.objects.get(id=pub_item_id)
    l_linked_news = Publication_Stories.objects.filter(publication_id=pub_item_id)
    l_all_news = NewsItem.objects.filter(status__in=[4,5]).order_by("-pub_date")
    b_debug_mode = False

    # Gte a blank form to add the new mapping
    print('first call')

    if request.method != 'POST':
        # Create empty form the first time page opened
        form = PublicationStoryForm(prefix='news')
        link_form = PublicationStoryForm(prefix='link')
    else:
        form = PublicationStoryForm(data=request.POST, prefix='news')
        link_form = PublicationStoryForm(data=request.POST, prefix='link')
        if form.is_valid():
            new_story_mapping = form.save(commit=False)
            new_story_mapping.save()
            # return HttpResponseRedirect(reverse('podcasts:publications'))

    # context = {'pub_item': pub_item, 'form': form}
    # return render(request, 'article_edit.html', context)


    l_stories = []
    for linked_news_item in l_linked_news:
        news_story = linked_news_item.news_item_id
        l_stories = l_stories + [news_story]

    context = {'pub_item': pub_item,
               'news_items': l_linked_news,
               'l_stories': l_stories,
               'l_all_news': l_all_news,
               'form': form,
               'link_form': form,
               'b_debug_mode': b_debug_mode
               }
    return render(request, 'article_story_map_new.html', context)

# *************
@login_required
def ArticleMapStoryLinkNewView(request, pub_item_id, news_item_id):
    """ Link an existing article to new news story
    only registered users can map an articel to a story
    """
    """ to enable the mapping of the article to stories"""
    pub_item = Publication.objects.get(id=pub_item_id)
    link_to_story = Publication_Stories.objects.filter(publication_id=pub_item_id)
    news_item = NewsItem.objects.get(id=news_item_id)
    b_debug_mode = True

    if request.method != 'POST':
        # Create empty form the first time page opened
        form = PublicationStoryForm(initial={'publication_id': pub_item_id, 'news_item_id': news_item_id})
    else:
        form = PublicationStoryForm(data=request.POST)
        if form.is_valid():
            new_story_mapping = form.save(commit=False)
            new_story_mapping.save()

    context = {'pub_item': pub_item,
               'news_item': news_item,
               'form': form,
               'b_debug_mode': b_debug_mode
               }

    return render(request, 'article_story_make_mapping.html', context)


# **************
@login_required
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
@login_required
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

# *** Create view to enable paging through news items and editing links
@login_required
def edit_news_item_links(request, news_item_id='1'):
    """ Edit an existing news item"""
    news_item = NewsItem.objects.get(id=news_item_id)
    prev_news_id = '2464'
    next_news_id = '2466'

    # filter the list by status of 3 == NEW
    status_new = Status.objects.filter(state='New')
    l_news_items = NewsItem.objects.filter(status=status_new[0].id).order_by("-pub_date")

    # Find the position matching ID in the list of news items
    # Confirm the length of the list of items
    # If there are more than 3 items in the list, set prev and next as one before an one after

    counter = 0
    for news_object in l_news_items:
        # print("list includes:" +str( news_object.id) + " Looking for: " + str(news_item_id))
        if str(news_object.id) == str(news_item_id):
            if counter > 0:
                prev_news_id = l_news_items[counter - 1].id
            else:
                prev_news_id = news_item_id
            if counter < (len(l_news_items) - 1):
                next_news_id = l_news_items[counter + 1].id
            else:
                next_news_id = news_item_id
        counter = counter + 1

    # Get list of all the linked items for this new item
    l_links_to_pubs = Publication_Stories.objects.filter(news_item_id=news_item_id)
    l_linked_pubs = []
    for plink in l_links_to_pubs:
        linked_pub = plink.publication_id
        l_linked_pubs = l_linked_pubs + [linked_pub]

    # l_stories = []
    # for linked_news_item in l_linked_news:
    #     news_story = linked_news_item.news_item_id
    #     l_stories = l_stories + [news_story]

    # Get list of all publications
    l_pubs = Publication.objects.all()



    if request.method != 'POST':
        # Initial request; pre-fill the form with the current entry
        form = NewsItemForm(instance=news_item, prefix='news')
        link_form = NewsArticleMapForm(prefix='link')
        pub_link_form = NewsLinkPubForm(prefix='PubLink', initial={'news_item_id': news_item_id})


    else:
        # POST data submitted; process data
        form = NewsItemForm(instance=news_item, data=request.POST, prefix='news')
        pub_link_form = NewsLinkPubForm(data=request.POST, prefix='PubLink')
        if form.is_valid() and pub_link_form.is_valid():
            form.save()
            print("from IS valid" )
            print(request.POST)
            # new_story_mapping = pub_link_form.save(commit=False)
            pub_link_form.save()
            return HttpResponseRedirect(reverse('podcasts:edit_news_item_links', args=[news_item.id]))


    context = {'news_item': news_item,
               'form': form,
               'pub_link_form': pub_link_form,
               'l_linked_pubs': l_linked_pubs,
               'l_pubs': l_pubs,
               'l_links_pubs': l_links_to_pubs,
               'prev_news_id': prev_news_id,
               'next_news_id': next_news_id}
    return render(request, 'edit_news_item_links.html', context)


# ***** edit_news_links_changed *******
# This view is called when the PREVIOUS and NEXT item links are specified on the URL in the GET
# It is called when reviewing the News items with Status NEW after the statis is changed so that
# the previous and next items can still be found.

@login_required
def edit_news_links_changed(request, news_item_id='1', prev_news_id='1', next_news_id='1'):
    """ Edit an existing news item"""
    news_item = NewsItem.objects.get(id=news_item_id)

    # filter the list by status of 3 == NEW
    status_new = Status.objects.filter(state='New')
    l_news_items = NewsItem.objects.filter(status=status_new[0].id).order_by("-pub_date")

    if request.method != 'POST':
        # Initial request; pre-fill the form with the current entry
        form = NewsItemForm(instance=news_item, prefix='news')
        link_form = NewsArticleMapForm(prefix='link')
        pub_link_form = NewsLinkPubForm(prefix='PubLink')
    else:
        # POST data submitted; process data
        form = NewsItemForm(instance=news_item, data=request.POST, prefix='news')
        link_form = NewsArticleMapForm(request.POST, prefix='link')
        pub_link_form = NewsLinkPubForm(data=request.POST, prefix='Publink')

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('podcasts:edit_news_links_changed') + '/' + news_item_id + '/' + prev_news_id + '/' + next_news_id)

    context = {'news_item': news_item,
               'form': form,
               'link_form': link_form,
               'pub_link_form': pub_link_form,
               'prev_news_id': prev_news_id,
               'next_news_id': next_news_id}
    return render(request, 'edit_news_item_links.html', context)


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

# **************************
@login_required
def page_export(request, page_export_id='1'):
    """ Show a single news item"""
    page_export = PageExport.objects.get(id=page_export_id)
    context = {'page_export': page_export}

    # Call the source page using request to the source page using the static template
    # Passing the local directory refrences fro use in the template and save locally
    export_page(page_export.source_page_url, page_export.local_file)


    # Save the con

    return render(request, 'page_export.html', context)

# ***************************

@login_required
def PageExportEditView(request, page_export_id='1'):
    """ Edit an existing article
    Only the owner of the article can edit the article
    """
    """ Show a single publication"""
    pub_item = Publication.objects.get(id=pub_item_id)
    l_linked_news = Publication_Stories.objects.filter(publication_id=pub_item_id)
    if pub_item.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = ArticleForm(instance=pub_item )
    else:
        form = ArticleForm(instance=pub_item, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('podcasts:publications'))