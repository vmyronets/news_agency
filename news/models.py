from django.db import models


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Topics"
        ordering = ["name"]

    def __str__(self):
        return self.name


