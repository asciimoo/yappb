from django.db import models
from django.conf import settings

class Tags(models.Model):
    text = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.text
   
    class Meta:
        ordering = ["text"]
   
    class Admin:
        pass
    def get_link(self):
        return '<a href="/tag/%(tag)s">%(tag)s</a>' % { "tag": self.text }

class Posts(models.Model):
    author = models.CharField(max_length=128)
    title = models.CharField(max_length=256)
    post = models.TextField()
    date = models.DateTimeField()
    tags = models.ManyToManyField(Tags)
   
    def __unicode__(self):
        return self.title
   
    class Meta:
        ordering = ["-date"]
   
    class Admin:
        pass
   
    def get_summary(self):
        if len(self.post) < 400:
            return self.post
        else:
            return self.post[:400] + " [...]"

    def get_id(self):
        return self.id

    def get_comments(self):
        return self.comments_set.all()
   
    def get_comments_num(self):
        return len(self.comments_set.all())
   
    def get_tags(self):
        # http://www.skymind.com/~ocrow/python_string/
        return ', '.join([tag.get_link() for tag in self.tags.all()])
   
    def get_nice_url(self):
        return ("%s/%d/%s") % (settings.ROOT_URL, self.id, self.title)
   
    def get_absolute_url(self):
        return "http://localhost:1337" + self.get_nice_url()


class Comments(models.Model):
    author = models.CharField(max_length=30)
    website = models.URLField(blank=True, verify_exists=False)
    comment = models.TextField()
    date = models.DateTimeField()
    post = models.ForeignKey(Posts)
   
    def __unicode__(self):
        #return '%s (%s)' % (self.author, self.email)
        return '%s' % self.author
   
    class Meta:
        ordering = ["-date"]
   
    class Admin:
        pass
   
    def get_header(self):
        if self.website == "":
            return "%(author)s on %(date)s" % { "author": self.author,
                                              "date": self.date }

        else:
            return '<a href="%(website)s">%(author)s</a> on %(date)s' % { "website": self.website,
                                                                       "author": self.author,
                                                                       "date": self.date }
