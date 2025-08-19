import markdown2
import random
from . import util
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def error(request):
    return render(request, "encyclopedia/404notfound.html")


def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/404notfound.html", {
            "message": "404 not found."
        })

    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })


def random_page(request): 
    entries = util.list_entries()
    if entries:
        selected = random.choice(entries)
        return redirect("entry", title=selected)
    else:
        return render(request, "encyclopedia/404notfound.html", {
            "message": "404 not found."
        })


class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")


def new_entry(request):
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].strip()
            content = form.cleaned_data["content"]

            if util.get_entry(title):
                return render(request, "encyclopedia/new_entry.html", {
                    "form": form,
                    "error": "This page already exists."
                })

            util.save_entry(title, content)
            return redirect("entry", title=title)
    else:
        form = EntryForm()

    return render(request, "encyclopedia/new_entry.html", {
        "form": form
    })


class EditForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")


def edit(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/404notfound.html", {
            "message": f"The page '{title}' was not found."
        })

    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data["title"].strip()
            new_content = form.cleaned_data["content"]

            if new_title != title and util.get_entry(new_title):
                return render(request, "encyclopedia/edit.html", {
                    "form": form,
                    "title": title,
                    "error": "Title already exists."
                })

            if new_title != title:
                util.delete_entry(title)

            util.save_entry(new_title, new_content)
            return redirect("entry", title=new_title)
    else:
        form = EditForm(initial={"title": title, "content": content})

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form
    })

def delete(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/404notfound.html", {
            "message": f"The page '{title}' was not found."
        })

    util.delete_entry(title)
    return redirect("index")

def search(request):
    if request.method == "GET":
        query = request.GET.get("q", "").strip().lower()
        if not query:
            return redirect("index")

        all_entries = util.list_entries()
        results = [entry for entry in all_entries if query in entry.lower()]

        for entry in all_entries:
            if entry.lower() == query:
                return redirect("entry", title=entry)

        if not results:
            return render(request, "encyclopedia/404notfound.html", {
                "message": f'No results found for "{query}".'
            })

        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": results
        })
    