# Generated by Django 4.1.2 on 2022-12-06 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0005_book_thumnail"),
    ]

    operations = [
        migrations.RenameField(
            model_name="book", old_name="thumnail", new_name="thumbnail",
        ),
    ]
