from django.db import models

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # This is the foreign key to Category
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,      # allow NULL values for existing products
        blank=True      # allow empty in forms
    )

    def __str__(self):
        return self.name
