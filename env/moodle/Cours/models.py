
from django.db import models
from django.utils import timezone
from django.core.files import File
from django.conf import settings
import os

# Modèle pour les professeurs
class Professeur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    departement = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='professeurs_photos/', blank=True, null=True)
    biographie = models.TextField(blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    date_embauche = models.DateField(blank=True, null=True)
    specialite = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nom

# Modèle pour les cours
class Cours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    professeur = models.ForeignKey('Professeur', related_name='cours', on_delete=models.CASCADE)
    date_debut = models.DateField(default=timezone.now)  # Ajoute la date de début
    date_fin = models.DateField(null=True, blank=True)  # Ajoute la date de fin (optionnelle)
    nombre_heures = models.PositiveIntegerField(blank=True, null=True)
    niveau = models.CharField(max_length=50, choices=(('débutant', 'Débutant'), ('intermédiaire', 'Intermédiaire'), ('avancé', 'Avancé')), blank=True, null=True)
    illustration = models.ImageField(upload_to='cours_illustrations/', blank=True, null=True)  # Ajouter une image pour le cours

    def __str__(self):
        return self.titre

# Modèle pour les ressources
class Ressource(models.Model):
    cours = models.ForeignKey(Cours, related_name='ressources', on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='ressources/')
    type = models.CharField(max_length=100, choices=(('pdf', 'PDF'), ('word', 'WORD'), ('excel', 'EXCEL'), ('python', 'PYTHON'), ('power', 'POWER')))
    description = models.TextField(blank=True, null=True)
    illustration = models.ImageField(upload_to='ressources_illustrations/', blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

    def get_default_illustration(self):
        extension = self.type.lower()
        if extension == 'pdf':
            return 'default_images/illust_pdf.png'
        elif extension == 'python':
            return 'default_images/illust_pyton.jpg'
        elif extension == 'word':
            return 'default_images/illust_word.png'
        elif extension == 'excel':
            return 'default_images/illust_excel.webp'
        elif extension == 'power':
            return 'default_images/illust_powerpoint.jpg'
        else:
            return 'default_images/image_default.jpg'

    def save(self, *args, **kwargs):
        if not self.illustration:
            default_image_path = os.path.join(settings.MEDIA_ROOT, self.get_default_illustration())
            
            # Vérifie si le fichier existe
            if os.path.exists(default_image_path):
                # Ouvre le fichier et l'assigne à l'illustration
                with open(default_image_path, 'rb') as f:
                    self.illustration.save(os.path.basename(default_image_path), File(f), save=False)
            else:
                # Optionnel : log ou gérer le cas où l'image par défaut n'existe pas
                print(f"Le fichier {default_image_path} n'existe pas.")
        
        super().save(*args, **kwargs)

