from django import forms

from .models import NewsItem, Publication, Publication_Stories

class NewsItemForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ['comment', 'status']
        labels = {'comment': '', 'status': ''}
# *************************************
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = [ 'title',
                   'description',
                   'image_file'
                   ]
        labels = { 'title': '',
                   'description': '',
                   'image_file': 'File name in static/img directory'
                   }
        widgets = {'description': forms.Textarea(attrs={'cols': 80})}
# **************************************
class PublicationStoryForm(forms.ModelForm):
    class Meta:
        model = Publication_Stories
        fields = ['publication_id', 'news_item_id']
        labels = {'publication_id': 'Publication Ref: ', 'news_item_id': 'News Ref: '}
        widgets = {'publication_id': forms.HiddenInput(),
                   'news_item_id': forms.HiddenInput()
                   }


