from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

import json
from django.contrib import messages

from .models import *


def HomeView(request):
  #  try:
  #      customer = request.user.customer
  #  except:
 #       device = request.COOKIES['device']
  #      customer, created = Customer.objects.get_or_create(device=device)

 #   order, created = Order.objects.get_or_create(customer=customer, ordered=False)
 #   order_items = order.items.all()
 #   cartItems = order.get_items_total


    #products = Product.objects.all()
    #context = { 'products': products, 'cartItems': cartItems}
    return render(request, 'index.html')


def ProductDetailView(request, id):
    product = Product.objects.get(pk=id)

    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, ordered=False)
    order_items = order.items.all()
    cartItems = order.get_items_total
    
    context = {'product': product, 'cartItems':cartItems}
    return render(request, 'product-page.html', context)


def OrderSummaryView(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order = Order.objects.get(customer=customer, ordered=False)
    order_items = order.items.all()
    cartItems = order.get_items_total

    context = { 'order': order, 'order_items':order_items, 'cartItems': cartItems }
    return render(request, 'summary.html', context)


def CheckoutView(request):
    if request.method == "POST":
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order = Order.objects.get(customer=customer, ordered=False)
        if request.POST['name'] and request.POST['mobile_number']:
            customer.name = request.POST['name']
            customer.mobile_number = request.POST['mobile_number']           
            customer.save()
            order.name = customer.name
            order.mobile_number = customer.mobile_number
            order.save()

            messages.info(request, "You data was send.")
            return redirect('core:home')
    else:     
        try:
            customer = request.user.customer
        except:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)

        order = Order.objects.get(customer=customer, ordered=False)
        order_items = order.items.all()
        cartItems = order.get_items_total

        context = { 'order': order, 'order_items':order_items, 'cartItems': cartItems }
        return render(request, 'checkout-page.html', context)



def add_to_cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:', action)
    print('productId:', productId)

    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    product = Product.objects.get(id=productId)
    order_item, created = OrderItem.objects.get_or_create(item=product, user=customer, ordered=False)
    order, created = Order.objects.get_or_create(customer=customer, ordered=False)

    if order.items.filter(item__id=product.id).exists():

            if action == 'add':
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "this item was +1")
            
            if action == 'remove':
                order_item.quantity -= 1
                if order_item.quantity <= 0:
                    order_item.delete()
                    messages.info(request, "Deleted")
                else:
                    order_item.save()
                    messages.info(request, "Removed")

    else:
        
        order.items.add(order_item)
        messages.info(request, "this item was Added")

    return JsonResponse('Item was added', safe=False)



# for + button only
def add(request, id):
    product = get_object_or_404(Product, pk=id)
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order = Order.objects.get(customer=customer, ordered=False)
    order_item = OrderItem.objects.get(item=product, user=customer, ordered=False)

    order_item.quantity += 1
    order_item.save()
    messages.info(request, 'Added')
    return redirect('core:order_summary')

# for - button only
def remove(request, id):
    product = get_object_or_404(Product, pk=id)
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order = Order.objects.get(customer=customer, ordered=False)
    order_item = OrderItem.objects.get(item=product, user=customer, ordered=False)

    order_item.quantity -= 1
    
    if order_item.quantity <= 0:
        order_item.delete()
        messages.info(request, "Deleted")
        return redirect('core:order_summary')
    else:
        order_item.save()
        messages.info(request, 'Minus')
        return redirect('core:order_summary')

# for delete button in order_summary only
def delete(request, id):
    product = get_object_or_404(Product, pk=id)
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    order = Order.objects.get(customer=customer, ordered=False)
    order_item = OrderItem.objects.get(item=product, user=customer, ordered=False)

    order_item.delete()
    messages.info(request, 'Deleted successfully')
    return redirect('core:order_summary')
    
   


    