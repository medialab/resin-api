from rest_framework import serializers
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

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

    def validate_skills(self, skills):
        if len(skills) > 6:
            raise serializers.ValidationError(
                "Vous ne pouvez pas sélectionner plus de 6 compétences."
            )

        return skills

    def validate_photo(self, photo):
        # Resize photo to 1000px max width
        if photo:
            img = Image.open(photo)
            if img.width > 1000 or img.height > 1000:
                img.thumbnail((1000, 1000))
                img_bytes = BytesIO()
                img.save(img_bytes, format="JPEG")
                img_bytes.seek(0)
                photo = InMemoryUploadedFile(
                    img_bytes,
                    None,
                    photo.name,
                    "image/jpeg",
                    img_bytes.tell(),
                    None,
                )

        return photo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")

        # Show birth year to user if they are logged in
        # and viewing their own profile
        if (
            request.method == "GET"
            and request.user
            and request.user.is_authenticated
            and "instance" in kwargs
            and request.user.id == kwargs["instance"].id
        ):
            self.fields["birth_year"].write_only = False

    class Meta:
        model = Member
        fields = [
            "id",
            "slug",
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
        ]
        read_only_fields = ["id", "slug"]


class MemberAuthLinkRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label="Adresse email renseignée lors de l'inscription"
    )
    birth_year = serializers.IntegerField(
        label="Année de naissance renseignée lors de l'inscription",
        min_value=1900,
        max_value=2020,
    )
