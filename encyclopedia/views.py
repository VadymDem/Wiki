from django.shortcuts import render, redirect
from . import util
import markdown


def index(request):
    if request.method == "GET":
        query = request.GET.get('q', '')
        if query:
            entry = util.get_entry(query)
            if entry:
                # Якщо стаття знайдена, перенаправте користувача на сторінку статті
                return redirect('entry', title=query)
            else:
                # Якщо стаття не знайдена, перенаправте користувача на сторінку результатів пошуку
                entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
                return render(request, "encyclopedia/search_results.html", {
                    "query": query,
                    "entries": entries
                })
        else:
            # Якщо запит не був введений, просто поверніть головну сторінку
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })


def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "error": "The requested page was not found."
        })
    else:
        # Конвертуємо Markdown у HTML
        content_html = markdown.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content_html
        })


def create_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/create_page.html", {
                "error": "Page with this title already exists."
            })
        else:
            util.save_entry(title, content)
            return redirect('entry', title=title)
    else:
        return render(request, "encyclopedia/create_page.html")
