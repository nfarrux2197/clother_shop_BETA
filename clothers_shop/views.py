from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product


def home(request):
    categories = Category.objects.all()
    new_products = Product.objects.filter(is_new=True, is_available=True)[:8]
    popular_products = Product.objects.filter(is_available=True)[:8]
    context = {
        'categories': categories,
        'new_products': new_products,
        'popular_products': popular_products,
    }
    return render(request, 'clothers_shop/home.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_available=True)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'clothers_shop/category.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'clothers_shop/product.html', context)


def gender_section(request, gender):
    gender_names = {
        'women': 'Женщинам',
        'men': 'Мужчинам',
        'kids': 'Детям',
    }
    section_name = gender_names.get(gender, 'Все товары')
    categories = Category.objects.filter(gender=gender)
    products = Product.objects.filter(category__gender=gender, is_available=True)
    context = {
        'section_name': section_name,
        'categories': categories,
        'products': products,
        'gender': gender,
    }
    return render(request, 'clothers_shop/section.html', context)


def new_products(request):
    products = Product.objects.filter(is_new=True, is_available=True)
    context = {
        'section_name': 'Новинки',
        'products': products,
    }
    return render(request, 'clothers_shop/section.html', context)


def sale_products(request):
    products = Product.objects.filter(is_available=True, old_price__isnull=False)
    context = {
        'section_name': 'Скидки',
        'products': products,
    }
    return render(request, 'clothers_shop/section.html', context)

from django.contrib.auth.decorators import login_required
from .models import Category, Product, Cart, CartItem


@login_required
def cart(request):
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart_obj,
    }
    return render(request, 'clothers_shop/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product)

    if created:
        messages.success(request, f'"{product.name}" добавлен в корзину!')
    else:
        messages.error(request, f'"{product.name}" уже есть в корзине!')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Товар удалён из корзины!')
    return redirect('cart')