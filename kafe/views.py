from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from users.models import *
from .forms import OrderForm, RateForm, CartItemForm
from django.db.models import Q

@login_required(login_url='users/sign_in')
def home(request):
    return render(request, 'home.html')


@login_required(login_url='http://127.0.0.1:8000/')
def helper(request):
    return render(request, 'helper.html')

@login_required(login_url='http://127.0.0.1:8000/')
def info_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    }

    return render(request, 'info_order.html', context)


@login_required(login_url='http://127.0.0.1:8000/')
def foods_list(request):
    category = request.GET.get('category')
    slides = Slide.objects.all()
    foods = Food.objects.all()
    for food in foods:
        food.comment_count = food.comment_count()
    search = request.GET.get('search')
    foods = foods.filter(Q(title__icontains=search) |
                           Q(description__icontains=search)) if search else foods
    foods = foods.filter(category=category) if category else foods
    food_id = request.GET.get('food')
    if food_id:
        food = get_object_or_404(Food, pk=food_id)
        cart_item = CartItem.objects.filter(food=food, customer=request.user)
        if not cart_item:
            CartItem.objects.create(customer=request.user, food=food, quantity=1)
            return redirect('kafe:foods')
        for item in cart_item:
            item.quantity += 1
            item.save()
    return render(request, 'foods.html', {
        'foods': foods,
        'slides': slides,
    })

@login_required(login_url='http://127.0.0.1:8000/')
def discounted_foods(request):
    discounted_foods = Food.objects.filter(is_discounted=True)
    return render(request, 'foods_discounted.html', {'foods': discounted_foods})

@login_required(login_url='http://127.0.0.1:8000/')
def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    cart_item_forms = []
    for cart_item in cart_items:
        form = CartItemForm(initial={'quantity': cart_item.quantity})
        cart_item_forms.append((cart_item, form))

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'cart_item_forms': cart_item_forms,
    })


@login_required(login_url='http://127.0.0.1:8000/')
def delete_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk).delete()
    return redirect('kafe:cart')


@login_required(login_url='http://127.0.0.1:8000/')
def edit_cart_item(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    action = request.GET.get('action')

    if action == 'clear':
        cart_item.delete()
        return redirect('kafe:cart')

    if action == 'take' and cart_item.quantity > 0:
        if cart_item.quantity == 1:
            cart_item.delete()
            return redirect('kafe:cart')
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('kafe:cart')
    cart_item.quantity += 1
    cart_item.save()
    return redirect('kafe:cart')


@login_required(login_url='users/sign_in')
def food_detail(request, pk):
    food = get_object_or_404(Food, pk=pk)
    discounted_foods = Food.objects.filter(is_discounted=True)
    reviews = Review.objects.filter(food=food)
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Проверяем, заказывал ли пользователь данный продукт
    has_ordered = OrderFood.objects.filter(order__customer=request.user, food=food).exists()
    context = {
        'food': food,
        'reviews': reviews,
        'form': RateForm(request.POST or None),
        'discounted_foods': discounted_foods,
        'profile_pic': profile.profile_pic if profile else None,
        'has_ordered': has_ordered 
    }

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.food = food
            instance.save()
            return redirect('kafe:food_detail', pk=food.pk)

    return render(request, 'food_detail.html', context)

@login_required(login_url='http://127.0.0.1:8000/')
def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.total_price = total_price
            order.save()

            for cart_item in cart_items:
                OrderFood.objects.create(
                    order=order,
                    food=cart_item.food,
                    amount=cart_item.quantity,
                    total=cart_item.total_price()
                )
            cart_items.delete()
            return redirect('kafe:cart')
    else:
        form = OrderForm()

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
        'form': form
    }

    return render(request, 'order_creation_page.html', context)

@login_required(login_url='http://127.0.0.1:8000/')
def info_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    }

    return render(request, 'info_order.html', context)


@login_required(login_url='http://127.0.0.1:8000/')
def orders(request):
    orders_list = Order.objects.filter(customer=request.user)
    return render(request, 'orders.html', {
        'orders': orders_list
    })