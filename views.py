from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings
from engine.forms import CommentForm, PostForm
from engine.models import Posts, Tags
from captcha import captcha

def index(request):
    post_num = len(Posts.objects.all())
    posts = Posts.objects.all()[:10]
    tags = Tags.objects.all()
    return render_to_response('index.html', {'posts': posts, 'tags': tags})

def add_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save()
            return HttpResponseRedirect("%s" % post.get_nice_url())
    else:
        form = PostForm()
    return render_to_response('add_post.html', { 'form': form})

def view_post(request, post_id):
    try:
        post = Posts.objects.get(id=int(post_id))
    except:
        return render_to_response('error.html', {'msg': u'not found'})
    form = CommentForm(request)
    return render_to_response('view_post.html', {'post': post, 'comment_form': form})

def search(request):
    if request.method == 'GET':
        return render_to_response('search.html', {'query': request.GET['q']})
    else:
        return render_to_response('error.html', {'msg': u'wrong search query!!'})

def posts_by_tag(request, tag_name):
    #TODO get posts from Tags class (works =>many-to-many)
    posts = []
    for post in Posts.objects.all():
        try:
            post.tags.get(text=tag_name)
            posts.append({'title': post.title, 'id': post.id})
        except:
            pass

    return render_to_response('posts_by_tag.html', {'tag': tag_name, 'posts': posts})

def add_comment(request, post_id):
    try:
        post = Posts.objects.get(id=int(post_id))
    except:
        return render_to_response('error.html', {'msg': u'not found'})
    if request.method == 'POST':
        form = CommentForm(request, data=request.POST)
        if form.is_valid():
            comment = form.save(post_id)
            return HttpResponseRedirect("%s" % post.get_nice_url())
    else:
        form = CommentForm(request)
    return render_to_response('view_post.html', {'post': post, 'comment_form': form, 'post_id': post_id})
