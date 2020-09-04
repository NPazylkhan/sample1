from django.db import models
# import uuid
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError

# example for create Relation OneToOne
class AdvUser(models.Model):
    is_activated = models.BooleanField(default = True)
    user = models.OneToOneField(User, on_delete = models.CASCADE)

# example for create Relation ManyToMany
class Sp(models.Model):
    name = models.CharField(max_length=20)

class Machine(models.Model):
    name = models.CharField(max_length=20)
    spares = models.ManyToManyField(Sp)
    
def validate_even(val):
        if val % 2 != 0:
            raise ValidationError('Value %{value}s does not even!', code='odd', params={'value':val})

class Bb(models.Model):
    Kinds = (
        (None,'Choose advertise'),
        ('buy','Buy'),
        ('sell','Sell'),
        ('change','Change'),
    )
    # id = models.UUIDField(primary_key = True, default=uuid.uuid4,editable=False)
    title = models.CharField(max_length=50, verbose_name = 'Goods')
    content = models.TextField(null=True, blank=True, verbose_name = 'Describe')
    price = models.FloatField(null=True, blank=True, verbose_name = "Price", validators = [validate_even])
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name = "PublishedDate")
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Rubric',related_name='entries')
    kind = models.CharField(max_length=10, choices = Kinds,verbose_name='Some Kind of Choises')
        
    class Meta:
        # order_with_respect_to = 'rubric'
        verbose_name_plural = 'Publication'
        verbose_name = 'Publication'
        ordering = ['-published']
    
    def title_and_price(self):
        if self.price:
            return '%s (%.3f)' % (self.title, self.price)
        else:
            return self.title
    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Where is Content')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Write the plus type digit')
        if errors:
            raise ValidationError(errors)

    title_and_price.short_description = "Title and price"

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name = 'Title')
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Rubrics'
        verbose_name = 'Rubric'
        ordering = ['name']

class MinMaxValueValidation:
    def __init__(self,min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, val):
        if val < self.min_value or val > self.max_value:
            raise ValidationError('Value should be in range %(min)s to %(max)s ', code='out_of_range', params={'min':self.min_value,'max':self.max_value})