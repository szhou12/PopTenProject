from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .forms import cuisineForm
from . import main_algorithm

# Create your views here.
'''
def home(request):
    def home(request):

    if request.method == 'POST':
        form = RecommendationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            print(data)
            template = 'results.html'
            criteris_met, context = algorithm.recommend(data)
            #Criteria met show result.html page
            if criteris_met:
            	return render(request, template, context)
            #Criteria NOT met show noresult.html page
            else:
            	template = 'noresults.html'
            	return render(request, template, context)
    else:
        form = RecommendationForm()
        template = 'home.html'
        context = {'form':form}
    return render(request, template, context)
'''

def get_name(request):
    if request.method == 'POST':
        form = cuisineForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data
            template = 'results.html'#pending
            has_result, context = main_algorithm.main_algorithm(data)
            if has_result:
                return render(request, template, context)
            else:
                template = 'noresult.html'#pending
                return render(request, template, context)
            #return
#    else:
#        form = cuisineForm()
#    return render(request, 'temp.html', {'form': form})

    #return render(request, 'home.html', locals())
