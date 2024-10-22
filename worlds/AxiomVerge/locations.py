from BaseClasses import Location, CollectionState, Entrance
from . import logicfunction
from typing import NamedTuple, Callable


class AVLocation(NamedTuple):
    name: str
    code: int
    logic: Callable[[CollectionState], bool] = Entrance.access_rule


BASE_ID = 332200000
axiom_verge_locations = {
    "Disruptor Room_East": [AVLocation("Eribu - Starter Weapon", BASE_ID+0)],
    "Nova Room": [AVLocation("Eribu - Nova", BASE_ID+1, logic=lambda state: logicfunction.breakblock(state))],
    "False Reflector": [AVLocation("Eribu - Corrupted Tower", BASE_ID+2, logic=lambda state: logicfunction.trenchcoat(state) or logicfunction.shortdrone(state) or state.has("Grapple"))],
    "Bubbled Altar": [AVLocation("Eribu - Bubble Altar", BASE_ID+3, logic=lambda state: logicfunction.breakblock(state))],
    "Multi Disruptor_Lower": [AVLocation("Eribu - Multi Disruptor", BASE_ID+4)],
    "Forbidden Corridor_West": [AVLocation("Eribu - Password Hall", BASE_ID+5)],
    "Drill Room_Upper": [AVLocation("Eribu - Drill", BASE_ID+6, logic=lambda state: logicfunction.breakblock(state))],
    "Xedur Basement_West": [AVLocation("Eribu - Under Xedur", BASE_ID+7, logic=lambda state: logicfunction.drill(state))],
    "Wheelchair": [AVLocation("Eribu - Faded Note", BASE_ID+8)],
    "Primordial Cavern_Center": [AVLocation("Eribu - Primordial Cavern", BASE_ID+9)],
    "Flamethrower Room": [AVLocation("Eribu - Flamethrower", BASE_ID+10, logic=lambda state: state.has("Passcode Tool") and logicfunction.redcoat(state))],
    "Weapons Vault": [AVLocation("Eribu - Lightning Gun", BASE_ID+11, logic=lambda state: logicfunction.drone(state))],
    "Eribu to Indi_East": [AVLocation("Eribu - Exit to Indi", BASE_ID+12, logic=lambda state: (logicfunction.shortdrone(state) and logicfunction.anycoat(state)) or (logicfunction.redcoat(state) and state.has("Grapple")))],
    "Bubblewrap": [AVLocation("Eribu - Exit to Absu", BASE_ID+13)],
    "Secret Chamber_Upper": [AVLocation("Eribu - Trapclaw Ledge", BASE_ID+14)],
    "Discharge Chamber": [AVLocation("Eribu - Orbital Discharge", BASE_ID+15, logic=lambda state: state.has("Grapple") or logicfunction.shortdrone(state) or logicfunction.longwarp(state))],
    "Slug": [AVLocation("??? - Glitchy Slug", BASE_ID+16, logic=lambda state: logicfunction.anyglitch(state))],
    "Absu Shaft_Upper": [AVLocation("Absu - Entrance Shaft", BASE_ID+17, logic=lambda state: logicfunction.drill(state))],
    "Ventilation_Center": [AVLocation("Absu - Hallway Vault", BASE_ID+18, logic=lambda state: logicfunction.anycoat(state) or state.has("ShortPierce"))],
    "Upper Shaft Basement": [AVLocation("Absu - Shaft Basement", BASE_ID+19)],
    "Lower Shaft Basement": [AVLocation("Absu - Data Bomb", BASE_ID + 20)],
    "Donut Vault": [AVLocation("Absu - Glitch the Donuts", BASE_ID+21, logic=lambda state: logicfunction.redcoat(state) or (logicfunction.anyglitch(state) and (logicfunction.anycoat(state) or state.has("ShortPierce"))))],
    "Attic_West": [AVLocation("Absu - Attic Left Altar", BASE_ID+22)],
    "Attic_Center West": [AVLocation("Absu - Attic Glitch Barriers", BASE_ID+23)],
    "Attic_Center East": [AVLocation("Absu - Attic Mushrooms", BASE_ID+24)],
    "Attic_Upper East": [AVLocation("Absu - Attic Right Altar", BASE_ID+25)],
    "Prison Cellar Secret": [AVLocation("Absu - Basement Spiral", BASE_ID+26)],
    "Elsenova": [AVLocation("Absu - Elsenova", BASE_ID+27)],
    "Prison Tower": [AVLocation("Absu - Jail Cell", BASE_ID+28, logic=lambda state: logicfunction.anycoat(state))],
    "Telal Treasury_West": [AVLocation("Absu - Address Disruptor 1", BASE_ID+29, logic=lambda state: logicfunction.breakblock(state))],
    "Telal Secret Access 4": [AVLocation("Absu - Spider Hall", BASE_ID+30, logic=lambda state: state.has("Weapon"))],
    "Telal Exit": [AVLocation("Absu - Behind Telal", BASE_ID+31)],
    "Ducts 1 Secret 3": [AVLocation("Absu - Deep Prison", BASE_ID+32)],
    "Ducts 2": [AVLocation("Absu - A Block too High", BASE_ID+33, logic=lambda state: (logicfunction.drill(state) or logicfunction.trenchcoat(state)) and ((logicfunction.trenchcoat(state) or logicfunction.shortdrone(state) or state.has("Grapple")) or logicfunction.anyglitch(state)))],
    "Purple Diatoms 1_Upper": [AVLocation("Absu - Donut Shortcut", BASE_ID+34, logic=lambda state: logicfunction.drill(state) or logicfunction.anyglitch(state))],
    "Lava Secret": [AVLocation("Absu - Lava Hall", BASE_ID+35)],
    "Green Fungus 1_Upper": [AVLocation("Absu - Inconspicuous Wall", BASE_ID+36, logic=lambda state: logicfunction.drill(state))],
    "Green Fungus 1 Secret 1": [AVLocation("Absu - Through the Crags", BASE_ID+37)],
    "Chasms": [AVLocation("Absu - Chasms", BASE_ID+38, logic=lambda state: logicfunction.redcoat(state) or logicfunction.drone(state))],
    "Fungus Forest": [AVLocation("Absu - Remote Detonation", BASE_ID+39, logic=lambda state: logicfunction.drill(state) and (logicfunction.anycoat(state) or (logicfunction.anyglitch(state) and logicfunction.breakblock(state)) or state.has("LongPierce")))],
    "Fungus Shrine": [AVLocation("Absu - Inertial Pulse", BASE_ID+40, logic=lambda state: logicfunction.redcoat(state) or (logicfunction.glitch2(state) and logicfunction.drill(state)))],
    "Absu to Zi": [AVLocation("Absu - Spider Nest", BASE_ID+41, logic=lambda state: logicfunction.drill(state))],
    "Steam Room 2_Upper": [AVLocation("Zi - Steam Room", BASE_ID+42, logic=lambda state: logicfunction.anycoat(state))],
    "Central Access": [AVLocation("Zi - Blue Hall Ceiling", BASE_ID+43, logic=lambda state: logicfunction.drill(state) and logicfunction.anyupnoceiling(state))],
    "Eye Stalk Secret 2": [AVLocation("Zi - Sucker Hall", BASE_ID+44, logic=lambda state: logicfunction.trenchcoat(state) or state.has("Weapon"))],
    "Arterial Access": [AVLocation("Zi - Orange Hall Ceiling", BASE_ID+45, logic=lambda state: (logicfunction.anyup(state) and state.has("Weapon")) or logicfunction.trenchcoat(state))],
    "Arterial Shaft": [AVLocation("Zi - Under the Shaft", BASE_ID+46, logic=lambda state: logicfunction.drone(state) or logicfunction.trenchcoat(state))],
    "Veruska Basement": [AVLocation("Zi - Veruska Right Item", BASE_ID+47)],
    "Veruska Secret": [AVLocation("Zi - Veruska Left Item", BASE_ID+48)],
    "Steam 1 Secret": [AVLocation("Zi - Lower Bioflux Accelerator", BASE_ID+49)],
    "Arterial Filtration": [AVLocation("Zi - VIP Box", BASE_ID+50, logic=lambda state: logicfunction.anyup(state) and logicfunction.anycoat(state))],
    "Arterial Bypass Entrance": [AVLocation("Zi - Purple Hall Ceiling", BASE_ID+51, logic=lambda state: logicfunction.drill(state) and logicfunction.anyup(state))],
    "Venous Maintenance 3": [AVLocation("Zi - Above Voranj", BASE_ID+52)],
    "Venous Maintenance Secret": [AVLocation("Zi - Voranj", BASE_ID+53, logic=lambda state: logicfunction.breakblock(state))],
    "Uruku_Upper": [AVLocation("Zi - Uruku", BASE_ID+54, logic=lambda state: logicfunction.anycoat(state))],
    "Filtration_Upper": [AVLocation("Zi - Filter Ceiling", BASE_ID+55, logic=lambda state: logicfunction.dronefly(state) or state.has("Grapple") or (logicfunction.longdrone(state) and (logicfunction.redcoat(state) or (logicfunction.trenchcoat(state) and state.has("Field Disruptor")))))],
    "Labcoat Room": [AVLocation("Zi - Labcoat", BASE_ID+56, logic=lambda state: logicfunction.anyup(state))],
    "Kur Shaft_Transit": [AVLocation("Kur - Main Shaft", BASE_ID+57)],
    "Address Disruptor 2_Secret": [AVLocation("Kur - Address Disruptor 2", BASE_ID+58)],
    "Cavern Access_Main": [AVLocation("Kur - Tunnel Bore", BASE_ID+59, logic=lambda state: logicfunction.drone(state))],
    "High Jump Access_Upper": [AVLocation("Kur - Firewall", BASE_ID+60, logic=lambda state: logicfunction.anyup(state) or logicfunction.drone(state))],
    "Tethered Charge": [AVLocation("Kur - Tethered Charge", BASE_ID+61)]
}

av_locations_unpacked = {}
for locationgroup in axiom_verge_locations.values():
    for location in locationgroup:
        assert location.name not in av_locations_unpacked
        av_locations_unpacked[location.name] = location.code
