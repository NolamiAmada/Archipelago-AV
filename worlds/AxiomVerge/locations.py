from BaseClasses import Location, CollectionState, Entrance
from typing import NamedTuple, Callable


class AVLocation(NamedTuple):
    name: str
    code: int
    logic: Callable[[CollectionState], bool] = Entrance.access_rule


BASE_ID = 332200000
axiom_verge_locations = {
    "Disruptor Room_East": [AVLocation("Eribu - Starter Weapon", BASE_ID+0)],
    "Nova Room": [AVLocation("Eribu - Right Tower", BASE_ID+1)],
    "False Reflector": [AVLocation("Eribu - Left Tower", BASE_ID+2)],
    "Bubbled Altar": [AVLocation("Eribu - Bubbled Altar", BASE_ID+3)],
    "Multi Disruptor_Lower": [AVLocation("Eribu - Multi Disruptor", BASE_ID+4)],
    "Forbidden Corridor_West": [AVLocation("Eribu - Cryptography Gate", BASE_ID+5)],
    "Drill Room_Upper": [AVLocation("Eribu - Xedur Item", BASE_ID+6)],
    "Xedur Basement_West": [AVLocation("Eribu - Xedur Basement", BASE_ID+7)],
    "Wheelchair": [AVLocation("Eribu - Wheelchair", BASE_ID+8)],
    "Primordial Cavern_Center": [AVLocation("Eribu - Primordial Cavern", BASE_ID+9)],
    "Flamethrower Room": [AVLocation("Eribu - Flamethrower", BASE_ID+10)],
    "Weapons Vault": [AVLocation("Eribu - Weapons Vault", BASE_ID+11)],
    "Eribu to Indi_East": [AVLocation("Eribu - Exit to Indi", BASE_ID+12)],
    "Bubblewrap": [AVLocation("Eribu - Exit to Absu", BASE_ID+13)],
    "Secret Chamber_Upper": [AVLocation("Eribu - Trapclaw Ledge", BASE_ID+14)],
    "Discharge Chamber": [AVLocation("Eribu - Orbital Discharge", BASE_ID+15)],
    "Slug": [AVLocation("??? - Glitchy Slug", BASE_ID+16)],
    "Absu Shaft_Upper": [AVLocation("Absu - Entrance Shaft", BASE_ID+17)],
    "Ventilation_Center": [AVLocation("Absu - Hallway Vault", BASE_ID+18)],
    "Upper Shaft Basement": [AVLocation("Absu - Upper Shaft Basement", BASE_ID+19)],
    "Lower Shaft Basement": [AVLocation("Absu - Lower Shaft Basement", BASE_ID + 20)],
    "Donut Vault": [AVLocation("Absu - Donut Vault", BASE_ID+21)],
    "Attic_West": [AVLocation("Absu - Attic Left Altar", BASE_ID+22)],
    "Attic_Center West": [AVLocation("Absu - Attic Glitch Barriers", BASE_ID+23)],
    "Attic_Center East": [AVLocation("Absu - Attic Mushrooms", BASE_ID+24)],
    "Attic_Upper East": [AVLocation("Absu - Attic Right Altar", BASE_ID+25)],
    "Prison Cellar Secret": [AVLocation("Absu - Basement Spiral", BASE_ID+26)],
    "Elsenova": [AVLocation("Absu - Elsenova", BASE_ID+27)],
    "Prison Tower": [AVLocation("Absu - Jail Cell", BASE_ID+28)],
    "Telal Treasury_West": [AVLocation("Absu - Telal Item", BASE_ID+29)],
    "Telal Secret Access 4": [AVLocation("Absu - Spider Hall", BASE_ID+30)],
    "Telal Exit": [AVLocation("Absu - Behind Telal", BASE_ID+31)],
    "Ducts 1 Secret 3": [AVLocation("Absu - Deep Prison", BASE_ID+32)],
    "Ducts 2": [AVLocation("Absu - On the Block", BASE_ID+33)],
    "Purple Diatoms 1_Upper": [AVLocation("Absu - Donut Shortcut", BASE_ID+34)],
    "Lava Secret": [AVLocation("Absu - Lava Hall", BASE_ID+35)],
    "Green Fungus 1_Upper": [AVLocation("Absu - Green Wall", BASE_ID+36)],
    "Green Fungus 1 Secret 1": [AVLocation("Absu - Past the Crags", BASE_ID+37)],
    "Chasms": [AVLocation("Absu - Chasms", BASE_ID+38)],
    "Fungus Forest": [AVLocation("Absu - Remote Detonation", BASE_ID+39)],
    "Fungus Shrine": [AVLocation("Absu - Glitchy Mushrooms", BASE_ID+40)],
    "Absu to Zi": [AVLocation("Absu - Spider Nest", BASE_ID+41)],
    "Steam Room 2_Upper": [AVLocation("Zi - Behind the Blocks", BASE_ID+42)],
    "Central Access": [AVLocation("Zi - Blue Attic", BASE_ID+43)],
    "Eye Stalk Secret 2": [AVLocation("Zi - Past the Furglots", BASE_ID+44)],
    "Arterial Access": [AVLocation("Zi - Orange Ceiling", BASE_ID+45)],
    "Arterial Shaft": [AVLocation("Zi - Under the Shaft", BASE_ID+46)],
    "Veruska Basement": [AVLocation("Zi - Veruska Right Item", BASE_ID+47)],
    "Veruska Secret": [AVLocation("Zi - Veruska Left Item", BASE_ID+48)],
    "Steam 1 Secret": [AVLocation("Zi - Past the Mutants", BASE_ID+49)],
    "Arterial Filtration": [AVLocation("Zi - Taunting Chamber", BASE_ID+50)],
    "Arterial Bypass Entrance": [AVLocation("Zi - Purple Ceiling", BASE_ID+51)],
    "Venous Maintenance 3": [AVLocation("Zi - Drone Safari Upper Item", BASE_ID+52)],
    "Venous Maintenance Secret": [AVLocation("Zi - Drone Safari Lower Item", BASE_ID+53)],
    "Uruku_Main": [AVLocation("Zi - Uruku Box Item", BASE_ID+54)],
    "Filtration_Upper": [AVLocation("Zi - Uruku Upper Item", BASE_ID+55)],
    "Labcoat Room": [AVLocation("Zi - Uruku Lower Item", BASE_ID+56)]
}

av_locations_unpacked = {}
for locationgroup in axiom_verge_locations.values():
    for location in locationgroup:
        assert location.name not in av_locations_unpacked
        av_locations_unpacked[location.name] = location.code
