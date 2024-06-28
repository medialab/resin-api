from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from annuaire.models import Member, SkillChoice


class APIUserTestCase(APITestCase):
    post_data = {
        "email": "bonjour@maudroyer.fr",
        "first_name": "Maud",
        "last_name": "Royer",
        "birth_year": 1992,
        "institution": "Université de La Villette",
        "expertise": [
            SkillChoice.objects.filter(skill="").first().pk,
        ],
        "skills": [
            SkillChoice.objects.exclude(skill="").first().pk,
        ],
    }

    patch_data = {
        "email": "hello@maudroyer.fr",
        "first_name": "Maud",
        "last_name": "Royer",
        "birth_year": 1992,
        "institution": "Université de Pantin",
        "expertise": [
            SkillChoice.objects.filter(skill="").last().pk,
        ],
        "skills": [
            SkillChoice.objects.exclude(skill="").last().pk,
        ],
    }

    @staticmethod
    def create_member(email="bonjour@maudroyer.fr"):
        member = Member.objects.create(
            email=email,
            first_name="Maud",
            last_name="Royer",
            birth_year=1992,
            institution="Université de La Villette",
            reviewed=True,
        )

        member.expertise.set([SkillChoice.objects.filter(skill="").first()]),
        member.skills.set([SkillChoice.objects.exclude(skill="").first()])
        return member

    def test_post_new_member(self):
        response = self.client.post("/api/members/", self.post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().first_name, "Maud")
        self.assertEqual(Member.objects.get().last_name, "Royer")
        self.assertEqual(Member.objects.get().slug, "maud-royer")
        self.assertEqual(Member.objects.get().email, "bonjour@maudroyer.fr")
        self.assertEqual(Member.objects.get().birth_year, 1992)
        self.assertEqual(Member.objects.get().institution, "Université de La Villette")

    def test_patch_member_unauthenticated(self):
        member = self.create_member()
        response = self.client.patch(f"/api/members/{member.pk}/", self.patch_data)
        self.assertEqual(response.status_code, 403)

    def test_patch_member_wrong_user(self):
        member = self.create_member()
        other_member = self.create_member(email="hello@maudroyer.fr")
        Token.objects.create(user=member)
        response = self.client.patch(
            f"/api/members/{other_member.pk}/",
            self.patch_data,
            headers={"Authorization": f"Token {member.auth_token}"},
        )
        self.assertEqual(response.status_code, 403)

    def test_patch_member(self):
        member = self.create_member()
        Token.objects.create(user=member)
        response = self.client.patch(
            f"/api/members/{member.pk}/",
            self.patch_data,
            headers={"Authorization": f"Token {member.auth_token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().email, "hello@maudroyer.fr")
        self.assertEqual(Member.objects.get().institution, "Université de Pantin")
        self.assertEqual(Member.objects.get().expertise.count(), 1)
        self.assertEqual(
            Member.objects.get().expertise.last().pk,
            SkillChoice.objects.filter(skill="").last().pk,
        )
        self.assertEqual(Member.objects.get().skills.count(), 1)
        self.assertEqual(
            Member.objects.get().skills.last().pk,
            SkillChoice.objects.exclude(skill="").last().pk,
        )

    def test_max_six_skills(self):
        post_data = self.post_data.copy()
        post_data["skills"] = [
            SkillChoice.objects.exclude(skill="")[i].pk for i in range(7)
        ]
        response = self.client.post("/api/members/", post_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"skills": ["Vous ne pouvez pas sélectionner plus de 6 compétences."]},
        )
