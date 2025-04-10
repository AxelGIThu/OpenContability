from django.http import HttpResponse
from django.shortcuts import render
from .forms import CrearCliente


def index(request):
    form = CrearCliente
    return render(request, "index.html", { 'form' : form })