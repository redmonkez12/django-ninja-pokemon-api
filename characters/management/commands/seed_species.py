from django.core.management.base import BaseCommand

from characters.models import Species


class Command(BaseCommand):
    help = 'Seed the database with all Pokémon types'

    def handle(self, *args, **options):
        species_types = [
            {"name": "Normal", "value": Species.Type.NORMAL},
            {"name": "Fire", "value": Species.Type.FIRE},
            {"name": "Water", "value": Species.Type.WATER},
            {"name": "Electric", "value": Species.Type.ELECTRIC},
            {"name": "Grass", "value": Species.Type.GRASS},
            {"name": "Ice", "value": Species.Type.ICE},
            {"name": "Fighting", "value": Species.Type.FIGHTING},
            {"name": "Poison", "value": Species.Type.POISON},
            {"name": "Ground", "value": Species.Type.GROUND},
            {"name": "Flying", "value": Species.Type.FLYING},
            {"name": "Psychic", "value": Species.Type.PSYCHIC},
            {"name": "Bug", "value": Species.Type.BUG},
            {"name": "Rock", "value": Species.Type.ROCK},
            {"name": "Ghost", "value": Species.Type.GHOST},
            {"name": "Dragon", "value": Species.Type.DRAGON},
            {"name": "Dark", "value": Species.Type.DARK},
            {"name": "Steel", "value": Species.Type.STEEL},
            {"name": "Fairy", "value": Species.Type.FAIRY},
        ]

        for species in species_types:
            obj, created = Species.objects.get_or_create(
                name=species["name"],
                value=species["value"]
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created {species["name"]} type'))
            else:
                self.stdout.write(f'{species["name"]} type already exists')

        self.stdout.write(self.style.SUCCESS('Database seeded with Pokémon types successfully'))
