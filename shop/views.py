from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from shop.models import *
from django.db.models import Sum
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .tasks import send_greetings, send_order_details, send_message
from django.core.paginator import Paginator
from django.template.defaulttags import register
import json


def cart_quantity(request):
    if "client" in request.COOKIES.keys():
        client = request.COOKIES['client']
        cart, created = Cart.objects.get_or_create(client_id=client)
        if cart:
            cart_quantity = CartProduct.objects.filter(
                cart=cart).aggregate(Sum('quantity')).get('quantity__sum')
            if cart_quantity != None:
                return cart_quantity
    cart_quantity = 0
    return cart_quantity


def home(request):
    recommended_products = Product.objects.filter(
        status=1).filter(recommended=1)
    unique_category = Category.objects.filter(name='Unikaty')
    if len(unique_category) > 0:
        gallery_products = Product.objects.filter(
            categories=unique_category[0])[:4]
    else:
        gallery_products = []
    cart_qty = cart_quantity(request)
    context = {
        'recommended_products': recommended_products,
        'gallery_products': gallery_products,
        'cart_quantity': cart_qty
    }
    return render(request, "shop/index.html", context)


def catalog(request, slug=''):
    from_price = request.GET.get('from_price', "")
    to_price = request.GET.get('to_price', "")
    product_state = request.GET.get('product_state', "1")
    sort_product = request.GET.get('sort_product', "no_sort")
    categories = Category.objects.all().order_by('name')
    if slug != '':
        category = Category.objects.filter(slug=slug)[:1][0]
        products = Product.objects.filter(categories=category)
    else:
        category = ""
        products = Product.objects.all()
    if product_state == '1':
        products = products.filter(status=1)
    elif product_state == '2':
        products = products.filter(status=0)
    if from_price:
        products = products.filter(price__gte=from_price)
    if to_price:
        products = products.filter(price__lte=to_price)
    if sort_product == "price_asc":
        products = products.order_by('price')
    elif sort_product == "price_desc":
        products = products.order_by('-price')
    elif sort_product == "name_asc":
        products = products.order_by('name')
    elif sort_product == "name_desc":
        products = products.order_by('-name')
    products_paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    paginated_products = products_paginator.get_page(page)
    cart_qty = cart_quantity(request)
    context = {
        'categories': categories,
        'product_state': product_state,
        'from_price': from_price,
        'to_price': to_price,
        'sort_product': sort_product,
        'products': paginated_products,
        'products_paginator': products_paginator,
        'category': category,
        'cart_quantity': cart_qty
    }
    return render(request, "shop/catalog.html", context)


def product(request, slug):
    product = Product.objects.get(slug=slug)
    images = Image.objects.filter(product=product)
    images = images[:4]
    categories = product.categories.all()
    similar_products = Product.objects.none()
    for category in categories:
        similar_products = similar_products.union(
            Product.objects.filter(categories=category).exclude(id=product.id))
    similar_products = similar_products[:10]
    cart_qty = cart_quantity(request)
    context = {
        'product': product,
        'images': images,
        'categories': categories,
        'similar_products': similar_products,
        'cart_quantity': cart_qty
    }
    return render(request, "shop/product.html", context)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def cart(request):
    if "client" in request.COOKIES.keys():
        client = request.COOKIES['client']
        cart, created = Cart.objects.get_or_create(client_id=client)
        if cart:
            cart_products = CartProduct.objects.filter(cart=cart)
            cart_products_prices = {}
            for cart_product in cart_products:
                cart_products_prices[cart_product.product.name] = cart_product.quantity * \
                    cart_product.product.price
            total_cart_price = 0
            for price in cart_products_prices.values():
                total_cart_price = total_cart_price + price
            context = {
                'cart_products': cart_products,
                'cart_products_prices': cart_products_prices,
                'total_cart_price': total_cart_price
            }
    else:
        return redirect("/")
    cart_qty = cart_quantity(request)
    context['cart_quantity'] = cart_qty
    return render(request, "shop/cart.html", context)


