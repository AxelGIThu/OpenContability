from django.http import HttpResponse
from django.shortcuts import render
from .forms import CrearCliente


def index(request):
    return render(request, "index.html")