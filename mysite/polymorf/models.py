from django.db import models

# Create your models here.

from polymorphic.models import PolymorphicModel

class Project(PolymorphicModel):
    topic = models.CharField(max_length=30)

class ArtProject(Project):
    artist = models.CharField(max_length=30)

class ResearchProject(Project):
    supervisor = models.CharField(max_length=30)

#################################################
class ModelA(PolymorphicModel):
    field1 = models.CharField(max_length=10)

class ModelB(ModelA):
    field2 = models.CharField(max_length=10)

class ModelC(ModelB):
    field3 = models.CharField(max_length=10)