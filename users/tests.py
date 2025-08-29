from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthFlowTests(APITestCase):
	def setUp(self):
		cache.clear()

	def test_registration_and_login_and_reset(self):
		# Register
		resp = self.client.post(reverse("register"), {
			"full_name": "Test User",
			"email": "test@example.com",
			"password": "Str0ngP@ssw0rd!",
		}, format="json")
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		self.assertTrue(User.objects.filter(email="test@example.com").exists())

		# Obtain JWT token
		resp = self.client.post(reverse("token_obtain_pair"), {
			"username": "test@example.com",
			"password": "Str0ngP@ssw0rd!",
		}, format="json")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertIn("access", resp.data)

		# Forgot password
		resp = self.client.post(reverse("forgot_password"), {"email": "test@example.com"}, format="json")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

		# Get the token from cache by scanning (test-only approach)
		# Since we do not send emails, simulate retrieval by generating a new token
		# In real tests, we would capture the token return; here, call endpoint to get token
		resp = self.client.post(reverse("forgot_password"), {"email": "test@example.com"}, format="json")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		token = resp.data.get("reset_token")
		self.assertIsNotNone(token)

		# Reset password
		resp = self.client.post(reverse("reset_password"), {"token": token, "new_password": "N3wStr0ngP@ss!"}, format="json")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

		# Login with new password
		resp = self.client.post(reverse("token_obtain_pair"), {
			"username": "test@example.com",
			"password": "N3wStr0ngP@ss!",
		}, format="json")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
