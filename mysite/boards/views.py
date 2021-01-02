from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Board
from .models import Topic
from .models import Post

from .forms import NewTopicForm


def home(request):
    return HttpResponse('hello from boards application')

def home2(request):

    boards = Board.objects.all()
    context = {
        'boards': boards
    }

    return render(request, 'boards/home.html', context)
    # return HttpResponse('hello 2 from boards application')


def board_topics(request, pk):

    # board = Board.objects.get(pk=pk)
    board = get_object_or_404(Board, pk=pk)
    context = {
        'board': board
    }

    return render(request, 'boards/topics.html', context)


def new_topic(request, pk):

    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()


    if request.method == 'POST':
        # subject = request.POST['subject']
        # message = request.POST['message']

        # user = User.objects.first()  # TODO: get the currently logged in user

        # topic = Topic.objects.create(
        #     subject=subject,
        #     board=board,
        #     starter=user
        # )

        # post = Post.objects.create(
        #     message=message,
        #     topic=topic,
        #     created_by=user
        # )

        form = NewTopicForm(request.POST)
        if form.is_valid():

            topic = form.save(commit = False)
            topic.board = board
            topic.starter = user
            topic.save()

            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = user
            )

            # return redirect('/boards/', pk=board.pk)  # TODO: redirect to the created topic page
            return HttpResponseRedirect(reverse('boards:board_topics', args=(board.pk,))  )

    else:
        form = NewTopicForm()

    context = {
        'board': board,
        'form': form
    }

    # return HttpResponse('hello from boards application 2')

    return render(request, 'boards/new_topic.html', context)