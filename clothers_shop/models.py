from multiprocessing.resource_sharer import DupSocket
from tabnanny import verbose
from django.db import models

class Category(models.Model):
    GENDER_CHOICES = [
        ('women', 'Женщинам'),
        ('men', 'Мужчинам'),
        ('kids', 'Детям'),
        ('all', 'Всем'),
    ]
    name = models.CharField(max_length=100, verbose_name='Назване')
    slug = models.SlugField(unique=True, verbose_name='URL')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='Изображениие')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='all', verbose_name='Раздел')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Старая цена')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    is_new = models.BooleanField(default=False, verbose_name='Новинка')
    is_available = models.BooleanField(default=True, verbose_name='Доступно')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            discount = (self.old_price - self.price) / self.old_price * 100
            return int(discount)
        return None

from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина {self.user.username}'

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'{self.product.name} x{self.quantity}'

    def total_price(self):
        return self.product.price * self.quantity