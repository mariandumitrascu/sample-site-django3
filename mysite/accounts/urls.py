from django.urls import path

from . import views

# this is for the app to figure out the namespace of this app when constructing the links
app_name = 'accounts'


urlpatterns = [
    path('', views.signup, name='signup'),

    path('myaccount/', views.UserUpdateView.as_view(), name='myaccount')
]