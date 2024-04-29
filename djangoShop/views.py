import itertools

from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView

from shop_products_category.models import ProductCategory
from shop_slider.models import Slider
from shopproducts.models import Product
from shopsetting.models import ShopSetting


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def home(request):
    sliders = Slider.objects.all()

    most_seen = Product.objects.order_by('-visit_count').filter(active=True)[:10]
    grouped_most_seen = list(my_grouper(4, most_seen))

    latest_products = Product.objects.order_by('-id').all()[:8]
    grouped_latest_products = my_grouper(4, latest_products)

    context = {'sliders': sliders,
               'grouped_most_seen': grouped_most_seen,
               'grouped_latest_products': grouped_latest_products}
    return render(request, 'home.html', context)


def header(request, *args, **kwargs):
    context = {'data': ''}
    return render(request, 'shared/header.html', context)


def aboutus(request, *args, **kwargs):
    setting = ShopSetting.objects.first()
    context = {'setting': setting}
    return render(request, 'aboutus.html', context)


def footer(request, *args, **kwargs):
    setting = ShopSetting.objects.first()
    context = {'setting': setting}
    return render(request, 'shared/footer.html', context)


def category(request, *args, **kwargs):
    name = kwargs.get('name')
    products = Product.objects.filter(category__name__iexact=name)

    context = {'products': products}
    return render(request, 'category_partial.html', context)