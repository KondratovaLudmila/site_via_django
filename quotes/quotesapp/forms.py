from django.forms import ModelForm, CharField, TextInput, DateField, Textarea, ModelChoiceField, ModelMultipleChoiceField
from .models import Tag, Author, Quote


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']

class AuthorForm(ModelForm):

    fullname = CharField(min_length=5, max_length=50, required=True, widget=TextInput())
    born_date = DateField()
    born_location = CharField(max_length=150)
    description = CharField(widget=Textarea(), required=False, strip=True)

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

class QuoteForm(ModelForm):

    quote = CharField(min_length=10, max_length=150, required=True, widget=TextInput())
    author = ModelChoiceField(queryset=Author.objects.all())
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all())

    class Meta:
        model = Quote
        fields = ['quote', 'author', 'tags']

