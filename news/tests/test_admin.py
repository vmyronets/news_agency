from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestSiteAdmin(TestCase):
    def setUp(self) -> None:
        """Set up common test data."""
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin123",
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="test_redactor",
            password="testredactor123",
            years_of_experience=5,
        )

    def test_site_admin_is_accessible(self) -> None:
        """Test the site admin is accessible."""
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)

    def test_redactor_years_of_experience_displayed_correctly(self) -> None:
        """
        Verify that the redactor's years of experience are displayed correctly.

        This method is a test case designed to ensure that the redactor's total
        years of experience are presented accurately on the changelist. It
        evaluates the formatted display against the expected outcomes under
        various conditions.
        """
        url = reverse("admin:news_redactor_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_years_of_experience_displayed_on_change_page(self) -> None:
        """
        Test to verify the display of redactor years of experience on the change page.

        This function performs a verification check to ensure that the years of
        experience for a redactor are displayed correctly on the change page when
        accessed or updated.
        """
        url = reverse("admin:news_redactor_change", args=(self.redactor.id,))
        response = self.client.get(url)
        self.assertContains(response, self.redactor.years_of_experience)
