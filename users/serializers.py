from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
	first_name = serializers.CharField(max_length=150)
	last_name = serializers.CharField(max_length=150)
	# full_name = serializers.CharField(max_length=150)

	email = serializers.EmailField()
	password = serializers.CharField(write_only=True)

	def validate_email(self, value: str) -> str:
		validate_email(value)
		if User.objects.filter(email__iexact=value).exists():
			raise serializers.ValidationError(_("Email already registered"))
		return value

	def validate_password(self, value: str) -> str:
		validate_password(value)
		return value

	def create(self, validated_data):
		first_name = validated_data["first_name"].strip()
		last_name = validated_data["last_name"].strip()

		# full_name = first_name + " " + last_name if first_name and last_name else first_name or last_name
		email = validated_data["email"].lower()
		password = validated_data["password"]
		user = User.objects.create_user(username=email, email=email, first_name=first_name, last_name = last_name, password=password)
		return user


class EmailSerializer(serializers.Serializer):
	email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
	token = serializers.CharField()
	new_password = serializers.CharField(write_only=True)

	def validate_new_password(self, value: str) -> str:
		validate_password(value)
		return value
