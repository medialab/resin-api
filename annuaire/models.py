from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q

from annuaire.utils import create_slug

custom_error_messages = {
    "blank": "Veuillez renseigner ce champ",
    "invalid": "Veuillez renseigner une adresse e-mail valide",
}

skills = {
    "Analyse": {
        "Analyse qualitative": ["Analyse de discours", "Codage", "Thésaurus"],
        "Analyse quantitative": ["Analyse statistique de réseaux", "Scientométrie"],
        "Analyse spatiale": ["Cartographie", "Géomatique"],
        "Analyse visuelle": ["Design d’information", "Photographies", "Réseaux"],
        "Apprentissage automatique": [
            "Apprentissage non supervisé",
            "Apprentissage supervisé",
        ],
        "Dispositifs expérimentaux": ["Analyse contre-factuelle"],
        "Statistiques": [
            "Statistiques descriptives",
            "Statistiques inférentielles",
            "Modélisation",
        ],
        "TAL": [
            "Analyse syntaxique",
            "Analyse sémantique",
            "LLMs",
            "Lexicométrie",
            "Text-mining",
        ],
    },
    "Collecte": {
        "APIs": [],
        "Entrepôts de données": [],
        "Entretiens": ["Cognitifs", "Semi-directifs"],
        "Ethnographie": [],
        "Scraping": [],
        "Sondages": [],
    },
    "Curation": {
        "Aspects légaux": ["Anonymisation", "Réglementation (RGPD et DSA)"],
        "Chiffrement, protection, sécurité": [],
        "Enrichissement": ["Métadonnées"],
        "Nettoyage": ["Conversion"],
        "Sauvegarde, versioning": [],
    },
    "Outils": {
        "Administration de systèmes d'information": [
            "Ansible",
            "Docker",
            "Gestion de serveurs",
            "Kubernetes",
            "Shell",
        ],
        "Bases de données": ["NoSQL", "SQL", "SparkQL"],
        "CAQDAS": ["Atlas.ti", "MaxQDA", "Nvivo", "Taguette"],
        "Git": [],
        "Hyphe": [],
        "Langages de programmation": [
            "Bash",
            "CSS",
            "HTML",
            "Java",
            "Javascript",
            "PHP",
            "Perl",
            "Python",
            "R",
            "Ruby",
            "Rust",
            "SQLx",
            "Stata",
        ],
        "Limesurvey": [],
        "Open refine": [],
    },
    "Valorisation": {
        "Archivage": [],
        "Communication": [
            "Interviews",
            "Site web de laboratoire",
            "Édition numérique",
            "Édition papier",
        ],
        "Documentation": ["Plan de gestion de données"],
        "Enseignement": ["Ateliers", "Encadrement", "Innovation pédagogique"],
        "Exposition": [],
        "Gestion de projets": ["Agilité", "Management", "Reporting"],
        "Publication": ["Data papers", "Jeux de données", "Podcasts"],
        "Écologie du numérique": [],
    },
}

skills_choices = []


class SkillChoice(models.Model):
    field = models.CharField(max_length=255)
    skill = models.CharField(max_length=255, blank=True)
    detail = models.CharField(max_length=255, blank=True)
    deprecated = models.BooleanField(
        "Déprécié",
        default=False,
        help_text="Ce choix ne figure plus dans la liste des choix, "
        "mais il est conservé pour les profils qui l'ont déjà sélectionné.",
    )

    def __str__(self):
        if self.detail:
            return f"{self.field} - {self.skill} - {self.detail}"
        if self.skill:
            return f"{self.field} - {self.skill}"
        return self.field

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Choix de compétences"


class LanguageChoice(models.Model):
    pt2b = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}".capitalize()

    class Meta:
        verbose_name = "Langue"
        verbose_name_plural = "Choix de langues"


class MemberManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, birth_year):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            birth_year=birth_year,
            slug=create_slug(first_name, last_name),
        )
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, birth_year, password=None):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            birth_year=birth_year,
            slug=create_slug(first_name, last_name),
        )
        user.set_password(password)
        user.is_admin = True
        user.save()
        return user


