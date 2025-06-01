from django.contrib.auth import get_user_model
from django.test import TestCase

from news.models import Topic


class TestTopicModel(TestCase):
    def test_topic_str(self):
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

    def test_redactor_str(self):
        """Test the string representation of a Redactor model."""
        self.assertEqual(
            str(self.redactor),
            f"{self.redactor.username} "
            f"({self.redactor.first_name} {self.redactor.last_name})"
        )


