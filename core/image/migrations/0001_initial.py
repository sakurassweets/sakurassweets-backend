# Generated by Django 4.2.7 on 2023-12-06 16:53


from django.db import migrations, models
import django.db.models.deletion
import image.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=image.models.image_dir_path, verbose_name='Зображення')),
                ('main_image', models.BooleanField(default=False, verbose_name='Основне фото')),
                ('related_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='product.product', verbose_name='Відноситься до')),
            ],
        ),
    ]