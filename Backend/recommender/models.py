from django.db import models
#from django.forms.models import model_to_dict


class Recommendations(models.Model):
    age_from = models.FloatField()
    age_to = models.FloatField()
    
    Histidine = models.FloatField()
    Isoleucine = models.FloatField()
    Leucine = models.FloatField()
    Lysine = models.FloatField()
    Methionine = models.FloatField()
    Phenylalanine = models.FloatField()
    Threonine = models.FloatField()
    Tryptophan = models.FloatField()
    Valine = models.FloatField()
    Cysteine = models.FloatField()
    PhenylalinePlusTyrosine = models.FloatField() #aromatic amino acids
    MethioninePlusCysteine = models.FloatField() #sulfur amino acids
    TotalAminoAcidNitrogen = models.FloatField()


    