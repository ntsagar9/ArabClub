from django import forms
from .models import Comment, Post


class NewComment(forms.ModelForm):
    name = forms.CharField()
    email = forms.EmailField()
    body = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ("name", "email", "body")

    def comment_clean(self):
        cd = self.cleaned_data
        if cd["name"] is None:
            raise forms.ValidationError("قم بكتابة أسمك")
        return cd["name"]


class PostCreateView(forms.ModelForm):
    title = forms.CharField(label="عنوان التدوينة")
    content = forms.CharField(label="محتوي التدوينة", widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ["title", "content"]


class PostUpdateView(forms.ModelForm):
    title = forms.CharField(label="عنوان التدوينة")
    content = forms.CharField(label="محتوي التدوينة", widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ["title", "content"]
