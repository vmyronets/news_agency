from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from news.models import Newspaper, Topic
from news.forms import NewspaperForm, NewspaperSearchForm

NEWSPAPER_LIST_URL = reverse("news:newspaper-list")


class PublicNewspaperViewsTests(TestCase):
    def test_access_not_logged_in_users(self):
        """Test that login is required for accessing newspaper views."""
        urls = [
            NEWSPAPER_LIST_URL,
            reverse("news:newspaper-detail", args=[1]),
            reverse("news:newspaper-create"),
            reverse("news:newspaper-update", args=[1]),
            reverse("news:newspaper-delete", args=[1]),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateNewspaperViewsTests(TestCase):
    def setUp(self) -> None:
        """Set up common test data."""
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            first_name="Test",
            last_name="User",
            years_of_experience=5,
        )
        self.client.force_login(self.user)

        self.topic = Topic.objects.create(name="Test Topic")

        self.newspaper = Newspaper.objects.create(
            title="Test Newspaper", content="Test Content", topic=self.topic
        )
        self.newspaper.publishers.add(self.user)

    def test_newspaper_list_view(self):
        """
        Test the retrieval of the newspaper list view and verify
        its rendered content.

        This function tests the HTTP GET request to the newspaper list URL.
        It compares the retrieved list of newspapers from the context with the
        expected newspaper objects from the database. Additionally, it ensures
        that the correct template has been used to render the view.
        """
        response = self.client.get(NEWSPAPER_LIST_URL)
        newspapers = Newspaper.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["newspaper_list"]), list(newspapers))
        self.assertTemplateUsed(response, "news/newspaper_list.html")

    def test_newspaper_detail_view(self):
        """
        Tests the functionality of the newspaper detail view in the application.
        This includes ensuring the correct HTTP response status code, proper
        context data being passed to the template, and verifying that the
        correct template is used for rendering.
        """
        url = reverse("news:newspaper-detail", args=[self.newspaper.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["newspaper"], self.newspaper)
        self.assertTemplateUsed(response, "news/newspaper_detail.html")

    def test_newspaper_create_view_get(self):
        """
        Tests the GET request to the newspaper creation view.

        This method sends a GET request to the URL associated with
        the "news:newspaper-create" view, then verifies that the
        response status code is as expected, the correct form is
        included in the context, and the proper template is used to
        render the response.
        """
        url = reverse("news:newspaper-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], NewspaperForm)
        self.assertTemplateUsed(response, "news/newspaper_form.html")

    def test_newspaper_create_view_post(self):
        """
        Tests the POST request functionality for creating a new newspaper
        through the newspaper create view. Ensures the newspaper is successfully
        created with the provided data and a redirection occurs with the
        expected status code.
        """
        url = reverse("news:newspaper-create")
        data = {
            "title": "New Test Newspaper",
            "content": "New Test Content",
            "topic": self.topic.id,
            "publishers": [self.user.id],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Newspaper.objects.filter(title="New Test Newspaper").exists())

    def test_newspaper_update_view_get(self):
        """
        Tests the GET request to the newspaper update view.

        This method sends a GET request to the URL associated with
        the "news:newspaper-update" view, then verifies that the
        response status code is as expected, the correct form is
        included in the context with the correct initial data, and
        the proper template is used to render the response.
        """
        url = reverse("news:newspaper-update", args=[self.newspaper.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], NewspaperForm)
        self.assertEqual(response.context["form"].instance, self.newspaper)
        self.assertTemplateUsed(response, "news/newspaper_form.html")

    def test_newspaper_update_view_post(self):
        """
        Tests the POST request functionality for updating an existing newspaper
        through the newspaper update view. Ensures the newspaper is successfully
        updated with the provided data and a redirection occurs with the
        expected status code.
        """
        url = reverse("news:newspaper-update", args=[self.newspaper.id])
        data = {
            "title": "Updated Test Newspaper",
            "content": "Updated Test Content",
            "topic": self.topic.id,
            "publishers": [self.user.id],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.newspaper.refresh_from_db()
        self.assertEqual(self.newspaper.title, "Updated Test Newspaper")
        self.assertEqual(self.newspaper.content, "Updated Test Content")

    def test_newspaper_delete_view_get(self):
        """
        Tests the GET request to the newspaper delete view.

        This method sends a GET request to the URL associated with
        the "news:newspaper-delete" view, then verifies that the
        response status code is as expected and the proper template
        is used to render the response.
        """
        url = reverse("news:newspaper-delete", args=[self.newspaper.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/newspaper_confirm_delete.html")

    def test_newspaper_delete_view_post(self):
        """
        Tests the POST request functionality for deleting an existing newspaper
        through the newspaper delete view. Ensures the newspaper is successfully
        deleted and a redirection occurs with the expected status code.
        """
        url = reverse("news:newspaper-delete", args=[self.newspaper.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Newspaper.objects.filter(id=self.newspaper.id).exists())

    def test_newspaper_search(self):
        """
        Tests the search functionality in the newspaper list view.

        This method creates multiple newspapers, then tests that the search
        form correctly filters the newspapers based on the search term.
        """
        # Create additional newspapers for testing search
        Newspaper.objects.create(
            title="Another Newspaper",
            content="Another Content",
            topic=self.topic,
        )
        Newspaper.objects.create(
            title="Third Newspaper",
            content="Third Content",
            topic=self.topic,
        )

        # Test search with a term that should match only one newspaper
        response = self.client.get(NEWSPAPER_LIST_URL + "?title=Another")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 1)
        self.assertEqual(
            response.context["newspaper_list"][0].title, "Another Newspaper"
        )

        # Test search with a term that should match multiple newspapers
        response = self.client.get(NEWSPAPER_LIST_URL + "?title=Newspaper")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 3)

        # Test search with a term that should match no newspapers
        response = self.client.get(NEWSPAPER_LIST_URL + "?title=NonExistent")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 0)
