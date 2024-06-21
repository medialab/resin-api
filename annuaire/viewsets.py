import urllib.parse

from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import constant_time_compare
from rest_framework import viewsets, permissions, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from annuaire.models import Member, LanguageChoice, SkillChoice
from annuaire.serializers import (
    MemberSerializer,
    LanguageChoiceSerializer,
    SkillChoiceSerializer,
    MemberAuthLinkRequestSerializer,
)
from annuaire.utils import send_mail


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

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == "POST"
            or obj == request.user
            or request.user.is_staff
        )


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.filter(reviewed=True)
    serializer_class = MemberSerializer
    permission_classes = [MemberPermissions]
    admin_recipients = Member.objects.filter(is_admin=True).values_list(
        "email", flat=True
    )

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
            self.admin_recipients,
            fail_silently=False,
            html_message=render_to_string(
                "annuaire/emails/create_member.html",
                {"admin_link": admin_link},
            ),
        )

    def perform_update(self, serializer):
        super().perform_update(serializer)
        send_mail(
            "Mise à jour de votre profil sur l'annuaire RésIn",
            render_to_string(
                "annuaire/emails/update_member.txt",
                {},
            ),
            settings.EMAIL_FROM,
            self.admin_recipients,
            fail_silently=False,
            html_message=render_to_string(
                "annuaire/emails/update_member.html",
                {},
            ),
            reply_to_list=self.admin_recipients,
        )

    @action(
        detail=False, methods=["post"], serializer_class=MemberAuthLinkRequestSerializer
    )
    def new_auth_link(self, request):
        serializer = MemberAuthLinkRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = Member.objects.get(email=serializer.validated_data["email"])
        except Member.DoesNotExist:
            raise PermissionDenied(
                "L'adresse email ou l'année de naissance est invalide"
            )
        if not constant_time_compare(
            user.birth_year, serializer.validated_data["birth_year"]
        ):
            raise PermissionDenied(
                "L'adresse email ou l'année de naissance est invalide"
            )

        token = Token.objects.create(user=user)
        link = (
            settings.EDIT_PROFILE_URL
            + "?"
            + urllib.parse.urlencode({"uid": user.pk, "token": token})
        )
        send_mail(
            "Lien d'authentification pour l'annuaire RésIn",
            render_to_string(
                "annuaire/emails/send_auth_link.txt",
                {"auth_link": link},
            ),
            settings.EMAIL_FROM,
            [user.email],
            fail_silently=False,
            html_message=render_to_string(
                "annuaire/emails/send_auth_link.html",
                {"auth_link": link},
            ),
            reply_to_list=self.admin_recipients,
        )
        return Response({"detail": "Email envoyé avec succès"})
