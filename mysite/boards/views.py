from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import View

from .models import Board
from .models import Topic
from .models import Post

from .forms import NewTopicForm
from .forms import PostForm


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
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts'))  # md: very interesting
    context = {
        'board': board,
        'topics': topics,
    }

    return render(request, 'boards/topics.html', context)

@login_required
def new_topic(request, pk):

    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()


    if request.method == 'POST':
        # subject = request.POST['subject']
        # message = request.POST['message']

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
            topic.starter = request.user
            topic.save()

            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = request.user
            )

            # return redirect('/boards/', pk=board.pk)  # TODO: redirect to the created topic page
            return HttpResponseRedirect(reverse('boards:topic_posts', args=(board.pk,topic.pk, ))  )

    else:
        form = NewTopicForm()

    context = {
        'board': board,
        'form': form
    }

    # return HttpResponse('hello from boards application 2')

    return render(request, 'boards/new_topic.html', context)


def topic_posts(request, pk, topic_pk):

    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)

    topic.views += 1
    topic.save()

    context = {
        'topic': topic
    }

    return render(request, 'boards/topic_posts.html', context)


@login_required
def reply_topic(request, pk, topic_pk):

    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            return redirect(reverse('boards:topic_posts', args=(pk, topic_pk)))
            # return redirect('boards/topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()

    context ={
        'topic': topic,
        'form': form
    }

    return render(request, 'boards/reply_topic.html', context)


class NewPostView(View):
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('boards:post_list'))

        context = {
            'form': form
        }
        return render(request, 'boards/new_post.html', context)

    def get(self, request):
        form = PostForm()
        context = {
            'form': form
        }
        return render(request, 'boards/new_post.html', context)
