from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save, post_save
from datetime import datetime

class EntryCount(models.Model):
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['year', 'month']

class Category(models.Model):
    patternName = models.CharField(max_length=30, unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.patternName

class Website(models.Model):
    category = models.ManyToManyField(Category)
    baseURL = models.CharField(max_length=100, unique=True)
    webName = models.CharField(max_length=30)
    lastFlagAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-lastFlagAt"]

    def __str__(self) -> str:
        return self.webName

    def contains(self):
        return ','.join([str(c) for c in self.category.all()])

    @classmethod
    def create_or_update_website(cls, baseURL, webName, category_names):
        category_ids = Category.objects.filter(patternName__in=category_names).values_list('id', flat=True)
        existing_website = cls.objects.filter(baseURL=baseURL).first()

        if existing_website:
            existing_website.webName = webName.title()
            for category_id in category_ids:
                if category_id not in existing_website.category.values_list('id', flat=True):
                    existing_website.category.add(category_id)
                    category = Category.objects.get(id=category_id)
                    category.count += 1
                    category.save()
            existing_website.save()

            return existing_website
        else:
            new_website = cls.objects.create(baseURL=baseURL, webName=webName.title())
            for category_id in category_ids:
                new_website.category.add(category_id)
                category = Category.objects.get(id=category_id)
                category.count += 1
                category.save()

            return new_website
    def delete(self, *args, **kwargs):
        for category in self.category.all():
            category.count -= 1
            category.save()

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        created_at = self.lastFlagAt
        year, month = created_at.year, created_at.month

        entry_count, created = EntryCount.objects.get_or_create(year=year, month=month)
        entry_count.count += 1
        entry_count.save()

class websiteFlagCount(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ['website', 'year', 'month']

class validationWithTime(models.Model):
    baseUrl = models.CharField(max_length = 100)
    prod_name = models.CharField(max_length = 200)
    shown_time = models.BigIntegerField()
    init_time = models.DateTimeField(auto_now = True)
    class Meta:
        unique_together = ['baseUrl', 'prod_name']

class validationForLowStock(models.Model):
    baseUrl = models.CharField(max_length = 100)
    prod_name = models.CharField(max_length = 200)
    quantity = models.IntegerField()

    class Meta:
        unique_together = ['baseUrl', 'prod_name']

class validationForActivityNotification(models.Model):
    baseUrl = models.CharField(max_length = 100)
    prod_name = models.CharField(max_length = 200)
    msg = models.CharField(max_length = 100)
    timestamp = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ['baseUrl', 'prod_name', 'msg']
    


@receiver(post_save, sender=Website)
def update_website_visit_count(sender, instance, **kwargs):
    last_flag_at = datetime.now()
    year, month = last_flag_at.year, last_flag_at.month

    website_visit_count, created = websiteFlagCount.objects.get_or_create(
        website=instance,
        year=year,
        month=month
    )
    website_visit_count.count += 1
    website_visit_count.save()

@receiver(pre_delete, sender=Website)
def decrement_category_count(sender, instance, **kwargs):
    for category in instance.category.all():
        category.count -= 1
        category.save()

