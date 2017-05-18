from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader, RequestContext


from .models import Choice, Question
from .models import Document
from .forms import DocumentForm

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)
    #return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
    ## try:
    ##     question = Question.objects.get(pk=question_id)
    ## except Question.DoesNotExist:
    ##     raise Http404("Question does not exist")
    ## return render(request, 'polls/detail.html', {'question': question})
    #return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    #response = "You're looking at the results of question %s."
    #return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
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
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def list(request):
    print('hi')
    # Handle file upload
    # if request.method == 'POST':
    form = DocumentForm(request.POST, request.FILES)
    if form.is_valid():
        newdoc = Document(docfile = request.FILES['docfile'])
        newdoc.save()
        # Redirect to the document list after POST
        return HttpResponseRedirect(reverse('polls:list'))
    else:
        form = DocumentForm() # A empty, unbound form
        # Load documents for the list page
        documents = Document.objects.all()
    
        # Render list page with the documents and the form
        context = {'documents': documents, 'form': form}
        return render(request, 'polls/list.html', context)
