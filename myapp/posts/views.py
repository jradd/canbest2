from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Post

from comments.models import Comment
from comments.forms import CommentForm


def post_list(request):
    posts = Post.objects.active()
    if check_authenticated(request):
        posts = Post.objects.all()

    query = request.GET.get("q")
    posts = posts.filter(Q(title__icontains=query) |
                         Q(content__icontains=query) |
                         Q(user__first_name__icontains=query) |
                         Q(user__last_name__icontains=query)).distinct() if query else posts

    page_request_var = "page"
    paginated_posts = paginated_res(request, posts, 5, page_request_var)
    ctx = {
        "instance": paginated_posts,
        "page_request_var": "page",
        "now": timezone.now()
    }
    return render(request, "posts/index.html", ctx)


def post_detail(request, slug=None):
    obj = get_object_or_404(Post, slug=slug)
    draft = obj.draft or obj.publish > timezone.now()
    if draft:
        check_authenticated_with_404(request)

    initial_data = {
        'content_type': obj.get_content_type,
        'object_id': obj.id,
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)

    if comment_form.is_valid() and request.user.is_authenticated():
        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        object_id = comment_form.cleaned_data.get("object_id")
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None
        parent_obj = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            parent_obj = parent_qs.first() if parent_qs.exists() else None

        content = comment_form.cleaned_data.get("content")

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content,
            parent=parent_obj
        )

        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = Comment.objects.filter_by_instance(obj)
    ctx = {
        'instance': obj,
        'draft': draft,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, "posts/post_detail.html", ctx)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Post created successfully", extra_tags='')
        return HttpResponseRedirect(instance.get_absolute_url())
    ctx = {
        'form': form,
        'label': "Create Post"
    }
    return render(request, "posts/post_form.html", ctx)


@login_required
def post_update(request, slug=None):
    obj = get_object_or_404(Post, slug=slug)

    form = PostForm(request.POST or None, request.FILES or None, instance=obj)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post updated successfully", extra_tags='')
        return HttpResponseRedirect(instance.get_absolute_url())

    ctx = {
        'title': obj.title,
        'content': obj.content,
        'form': form,
        'label': "Update Post"
    }
    return render(request, "posts/post_form.html", ctx)


@login_required
def post_delete(request, slug=None):
    obj = get_object_or_404(Post, slug=slug)
    if obj:
        obj.delete()
        messages.success(request, "Post deleted successfully", extra_tags='')
        return redirect("posts:list")
    return redirect("posts:list")


def paginated_res(request, obj, per_page, page_request_var="page"):
    paginator = Paginator(obj, per_page=per_page)
    page = request.GET.get(page_request_var) or 1
    try:
        res = paginator.page(page)
    except PageNotAnInteger:
        res = paginator.page(1)
    except EmptyPage:
        res = paginator.page(paginator.num_pages)
    return res or None


def check_authenticated(request):
    return False if not request.user.is_staff or not request.user.is_superuser else True


def check_authenticated_with_404(request):
    if not check_authenticated(request):
        raise Http404
    return True
