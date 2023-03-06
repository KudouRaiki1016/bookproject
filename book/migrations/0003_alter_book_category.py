# Generated by Django 4.1.2 on 2022-11-25 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0002_book_delete_samplemodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="category",
            field=models.CharField(
                choices=[("business", "ビジネス"), ("life", "生活"), ("other", "その他")],
                max_length=100,
            ),
        ),
    ]