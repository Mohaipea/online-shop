import datetime
import time

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from shopproducts.models import Product
from .models import Order, OrderDetails
from .forms import OrderForm
from django.conf import settings
import requests
import json
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from suds.client import Client


@login_required(login_url='login')
def add_user_order(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if order is None:
            order = Order.objects.create(owner_id=request.user.id)

        product_id = form.cleaned_data.get('product_id')
        quantity = form.cleaned_data.get('quantity')
        if quantity < 0:
            quantity = 1
        product = Product.objects.get_by_id(pk=product_id)

        order.orderdetails_set.create(product_id=product_id, price=product.price, quantity=quantity)
        return redirect('productdetail', pk=product_id)
    return redirect('/')


@login_required(login_url='login')
def open_order(request):

    openorder: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    context = {'order': None,
               'orderdetails': None,
               'total': 0}

    if openorder is not None:
        context['order'] = openorder
        context['orderdetails'] = openorder.orderdetails_set.all()
        context['total'] = openorder.get_total_price()

    return render(request, 'shoporders/open_orders.html', context)


def remove_order(request, *args, **kwargs):
    order_id = kwargs.get('order_id')
    if order_id is not None:
        order_detail = OrderDetails.objects.get_queryset().get(id=order_id, order__owner_id=request.user.id)
        if order_detail is not None:
            order_detail.delete()
        return redirect('openorder')
    raise Http404()


ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://sandbox.zarinpal.com/pg/StartPay/"


MERCHANT = '9e45f1bd-4c43-4d48-9358-e099c0657de9'  # Required
client = Client('https://sandbox.zarinpal.com/pg/services/WebGate/wsdl')  # Required
amount = 10  # Amount will be based on Toman  Required
description = u'توضیحات تراکنش تستی'  # Required
email = 'user@userurl.ir'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://127.0.0.1:8000/verify/'


def send_request(request):
    openorder: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
    total_price = 0
    if openorder is not None:
        total_price = openorder.get_total_price()
        result = client.service.PaymentRequest(MERCHANT, total_price, description, email, mobile, f'{CallbackURL}{openorder.id}')
        if result.Status == 100:

            return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + result.Authority)
        else:
            return HttpResponse('Error')
    raise Http404('Order not found')


def verify(request, *args, **kwargs):
    order_id = kwargs.get('orderid')
    user_order = Order.objects.get_queryset().get(id=order_id)
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], user_order.get_total_price())
        if result.Status == 100:
            user_order.is_paid = True
            user_order.payment_date = datetime.datetime.now()
            user_order.ref_id = str(result.RefID)
            user_order.save()
            return HttpResponse('Transaction success. RefID: ' + str(result.RefID) + '\n you nailed it')
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed. Status: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')
