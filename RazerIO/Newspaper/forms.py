from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Article, Article_Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('Title', 'Text',)

class ArticleCommentForm(forms.ModelForm):

    class Meta:
        model = Article_Comment
        fields = ['Text', 'Is_Anonymous', 'Show_Company']