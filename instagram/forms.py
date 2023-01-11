from django import forms

from instagram.models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo', 'caption', 'location']
        widgets = {
            'caption': forms.Textarea,
        }


# detail, comment_new , index view에서 사용
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['messages']
        widgets = {
            'messages': forms.Textarea(attrs={"rows": 3})
        }