def data(request):
    if "client" in request.COOKIES.keys():
        client = request.COOKIES['client']
        cart, created = Cart.objects.get_or_create(client_id=client)
        if cart:
            if CartProduct.objects.filter(cart=cart).count() > 0:
                cartData = {}
                if cart.customer_name:
                    customer_name = cart.customer_name.split()
                    cartData["customer_firstname"] = customer_name[0]
                    cartData["customer_lastname"] = customer_name[1]
                if cart.customer_phone:
                    cartData["customer_phone"] = cart.customer_phone
                if cart.customer_email:
                    cartData["customer_email"] = cart.customer_email
                if cart.to_zip:
                    cartData["to_zip"] = cart.to_zip
                if cart.to_city:
                    cartData["to_city"] = cart.to_city
                if cart.to_street:
                    cartData["to_street"] = cart.to_street
                if cart.to_house_number:
                    cartData["to_house_number"] = cart.to_house_number
                if cart.address:
                    cartData["address"] = cart.address

                if cart.customer_name_other:
                    customer_name_other = cart.customer_name_other.split()
                    cartData["customer_firstname_other"] = customer_name_other[0]
                    cartData["customer_lastname_other"] = customer_name_other[1]
                if cart.customer_phone_other:
                    cartData["customer_phone_other"] = cart.customer_phone_other
                if cart.customer_email_other:
                    cartData["customer_email_other"] = cart.customer_email_other
                if cart.to_zip_other:
                    cartData["to_zip_other"] = cart.to_zip_other
                if cart.to_city_other:
                    cartData["to_city_other"] = cart.to_city_other
                if cart.to_street_other:
                    cartData["to_street_other"] = cart.to_street_other
                if cart.to_house_number_other:
                    cartData["to_house_number_other"] = cart.to_house_number_other
                if cart.address_other:
                    cartData["address_other"] = cart.address_other
                context = {
                    'cartData': cartData
                }
            else:
                return redirect("/")
    else:
        return redirect("/")
    cart_qty = cart_quantity(request)
    context['cart_quantity'] = cart_qty
    return render(request, "shop/data.html", context)


def checkout(request):
    if "client" in request.COOKIES.keys():
        client = request.COOKIES['client']
        cart, created = Cart.objects.get_or_create(client_id=client)
        context = {}
        if cart:
            if CartProduct.objects.filter(cart=cart).count() > 0 and cart.customer_name:
                cart_products = CartProduct.objects.filter(cart=cart)
                cart_products_prices = {}
                for cart_product in cart_products:
                    cart_products_prices[cart_product.product.name] = cart_product.quantity * \
                        cart_product.product.price
                total_cart_price = 0
                for price in cart_products_prices.values():
                    total_cart_price = total_cart_price + price

                cartData = {}
                if cart.customer_name:
                    customer_name = cart.customer_name.split()
                    cartData["customer_firstname"] = customer_name[0]
                    cartData["customer_lastname"] = customer_name[1]
                if cart.customer_phone:
                    cartData["customer_phone"] = cart.customer_phone
                if cart.customer_email:
                    cartData["customer_email"] = cart.customer_email
                if cart.to_zip:
                    cartData["to_zip"] = cart.to_zip
                if cart.to_city:
                    cartData["to_city"] = cart.to_city
                if cart.to_street:
                    cartData["to_street"] = cart.to_street
                if cart.to_house_number:
                    cartData["to_house_number"] = cart.to_house_number
                if cart.address:
                    cartData["address"] = cart.address

                if cart.customer_name_other:
                    customer_name_other = cart.customer_name_other.split()
                    cartData["customer_firstname_other"] = customer_name_other[0]
                    cartData["customer_lastname_other"] = customer_name_other[1]
                if cart.customer_phone_other:
                    cartData["customer_phone_other"] = cart.customer_phone_other
                if cart.customer_email_other:
                    cartData["customer_email_other"] = cart.customer_email_other
                if cart.to_zip_other:
                    cartData["to_zip_other"] = cart.to_zip_other
                if cart.to_city_other:
                    cartData["to_city_other"] = cart.to_city_other
                if cart.to_street_other:
                    cartData["to_street_other"] = cart.to_street_other
                if cart.to_house_number_other:
                    cartData["to_house_number_other"] = cart.to_house_number_other
                if cart.address_other:
                    cartData["address_other"] = cart.address_other

                context = {
                    'cart_products': cart_products,
                    'cart_products_prices': cart_products_prices,
                    'total_cart_price': total_cart_price,
                    'cartData': cartData
                }
            else:
                return redirect("/")
        cart_qty = cart_quantity(request)
        context['cart_quantity'] = cart_qty
        return render(request, "shop/checkout.html", context)
    else:
        return redirect("/")


