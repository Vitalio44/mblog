from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect

from .form import PostForm
from .models import Post


def post_list(request):
    queryset_list = Post.objects.all()
    search = request.GET.get("s")
    if search:
        queryset_list = queryset_list.filter(
            Q(title__icontains = search) |
            Q(content__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        ).distinct()
    paginator = Paginator(queryset_list, 5)  # Show 5 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "List"
    }
    return render(request, "post_list.html", context)


def post_create(request):
    if not request.user.is_authenticated():
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    context = {
        "instance": instance,
        "title": instance.title
    }
    return render(request, "post_detail.html", context)


def post_update(request, slug=None):
    if not request.user.is_authenticated():
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Updated!")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "instance": instance,
        "title": instance.title,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    if not request.user.is_authenticated():
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Deleted!")
    return redirect(post_list)
