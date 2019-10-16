from django.views.generic import ListView
from django.shortcuts import render

from articles.models import Article, Relationship


def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'
    articles = Article.objects.order_by(ordering).prefetch_related('section')
    relation = Relationship.objects.all()
    object_list = []
    for a in articles:
        a_object = {}
        a_object['id'] = a.id
        a_object['title'] = a.title
        a_object['image'] = a.image
        a_object['text'] = a.text
        scopes = []
        for s in a.section.all():
            for r in relation:
                if r.article.title == a.title and r.section.name == s.name:
                    scopes.append({'topic': s.name, 'is_main': r.main_section})
        a_object['scopes'] = scopes
        object_list.append(a_object)

    context = {
        'object_list': object_list
    }

    return render(request, template, context)
