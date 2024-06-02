from django.db import models


class Species(models.Model):
    class Type(models.TextChoices):
        NORMAL = "NO", "Normal"
        FIRE = "FI", "Fire"
        WATER = "WA", "Water"
        ELECTRIC = "EL", "Electric"
        GRASS = "GR", "Grass"
        ICE = "IC", "Ice"
        FIGHTING = "FG", "Fighting"
        POISON = "PO", "Poison"
        GROUND = "GD", "Ground"
        FLYING = "FL", "Flying"
        PSYCHIC = "PS", "Psychic"
        BUG = "BG", "Bug"
        ROCK = "RK", "Rock"
        GHOST = "GH", "Ghost"
        DRAGON = "DR", "Dragon"
        DARK = "DK", "Dark"
        STEEL = "ST", "Steel"
        FAIRY = "FA", "Fairy"

    name = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=2, choices=Type.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "species"
        verbose_name = "Species"
        verbose_name_plural = "Species"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=100, unique=True)
    strength = models.IntegerField(default=0)
    species = models.ForeignKey(Species, on_delete=models.CASCADE)

    class Meta:
        db_table = "characters"

    def __str__(self):
        return self.name
