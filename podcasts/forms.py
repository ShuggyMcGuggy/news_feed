from django import forms

from .models import NewsItem, Publication

class NewsItemForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ['comment', 'status']
        labels = {'comment': '', 'status': ''}

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
