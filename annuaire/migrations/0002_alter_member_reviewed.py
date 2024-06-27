from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("annuaire", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="reviewed",
            field=models.BooleanField(default=False, verbose_name="Profil validé"),
        ),
    ]
