# Generated by Django 5.0.6 on 2024-06-28 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("annuaire", "0004_alter_languagechoice_pt2b"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="comments",
        ),
    ]
