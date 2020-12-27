from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import datetime

# reference:
# https://docs.djangoproject.com/en/3.1/intro/tutorial02/

class Question(models.Model):
    question_text = models.CharField(
        max_length=200,

        )
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    # a filed coming from a method cannot be ordered
    # by default the heading of the field in the table shows the name of the method
    # thats why we set .short_description
    # reference on thse type of fields:
    # https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

#############################################################################################################################

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class StudyElement(models.Model):
    """[summary]
    A study database model element.

    Args:
        models ([type]): [description]

    Returns:
        [type]: [description]
    """
    #################################################
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate'),
    ]

    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
        verbose_name="year in school v1",
    )

    def is_upperclass(self):
        return self.year_in_school in {self.JUNIOR, self.SENIOR}

    ##############################################
    class YearInSchool(models.TextChoices):
        FRESHMAN = 'FR', _('Freshman')
        SOPHOMORE = 'SO', _('Sophomore')
        JUNIOR = 'JR', _('Junior')
        SENIOR = 'SR', _('Senior')
        GRADUATE = 'GR', _('Graduate')


    year_in_school_02 = models.CharField(
        max_length=2,
        choices=YearInSchool.choices,
        default=YearInSchool.FRESHMAN,
        # verbose_name="year in school version v2",
        # editable=True,
        # error_messages='this is the error message for year_in_school_02 field',
        # help_text='help for year_in_school_02 field'
        )

    def is_upperclass_02(self):
        return self.year_in_school_02 in {
            self.YearInSchool.JUNIOR,
            self.YearInSchool.SENIOR,
        }

    ##############################################

    my_date_field = models.DateTimeField(
        # auto_now=True, # Automatically set the field to now every time the object is saved. Useful for “last-modified” timestamps.
        auto_now_add=True, # Automatically set the field to now when the object is first created. Useful for creation of timestamps.
        editable=True,

    )
    ##############################################
    my_file_field_01 = models.FileField(
        upload_to='uploads/%Y/%m/%d/'
    )
    ##############################################
    my_file_field_02 = models.FileField(
        upload_to=user_directory_path
    )


    ##############################################
    my_path_field = models.FilePathField(
        path='/',
        recursive=True,
        allow_files=True,
        match='*.py'
    )
    ##############################################
    my_image_field = models.ImageField(
        upload_to = 'uploads/'
    )
    ##############################################
    my_text_field = models.TextField(

    )
    ##############################################
    def __str__(self):
        return self.year_in_school


####################################################################
# helper methods and classes





####################################################################
class Person(models.Model):
    name = models.CharField(max_length=50)

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(
        Person,
        through='Membership',
        through_fields=('group', 'person'),
    )

class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    inviter = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=64)

######################################################################

class MySpecialUser(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    supervisor = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='supervisor_of',
    )

    # reference:
    # https://docs.djangoproject.com/en/dev/ref/models/options/
    class Meta:
        ordering = ["user"]
        verbose_name_plural = "myspecials"


#####################################################################################################################################################
# reference
# https://docs.djangoproject.com/en/dev/topics/forms/modelforms/

from django.db import models
from django.forms import ModelForm

TITLE_CHOICES = [
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
]

class Author(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']