class Member(AbstractBaseUser):
    """Member model for the annuaire.

    We base our model on Django's AbstractBaseUser,
    which allows us to unleash the power of Django auth system.
    """

    # Django auth and admin logic
    objects = MemberManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "birth_year"]
    is_admin = models.BooleanField(
        "Permissions d'administration",
        default=False,
        help_text="Cocher cette case permet à la personne de se connecter à cette interface.",
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.last_name

    @property
    def is_staff(self):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"

    # DB Fields
    slug = models.SlugField("Slug", unique=True)
    created_at = models.DateTimeField("Création", auto_now_add=True)
    updated_at = models.DateTimeField("Dernière modification", auto_now=True)
    reviewed = models.BooleanField("Profil validé", default=False)

    first_name = models.CharField(
        "Prénom", max_length=255, error_messages=custom_error_messages
    )
    last_name = models.CharField(
        "Nom", max_length=255, error_messages=custom_error_messages
    )
    birth_year = models.IntegerField(
        "Année de naissance",
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
        error_messages={
            "blank": "Veuillez renseigner ce champ",
        },
        help_text="Votre année de naissance ne sera pas visible sur votre profil. "
        "Elle sera utilisée, uniquement, pour confirmer votre identité.",
    )
    email = models.EmailField(
        "E-mail",
        error_messages={
            "email": "Veuillez renseigner une adresse e-mail valide",
            "blank": "Veuillez renseigner ce champ",
            "unique": "Cet email est déjà enregistré dans l'annuaire",
        },
        unique=True,
    )
    gender = models.CharField(
        "Genre",
        blank=True,
        choices=(
            ("F", "Femme"),
            ("M", "Homme"),
            ("X", "Je ne me reconnais comme aucun des genres ci-dessus"),
        ),
        max_length=100,
        help_text="Permettre d'afficher le genre sur les profils est un parti pris de l'équipe "
        "qui a développé l'annuaire. Cette démarche vise à favoriser la parité, en facilitant "
        "la recherche de profils féminins. ",
    )
    photo = models.ImageField("Photo", upload_to="photos/", blank=True)
    languages = models.ManyToManyField(
        LanguageChoice,
        verbose_name="Langues parlées",
        blank=True,
    )
    short_bio = models.CharField(
        "Phrase de description",
        max_length=200,
        blank=True,
        help_text='Exemple : "Je travaille à la collecte, l’indexation et l’analyse automatique '
        'de grands volumes de données."',
    )
    institution = models.CharField(
        "Institution de rattachement",
        max_length=255,
        error_messages=custom_error_messages,
    )
    institution_city = models.CharField(
        "Ville de l'institution", max_length=255, blank=True
    )
    main_activity = models.CharField(
        "Fonction principale",
        max_length=255,
        blank=True,
        help_text="Nous vous encourageons à mettre en avant votre fonction spécifique, "
        'indépendamment de votre statut officiel. Exemple : "Responsable de projets numériques".',
    )
    long_bio = models.TextField("Biographie", blank=True)
    expertise = models.ManyToManyField(
        SkillChoice,
        verbose_name="Domaines d'expertise",
        limit_choices_to=Q(skill=""),
        related_name="+",
        error_messages={
            "required": "Veuillez renseigner au moins un domaine d'expertise",
        },
    )
    skills = models.ManyToManyField(
        SkillChoice,
        verbose_name="Compétences",
        limit_choices_to=~Q(skill=""),
        related_name="+",
        error_messages={
            "required": "Veuillez renseigner au moins une compétence",
        },
    )
    additional_skills = models.CharField(
        "Compétences supplémentaires",
        max_length=255,
        blank=True,
        help_text="Si vous avez des compétences qui ne figurent pas dans la liste ci-dessus, "
        "renseignez-les dans ce champ. Votre contribution nous permettra d'enrichir notre arbre "
        "des compétences. Veuillez cependant vous assurer que la compétence n'est pas déjà renseignée "
        "avant de faire cette demande d'ajout.",
    )
    publications = models.TextField("Publications", blank=True)
    training = models.TextField("Formations suivies", blank=True)
