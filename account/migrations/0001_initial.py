# Generated by Django 4.1.6 on 2023-02-09 22:15

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserBase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="email address"
                    ),
                ),
                ("user_name", models.CharField(max_length=150, unique=True)),
                ("full_name", models.CharField(blank=True, max_length=150)),
                (
                    "about",
                    models.TextField(blank=True, max_length=500, verbose_name="about"),
                ),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("phone_number", models.CharField(blank=True, max_length=15)),
                ("postcode", models.CharField(blank=True, max_length=12)),
                ("address_line_1", models.CharField(blank=True, max_length=150)),
                ("address_line_2", models.CharField(blank=True, max_length=150)),
                ("town_city", models.CharField(blank=True, max_length=150)),
                ("is_active", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_subscribed", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Accounts",
                "verbose_name_plural": "Accounts",
            },
        ),
    ]
