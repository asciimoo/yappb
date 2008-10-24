from django.conf.urls.defaults import *
from django.conf import settings
from engine.feeds import Atom, RSS2
from captcha import captcha
import views

feeds = { 'rss': RSS2, 'atom': Atom }

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

root_url = r'^'+settings.ROOT_URL[1:]

urlpatterns = patterns('',
    (root_url+'/$', views.index),
    (root_url+'/add_comment/(?P<post_id>\d+)$', views.add_comment),
    (root_url+'/(?P<post_id>\d+)/*', views.view_post),
    (root_url+'/add_post$', views.add_post),
    (root_url+'/search/*', views.search),
    (root_url+'/tags/(?P<tag_name>.*)$', views.posts_by_tag),
    (root_url+'/feeds/(?P<url>.*)$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (root_url+'/captcha/$', captcha.image),

    # Example:
    # (r'^faszkorbacsblog/', include('faszkorbacsblog.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
