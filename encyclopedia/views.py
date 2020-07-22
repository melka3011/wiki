from django.shortcuts import render, redirect
from django.conf import settings
from markdown2 import Markdown
from django import forms

import os
from random import choice

from . import util

markdowner = Markdown()

class newpage_form(forms.Form):
    title = forms.CharField(label="Title")
    entry = forms.CharField(label="Wiki Entry",widget=forms.Textarea)

class editpage_form(forms.Form):
    entry = forms.CharField(label="Wiki Entry",widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    wiki = util.get_entry(title)
    if wiki != None:
        return render(request,"encyclopedia/wiki.html",{'wiki':markdowner.convert(wiki),'title':title})

    error = 'Wiki entry does not exist'    
    return render(request, "encyclopedia/error.html",{'error':error})

def newpage(request):
    if request.method == 'POST':

        form = newpage_form(request.POST)

        if form.is_valid():

            title = form.cleaned_data['title'].capitalize()
            entry = form.cleaned_data['entry']

            if util.get_entry(title) != None:
                error = 'Wiki entry already exists'
                return render(request, 'encyclopedia/error.html',{'error':error})

            util.save_entry(title,entry)

            return redirect(f'/wiki/{title}/')
        
        else:
            return render(request, "encyclopedia/newpage.html",{"form":form})

    return render(request, "encyclopedia/newpage.html",{"form":newpage_form()})

def editpage(request,title):
    if request.method == "POST":

        form = editpage_form(request.POST)

        if form.is_valid():

            title = title.capitalize()
            entry = form.cleaned_data['entry']

            util.save_entry(title,entry)

            return redirect(f'/wiki/{title}/')
        
        else:
            return render(request, "encyclopedia/editpage.html",{"form":form})

    wiki = util.get_entry(title)
    return render(request, "encyclopedia/editpage.html",{"form":editpage_form({'entry':wiki}),'title':title})

def random(request):
    wiki = choice(util.list_entries())
    return render(request,'encyclopedia/wiki.html',{'wiki':markdowner.convert(util.get_entry(wiki)),'title':wiki})

def search(request):
    query = request.GET['q'].capitalize()

    if query in util.list_entries():
        return redirect(f'/wiki/{query}')
    
    eligible_entries = []

    for entry in util.list_entries():
        if query.lower() in entry.lower():
            eligible_entries.append(entry)
    
    return render(request,'encyclopedia/index.html',{'entries':eligible_entries})