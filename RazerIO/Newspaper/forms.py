from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Article, Article_Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('Category', 'Title', 'Text')

class ArticleCommentForm(forms.ModelForm):

    class Meta:
        model = Article_Comment
        fields = ['Text', 'Is_Anonymous', 'Show_Company']
        labels = {
            'Text': 'Add comment',
            'Is_Anonymous': 'Post as Anonymous',
            'Show_Company': 'Show Company Name'
        }
        widgets = {
            'Text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'Is_Anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Show_Company': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
