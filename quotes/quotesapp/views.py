from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse

from .forms import TagForm, AuthorForm, QuoteForm
from .models import Author, Quote, Tag

import subprocess
from concurrent.futures import ThreadPoolExecutor

Pool = ThreadPoolExecutor(max_workers=1)
scrapper = []

RECORDS_PER_PAGE = 10

# Create your views here.
def main(request, page=1):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, RECORDS_PER_PAGE)
    paginator.get_page(page).previous_page_number
    return render(request, 'quotesapp/index.html', {'quotes': paginator.get_page(page),
                                                    "top_ten_tags": Tag.top_ten_tags()})

@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/tag.html', {'form': form})

    return render(request, 'quotesapp/tag.html', {'form': TagForm()})

@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/author.html', {'form': form})
        
    return render(request, 'quotesapp/author.html', {'form': AuthorForm()})


def author_detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotesapp/author_detail.html', {"author": author})


def quotes_by_tag(request, tag_id, page=1):
    tag = Tag.objects.get(pk=tag_id)
    quotes = Quote.objects.filter(tags__pk=tag_id)
    paginator = Paginator(quotes, RECORDS_PER_PAGE)
    return render(request, 'quotesapp/quotes_by_tag.html', {"quotes": paginator.get_page(page), 
                                                            "tag": tag,
                                                             "top_ten_tags": Tag.top_ten_tags()})


@login_required
def quote(request):
    authors = Author.objects.all()
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/quote.html', {'form': form, 'authors': authors, "tags": tags})
        
    return render(request, 'quotesapp/quote.html', {'form': QuoteForm(), 'authors': authors, "tags": tags})


@login_required
def load_data(request):
    command = 'python -m utils.scrap_and_load'
    if not scrapper:
        future = Pool.submit(subprocess.run, command, shell=True)
        scrapper.append(future)
    
    return JsonResponse({"success": True})

@login_required
def load_check(request):
    if not scrapper:
        return JsonResponse({"success": False, "not_loading": True})
    if scrapper and scrapper[0].done():
        scrapper.pop()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "not_loading": False})