# encoding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from bs4 import BeautifulSoup
from time import gmtime, strftime, time
from django.views.decorators.csrf import csrf_exempt
import cluster
import subscription
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
import pickle
import json
client = MongoClient()
documents = client.rss.documents
notes = client.rss.notes
summary = client.rss.summary

def robots(request):
    return render(request, 'robots.txt',{})

def home(request):
    output = 'hello world'
    return render(request, 'home.html')


def note(request):        
    return render(request, 'note.html', {"notes":notes.find({'status':'published'}), "tags": get_tags(),"categories":get_categories()})


def get_categories():
    categories={}
    for item in notes.find({'status':'published'},{'category':1}):
        if 'category' not in item:
            continue
        for category in item['category'].split(';'):
            categories.setdefault(category, 0)
            categories[category]+=1
    return categories        


def get_tags():
    tags = summary.find_one({'name':'tags'})['value']
    dict_tags = [{'name':x[0],'count':x[1]} for x in tags.items()]
    sorted_tags = sorted(dict_tags, key=lambda x:x['count'],reverse=True)
    return sorted_tags

def get_notes_by_category(request,query):        
    return render(request, 'search_result.html', {"notes":notes.find({'category': query,'status':'published'}),'label':'类别', 'query':query, 'tags': get_tags(),"categories":get_categories()})    


    
def get_notes_by_tag(request,query):        
    return render(request, 'search_result.html', {"notes":notes.find({'content': {'$regex': query,'$options':'i'},'status':'published'}),'label':'标签', 'query':query, "tags": get_tags(),"categories":get_categories()})    


def show_note(request, id):
    note =notes.find_one({'_id': id})
    if 'related' in note:        
        note['related'] ={x['_id']: x['title'] for x in notes.find({'_id':{'$in': note['related']}}, {'title':1})}
    return render(request, 'detail.html', {'note': note})


def edit_note(request, id):
    return render(request, 'edit_note.html', {'note': notes.find_one({'_id': id})})



def lab(request):
    # subscription.start()
    sites = subscription.get_all_sites()
    return render(request, 'lab.html', {'sites': sites, 'range': xrange(0, 10)})


def api(request, id):
    doc = subscription.get_document(id)
    subscription.set_as_read(id)
    return render(request, 'article.html', {'doc': doc})


def star(request, id):
    doc = subscription.get_document(id)
    subscription.star(id)
    return HttpResponse({"status": "ok"})


def read(request):
    sites = subscription.get_all_sites()
    items = subscription.get_latest_items(100)
    cates = subscription.get_cates()
    return render(request, 'read.html', {'sites': sites, 'cates': cates})


def new_note(request):
    return render(request, 'new_note.html', {})


@csrf_exempt
def save_note(request):
    if request.method == 'POST':
        new_node = request.POST.dict()
        if len(new_node['_id']) == 0:
            new_node['_id'] = str(time()).replace('.', '')
            notes.insert(new_node)
        else:
            if len(new_node['content'].strip()) != 0:
                notes.update({'_id': new_node['_id']}, {'$set': dict((k, v) for k, v in new_node.items() if k != '_id')})
        return HttpResponse(json.dumps({'_id': new_node['_id']}), content_type="application/json")


def get_items(request, field, query):
    sort_condition = [("published_parsed", -1)]
    limit_size = 100
    if field == 'type':
        filter_conditons = {'all': {}, 'read': {"read": 1},
                            'unread': {'read': None}, 'star': {'star': 1}}
        query = filter_conditons[query]
    if field == 'category':
        query = {'category': query}
    if field == 'site':
        query = {'site_title': query}
    print query
    items = documents.find(query).sort(
        sort_condition).limit(limit_size)
    return render(request, 'item-list.html', {"items": items})


def about(request):
    with open('thinkhard/resume.txt') as f:        
        resume =  json.loads(f.read())            
    return render(request, 'about.html',{'note': notes.find_one({'_id':'140825547899'}), 'resume': resume})