def confirmation(request):
    if "client" in request.COOKIES.keys():
        client = request.COOKIES['client']
        order = Order.objects.filter(client_id=client)
        if order:
            order = Order.objects.get(client_id=client)
            if (order.customer_name and order.customer_phone and order.customer_email and order.to_zip and order.to_city and order.to_street and order.to_house_number and order.products):
                url_home = reverse("home")
                context = {
                    'order_number': order.order_number,
                    'url': url_home
                }
                return render(request, "shop/confirmation.html", context)
            else:
                return redirect("/")
        else:
            return redirect("/")
    else:
        return redirect("/")


def about(request):
    context = {}
    cart_qty = cart_quantity(request)
    context['cart_quantity'] = cart_qty
    return render(request, "shop/about.html", context)


def contact(request):
    context = {}
    cart_qty = cart_quantity(request)
    context['cart_quantity'] = cart_qty
    return render(request, "shop/contact.html", context)


def status(request, number):
    if number != '':
        if Order.objects.filter(order_number=number):
            order = Order.objects.get(order_number=number)
            order_products = OrderProduct.objects.filter(order=order)
            order_products_prices = {}
            for order_product in order_products:
                order_products_prices[order_product.product.name] = order_product.quantity * \
                    order_product.product.price
            total_order_price = 0
            for price in order_products_prices.values():
                total_order_price = total_order_price + price
            context = {
                'order': order,
                'order_products': order_products,
                'order_products_prices': order_products_prices,
                'total_order_price': total_order_price
            }
            return render(request, "shop/status.html", context)
        else:
            return redirect("/")
    else:
        return redirect("/")


def availableProducts(request):
    products = Product.objects.filter(status=1).values_list('name', flat=True)
    productsList = list(products)
    return JsonResponse(productsList, safe=False)


def searchProduct(request):
    if request.method == "POST":
        searchedProduct = request.POST.get('productsearch')
        if searchedProduct == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product = Product.objects.filter(
                name__contains=searchedProduct).first()
            if product:
                return redirect('produkt/' + product.slug)
            else:
                messages.info(
                    request, "Żaden produkt nie pasuje do Twojego wyszukiwania")
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect("/")


def addToCart(request):
    if request.method == 'POST':
        if "client" in request.COOKIES.keys():
            client = request.COOKIES['client']
            cart, created = Cart.objects.get_or_create(client_id=client)
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=int(product_id))
            quantity = request.POST.get('product_qty', 1)
            if (product):
                if (CartProduct.objects.filter(cart=cart, product=product)):
                    cart_product = CartProduct.objects.get(
                        cart=cart, product=product)
                    if (product.quantity and product.status == 1):
                        if (cart_product.quantity + int(quantity) <= product.quantity):
                            cart_product.quantity = cart_product.quantity + \
                                int(quantity)
                        else:
                            response = JsonResponse(
                                {'error': "Niewystarczająca ilość wybranego produktu"})
                            response.status_code = 403
                            return response
                    elif (product.status == 1):
                        cart_product.quantity = cart_product.quantity + \
                            int(quantity)
                    cart_product.save()
                else:
                    if (product.quantity and product.status == 1):
                        if (int(quantity) <= product.quantity):
                            cart.products.add(product)
                            cart_product = CartProduct.objects.get(
                                cart=cart, product=product)
                            cart_product.quantity = quantity
                        else:
                            response = JsonResponse(
                                {'error': "Niewystarczająca ilość wybranego produktu"})
                            response.status_code = 403
                            return response
                    elif (product.status == 1):
                        cart.products.add(product)
                        cart_product = CartProduct.objects.get(
                            cart=cart, product=product)
                        cart_product.quantity = quantity
                    cart_product.save()
                cart_qty = cart_quantity(request)
                return JsonResponse({'status': "Produkt został dodany do koszyka", 'cart_quantity': cart_qty})
        else:
            return redirect("/")
    else:
        return redirect("/")


