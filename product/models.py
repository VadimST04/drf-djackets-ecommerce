from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:  # options for the model
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Product(models.Model):
    objects = None
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='upload/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='upload/', blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

    class Meta:  # options for the model
        ordering = ('-date_added',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        print(f'absolute_url = /{self.category.slug}/{self.slug}/')
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            print(f'image = http://127.0.0.1:8000 + {self.image.url}')
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            print(f'thumbnail = http://127.0.0.1:8000 + {self.thumbnail.url}')
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                print(f'thumbnail = http://127.0.0.1:8000 + {self.thumbnail.url}')
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(100, 100)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
