from django.shortcuts import render


def menu_test_view(request):
    return render(request, 'base.html')


def home(request):
    return render(request, 'home.html')
