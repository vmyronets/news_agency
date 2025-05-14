from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        verbose_name = "topic"
        verbose_name_plural = "topics"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Newspaper(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    published_date = models.DateTimeField(auto_now_add=True)
    topics = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name="newspapers")
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="newspapers"
    )

    class Meta:
        verbose_name = "newspaper"
        verbose_name_plural = "newspapers"
        ordering = ["-published_date"]

    def __str__(self):
        return self.title
