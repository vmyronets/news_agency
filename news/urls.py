from django.urls import path
from news.views import(
    index,
    TopicListView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView,
    NewspaperListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("topics/create/", TopicCreateView.as_view(), name="topic-create"),
    path(
        "topics/<int:pk>/update/",
        TopicUpdateView.as_view(),
        name="topic-update"
    ),
    path(
        "topics/<int:pk>/delete/",
        TopicDeleteView.as_view(),
        name="topic-delete"
    ),
    path("newspapers/", NewspapersListView.as_view(), name="newspapers-list"),
    path(
        "newspapers/<int:pk>/",
        NewspapersDetail.as_view(),
        name="newspapers-detail"
    ),
]

app_name = "news"