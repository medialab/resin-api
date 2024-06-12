from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework import viewsets, permissions, mixins

from annuaire.models import Member, LanguageChoice, SkillChoice
from annuaire.serializers import (
    MemberSerializer,
    LanguageChoiceSerializer,
    SkillChoiceSerializer,
)


class FieldChoiceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SkillChoice.objects.filter(detail="", skill="")
    serializer_class = SkillChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SkillChoiceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SkillChoice.objects.exclude(skill="")
    serializer_class = SkillChoiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LanguageChoiceViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LanguageChoice.objects.all()
    serializer_class = LanguageChoiceSerializer


class MemberPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == "POST"
            or request.user
            and request.user.is_authenticated
        )


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.filter(reviewed=True)
    serializer_class = MemberSerializer
    permission_classes = [MemberPermissions]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        admin_link = self.request.build_absolute_uri(
            reverse("admin:annuaire_member_change", args=[serializer.instance.pk])
        )
        send_mail(
            "Nouvelle inscription sur l'annuaire RésIn",
            render_to_string(
                "annuaire/emails/create_member.txt",
                {"admin_link": admin_link},
            ),
            settings.EMAIL_FROM,
            [settings.EMAIL_ADMIN],  # TODO : change this to the actual admin email
            fail_silently=False,
            html_message=render_to_string(
                "annuaire/emails/create_member.html",
                {"admin_link": admin_link},
            ),
        )
