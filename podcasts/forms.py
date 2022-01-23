from django import forms

from .models import NewsItem

class NewsItemForm(forms.ModelForm):
    class Meta:
        model = NewsItem
        fields = ['comment', 'status']
        labels = {'comment': '', 'status': ''}