def updateCart(request):
    if request.method == 'POST':
        if "client" in request.COOKIES.keys():
            client = request.COOKIES['client']
            cart = Cart.objects.get(client_id=client)
            cart_product_id = request.POST.get('product_id')
            quantity = request.POST.get('product_qty')
            print(quantity)
            if (CartProduct.objects.filter(id=int(cart_product_id), cart=cart)):
                cart_product = CartProduct.objects.get(
                    id=int(cart_product_id), cart=cart)
                if (cart_product.product.quantity and cart_product.product.status == 1):
                    if (int(quantity) <= cart_product.product.quantity):
                        cart_product.quantity = int(quantity)
                    else:
                        response = JsonResponse(
                            {'error': "Niewystarczająca ilość wybranego produktu"})
                        response.status_code = 403
                        return response
                elif (cart_product.product.status == 1):
                    cart_product.quantity = int(quantity)
                cart_product.save()
                cart_products = CartProduct.objects.filter(cart=cart)
                cart_products_prices = {}
                for cart_product in cart_products:
                    cart_products_prices[cart_product.product.name] = cart_product.quantity * \
                        cart_product.product.price
                cart_product = CartProduct.objects.get(
                    id=int(cart_product_id), cart=cart)
                cart_product_price = cart_products_prices.get(
                    cart_product.product.name)
                total_cart_price = 0
                for price in cart_products_prices.values():
                    total_cart_price = total_cart_price + price
                cart_product_qty = cart_product.quantity
                cart_qty = cart_quantity(request)
                return JsonResponse({'status': "Koszyk został zaktualizowany", 'cart_product_quantity': cart_product_qty, 'cart_product_price': cart_product_price, 'total_cart_price': total_cart_price, 'cart_quantity': cart_qty})
        else:
            return redirect("/")
    else:
        return redirect("/")


def deleteFromCart(request):
    if request.method == 'POST':
        if "client" in request.COOKIES.keys():
            client = request.COOKIES['client']
            cart = Cart.objects.get(client_id=client)
            cart_product_id = int(request.POST.get('product_id'))
            if (CartProduct.objects.filter(id=cart_product_id, cart=cart)):
                cart_product = CartProduct.objects.get(
                    id=cart_product_id, cart=cart)
                cart_product.delete()
                cart_products = CartProduct.objects.filter(cart=cart)
                cart_products_prices = {}
                for cart_product in cart_products:
                    cart_products_prices[cart_product.product.name] = cart_product.quantity * \
                        cart_product.product.price
                total_cart_price = 0
                for price in cart_products_prices.values():
                    total_cart_price = total_cart_price + price
                cart_qty = cart_quantity(request)
                return JsonResponse({'status': "Koszyk został zaktualizowany", 'total_cart_price': total_cart_price, 'cart_quantity': cart_qty})
        else:
            return redirect("/")
    else:
        return redirect("/")


def updateDataCart(request):
    if request.method == 'POST':
        if "client" in request.COOKIES.keys():
            client = request.COOKIES['client']
            cart = Cart.objects.get(client_id=client)
            cartData = request.POST.get('cartData')
            cartDataAlternative = request.POST.get('cartDataAlternative')
            cartDataJson = json.loads(cartData)
            cart.customer_name = cartDataJson["firstname"] + \
                " " + cartDataJson["lastname"]
            cart.customer_phone = cartDataJson["phone"]
            cart.customer_email = cartDataJson["email"]
            cart.to_zip = cartDataJson["zipcode"]
            cart.to_city = cartDataJson["city"]
            cart.to_street = cartDataJson["street"]
            cart.to_house_number = cartDataJson["housenumber"]
            if "address" in cartDataJson:
                cart.address = cartDataJson["address"]
            cartDataAlternativeJson = json.loads(cartDataAlternative)
            if cartDataAlternativeJson.get("firstname-a"):
                cart.customer_name_other = cartDataAlternativeJson["firstname-a"] + \
                    " " + cartDataAlternativeJson["lastname-a"]
                cart.customer_phone_other = cartDataAlternativeJson["phone-a"]
                cart.customer_email_other = cartDataAlternativeJson["email-a"]
                cart.to_zip_other = cartDataAlternativeJson["zipcode-a"]
                cart.to_city_other = cartDataAlternativeJson["city-a"]
                cart.to_street_other = cartDataAlternativeJson["street-a"]
                cart.to_house_number_other = cartDataAlternativeJson["housenumber-a"]
                if "address-a" in cartDataAlternativeJson:
                    cart.address_other = cartDataAlternativeJson["address-a"]
            cart.save()
            return JsonResponse({'url': reverse('checkout')})
        else:
            return redirect("/")
    else:
        return redirect("/")


