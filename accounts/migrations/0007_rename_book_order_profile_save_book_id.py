# Generated by Django 4.1.2 on 2023-02-17 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_profile_book_order"),
    ]

    operations = [
        migrations.RenameField(
            model_name="profile", old_name="book_order", new_name="save_book_id",
        ),
    ]
