from django.views.generic import ListView
from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'
    articles = Article.objects.order_by(ordering).prefetch_related('section').values('id', 'title', 'image', 'text',
                                                                                     'section__name', 'relationship__main_section')

    object_list = []
    articles_counter = []
    for a in articles:
        if a['id'] not in articles_counter:
            articles_counter.append(a['id'])
            a_object = {}
            a_object['id'] = a['id']
            a_object['title'] = a['title']
            a_object['image'] = a['image']
            a_object['text'] = a['text']
            a_object['scopes'] = [{'topic': a['section__name'], 'is_main': a['relationship__main_section']}]
            object_list.append(a_object)
        else:
            for o in object_list:
                if o['id'] == a['id']:
                    o['scopes'].append({'topic': a['section__name'], 'is_main': a['relationship__main_section']})

    context = {
        'object_list': object_list
    }

    return render(request, template, context)
