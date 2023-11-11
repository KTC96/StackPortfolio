from django.test import TestCase
from technology.models import Tech


class TechnologyTest(TestCase):
    """
    Tests related to different tech
    that projects and users have.
    """

    def test_tech_model_exists(self):
        """
        Test that the tech model exists.
        """
        tech = Tech.objects.create(
            tech_name="Django",
            is_approved=True
        )
        self.assertTrue(isinstance(tech, Tech))
