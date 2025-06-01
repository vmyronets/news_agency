from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from news.models import Redactor, Newspaper, Topic
from news.forms import (
    RedactorCreationForm,
    RedactorSearchForm,
)

REDACTOR_LIST_URL = reverse("news:redactor-list")


class PublicRedactorViewsTests(TestCase):
    def test_access_not_logged_in_users(self):
        response = self.client.get(REDACTOR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateRedactorViewsTests(TestCase):
    def setUp(self) -> None:
        """Set up common test data."""
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            first_name="Test",
            last_name="User",
            years_of_experience=7
        )
        self.client.force_login(self.user)
        self.topic = Topic.objects.create(
            name="Test Topic",
        )
        self.newspaper = Newspaper.objects.create(
            title="Test Title",
            content="Test Content",
            topic=self.topic,
        )

    def test_redactor_list_view(self):
        """
        Test the retrieval of the redactor list view and verify
        its rendered content.

        This function tests the HTTP GET request to the redactor list URL.
        It compares the retrieved list of redactors from the context with the
        expected redactor objects from the database. Additionally, it ensures
        that the correct template has been used to render the view.

        :rtype: None
        """
        response = self.client.get(REDACTOR_LIST_URL)
        redactors = Redactor.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["redactor_list"]), list(redactors)
        )
        self.assertTemplateUsed(
            response, "news/redactor_list.html"
        )

    def test_redactor_detail_view(self) -> None:
        """
        Tests the functionality of the redactor detail view in the application.
         This includes ensuring the correct HTTP response status code, proper
         context data being passed to the template, and verifying that the
         correct template is used for rendering.

        :return: None
        """
        url = reverse("news:redactor-detail", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["redactor"], self.user)
        self.assertTemplateUsed(
            response, "news/redactor_detail.html"
        )

    def test_redactor_create_view_get(self) -> None:
        """
        Tests the GET request to the redactor creation view.

        This method sends a GET request to the URL associated with
        the "news:redactor-create" view, then verifies that the
        response status code is as expected, the correct form is
        included in the context, and the proper template is used to
        render the response.

        :param self: The instance of the test case.
        :type self: TestCase
        :return: None
        """
        url = reverse("news:redactor-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], RedactorCreationForm)
        self.assertTemplateUsed(
            response, "news/redactor_form.html"
        )

    def test_redactor_create_view_post(self) -> None:
        """
        Tests the POST request functionality for creating a new redactor user
        through the redactor create view. Ensures the redactor is successfully
        created with the provided data and a redirection occurs with the
        expected status code.

        :param data: Contains the information for creating a new redactor user,
            including username, passwords, first name, last name, and years
                of experience.
            - username : The username for the new redactor user (string).
            - password1 : The password for the new redactor (string).
            - password2 : The confirmation password for the new redactor
                (string).
            - first_name : The first name of the new redactor user (string).
            - last_name : The last name of the new redactor user (string).
            - years_of_experience : The number of years of experience for the
                redactor (integer).

        :return: Asserts that the response status code is 302
            (indicating redirection) and validates that the new redactor
            user is successfully created in the database.
        """
        url = reverse("news:redactor-create")
        data = {
            "username": "new_test_user",
            "password1": "test_password123",
            "password2": "test_password123",
            "first_name": "New",
            "last_name": "User",
            "years_of_experience": 7
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Redactor.objects.filter(username="new_test_user").exists()
        )

    def test_redactor_update_view_get(self) -> None:
        """
        Tests the GET request functionality of the redactor update view.

        This method performs an HTTP GET request to the redactor update view for
        a specific user's ID. It validates the response status code and ensures
        the correct template is used, confirming that the redactor update view
        is functioning correctly.

        :param self: The instance of the test case class used to execute the test.

        :return: None
        """
        url = reverse("news:redactor-update", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "news/redactor_form.html"
        )

    def test_redactor_update_view_post(self) -> None:
        """
        Tests the POST request functionality for updating a redactor user's
        details. This method checks that the user data is updated correctly
        when a POST request is sent to the appropriate redactor update view.

        :param self: Reference to the current instance of the test class
        :type self: TestCase

        :return: None
        """
        url = reverse("news:redactor-update", args=[self.user.id])
        data = {
            "username": "updated_username",
            "first_name": "User",
            "last_name": "Updated",
            "years_of_experience": 20
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updated_username")
        self.assertEqual(self.user.first_name, "User")
        self.assertEqual(self.user.last_name, "Updated")
        self.assertEqual(self.user.years_of_experience, 20)

    def test_redactor_delete_view_get(self) -> None:
        """
        Tests the GET request for the redactor delete view.

        This method verifies the HTTP response for the GET request to the
        redactor delete view by checking the status code and ensuring the
        correct template is used.

        :return: None
        """
        url = reverse("news:redactor-delete", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "news/redactor_confirm_delete.html"
        )

    def test_redactor_delete_view_post(self) -> None:
        """
        Handles the POST request for deleting a Redactor object based on the
        provided user ID. It performs the deletion operation and validates the
        response status code, ensuring successful removal of the specified
        Redactor object.

        :param self: Instance of the test class.
        :return: None
        """
        url = reverse("news:redactor-delete", args=[self.user.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Redactor.objects.filter(id=self.user.id).exists())

    def test_redactor_search(self) -> None:
        """
        Tests the search functionality of the redactor list endpoint where a
        specific username is queried. Verifies the correct HTTP response status
        code and ensures the returned redactor list corresponds to the expected
        user data.

        :param self:
            Instance of the test case, providing access to the test client's
            methods, attributes, and the test environment context.

        :return:
            None
        """
        url = f"{REDACTOR_LIST_URL}?username=test"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactor_list"]), 1)
        self.assertEqual(response.context["redactor_list"][0], self.user)

    def test_toggle_assign_to_newspaper(self) -> None:
        """
        Tests the functionality of assigning and unassigning a newspaper to/from
        a redactor. This function verifies that a newspaper can be toggled in the
        user's list of assigned newspapers through the respective endpoint.

        :param self: The class instance invoking this method.
        :type self: object
        :return: This method does not return a value. Instead, it performs test
            assertions to validate the toggle functionality.
        """
        # Test assigning a newspaper to the redactor
        url = reverse(
            "news:toggle-newspaper-assign", args=[self.user.id]
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertIn(self.newspaper, self.user.newspapers.all())

        # Test unassigning the newspaper from the redactor
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertNotIn(self.newspaper, self.user.newspapers.all())
