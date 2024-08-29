from django.db import models
from django.utils.text import slugify

# Create your models here.


class ProductManager(models.Manager):
    def with_images(self):
        return self.prefetch_related('images')

class Product(models.Model):
    title=models.CharField(max_length=255,null=True,unique=True)
    description=models.TextField(null=True)
    price=models.DecimalField(null=True,max_digits=10,decimal_places=2)
    slug=models.SlugField(max_length=255,unique=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title
    
    objects=models.Manager()
    objects_with_images=ProductManager()
    

    
class ProductImages(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image1=models.ImageField(upload_to='Product Images/',blank=True,null=True)
    image2=models.ImageField(upload_to='Product Images/',blank=True,null=True)
    image3=models.ImageField(upload_to='Product Images/',blank=True,null=True)

    def __str__(self):
        return self.product.title



