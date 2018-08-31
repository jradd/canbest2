from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from .models import Comment


def comment_thread(request, id):
    obj = get_object_or_404(Comment, id=id)
    initial_data = {
        'content_type': obj.content_type,
        'object_id': obj.object_id,
    }
    comment_form = CommentForm(request.POST or None, initial=initial_data)

    if comment_form.is_valid() and request.user.is_authenticated():

        c_type = comment_form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        object_id = comment_form.cleaned_data.get("object_id")

        parent_id = int(request.POST.get("parent_id")) or None
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

        return HttpResponseRedirect(obj.get_absolute_url())

    ctx = {
        'comment': obj,
        'comment_form': comment_form,
    }
    return render(request, "comments/comment_thread.html", ctx)


@login_required()
def comment_delete(request, id):
    try:
        obj = Comment.objects.get(id=id)
    except:
        raise Http404

    post_url = obj.content_object.get_absolute_url()

    if obj.user != request.user:
        return HttpResponseRedirect(post_url)

    if obj.parent:
        post_url = obj.parent.get_absolute_url()

    if request.method == "POST":
        obj.delete()
        messages.success(request, "Comment deleted successfully")
        return HttpResponseRedirect(post_url)
    ctx = {
        'comment': obj,
    }
    return render(request, "comments/confirm_delete.html", ctx)
