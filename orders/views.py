from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
import json
from .process import html_to_pdf
from accounts.models import UserProfile
from django.http import HttpResponse
from django.contrib import messages

from cart.models import CartItem
from .models import Order, Payment, OrderProduct, PromoCode
from .forms import OrderForm
import datetime
from django.conf import settings
from django.http import JsonResponse
from store.models import Product
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.urls import reverse
from coupons.validations import validate_coupon
from coupons.models import Coupon

def paymentview(request, id):
    current_user = request.user
    order = Order.objects.get(user=current_user, id=id)
    cart_items = CartItem.objects.filter(user=current_user)
    try:
        body = json.loads(request.body)
        payment = Payment(
            user=current_user,
            payment_id=body['referenceid'],
            amount_paid=body['amount'],
            status="completed",
            payment_method="Remita",
            created_at=datetime.datetime.now()

        )
        payment.save()
        order.is_ordered = True
        order.payment = payment
        order.save()
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user = request.user
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()
        #     # reduce quantity of sold products
        #
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
        # send order recived email
        current_site = get_current_site(request)
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': current_user,
            'order': order
        })
        to_email = current_user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        # clear cart
        CartItem.objects.filter(user=current_user).delete()

    except:
        payment = Payment()
        if request.method == 'POST':
            reference = request.POST.get('referenceid', False)
            amount = request.POST.get('amount', False)
            status = request.POST.get('status', "Pending")
            payment.user = current_user
            payment.payment_id = reference
            payment.amount_paid = amount
            payment.status = status
            payment.payment_method = "Paystack"
            payment.created_at = datetime.datetime.now()
            payment.save()

            order.is_ordered = True
            order.payment = payment
            order.save()
            # move cart items to order product table

            for item in cart_items:
                orderproduct = OrderProduct()
                orderproduct.order_id = order.id
                orderproduct.payment = payment
                orderproduct.user = request.user
                orderproduct.product_id = item.product_id
                orderproduct.quantity = item.quantity
                orderproduct.product_price = item.product.price
                orderproduct.ordered = True
                orderproduct.save()

                cart_item = CartItem.objects.get(id=item.id)
                product_variation = cart_item.variations.all()
                orderproduct = OrderProduct.objects.get(id=orderproduct.id)
                orderproduct.variations.set(product_variation)
                orderproduct.save()
        #
        #     # reduce quantity of sold products
        #
                product = Product.objects.get(id=item.product_id)
                product.stock -= item.quantity
                product.save()
        #     # send order recived email
            current_site = get_current_site(request)
            mail_subject = 'Thank you for your order!'
            message = render_to_string('orders/order_received_email.html', {
                'user': current_user,
                'order': order
            })
            to_email = current_user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
        # clear cart
        CartItem.objects.filter(user=current_user).delete()

        # send order number and transaction id back to user in thank u page
    try:
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        context = {
            'user': current_user,
            'order_id': order.id,
            'order_date': order.created_at,
            'ordered_products': ordered_products,
            'order': order
        }
        return render(request, 'orders/paymentverify.html', context)
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


def GeneratePdf(request, order_id):
    order = Order.objects.get(user=request.user, id=order_id)
    ordered_products = OrderProduct.objects.filter(order_id=order.id)
    context = {
        'user': request.user,
        'order_id': order.id,
        'order_date': order.created_at,
        'ordered_products': ordered_products,
        'order': order
    }
    open('templates/temp.html', "w+").write(render_to_string('orders/reciept.html', context))

    # Converting the HTML template into a PDF file
    pdf = html_to_pdf('temp.html')

    # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')


def placeorderview(request,  total=0, quantity=0):
    current_user = request.user
    profile = UserProfile.objects.get(user=current_user)
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total = 0
    shipping_fee = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    shipping_fee = (2 * total) / 100
    grand_total = total + shipping_fee
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone_number = form.cleaned_data['phone_number']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.shipping_address_same_as_billing = form.cleaned_data['shipping_address_same_as_billing']
            data.shipping_address = form.cleaned_data['shipping_address']
            data.shipping_state = form.cleaned_data['shipping_state']
            data.shipping_city = form.cleaned_data['shipping_city']
            data.shipping_country = form.cleaned_data['shipping_country']
            data.shipping_fee = shipping_fee
            data.order_total = grand_total
            data.total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            profile.address_line_1 = form.cleaned_data['address_line_1']
            profile.address_line_2 = form.cleaned_data['address_line_2']
            profile.state = form.cleaned_data['state']
            profile.city = form.cleaned_data['city']
            profile.country = form.cleaned_data['country']
            profile.shipping_address = form.cleaned_data['shipping_address']
            profile.shipping_state = form.cleaned_data['shipping_state']
            profile.shipping_city = form.cleaned_data['shipping_city']
            profile.shipping_country = form.cleaned_data['shipping_country']
            profile.save()

            # generate order number whth date and order id
            # yr = int(datetime.date.today().strftime('%Y'))
            # dt = int(datetime.date.today().strftime('%d'))
            # mt = int(datetime.date.today().strftime('%m'))
            # d = datetime.date(yr,mt,dt)
            #
            # current_date = d.strftime("%Y%m%d")
            #
            order_number = data.id
            data.order_number = data.id
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            paystack_pubkey = settings.PAYSTACK_PUBLIC_KEY
            stripe_pubkey = settings.STRIPE_PUBLISHABLE_KEY
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'shipping_fee': shipping_fee,
                'grand_total': data.total,
                'pk_key': paystack_pubkey,
                'stripe_pubkey': stripe_pubkey,
            }
            return render(request, 'orders/payments.html', context)

    else:
        return redirect('checkout')

from coupons.models import Coupon, CouponUser

def apply_coupon(request, id):
    user = UserProfile.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(user=request.user)
    order = Order.objects.get(user=request.user, is_ordered=False, id=id)
    paystack_pubkey = settings.PAYSTACK_PUBLIC_KEY
    stripe_pubkey = settings.STRIPE_PUBLISHABLE_KEY

    total = 0
    quantity = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    if request.method == 'POST':
        coupon_code = request.POST['coupon']
        print(coupon_code)
        status = validate_coupon(coupon_code=coupon_code, user=request.user)
        if status['valid']:
            coupon_code = Coupon.objects.get(code=coupon_code)
            coupon_code.use_coupon(user=request.user)
            order.coupon = request.POST['coupon']
            order.order_total = coupon_code.get_discounted_value(order.order_total)
            order.save()
            coupon_code.save()
            messages.success(request, 'You have successfully applied a coupon on your order')
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'pk_key': paystack_pubkey,
                'stripe_pubkey': stripe_pubkey,
            }
            return render(request, 'orders/coupon_applied.html', context)
        else:
            messages.error(request, f'{status['message']}')
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'pk_key': paystack_pubkey,
                'stripe_pubkey': stripe_pubkey,
            }
            return render(request, 'orders/coupon_applied.html', context)
    else:

        context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'pk_key': paystack_pubkey,
            'stripe_pubkey': stripe_pubkey,
        }
        return render(request, 'orders/coupon_applied.html', context)