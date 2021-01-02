

# python manage.py shell

from blog.models import Blog
b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
b.save()

b = Blog(name='Cheddar Talk', tagline='All about ceddar.')
b.save()

##################################
from blog.models import Blog, Entry, Author
entry = Entry()
# entry = Entry.objects.get(pk=1)
# entry.id = 1
entry.headline = 'entry headline 4'
entry.body_text = 'body text'
entry.pub_date = '2020-12-01'
entry.mod_date = '2020-12-01'
entry.blog = Blog.objects.get(pk=2)
entry.save()

a = Author.objects.get(pk=2)
entry.authors.add(a)
entry.save()



entry = Entry.objects.get(pk=1)
cheese_blog = Blog.objects.get(name="Cheddar Talk")
entry.blog = cheese_blog
entry.save()


#####################################
from blog.models import Author
joe = Author.objects.create(name="Joe")

marian = Author()
marian.name = 'Marian'
marian.save()

##############################################################################################################
##############################################################################################################
##############################################################################################################



