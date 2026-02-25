from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Voter


@admin.register(Voter)
class VoterAdmin(UserAdmin):
	model = Voter
	list_display = ("email", "full_name", "is_staff", "is_active")
	list_filter = ("is_staff", "is_active")
	search_fields = ("email", "full_name")
	ordering = ("email",)
	fieldsets = (
		(None, {"fields": ("email", "password")}),
		("Personal info", {"fields": ("full_name", "first_name", "last_name")}),
		(
			"Permissions",
			{
				"fields": (
					"is_active",
					"is_staff",
					"is_superuser",
					"groups",
					"user_permissions",
				)
			},
		),
		("Important dates", {"fields": ("last_login", "date_joined")}),
	)
	add_fieldsets = (
		(
			None,
			{
				"classes": ("wide",),
				"fields": ("email", "full_name", "password1", "password2", "is_staff", "is_active"),
			},
		),
	)
