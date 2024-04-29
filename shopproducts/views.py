import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic import ListView
from django.shortcuts import render
from shoporders.forms import OrderForm
from .models import Product, ProductGallery, Comment
from shop_products_category.models import ProductCategory
import itertools
from .forms import CommentForm


def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


@login_required(login_url='login')
def productdetail(request, pk):
    product: Product = Product.objects.get_by_id(pk)
    order_form = OrderForm(request.POST or None, initial={'product_id': product.id})

    gallery = ProductGallery.objects.filter(product=product)
    grouped_gallery = list(my_grouper(3, gallery))

    related_products = Product.objects.filter(category__product=product)
    grouped_related_products = list(my_grouper(4, related_products))
    comments = Comment.objects.filter(product=product)
    form = CommentForm(request.POST or None, initial={'product': product, 'user': request.user})
    if form.is_valid():
        product = product
        comment = form.cleaned_data.get('comment')
        Comment.objects.create(product=product, user=request.user, comment=comment)

    if product is None or not product.active:
        raise Http404('محصول یافت نشد')
    else:
        product.visit_count += 1
        product.save()
        context = {'product': product,
                   'gallery': grouped_gallery,
                   'related_products': grouped_related_products,
                   'order_form': order_form,
                   'form': form,
                   'comments': comments}
        return render(request, 'shopproducts/productdetail.html', context)


class ProductList(ListView):
    template_name = 'shopproducts/productlist.html'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.get_active_products()


class ProductListCategory(ListView):
    template_name = 'shopproducts/productlist.html'
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs['pk']
        category = ProductCategory.objects.filter(name__iexact=pk).first()
        if category is None:
            raise Http404('صفحه یافت نشد')

        return Product.objects.get_product_by_category(pk)


def categories_component(request):
    categories = ProductCategory.objects.all()
    context = {'categories': categories}
    return render(request, 'shopproducts/categories_component.html', context)


class SearchProductView(ListView):
    template_name = 'shopproducts/productlist.html'
    paginate_by = 10

    def get_queryset(self):
        request = self.request
        q = request.GET.get('q')
        return Product.objects.search_products(q)

