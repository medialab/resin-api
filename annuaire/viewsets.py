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
