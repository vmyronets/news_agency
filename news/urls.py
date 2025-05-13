from django.urls import path
from .views import index


urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topics"),
]

app_name = "news"