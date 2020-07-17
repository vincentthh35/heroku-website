from django.shortcuts import render
from .fetch import fetch

# Create your views here.
def query(request):
    df = fetch()
    return render(request, 'query.html', {'df': df})
