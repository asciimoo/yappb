from django import forms
from models import Posts, Comments, Tags
from datetime import datetime
from django.conf import settings

class BaseForm(forms.Form):
    def as_div(self):
        return self._html_output(u'<div class="form-row">%(label)s %(field)s<div class="helper-text">%(help_text)s</div> %(errors)s</div>', u'<div class="form-row">%s</div>', u'</div>', u'%s', False)

class CommentForm(BaseForm):
    author = forms.CharField(label=u'Author', max_length=128, required=True)
    website = forms.CharField(label=u'Website', max_length=256, required=False)
    comment = forms.CharField(label=u'Comment', widget=forms.Textarea, required=True)
    captcha_answer = forms.CharField(label=u'A lenti ket szam osszege', max_length=2, required=True)
    def __init__(self, request, *args, **kwargs):
        self.captcha = 1123765123812
        if 'captcha_answer' in request.session:
            self.captcha = int(request.session['captcha_answer'])
            del request.session['captcha_answer']
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean_captcha_answer(self):
        try:
            c = int(self.cleaned_data['captcha_answer'])
        except:
            raise forms.ValidationError(u'Matekzseni..')
        if c != self.captcha:
            raise forms.ValidationError(u'Matekzseni..')
        return c

    def save(self, post_id):
        try:
            post = Posts.objects.get(id=int(post_id))
        except:
            return False
        return Comments.objects.create(author = self.cleaned_data['author'], 
                                       website = self.cleaned_data['website'],
                                       comment = self.cleaned_data['comment'],
                                       post = post,
                                       date = datetime.now())

class PostForm(BaseForm):
    author = forms.CharField(label=u'Author', max_length=128, required=True)
    password = forms.CharField(label=u'Password', widget=forms.PasswordInput,  max_length=128, required=True)
    title = forms.CharField(label=u'Title', max_length=256, required=True)
    post = forms.CharField(label=u'Post', widget=forms.Textarea, required=True)
    tags = forms.CharField(label=u'Tags', max_length=1024, required=True)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data != settings.ADMIN_PASSWORD:
            raise forms.ValidationError("Nice try bitch.. wrong password")
        return data
    
    def save(self):
        new = Posts.objects.create(author = self.cleaned_data['author'],
                                   title = self.cleaned_data['title'],
                                   post = self.cleaned_data['post'],
                                   #tags = self.cleaned_data['tags'],
                                   date = datetime.now())


        for tag in self.cleaned_data['tags'].split(' '):
            try:
                t = Tags.objects.get(text=tag)
                new.tags.add(t)
            except:
                new.tags.create(text=tag)
        return new
