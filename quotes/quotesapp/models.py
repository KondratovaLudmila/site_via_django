from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.
    
class Tag(models.Model):
    name = models.CharField(max_length=35, null=False, unique=True)

    class Meta:
        db_table = "tags"

    def __str__(self):
        return f"{self.name}"
    
    @staticmethod
    def top_ten_tags():
        return Tag.objects.annotate(quotes_count=Count("quote")).order_by("-quotes_count")[:10]

class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.DateField()
    born_location = models.CharField(max_length=150)
    description = models.CharField()
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    class Meta:
        db_table = "authors"

    def __str__(self):
        return f"{self.fullname}"

class Quote(models.Model):
    quote = models.CharField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    class Meta:
        db_table = "quotes"

    def __str__(self):
        return f"{self.quote[:20]}..."
    
