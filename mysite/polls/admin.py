from django.contrib import admin
from .models import Question
from .models import Choice

# this tells django Choice objects are edited on the Question admin page
# by default provide enough fields for 3 choices
# reference for django.contrib.admin:
# https://docs.djangoproject.com/en/1.8/_modules/django/contrib/admin/options/
class ChoiceInline(admin.StackedInline):
# class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            'Question information',
            {
                'fields': ['question_text']
            }
        ),

        (
            'Date information',
            {
                'fields': ['pub_date']
            }
        ),
    ]

    # this makes the choices to be editable on same page with the Question
    inlines = [ChoiceInline]

    # By default, Django displays the str() of each object.
    # But sometimes it’d be more helpful if we could display individual fields.
    # To do that, use the list_display admin option,
    # which is a tuple of field names to display, as columns, on the change list page for the object:
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']  # this is adding a search box
    show_full_result_count = True
    # view_on_site = True

    # reference: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_per_page
    list_per_page = 2



# this makes to appear in the admin menu
# QuestionAdmin makes those separator bars between field sets to show
# admin.site.register(Question, QuestionAdmin)


# admin.site.register(Choice)

