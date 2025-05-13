from django.urls import path
from news.views import(
    index,
    TopicListView,
    TopicDetailView,

)


urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topics/create/", TopicCreatelView.as_view(), name="topic-create"),
]

app_name = "news"