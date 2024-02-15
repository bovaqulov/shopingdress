from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, null=True, blank=True, verbose_name='Kategoriya')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Rasm')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='subcategory',
                               verbose_name='Kategoriya')

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Kategoriya: pk={self.pk}, title={self.title}"

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class TeleUser(models.Model):
    telegram_id = models.CharField(max_length=20, verbose_name="telegram id")
    username = models.CharField(max_length=20, verbose_name="username")
    name = models.TextField(verbose_name="ismi")
    phone_number = models.CharField(max_length=15, verbose_name="telefon raqam")
    address = models.TextField(verbose_name="Manzil")
    birthday = models.CharField(max_length=30, verbose_name="tug'ulgan kun")


class Product(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Maxsulot', null=True, blank=True)
    price = models.FloatField(verbose_name='Narxi')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoriya', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30, verbose_name='Razmerlar')

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all()[0].image.url
            except:
                return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5igFUHiY5DMEZEKlymdVHp4r3MA9Pj7mEI6uKW_iT6A&s'
        return 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5igFUHiY5DMEZEKlymdVHp4r3MA9Pj7mEI6uKW_iT6A&s'

    class Meta:
        verbose_name = 'Maxsulot'
        verbose_name_plural = 'Maxsulotlar'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Rasmlar')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Rasm'
        verbose_name_plural = 'Rasmlar'


class FavouriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')

    def __str__(self):
        return f"{self.username} - {self.product.title}"

    class Meta:
        verbose_name = 'Избранный товар'
        verbose_name_plural = 'Избранные товары'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=250)
    email = models.EmailField()

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @property
    def get_cart_total_price(self):
        order_product = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_product])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_product = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_product])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250, verbose_name='Адрес')
    city = models.CharField(max_length=250, verbose_name='Город')
    state = models.CharField(max_length=250, verbose_name='Штаты')
    zipcode = models.CharField(max_length=250, verbose_name='Индексный номер')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'
