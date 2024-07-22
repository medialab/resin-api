# Generated by Django 5.0.6 on 2024-07-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("annuaire", "0007_alter_member_gender"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Je ne souhaite pas répondre"),
                    ("F", "Femme"),
                    ("M", "Homme"),
                    ("X", "Aucun des genres ci-dessus"),
                ],
                default="",
                help_text="Permettre d'afficher le genre sur les profils est un parti pris de l'équipe qui a développé l'annuaire. Cette démarche vise à favoriser la parité, en facilitant la recherche de profils féminins. ",
                max_length=100,
                verbose_name="Genre",
            ),
        ),
    ]