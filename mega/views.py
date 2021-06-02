from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, 'mega/mega.html', context)

def team1(request):
    context = {}
    return render(request, 'mega/team1/index.html', context)

def team2(request):
    context = {}
    return render(request, 'mega/team2/apple.html', context)

def team3(request):
    context = {}
    return render(request, 'mega/team3/유진.html', context)