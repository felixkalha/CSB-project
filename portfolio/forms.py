from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author_name', 'text']
        labels = {
                    'text': '',
        }
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Type here...', 'rows': 4}),
        }

