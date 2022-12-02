from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
   title = forms.CharField(max_length=255, label='Заголовок:')


   class Meta:
       model = Post
       fields = [
           'title',
           'text',
           #'rating',
           'author',
           'category',
       ]

   def clean(self):
       cleaned_data = super().clean()
       text = cleaned_data.get("description")
       if text is not None and len(text) < 20:
           raise ValidationError({
               "text": "Статья/новость не может быть менее 20 символов."
           })

       # title = cleaned_data.get("title")
       # if len(title) > 255:
       #     raise ValidationError(
       #         "Заголовок не должно быть длиннее 255 символов."
       #     )

       return cleaned_data