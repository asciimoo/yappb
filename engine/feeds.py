from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed, RssUserland091Feed, Rss201rev2Feed
from models import Posts
from django.conf import settings

class Atom(Feed):
    feed_type = Atom1Feed
    title = "Latest blog entries"
    link = settings.ROOT_URL[1:]+"/a"
    description = "Updates on the latest blog entries!"
   
    def items(self):
        return Posts.objects.all()[:10]

class RSS091(Atom):
    feed_type = RssUserland091Feed

class RSS2(Atom):
    feed_type = Rss201rev2Feed
