from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Snack

# Create your tests here.

class SnackTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="", password="pass"
        )

        self.snack = Snack.objects.create(
            name="snack6", description="test", owner=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "sanck6")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.name}", "snack6")
        self.assertEqual(f"{self.snack.owner}", "tester")
        self.assertEqual(f"{self.snack.description}", "test")

    def test_snack_list_view(self):
        response = self.client.get(reverse("snack_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "snack6")
        self.assertTemplateUsed(response, "snack-list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Owner: tester")
        self.assertTemplateUsed(response, "snack-detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("snack_create"),
            {
                "name": "Raker",
                "description": "test",
                "purchaser": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("snack_detail", args="2"))
        self.assertContains(response, "details about the snack")



    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("snack_update", args="1"),
            {"name": "Updated name","description":"new description","reviewer":self.user.id}
        )

        self.assertRedirects(response, reverse("snack_detail", args="1"))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("snack_delete", args="1"))
        self.assertEqual(response.status_code, 200)