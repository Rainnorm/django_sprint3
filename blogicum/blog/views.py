from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from django.http import Http404
from .models import Category, Post

# Create your views here.


def index(request):
    template = 'blog/index.html'

    posts = (
        Post.objects.filter(
            pub_date__lte=now(),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')[:5]
    )
    context = {'post_list': posts}

    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post, id=id)

    if post.pub_date > now():
        raise Http404("Публикация еще не доступна.")

    # Проверяем, что публикация опубликована
    if not post.is_published:
        raise Http404("Публикация скрыта.")

    # Проверяем, что категория публикации опубликована
    if not post.category.is_published:
        raise Http404("Категория этой публикации скрыта.")

    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)
    posts = (
        Post.objects.filter(
            category=category,
            is_published=True,
            pub_date__lte=now()
        )
        .order_by('-pub_date')
    )
    context = {'category': category, 'post_list': posts}
    return render(request, template, context)
