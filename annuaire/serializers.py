from rest_framework import serializers

from annuaire.models import Member, SkillChoice, LanguageChoice


class SkillChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillChoice
        fields = ["id", "field", "skill", "detail"]


class LanguageChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageChoice
        fields = ["pt2b", "name"]


class MemberSerializer(serializers.ModelSerializer):
    birth_year = serializers.IntegerField(
        label="Année de naissance", min_value=1900, max_value=2020, write_only=True
    )

    class Meta:
        model = Member
        fields = [
            "first_name",
            "last_name",
            "birth_year",
            "gender",
            "email",
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
        ]
