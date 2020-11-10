from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
            label='Title',
            max_length=255,
            widget=forms.TextInput(attrs={'class': 'input form-control', 'placeholder':"Article's title"}))

    text = forms.CharField(
            label='Text',
            max_length=5000,
            widget=forms.Textarea(attrs={'class': 'input form-control', 'placeholder':"Write article's content here"}))

    class Meta:
        model = Article
        fields = ('title', 'image', 'text',)

