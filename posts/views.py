### -*- coding: utf-8 -*- ###
from urllib.parse import quote_plus
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from posts.form import UserForm, UserProfileForm
from django.core.urlresolvers import reverse

from .form import PostForm, ContactForm
from .models import Post, Category, UserProfile


def post_list(request):
    queryset_list = Post.objects.all()
    category_list = Category.objects.all()
    search = request.GET.get("s")
    if search:
        queryset_list = queryset_list.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search)  # |
            # Q(user__first_name__icontains=search) |
            # Q(user__last_name__icontains=search)
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
        "category_list": category_list,
        "title": "Новое"
    }
    return render(request, "post_list.html", context)


def show_category(request, slug=None):
    category_show = {}
    try:
        category = Category.objects.get(slug=slug)
        pages = Post.objects.filter(category=category)
        category_show['pages'] = pages
        category_show['category'] = category
    except Category.DoesNotExist:
        raise Http404
    return render(request, 'category.html', category_show)


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


def post_detail(request, slug=None, category=None):
    instance = get_object_or_404(Post, slug=slug, category__slug=category)
    share_string = quote_plus(instance.title)
    context = {
        "instance": instance,
        "title": instance.title,
        "share_string": share_string,
    }
    return render(request, "post_detail.html", context)


def post_update(request, slug=None, category=None):
    if not request.user.is_authenticated():
        raise Http404
    instance = get_object_or_404(Post, slug=slug, category__slug=category)
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


def post_delete(request, slug=None, category=None):
    if not request.user.is_authenticated():
        raise Http404
    instance = get_object_or_404(Post, slug=slug, category__slug=category)
    instance.delete()
    messages.success(request, "Deleted!")
    return redirect(post_list)


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            name = form.cleaned_data['name']
            sender = form.cleaned_data['sender']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, name, message, sender)
            except BadHeaderError:  # Защита от уязвимости
                return HttpResponse('Invalid header found')
            # Переходим на другую страницу, если сообщение отправлено
            messages.success(request, "Отправлено!")
            return render(request, 'contact.html')
    else:
        # Заполняем форму
        form = ContactForm()
    # Отправляем форму на страницу
    return render(request, 'contact.html', {'form': form})


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,
                  'regist.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('list'))
            else:
                messages.warning(request, "Ваш аккаун не доступен")
                return render(request, 'login.html')
        else:
            print("Не верные данные для входа: {0}, {1}".format(username, password))
            messages.warning(request, "Неверные данные для входа.")
            return render(request, 'login.html')
    else:
        return render(request, 'login.html', {})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('list'))
