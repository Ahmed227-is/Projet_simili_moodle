
from django.contrib import admin
from django.utils.html import format_html
from .models import Professeur, Cours, Ressource
from django.contrib.admin import AdminSite

'''class MyAdminSite(admin.AdminSite):
    class Media:
        css = {
            'all': ('/static/css/custom_admin.css',),
        }

admin.site = MyAdminSite()'''

#Personnalisation de l'affichage des professeurs dans l'admin
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'departement', 'specialite', 'afficher_photo')

    def afficher_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:130px;width:130px;border-radius:50%;"/>', obj.photo.url)
        return "Pas d'image"

    afficher_photo.short_description = "Photo"

# Personnalisation de l'affichage des cours dans l'admin
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'professeur', 'date_debut', 'date_fin', 'afficher_illustration')

    def afficher_illustration(self, obj):
        if obj.illustration:
            return format_html('<img src="{}" style="height: 50px;width:90px"/>', obj.illustration.url)
        return "Pas d'image"
    
    afficher_illustration.short_description = "Illustration du Cours"

# Personnalisation de l'affichage des ressources dans l'admin
class RessourceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'type', 'afficher_illustration')

    def afficher_illustration(self, obj):
        if obj.illustration:
            return format_html('<img src="{}" style="height: 50px;"/>', obj.illustration.url)
        return "Pas d'image"
    
    afficher_illustration.short_description = "Illustration"

# Enregistrer les modèles avec leur configuration d'affichage personnalisée
admin.site.register(Professeur, ProfesseurAdmin)
admin.site.register(Cours, CoursAdmin)
admin.site.register(Ressource, RessourceAdmin)

# Modification du site d'administration
admin.site.site_header = "ADMIN DOODLE ENSEA"
admin.site.site_title = "Gestion des utilisateurs"
admin.site.index_title = "Bienvenue sur le panneau d'administration"

