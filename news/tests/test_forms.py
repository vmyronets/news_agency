from django.test import TestCase
from django.contrib.auth import get_user_model

from news.forms import (
    NewspaperForm,
    NewspaperSearchForm,
    RedactorCreationForm,
    RedactorSearchForm,
    TopicSearchForm,
)
from news.models import Topic


class NewspaperFormTests(TestCase):
    def setUp(self) -> None:
        """Set up common test data."""
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            first_name="Test",
            last_name="User",
            years_of_experience=5,
        )
        self.topic = Topic.objects.create(name="Test Topic")

    def test_newspaper_form_valid_data(self):
        """Test that the form is valid with valid data."""
        form_data = {
            "title": "Test Newspaper",
            "content": "Test Content",
            "topic": self.topic.id,
            "publishers": [self.user.id],
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_newspaper_form_no_data(self):
        """Test that the form is invalid with no data."""
        form = NewspaperForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)  # title, content, topic are required

    def test_newspaper_form_missing_title(self):
        """Test that the form is invalid with missing title."""
        form_data = {
            "content": "Test Content",
            "topic": self.topic.id,
            "publishers": [self.user.id],
        }
        form = NewspaperForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_newspaper_form_missing_content(self):
        """Test that the form is invalid with missing content."""
        form_data = {
            "title": "Test Newspaper",
            "topic": self.topic.id,
            "publishers": [self.user.id],
        }
        form = NewspaperForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_newspaper_form_missing_topic(self):
        """Test that the form is invalid with missing topic."""
        form_data = {
            "title": "Test Newspaper",
            "content": "Test Content",
            "publishers": [self.user.id],
        }
        form = NewspaperForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("topic", form.errors)

    def test_newspaper_form_publishers_optional(self):
        """Test that publishers field is optional."""
        form_data = {
            "title": "Test Newspaper",
            "content": "Test Content",
            "topic": self.topic.id,
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())


class RedactorCreationFormTests(TestCase):
    def test_redactor_creation_form_valid_data(self):
        """Test that the form is valid with valid data."""
        form_data = {
            "username": "test_user",
            "first_name": "Test",
            "last_name": "User",
            "years_of_experience": 5,
            "password1": "test_password",
            "password2": "test_password",
        }
        form = RedactorCreationForm(data=form_data)

        self.assertTrue(form.is_valid())


class RedactorSearchFormTests(TestCase):
    def setUp(self) -> None:
        self.form = RedactorSearchForm()

    def test_redactor_search_form_valid_data(self):
        """Test that the form is valid with valid data."""
        form_data = {"username": "test_user"}
        form = RedactorSearchForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])

    def test_redactor_search_form_field_label(self) -> None:
        """Test that the form field has the correct label."""
        self.assertEqual(self.form.fields["username"].label, "")

    def test_redactor_search_form_field_placeholder(self) -> None:
        """Test that the form field has the correct placeholder."""
        self.assertEqual(
            self.form.fields["username"].widget.attrs["placeholder"],
            "Search by username",
        )


class NewspaperSearchFormTests(TestCase):
    def test_newspaper_search_form_valid_data(self) -> None:
        """Test that the form is valid with valid data."""
        form_data = {"title": "Test Search"}
        form = NewspaperSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_newspaper_search_form_empty_data(self):
        """Test that the form is valid with empty data (search is optional)."""
        form_data = {"title": ""}
        form = NewspaperSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_newspaper_search_form_no_data(self):
        """Test that the form is valid with no data (search is optional)."""
        form = NewspaperSearchForm(data={})
        self.assertTrue(form.is_valid())

    def test_newspaper_search_form_placeholder(self):
        """Test that the form field has the correct placeholder."""
        form = NewspaperSearchForm()
        self.assertEqual(
            form.fields["title"].widget.attrs["placeholder"], "Search by title"
        )


class TopicSearchFormTests(TestCase):
    def setUp(self) -> None:
        self.form = TopicSearchForm()

    def test_topic_search_form_valid_data(self) -> None:
        """Test that the form is valid with valid data."""
        form_data = {"name": "Test Topic"}
        form = TopicSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], form_data["name"])

    def test_topic_search_form_field_label(self) -> None:
        """Test that the form field has the correct label."""
        self.assertEqual(self.form.fields["name"].label, "")

    def test_topic_search_form_field_placeholder(self) -> None:
        """Test that the form field has the correct placeholder."""
        self.assertEqual(
            self.form.fields["name"].widget.attrs["placeholder"], "Search by name"
        )
