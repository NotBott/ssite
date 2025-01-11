from django.db import models

from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название', unique=True)
    full_description = models.TextField(verbose_name='Полное описание')
    preview = models.ImageField(upload_to='product/images/', verbose_name='Фото')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.PositiveSmallIntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар',
        default=1
    )
    image = models.ImageField(
        upload_to='product/images/',
        null=True,
        blank=True,
        verbose_name='Фото'
    )

    def __str__(self):
        return f"Фото для {self.product.name}"

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'


class Favorites(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return f'Пользователь {self.user.id} | Продукт: {self.product.name}'

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f'Пользователь {self.user.id} | Продукт: {self.product.name}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def sum(self):
        return self.product.price * self.quantity


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    recall = models.PositiveSmallIntegerField(default=0, verbose_name='Отзыв')

    def __str__(self):
        return f'Пост-{self.product}: {self.author}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class UserVisit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    visit_count = models.PositiveIntegerField(default=0, verbose_name='Количество посещений')

    def __str__(self):
        return f'Пользователь {self.user.id} | Категория: {self.category.name}'

    class Meta:
        verbose_name = 'Посещение пользователя'
        verbose_name_plural = 'Посещение пользователей'
