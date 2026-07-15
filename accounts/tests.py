from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountTests(TestCase):
    def test_profile_created_on_signup(self):
        user = User.objects.create_user("alice", password="pw12345678")
        self.assertTrue(hasattr(user, "profile"))

    def test_registration_flow(self):
        r = self.client.post(
            reverse("accounts:register"),
            {
                "first_name": "New",
                "username": "newuser",
                "email": "new@example.com",
                "password1": "Str0ngPass!9",
                "password2": "Str0ngPass!9",
            },
        )
        self.assertEqual(r.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_duplicate_email_rejected(self):
        User.objects.create_user("a", email="dup@example.com", password="pw12345678")
        r = self.client.post(
            reverse("accounts:register"),
            {
                "first_name": "B",
                "username": "b",
                "email": "dup@example.com",
                "password1": "Str0ngPass!9",
                "password2": "Str0ngPass!9",
            },
        )
        self.assertEqual(r.status_code, 200)  # re-rendered with error
        self.assertFalse(User.objects.filter(username="b").exists())

    def test_profile_requires_login(self):
        r = self.client.get(reverse("accounts:profile"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/accounts/login/", r.url)
