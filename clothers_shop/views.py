from hmac import new
from django.shortcuts import render, get_object_or_404
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
    products = category.objects.filter(category=category, is_available=True)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'clothers_shop/category_detail.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    context = {
        'product': product,
    }
    return render(request, 'clothers_shop/product_detail.html', context)
