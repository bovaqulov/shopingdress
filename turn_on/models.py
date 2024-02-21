from django.db import models


class Category(models.Model):
    """
    category for products
    """
    title = models.CharField(max_length=100, verbose_name="Kategoriya nomi")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


class Product(models.Model):
    """
    Products class
    """
    title = models.CharField(max_length=100, verbose_name="Maxsulot nomi")
    price = models.IntegerField(verbose_name="Maxsulot narxi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="Kategoriya")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Maxsulot"
        verbose_name_plural = "Maxsulotlar"


class Gallery(models.Model):
    """
    Image for products
    """
    image = models.ImageField(upload_to="product/", verbose_name="Maxsulot rasmlari")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = "Rasm"
        verbose_name_plural = "Rasmlar"


class UserTelegram(models.Model):
    user_id = models.CharField(max_length=20, unique=True, verbose_name="Foydalanuvchi idisi")
    username = models.CharField(max_length=250, blank=True, null=True, verbose_name="Foydalanuvchi nomi")
    name = models.TextField(verbose_name="Foydalanuvchi ismi")
    phone_number = models.TextField(verbose_name="foydalanuvchi raqami")

    def __str__(self):
        return self.phone_number


class Order(models.Model):
    customer = models.ForeignKey(UserTelegram, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"

    @property
    def total_price(self):
        order_product = self.orderproduct_set.all()
        total_prices = sum([product.get_total_price for product in order_product])
        return total_prices

    @property
    def total_quantity(self):
        order_product = self.orderproduct_set.all()
        total_quantities = sum([product.quantity for product in order_product])
        return total_quantities


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Buyurtma bo'yicha mahsulot"
        verbose_name_plural = "Buyurtma bo'yicha mahsulotlar"

    def __str__(self):
        return self.added_at

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(UserTelegram, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250, verbose_name="Manzil")
    city = models.CharField(max_length=250, verbose_name="Shahar")
    region = models.CharField(max_length=200, verbose_name="Tuman")
    village = models.CharField(max_length=200, verbose_name="Mahalla")
    state = models.CharField(max_length=200, verbose_name="Ko'cha")
    home_number = models.IntegerField( verbose_name="uy raqami")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Yetkazib berish manzili"
        verbose_name_plural = "Yetkazib berish manzillari"

    def __str__(self):
        return self.created_at