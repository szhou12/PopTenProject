from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .forms import cuisineForm
from . import main_algorithm
from django.shortcuts import redirect


# Create your views here.

def temp(request):

    if request.method == 'POST':
        form = cuisineForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            template = 'results.html'#pending
            has_result, context = main_algorithm.main_algorithm(data)
            if has_result:
                return render(request, template, context)
            else:
                template = 'noresults.html'
                return render(request, template, context)
    else:
        form = cuisineForm()
        template = 'temp.html'
        context = {'form':form}
    return render(request, template, context)
