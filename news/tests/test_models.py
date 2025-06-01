from django.test import TestCase

from news.models import Topic


class TestTopicModel(TestCase):
    def test_topic_str(self):
        """Test the string representation of a Topic model."""
        topic = Topic(name="test")
        self.assertEqual(str(topic), topic.name)

