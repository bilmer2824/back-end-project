from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name="Kategoriya nomi")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"



class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name="Nomi")
    content = models.TextField(blank=True, verbose_name="Matni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'yilgan vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqti")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name="Rasmi")
    is_published = models.BooleanField(default=True, verbose_name="Saytga chiqarish")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    author = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    view = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_details', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Maqolalar"
        ordering = ['-created_at']




class User(AbstractUser):
    photo = models.ImageField(upload_to='user/', blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    telegram = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    github = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username



class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text