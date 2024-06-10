from django.apps import AppConfig
from django.db import transaction
from django.db.models.signals import post_migrate


def populate_choices(*args, **kwargs):
    # Fill database with skills choices
    from .models import SkillChoice, skills

    with transaction.atomic():
        SkillChoice.objects.all().update(deprecated=True)
        for field, skill, detail in (
            (field, skill, detail)
            for field in skills
            for skill in {"": [], **skills[field]}
            for detail in [""] + (skills[field][skill] if skill else [])
        ):
            SkillChoice.objects.update_or_create(
                field=field, skill=skill, detail=detail, defaults={"deprecated": False}
            )

    # Fill database with languages choices
    from .models import LanguageChoice
    import csv

    with open("annuaire/langues.csv", "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) != 2:
                continue
            LanguageChoice.objects.update_or_create(pt2b=row[0][:3], name=row[1])


class AnnuaireConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "annuaire"

    def ready(self):
        post_migrate.connect(
            populate_choices,
            dispatch_uid="annuaire.populate_choices",
        )
