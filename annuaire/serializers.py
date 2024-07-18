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
    delete_photo = serializers.BooleanField(
        write_only=True, required=False, default=False
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
        self.fields["email"].write_only = True
        self.fields["birth_year"].write_only = True

    def update(self, instance, validated_data):
        delete_photo = validated_data.pop("delete_photo", False)
        photo = validated_data.get("photo")

        if delete_photo:
            instance.photo.delete()
            instance.photo = None

        if photo:
            instance.photo = photo

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get("request")

        # Show birth year and email to user if they are logged in
        # and viewing their own profile
        if (
            request.method == "GET"
            and request.user
            and request.user.is_authenticated
            and request.user.id == instance.id
        ):
            ret["birth_year"] = instance.birth_year
            ret["email"] = instance.email

        # Show email if instance.display_email is True
        if instance.display_email:
            ret["email"] = instance.email

        return ret

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
            "delete_photo",
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
        write_only_fields = ["birth_year", "email"]


class MemberAuthLinkRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label="Adresse email renseignée lors de l'inscription"
    )
    birth_year = serializers.IntegerField(
        label="Année de naissance renseignée lors de l'inscription",
        min_value=1900,
        max_value=2020,
    )