def placeOrder(request):
    if request.method == 'POST':
        if "client" in request.COOKIES.keys():
            client = request.COOKIES['client']
            cart = Cart.objects.get(client_id=client)
            cart_products = cart.products.all()
            order = Order(customer_name=cart.customer_name, customer_phone=cart.customer_phone, customer_email=cart.customer_email,
                          to_zip=cart.to_zip, to_city=cart.to_city, to_street=cart.to_street, to_house_number=cart.to_house_number)
            if cart.address:
                order.address = cart.address
            if cart.customer_name_other:
                order.customer_name_other = cart.customer_name_other
            if cart.customer_phone:
                order.customer_phone = cart.customer_phone
            if cart.customer_email_other:
                order.customer_email_other = cart.customer_email_other
            if cart.to_zip_other:
                order.to_zip_other = cart.to_zip_other
            if cart.to_city_other:
                order.to_city_other = cart.to_city_other
            if cart.to_street_other:
                order.to_street_other = cart.to_street_other
            if cart.to_house_number_other:
                order.to_house_number_other = cart.to_house_number_other
            if cart.address_other:
                order.address_other = cart.address_other
            order.client_id = client
            order.save()
            for product in cart_products:
                cart_product = CartProduct.objects.get(
                    cart=cart, product=product)
                if (product.quantity and product.status == 1):
                    if cart_product.quantity <= product.quantity:
                        order.products.add(product)
                        order_product = OrderProduct.objects.get(
                            order=order, product=product)
                        order_product.quantity = cart_product.quantity
                        product.quantity = product.quantity - cart_product.quantity
                        if product.quantity == 0:
                            product.status = 0
                        product.save()
                    else:
                        cart_product.quantity = product.quantity
                        cart_product.save()
                        messages.error(
                            request, "Niewystarczająca ilość wybranych produktów - zaktualizowano koszyk")
                        response = JsonResponse({'url': reverse('cart')})
                        response.status_code = 403
                        return response
                elif product.status == 1:
                    order.products.add(product)
                    order_product = OrderProduct.objects.get(
                        order=order, product=product)
                    order_product.quantity = cart_product.quantity
                else:
                    CartProduct.objects.get(
                        cart=cart, product=product).delete()
                    messages.error(
                        request, "Niewystarczająca ilość wybranych produktów - zaktualizowano koszyk")
                    response = JsonResponse({'url': reverse('cart')})
                    response.status_code = 403
                    return response
                order_product.save()
            order.save()
            cart.delete()
            send_order_details.delay(order.order_number)
            return JsonResponse({'url': reverse('confirmation')})
        else:
            return redirect("/")
    else:
        return redirect("/")


def cancelOrder(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        if Order.objects.filter(order_number=order_number):
            order = Order.objects.get(order_number=order_number)
            if order.status == 'ordered':
                order_products = OrderProduct.objects.filter(order=order)
                for order_product in order_products:
                    product = order_product.product
                    if product.quantity:
                        product.quantity = product.quantity + order_product.quantity
                    else:
                        product.quantity = order_product.quantity
                        product.status = 1
                    product.save()
                order.delete()
                messages.info(request, "Pomyślnie anulowano zamówienie")
                return JsonResponse({'url': reverse('home')})
    else:
        return redirect("/")


def addToNewsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_email = Newsletter(customer_email=email)
        new_email.save()
        send_greetings.delay(new_email.customer_email)
        return JsonResponse({'status': "Pomyślnie zapisano do newslettera"})
    else:
        return redirect("/")


def cancelNewsletter(request, email=""):
    if email != "":
        if Newsletter.objects.filter(customer_email=email):
            newsletter_email = Newsletter.objects.filter(customer_email=email)
            newsletter_email.delete()
            messages.info(
                request, "Pomyślnie anulowano subskrypcję newslettera")
            return redirect("/")
    else:
        return redirect("/")


def sendMessage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        topic = request.POST.get('topic')
        message = request.POST.get('message')
        send_message.delay(email, topic, message)
        return JsonResponse({'status': "Pomyślnie wysłano wiadomość"})
    else:
        return redirect("/")
