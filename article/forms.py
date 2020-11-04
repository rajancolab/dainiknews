from django import forms
from .models import Article

class CreateArticleForm(forms.ModelForm):
    title = forms.CharField(
            label='Title',
            max_length=255,
            widget=forms.TextInput(attrs={'class': 'input form-control', 'placeholder':"Article's title"}))

    text = forms.CharField(
            label='Text',
            max_length=5000,
            widget=forms.Textarea(attrs={'class': 'input form-control', 'placeholder':"Write article's content here"}))

    image = forms.ImageField()
    class Meta:
        model = Article
        fields = ('title', 'image', 'text',)




# class CreateArticleForm(forms.Form):
#     title = forms.CharField(
#         label='Title',
#         max_length=255,
#         widget=forms.TextInput(attrs={'class': 'input form-control', 'placeholder':"Article's title"}))
#
#     text = forms.CharField(
#         label='Text',
#         max_length=5000,
#         widget=forms.Textarea(attrs={'class': 'input form-control', 'placeholder':"Write article's content here", 'id':'article_text_id', 'name': 'text1'}))
#
#     image = forms.ImageField()
#
#     def clean(self):
#         cleaned_data = super().clean()
#
#         title = cleaned_data.get('title')
#         text = cleaned_data.get('text')
#
#         if title and text:
#             if title == 'create_article':
#                 raise forms.ValidationError("Can't create article with this title")


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'image', 'text')
    #
    # title = forms.CharField(
    #     label='Title',
    #     max_length=255,
    #     widget=forms.TextInput(attrs={'class': 'input form-control', 'placeholder':"Article's title"}))
    #
    # text = forms.CharField(
    #     label='Text',
    #     max_length=5000,
    #     widget=forms.Textarea(attrs={'class': 'input form-control', 'placeholder':"Write article's content here", 'id':'article_text_id', 'name': 'text1'}))
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #
    #     title = cleaned_data.get('title')
    #     text = cleaned_data.get('text')
    #
    #     if title and text:
    #         if title == 'create_article':
    #             raise forms.ValidationError("Can't create article with this title")