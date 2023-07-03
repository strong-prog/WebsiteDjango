from django.db.models import Sum
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from .models import Item, Orders, Discount, Tax
import stripe

stripe.api_key = 'sk_test_51LiKCJDZaCFpukFPDA2l5UuRlzOKwX4u1TGA162MHolIIr8TwYtFTHT2JsxmeSHr0rRYQHYz3pFsWqOYpr1f6ZK500ETGcrt1G'


def calculate_price(price, discount, tax_percen):
    """Расчёт цены с учетом скидки и налога."""
    price_with_discount = int(price) - int(price) * int(discount) / 100
    tax = price_with_discount * int(tax_percen) / 100
    return price_with_discount + tax


def get_session(params):
    """Создание сессии на платежном сервисе."""
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': params['name'],
                    'description': params['description'],
                },
                'unit_amount': int(params['price']),
            },
            'quantity': params['quantity'],
        }],
        mode='payment',
        success_url='http://sportnote.ru/',
        cancel_url='http://sportnote.ru/',
    )
    return {
        'session': session,
    }


def item(request, item_id):
    """View страницы отдельного товара."""
    item = Item.objects.filter(id=int(item_id)).first()
    order = Orders.objects.filter(user_id=1).first()
    taxs = Tax.objects.filter(user_id=1).first()
    tax = taxs.tax
    discount = order.discount.discount if order else None
    price = item.price
    price_discount_tax = calculate_price(price, discount, tax)
    return render(
        request,
        'item.html',
        {'item': item,
         'discount': discount,
         'tax': tax,
         'price_discount_tax': price_discount_tax,
         },
    )


def items(request):
    """View списка товаров и корзины."""
    items = Item.objects.all().order_by('name')
    order = Orders.objects.filter(user_id=1).first()
    order_items = order.items.all() if order else []
    total = order.items.all().aggregate(price=Sum('price'))['price'] if order else None
    discount = order.discount.discount if order else None
    taxs = Tax.objects.filter(user_id=1).first()
    tax = taxs.tax
    if discount and total and tax:
        price_discount_tax = calculate_price(total, discount, tax)
    else:
        price_discount_tax = total

    context = {
        'items': items,
        'order_items': order_items,
        'order_items_ids': list(order_items.values_list('id', flat=True)) if order_items else [],
        'total': total,
        'discount': discount,
        'tax': tax,
        'price_discount_tax': price_discount_tax,
    }
    return render(
        request,
        'items.html',
        context,
    )


def buy_one(request, item_id):
    """Оплата одного товара без создания заказа (быстрая покупка)."""
    if request.method == 'POST':
        item = Item.objects.filter(id=int(item_id)).first()
        taxs = Tax.objects.filter(user_id=1).first()
        order = Orders.objects.filter(user_id=1).first()
        tax = taxs.tax
        price = int(item.price)

        if order.discount and order.discount.discount and tax:
            discount = order.discount.discount
            price_with_discount_tax = calculate_price(price, discount, tax)
        else:
            price_with_discount_tax = price
        session = get_session({
            'name': item.name,
            'description': item.description,
            'price': int(price_with_discount_tax) * 100,
            'quantity': 1,
        })
        resp = {
            'session': session,
        }
        return JsonResponse(resp)
    raise Http404


def add_to_basket(request):
    """Создание/обновление заказа."""

    # TODO В данной реализации рассчитано на то что у одного пользователя может быть только один заказ, доработать
    #  для хранения истории заказов, ввести статусы

    if request.method == 'POST':
        if request.POST.get('namerequest') == 'add_to_basket':
            ids = []
            for key in request.POST.keys():
                if key != 'namerequest':
                    ids.append(key.split('_')[-1])

            order = Orders.objects.filter(user_id=1).first()
            if not order:
                order = Orders(user_id=1)
                order.save()

            order.items.set(Item.objects.filter(id__in=ids))
            order.discount = Discount.objects.filter(user_id=1).order_by('-discount').first()
            order.save()

            return redirect('/')
        elif request.POST.get('namerequest') == 'remove_from_basket':
            pass

    raise Http404


def buy_many(request):
    """Оплата заказа."""
    if request.method == 'POST':
        order = Orders.objects.filter(user_id=1).first()
        taxs = Tax.objects.filter(user_id=1).first()

        if order:
            price = order.items.all().aggregate(price=Sum('price'))['price'] * 100
        else:
            raise Exception('Order не найден')

        if order.discount and order.discount.discount:
            discount = order.discount.discount
            tax = taxs.tax
            price_with_discount_tax = calculate_price(price, discount, tax)
        else:
            price_with_discount_tax = price

        params = {
            'name': 'Order %s' % order.id,
            'description': order.id,
            'quantity': 1,
            'price': price_with_discount_tax,
        }
        session = get_session(params)
        return redirect('/redirect-to-pay-form/?session=%s' % session.get('session').get('id'))

    raise Http404


def redirect_to_pay_form(request):
    """Служебная View для редиректа через js библиотеку stripe (по условиям задания)."""
    if request.GET.get('session'):
        return render(request, 'redirect_to_pay_form.html', {'session': request.GET.get('session')})
    raise Http404
