from django.shortcuts import render

def custom404View(request, exception):
    return render(request, '404.html', {})

def custom500View(request):
    return render(request, '500.html', {})
