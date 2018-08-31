from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from markdown_deux import markdown

from comments.models import Comment

from .utils import get_read_time


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False, publish__lte=timezone.now())


def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, max_length=200)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field="height_field",
                              height_field="width_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    read_time = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def get_markdown(self):
        return mark_safe(markdown(self.content))

    @property
    def comments(self):
        return Comment.objects.filter_by_instance(self)

    @property
    def get_content_type(self):
        return ContentType.objects.get_for_model(self.__class__)

    class Meta:
        ordering = ["-timestamp", "-updated"]


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    instance.slug = create_slug(instance)

    if instance.content:
        instance.read_time = get_read_time(markdown(instance.content))


def create_slug(instance, new_slug=None):
    if instance.slug:
        return instance.slug
    slug = slugify(instance.title)
    if new_slug:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()

    if exists:
        new_slug = "{}-{}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


pre_save.connect(pre_save_post_receiver, sender=Post)
