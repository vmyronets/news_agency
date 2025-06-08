from django.contrib.auth import get_user_model
from django.test import TestCase

from news.models import Topic, Newspaper


class TestTopicModel(TestCase):
    def test_topic_str(self) -> None:
        """Test the string representation of a Topic model."""
        topic = Topic(name="test")
        self.assertEqual(str(topic), topic.name)


class TestRedactorModel(TestCase):
    def setUp(self):
        """Set up common test data."""
        self.redactor = get_user_model().objects.create_user(
            username="test_name",
            password="test_password",
            first_name="test_first_name",
            last_name="test_last_name",
            years_of_experience=11,
        )

    def test_redactor_str(self) -> None:
        """Test the string representation of a Redactor model."""
        self.assertEqual(
            str(self.redactor),
            f"{self.redactor.username} "
            f"({self.redactor.first_name} {self.redactor.last_name})",
        )

    def test_experienced_redactor_creation(self) -> None:
        """
        Test creation of redactor with experience and password verification.
        """
        password = "test_password"
        year_of_experience = 11
        self.assertEqual(self.redactor.years_of_experience, year_of_experience)
        self.assertTrue(self.redactor.check_password(password))

    def test_get_absolute_url(self) -> None:
        """Test the redactor's get_absolute_url method."""
        self.assertEqual(self.redactor.get_absolute_url(), "/redactors/1/")


class TestNewspaperModel(TestCase):
    def test_newspaper_str(self) -> None:
        """Test the string representation of a Newspaper model."""
        topic = Topic.objects.create(name="test_topic")
        newspaper = Newspaper.objects.create(
            title="test_title",
            content="test_content",
            topic=topic,
        )
        self.assertEqual(str(newspaper), newspaper.title)
