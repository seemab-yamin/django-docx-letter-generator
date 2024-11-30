from django.shortcuts import render
from django.http import HttpResponse

def render_form(request):
    return HttpResponse("Welcome to the Dynamic Form Handler!")