from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.template.loader import render_to_string

from annuaire.models import Member, LanguageChoice, SkillChoice
from annuaire.utils import send_mail


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
    prepopulated_fields = {"slug": ("first_name", "last_name")}

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
                    "slug",
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
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if "reviewed" in form.changed_data and obj.reviewed:
            profile_link = settings.PROFILE_URL + "/" + str(obj.slug)
            send_mail(
                "Validation de votre profil sur l'annuaire RésIn",
                render_to_string(
                    "annuaire/emails/reviewed_member.txt",
                    {"profile_link": profile_link},
                ),
                settings.EMAIL_FROM,
                [obj.email],
                fail_silently=False,
                html_message=render_to_string(
                    "annuaire/emails/reviewed_member.html",
                    {"profile_link": profile_link},
                ),
                reply_to_list=Member.objects.filter(is_admin=True).values_list(
                    "email", flat=True
                ),
            )

        return super().save_model(request, obj, form, change)


admin.site.unregister(Group)
