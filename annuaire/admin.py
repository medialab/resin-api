from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from annuaire.models import Member, LanguageChoice, SkillChoice


@admin.register(LanguageChoice)
class LanguageChoiceAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    pass


@admin.register(SkillChoice)
class SkillChoiceAdmin(admin.ModelAdmin):
    search_fields = ("field", "skill", "detail")
    pass


@admin.register(Member)
class MemberAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "institution",
        "updated_at",
        "reviewed",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "institution",
        "institution_city",
    )
    list_filter = [
        "languages",
        "skills",
    ]
    readonly_fields = ("last_login",)
    date_hierarchy = "updated_at"
    ordering = ("is_admin", "-updated_at")
    filter_horizontal = ()
    autocomplete_fields = ("languages", "skills")

    fieldsets = (
        (
            "Permissions d'administration",
            {
                "fields": (
                    "password",
                    "is_admin",
                    "last_login",
                )
            },
        ),
        (
            "Profil annuaire",
            {
                "fields": (
                    "reviewed",
                    "first_name",
                    "last_name",
                    "birth_year",
                    "email",
                    "gender",
                    "photo",
                    "languages",
                    "short_bio",
                    "institution",
                    "institution_city",
                    "main_activity",
                    "long_bio",
                    "expertise",
                    "skills",
                    "additional_skills",
                    "publications",
                    "training",
                    "comments",
                )
            },
        ),
    )


admin.site.unregister(Group)
