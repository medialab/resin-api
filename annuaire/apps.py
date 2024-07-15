import json

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

    with open("annuaire/languages.json", "r") as f:
        languages = json.load(f)
        for code, name in languages.items():
            LanguageChoice.objects.update_or_create(pt2b=code, defaults={"name": name})


class AnnuaireConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "annuaire"

    def ready(self):
        post_migrate.connect(
            populate_choices,
            dispatch_uid="annuaire.populate_choices",
        )
