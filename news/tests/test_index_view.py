from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from news.models import Topic, Newspaper

INDEX_URL = reverse("news:index")


class IndexViewTests(TestCase):
    def setUp(self):
        """Set up common test data."""
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            first_name="Test",
            last_name="User",
            years_of_experience=5
        )
        self.client.force_login(self.user)

        self.topic = Topic.objects.create(
            name="Test Topic",
        )

        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Test Content",
            topic=self.topic,
        )
        self.newspaper.publishers.add(self.user)

    def test_index_view_status_code(self):
        """Test that the index view returns a 200 status code for logged-in users."""
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        """Test that the index view uses the correct template."""
        response = self.client.get(INDEX_URL)
        self.assertTemplateUsed(response, "news/index.html")

    def test_index_view_context(self):
        """Test that the index view provides the correct context data."""
        # Create additional data to test counts
        Topic.objects.create(name="Another Topic")
        Newspaper.objects.create(
            title="Another Newspaper",
            content="Another Content",
            topic=self.topic,
        )
        get_user_model().objects.create_user(
            username="another_user",
            password="test_password",
            years_of_experience=3
        )

        response = self.client.get(INDEX_URL)

        # Check that the context contains the correct counts
        self.assertEqual(response.context["num_redactors"], 2)
        self.assertEqual(response.context["num_newspapers"], 2)
        self.assertEqual(response.context["num_topics"], 2)

        # Check that num_visits is in the context and increments
        self.assertEqual(response.context["num_visits"], 1)

        # Make another request to check that num_visits increment
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.context["num_visits"], 2)

    def test_index_view_not_logged_in(self):
        """Test that the index view redirects for non-logged-in users."""
        # Log out the user
        self.client.logout()

        response = self.client.get(INDEX_URL)

        # Should redirect to the login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))
