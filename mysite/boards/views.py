from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Board


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