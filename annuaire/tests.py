from rest_framework.test import APITestCase

from annuaire.models import Member, SkillChoice


class APIUserTestCase(APITestCase):
    def test_post_new_member(self):
        data = {
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
        response = self.client.post("/api/members/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().first_name, "Maud")
        self.assertEqual(Member.objects.get().last_name, "Royer")
        self.assertEqual(Member.objects.get().email, "bonjour@maudroyer.fr")
        self.assertEqual(Member.objects.get().birth_year, 1992)
        self.assertEqual(Member.objects.get().institution, "Université de La Villette")
