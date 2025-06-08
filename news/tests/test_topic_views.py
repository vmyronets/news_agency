from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from news.models import Topic
from news.forms import TopicSearchForm

TOPIC_URL = reverse("news:topic-list")


class PublicTopicViewsTest(TestCase):
    def test_access_not_logged_in_users(self) -> None:
        """Test that the topic list view returns an unsuccessful status code."""
        response = self.client.get(TOPIC_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTopicViewsTest(TestCase):
    def setUp(self) -> None:
        """Set up common test data."""
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(name="test_topic")

    def test_topic_list_view(self) -> None:
        """
        Tests the topic list view by performing a GET request to the topic URL,
        verifying the status code, response context, template used, and
        ensuring the expected types and data are present in the response.
        """
        response = self.client.get(TOPIC_URL)
        topics = Topic.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual = list(response.context["topic_list"]), list(topics)
        self.assertTemplateUsed(response, "news/topic_list.html")
        self.assertIsInstance(response.context["search_topic"], TopicSearchForm)

    def test_topic_search(self) -> None:
        """
        Tests the behavior of the topic search functionality to ensure that it
        returns the correct topics based on the provided query parameter. This
        test verifies the search capability for different cases, including
        exact matches and cases with an empty query string.
        """
        topic = Topic.objects.create(name="different_topic")

        url = f"{TOPIC_URL}?name=test_topic"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 1)
        self.assertEqual(response.context["topic_list"][0], self.topic)

        url = f"{TOPIC_URL}?name=different"
        response = self.client.get(url)

        self.assertEqual(len(response.context["topic_list"]), 1)
        self.assertEqual(response.context["topic_list"][0], topic)

        url = f"{TOPIC_URL}?name="
        response = self.client.get(url)

        self.assertEqual(len(response.context["topic_list"]), 2)

    def test_topic_create_view_get(self) -> None:
        """
        Tests the ability of the `topic-create` view to handle HTTP GET
        requests successfully. Ensures that the view responds with the correct
        status code and renders the expected template when accessed.
        """
        url = reverse("news:topic-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/topic_form.html")

    def test_topic_create_view_post(self) -> None:
        """
        Tests the topic creation functionality using POST request to verify
        that a new topic is successfully created and a redirection occurs.
        """
        url = reverse("news:topic-create")
        data = {"name": "New Topic"}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Topic.objects.filter(name="New Topic").exists())

    def test_topic_update_view_get(self) -> None:
        """
        Tests the GET request handling for the "topic-update" view. Ensures
        that the correct status code and template are used when accessing the
        topic update page.
        """
        url = reverse("news:topic-update", args=[self.topic.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/topic_form.html")

    def test_topic_update_view_post(self) -> None:
        """
        Tests the HTTP POST method handling for the topic update view.

        This test verifies that submitting a valid update request for an
        existing topic successfully updates the topic's data and redirects the
        user to the appropriate page. The test ensures the database is updated
        with the new values provided in the request payload.
        """
        url = reverse("news:topic-update", args=[self.topic.id])
        data = {"name": "Updated Topic"}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.topic.refresh_from_db()
        self.assertEqual(self.topic.name, "Updated Topic")

    def test_topic_delete_view_get(self) -> None:
        """
        Tests the GET request for the topic delete view.

        This method verifies the behavior of the topic delete view by sending
        a GET request to the specified URL for deleting a topic and checks
        the response status code and the template used.
        """
        url = reverse("news:topic-delete", args=[self.topic.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/topic_confirm_delete.html")

    def test_topic_delete_view_post(self) -> None:
        """
        Handles testing the POST request to the topic delete view. This test
         ensures that a topic is properly deleted upon a successful POST
         request to the appropriate URL endpoint.
        """
        url = reverse("news:topic-delete", args=[self.topic.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Topic.objects.filter(id=self.topic.id).exists())
