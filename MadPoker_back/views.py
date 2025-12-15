from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    pass
    
    return render(request, 'basic.html', {})   

def react_test(request, pk=None):

    return JsonResponse({'value':'good'})