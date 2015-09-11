from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'thinkhard.views.home', name='home'),
    url(r'^robots\.txt$', 'thinkhard.views.robots', name='robots.txt'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^home/', 'thinkhard.views.home', name='home'),
    url(r'^note/$', 'thinkhard.views.note', name='note'),
    url(r'^note/new/$', 'thinkhard.views.new_note', name='new note'),
    url(r'^note/edit/(\w.*)/$', 'thinkhard.views.edit_note', name='edit note page'),
    url(r'^note/save$', 'thinkhard.views.save_note', name='save note'),
    url(r'^note/category/(\w.*)/$', 'thinkhard.views.get_notes_by_category', name='get notes by category'),
    url(r'^note/tag/(\w.*)/$', 'thinkhard.views.get_notes_by_tag', name='get notes by category'),
    url(r'^note/(\w.*)/$', 'thinkhard.views.show_note', name='note detail page'),
	
    url(r'^lab/', 'thinkhard.views.lab', name='lab'),
    url(r'^api/(\w.*)/$', 'thinkhard.views.api', name='api'),
    url(r'^get_items/(\w.*)/(\w.*)/$', 'thinkhard.views.get_items', name='get_items'),
    url(r'^get_notes/$', 'thinkhard.views.get_notes', name='get all notes'),
    url(r'^star/(\w.*)/$', 'thinkhard.views.star', name='star'),
    url(r'^read/', 'thinkhard.views.read', name='read'),
    url(r'^about/', 'thinkhard.views.about', name='about me'),
    url(r'^google1133f92c3042058c.html/', 'thinkhard.views.home', name='about me2'),
    # url(r'^admin/', include(admin.site.urls)),
)
