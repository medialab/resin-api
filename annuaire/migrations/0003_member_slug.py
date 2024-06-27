from django.db import migrations, models

from annuaire.utils import create_slug


def update_slug(apps, schema_editor):
    Member = apps.get_model("annuaire", "Member")
    for member in Member.objects.all():
        member.slug = create_slug(member.first_name, member.last_name)
        member.save()


class Migration(migrations.Migration):
    dependencies = [
        ("annuaire", "0002_alter_member_reviewed"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="slug",
            field=models.SlugField(verbose_name="Slug", default=""),
        ),
        migrations.RunPython(update_slug, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name="member",
            name="slug",
            field=models.SlugField(
                unique=True,
                verbose_name="Slug",
            ),
        ),
    ]
