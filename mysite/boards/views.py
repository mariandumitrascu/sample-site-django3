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
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils import timezone
from django.urls import reverse_lazy


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
# refactring home2

class HomeListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'boards/home.html'


def board_topics(request, pk):

    # board = Board.objects.get(pk=pk)
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts'))  # md: very interesting
    page = request.GET.get('page', 1) # access a url parameter, with default to 1

    # instantiate a Paginator
    paginator = Paginator(queryset, 5)

    # get the curent query set
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)

    context = {
        'board': board,
        'topics': topics,
    }

    return render(request, 'boards/topics.html', context)

# refactored
class TopicsListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'boards/topics.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        """[summary] generate the context data for topics

        Args:
            self ([type]): [description]
        """
        # prepare the 'boards' context data to be available in html
        # attach an extra variable to kwargs
        kwargs['board'] = self.board
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        # get the parent board, create a self.board variable
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('last_updated').annotate(replies=Count('posts') - 1)
        return queryset


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


# refactored
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'boards/topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(
            Topic,
            board__pk=self.kwargs.get('pk'),
            pk=self.kwargs.get('topic_pk')
            )

        queryset = self.topic.posts.order_by('created_at')
        return queryset


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

            # return redirect(reverse('boards:topic_posts', args=(pk, topic_pk)))
            return redirect(reverse(
                'boards:topic_posts',
                kwargs=
                {
                    'pk': pk,
                    'topic_pk': topic_pk
                })
            )
            # return redirect('boards/topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()

    context ={
        'topic': topic,
        'form': form
    }

    return render(request, 'boards/reply_topic.html', context)


class NewPostView(View):

    def render(self, request):
        context = {
            'form': self.form
        }
        return render(request, 'boards/new_post.html', context)

    def post(self, request):
        self.form = PostForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            return redirect(reverse('boards:post_list'))

        return self.render(request)

    def get(self, request):
        self.form = PostForm()
        return self.render(request)


class NewPostView02(CreateView):
    model = Post
    form_class = PostForm # is either form_class or fields
    success_url = reverse_lazy('boards:post_list')
    # success_url = reverse('boards:post_list')
    template_name = 'boards/new_post.html'

from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = (
        'message',
    )
    template_name = 'boards/edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    # is hard to create this url bc we need to get the board_pk and topic_pk
    # success_url = '/boards/{}/topics/{}/'.format(1, 1)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        # self.kwargs['pk']
        # self.kwargs['topic_pk']
        return redirect(
            reverse(
                'boards:topic_posts',
                kwargs=
                    {
                        'pk': post.topic.board.pk,
                        'topic_pk': post.topic.pk
                    }
                )
            )

    # def get_success_url(self):
    #     return redirect(
    #         reverse(
    #             'boards:topic_posts',
    #             # args=(self.object.topic.board.pk, self.object.topic.pk)
    #             args=(1, 1)
    #             )
    #         )

