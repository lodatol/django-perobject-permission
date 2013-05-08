django-perobject-permission
===========================

Simple, flexible and scalable Django authorization backend that handle per-object permission management.

This project take some ideas from django-rules and django-rulez but I need somethink more simple and more dry.

Moreover an important requirement is that I am able to see at compile time if a rule is undefined.

Philosophy
==========
 - Django 1.5 compatibility
 - No authorization backend. I don't want add complexity to my settings.py.
 - Small (very small). Less lines of code mean less complexity, faster execution.
 - You can implement each authorization constraint as a boolean attribute, property or method of the model, whichever you prefer for each rule. This way you will be able to re-implement how authorizations work at any time
 - No database usage, I don't want hit db for every permission check (like django-rules)
 - No huge memory usage, I don't want a dict in memory with all rule (like django-rulez)
 - More Dry


Installation
============

<pre>
pip install -e git+https://github.com/lodatol/django-perobject-permission#egg=django-perobject-permission
</pre>


Configuration
==============
Add it to the list of INSTALLED_APPS in settings.py:
<pre>
INSTALLED_APPS = (
    ...
    'django_perobject_permission',
)
</pre>


Rules
=====
A rule represents a functional authorization constraint that restricts the actions that a certain user can carry out on a certain object (an instance of a Model).

We need to code only the functional authorization in the model.

This function take as input the selected object and the user.

<pre>
from django.db import models

class Post(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    def can_see(self, user):
        if user.level = user.MANAGER:
            return True
        if self in user.get_profile().posts:
            return True
        return False
    def __unicode__(self):
        return u"%s"%self.text
</pre>


Rule Usage
==========

We can use the decorator <i>object_permission_required</i>, it take 5 parameters:
* func: functional authorization constraint defined (eg. Post.can_see)
* view_param_pk: The view parameter’s name to use for getting the primary key of the model (default: 'pk').
* login_url: If user isn't authenticated the login url were he can be log in. If none it points to default login url (default: None)
* raise_exception: If must be raised a PermissionDenied when user isn't authorized (default: False)

Example:
* With a class based view:
<pre>
  from django.conf.urls import patterns, include, url
  from django_perobject_permission.decorators import object_permission_required
  from .views import *
  from .models import *
  urlpatterns = patterns('test.views',
      url(r'home/$', home),
      url(r'post/(?P\<post_id\>\d+)/$', object_permission_required(Post.can_see,'post_id')(PostDetail.as_view()))
  )
</pre>
* With a function based view:
<pre>
  ...
  from django_perobject_permission.decorators import object_permission_required
  from .models import *
  @object_permission_required(Post.can_see,'post_id')
  def post_detail(request,post_id):
      post = get_object_or_404(Post, pk=post_id)
      return render_to_response('detail.html',{post:post},context_instance=RequestContext(request))
</pre>
