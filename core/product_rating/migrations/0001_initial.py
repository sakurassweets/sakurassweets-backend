# Generated by Django 4.2.7 on 2024-05-09 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import product_rating.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product", "0006_alter_producttype_options_alter_product_components_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductRating",
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
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
                        default=0,
                        validators=[product_rating.models.validate_rating],
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                        verbose_name="Відноситься до продукту",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Відноситься до користувача",
                    ),
                ),
            ],
        ),
    ]
