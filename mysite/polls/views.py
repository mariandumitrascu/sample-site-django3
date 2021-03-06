from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]

    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')

    context = {
        'latest_question_list': latest_question_list,
    }

    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'polls/detail.html', {'question': question})

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    # answer = request.POST['choice']
    # response = "voting on question {} the answer is {}".format(question_id, answer)
    # # return HttpResponse("You're voting on question %s." % question_id)
    # return HttpResponse(response)
    question = get_object_or_404(Question, pk=question_id)
    try:
        # get the selected choice from the database
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        # We are using the reverse() function in the HttpResponseRedirect constructor in this example.
        # This function helps avoid having to hardcode a URL in the view function.
        # It is given the name of the view that we want to pass control to and the variable portion of the URL pattern that points to that view.
        # In this case, using the URLconf we set up in Tutorial 3, this reverse() call will return a string like

        # '/polls/3/results/'

        # where the 3 is the value of question.id.
        # This redirected URL will then call the 'results' view to display the final page.

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,))  )


########################################################################################################
# reference on generic-views:
# https://docs.djangoproject.com/en/3.1/topics/class-based-views/

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



##########################################################################################################################
from .forms import NameForm
from .forms import ContactForm



def view_get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            your_name = form.cleaned_data['your_name']

            # redirect to a new URL:
            #
            # return HttpResponseRedirect('/polls/thanks/')
            # return HttpResponseRedirect(reverse('polls:thanks'))

            context = {
                'yourname': your_name
            }
            return render(request, 'polls/thanks.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:

        form = NameForm()


    contact_form = ContactForm()

    context = {
        'form': form,
        'contact_form': contact_form,
    }

    return render(request, 'polls/name-form.html', context )


def view_thanks(request):
    r = request
    return render(request, 'polls/thanks.html', {'yourname': 'name entered'})