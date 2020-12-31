from django.db import models

# Create your models here.

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField(
        auto_now_add=True,
        editable=True
    )
    mod_date = models.DateField(
        auto_now=True
    )
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(
        default=0
    )
    number_of_pingbacks = models.IntegerField(
        default=0
    )
    rating = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.headline