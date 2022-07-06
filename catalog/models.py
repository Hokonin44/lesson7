from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def price_som(self):
        return self.price * 82

    @property
    def tag_list_2(self):
        return [i.name for i in self.tags.all()]
    @property
    def rating(self):
        reviews = self.reviews.all()  # [4]
        if not reviews:
            return 0
        average = 0
        for i in reviews:
            average += i.stars
        return average / reviews.count()  # 4/1



STAR_CHOICES = (
    (1, '*'),
    (2, '* *'),
    (3, '* * *'),
    (4, '* * * *'),
    (5, '* * * * *'),
)


class Review(models.Model):
    author = models.CharField(max_length=100, default='', blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')
    stars = models.IntegerField(default=1, choices=STAR_CHOICES)

    def __str__(self):
        return self.text
