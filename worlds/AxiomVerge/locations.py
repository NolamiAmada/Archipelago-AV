from BaseClasses import Location, CollectionState, Entrance
from . import logicfunction
from .logicfunction import LogicInfo
from typing import NamedTuple, Callable, Optional


class AVLocation(NamedTuple):
    name: str
    code: Optional[int]
    logic: Callable[[LogicInfo], Callable[[CollectionState], bool]] = lambda logic_info: Entrance.access_rule


BASE_ID = 332200000
axiom_verge_locations = {
    "Infection Sequence": [AVLocation("Infection Sequence", None, logic=logicfunction.anyweapon and (logicfunction.trenchcoat or (logicfunction.fielddisruptor and logicfunction.anycoat)))],
    "Athetos": [AVLocation("Athetos Defeated", None, logic=logicfunction.longweapon and logicfunction.anyupnoceiling)],
    "Disruptor Room_East": [AVLocation("Eribu - Starter Weapon", BASE_ID+0)],
    "Nova Room": [AVLocation("Eribu - Nova", BASE_ID+1, logic=logicfunction.breakblock)],
    "False Reflector": [AVLocation("Eribu - Corrupted Tower", BASE_ID+2, logic=logicfunction.trenchcoat or logicfunction.shortdrone or logicfunction.grapple)],
    "Bubbled Altar": [AVLocation("Eribu - Bubble Altar", BASE_ID+3, logic=logicfunction.breakblock)],
    "Multi Disruptor_Lower": [AVLocation("Eribu - Multi Disruptor", BASE_ID+4)],
    "Forbidden Corridor_West": [AVLocation("Eribu - Password Hall", BASE_ID+5)],
    "Drill Room_Upper": [AVLocation("Eribu - Drill", BASE_ID+6, logic=logicfunction.breakblock)],
    "Xedur Basement_West": [AVLocation("Eribu - Under Xedur", BASE_ID+7, logic=logicfunction.drill)],
    "Wheelchair": [AVLocation("Eribu - Faded Note", BASE_ID+8)],
    "Primordial Cavern_Center": [AVLocation("Eribu - Primordial Cavern", BASE_ID+9)],
    "Flamethrower Room": [AVLocation("Eribu - Flamethrower", BASE_ID+10, logic=logicfunction.passcodetool and logicfunction.redcoat)],
    "Weapons Vault": [AVLocation("Eribu - Lightning Gun", BASE_ID+11, logic=logicfunction.drone)],
    "Eribu to Indi_East": [AVLocation("Eribu - Exit to Indi", BASE_ID+12, logic=(logicfunction.shortdrone and logicfunction.anycoat) or (logicfunction.redcoat and logicfunction.grapple))],
    "Bubblewrap": [AVLocation("Eribu - Exit to Absu", BASE_ID+13)],
    "Secret Chamber_Upper": [AVLocation("Eribu - Trapclaw Ledge", BASE_ID+14)],
    "Discharge Chamber": [AVLocation("Eribu - Orbital Discharge", BASE_ID+15, logic=logicfunction.grapple or logicfunction.shortdrone or logicfunction.longwarp)],
    "Slug": [AVLocation("??? - Glitchy Slug", BASE_ID+16, logic=logicfunction.anyglitch)],
    "Absu Shaft_Upper": [AVLocation("Absu - Entrance Shaft", BASE_ID+17, logic=logicfunction.drill)],
    "Ventilation_Center": [AVLocation("Absu - Hallway Vault", BASE_ID+18, logic=logicfunction.anycoat or logicfunction.shortpierce)],
    "Upper Shaft Basement": [AVLocation("Absu - Shaft Basement", BASE_ID+19)],
    "Lower Shaft Basement": [AVLocation("Absu - Data Bomb", BASE_ID + 20)],
    "Donut Vault": [AVLocation("Absu - Glitch the Donuts", BASE_ID+21, logic=logicfunction.redcoat or (logicfunction.anyglitch and (logicfunction.anycoat or logicfunction.shortpierce)))],
    "Attic_West": [AVLocation("Absu - Attic Left Altar", BASE_ID+22)],
    "Attic_Center West": [AVLocation("Absu - Attic Glitch Barriers", BASE_ID+23)],
    "Attic_Center East": [AVLocation("Absu - Attic Mushrooms", BASE_ID+24)],
    "Attic_Upper East": [AVLocation("Absu - Attic Right Altar", BASE_ID+25)],
    "Prison Cellar Secret": [AVLocation("Absu - Basement Spiral", BASE_ID+26)],
    "Elsenova": [AVLocation("Absu - Elsenova", BASE_ID+27)],
    "Prison Tower": [AVLocation("Absu - Jail Cell", BASE_ID+28, logic=logicfunction.anycoat)],
    "Telal Treasury_West": [AVLocation("Absu - Address Disruptor 1", BASE_ID+29, logic=logicfunction.breakblock)],
    "Telal Secret Access 4": [AVLocation("Absu - Spider Hall", BASE_ID+30, logic=logicfunction.anyweapon)],
    "Telal Exit": [AVLocation("Absu - Behind Telal", BASE_ID+31)],
    "Ducts 1 Secret 3": [AVLocation("Absu - Deep Prison", BASE_ID+32)],
    "Ducts 2": [AVLocation("Absu - A Block too High", BASE_ID+33, logic=(logicfunction.drill or logicfunction.trenchcoat) and ((logicfunction.trenchcoat or logicfunction.shortdrone or logicfunction.grapple) or logicfunction.anyglitch))],
    "Purple Diatoms 1_Upper": [AVLocation("Absu - Donut Shortcut", BASE_ID+34, logic=logicfunction.drill or logicfunction.anyglitch)],
    "Lava Secret": [AVLocation("Absu - Lava Hall", BASE_ID+35)],
    "Green Fungus 1_Upper": [AVLocation("Absu - Inconspicuous Wall", BASE_ID+36, logic=logicfunction.drill)],
    "Green Fungus 1 Secret 1": [AVLocation("Absu - Through the Crags", BASE_ID+37)],
    "Chasms": [AVLocation("Absu - Chasms", BASE_ID+38, logic=logicfunction.redcoat or logicfunction.drone)],
    "Fungus Forest": [AVLocation("Absu - Remote Detonation", BASE_ID+39, logic=logicfunction.drill and (logicfunction.anycoat or (logicfunction.anyglitch and logicfunction.breakblock) or logicfunction.longpierce))],
    "Fungus Shrine": [AVLocation("Absu - Inertial Pulse", BASE_ID+40, logic=logicfunction.redcoat or (logicfunction.glitch2 and logicfunction.drill))],
    "Absu to Zi": [AVLocation("Absu - Spider Nest", BASE_ID+41, logic=logicfunction.drill)],
    "Steam Room 2_Upper": [AVLocation("Zi - Steam Room", BASE_ID+42, logic=logicfunction.anycoat)],
    "Central Access": [AVLocation("Zi - Blue Hall Ceiling", BASE_ID+43, logic=logicfunction.drill and logicfunction.anyupnoceiling)],
    "Eye Stalk Secret 2": [AVLocation("Zi - Sucker Hall", BASE_ID+44, logic=logicfunction.trenchcoat or logicfunction.anyweapon)],
    "Arterial Access": [AVLocation("Zi - Orange Hall Ceiling", BASE_ID+45, logic=(logicfunction.anyup and logicfunction.anyweapon) or logicfunction.trenchcoat)],
    "Arterial Shaft": [AVLocation("Zi - Under the Shaft", BASE_ID+46, logic=logicfunction.drone or logicfunction.trenchcoat)],
    "Veruska Basement": [AVLocation("Zi - Veruska Right Item", BASE_ID+47)],
    "Veruska Secret": [AVLocation("Zi - Veruska Left Item", BASE_ID+48)],
    "Steam 1 Secret": [AVLocation("Zi - Lower Bioflux Accelerator", BASE_ID+49)],
    "Arterial Filtration": [AVLocation("Zi - VIP Box", BASE_ID+50, logic=logicfunction.anyup and logicfunction.anycoat)],
    "Arterial Bypass Entrance": [AVLocation("Zi - Purple Hall Ceiling", BASE_ID+51, logic=logicfunction.drill and logicfunction.anyup)],
    "Venous Maintenance 3": [AVLocation("Zi - Above Voranj", BASE_ID+52)],
    "Venous Maintenance Secret": [AVLocation("Zi - Voranj", BASE_ID+53, logic=logicfunction.breakblock)],
    "Uruku_Upper": [AVLocation("Zi - Uruku", BASE_ID+54, logic=logicfunction.anycoat)],
    "Filtration_Upper": [AVLocation("Zi - Filter Ceiling", BASE_ID+55, logic=logicfunction.dronefly or logicfunction.grapple or (logicfunction.longdrone and (logicfunction.redcoat or (logicfunction.trenchcoat and logicfunction.fielddisruptor))))],
    "Labcoat Room": [AVLocation("Zi - Labcoat", BASE_ID+56, logic=logicfunction.anyup)],
    "Kur Shaft_Transit": [AVLocation("Kur - Main Shaft", BASE_ID+57)],
    "Address Disruptor 2_Secret": [AVLocation("Kur - Address Disruptor 2", BASE_ID+58)],
    "Cavern Access_Main": [AVLocation("Kur - Tunnel Bore", BASE_ID+59, logic=logicfunction.drone)],
    "High Jump Access_Upper": [AVLocation("Kur - Firewall", BASE_ID+60, logic=logicfunction.anyup or logicfunction.drone)],
    "Tethered Charge": [AVLocation("Kur - Tethered Charge", BASE_ID+61)],
    "Indi to Eribu": [AVLocation("Indi - Ceiling", BASE_ID+62, logic=logicfunction.drone)],
    "Indi to Edin": [AVLocation("Indi - Box", BASE_ID+63, logic=logicfunction.trenchcoat)],
    "Left Leg Shaft_Lower_Upper": [AVLocation("Ukkin-Na - Robot Step Stool", BASE_ID+64)],
    "Left Leg Shaft_Transit": [AVLocation("Ukkin-Na - A Long Fall", BASE_ID+65, logic=logicfunction.breakblock or logicfunction.infectiondone)],
    "Left Leg Shaft_Upper_Center": [AVLocation("Ukkin-Na - After Infection", BASE_ID+66, logic=logicfunction.infectiondone)],
    "Ophelia's Attic": [AVLocation("Ukkin-Na - Above Ophelia", BASE_ID+67, logic=logicfunction.infectiondone and (logicfunction.redcoat or logicfunction.shortdrone or (logicfunction.longwarp or (logicfunction.grapple and (logicfunction.fielddisruptor or logicfunction.trenchcoat)))))],
    "Entrance to Madness_Lower": [AVLocation("Ukkin-Na - Start of Infection", BASE_ID+68, logic=logicfunction.redcoat or logicfunction.trenchcoat and (logicfunction.scissorbeam or logicfunction.fatbeam))],
    "Ukkin-Na Hidden Item": [AVLocation("Ukkin-Na - Past the Slugs", BASE_ID+69, logic=logicfunction.drone)],
    "Trenchcoat Chamber_Upper": [AVLocation("Ukkin-Na - Trenchcoat", BASE_ID+70)],
    "Trenchcoat Chamber_Lower": [AVLocation("Ukkin-Na - Under Trenchcoat", BASE_ID+71, logic=logicfunction.trenchcoat)],
    "Living Room of Illusion": [AVLocation("Ukkin-NA - Floorbreakers", BASE_ID+72, logic=logicfunction.anyup and logicfunction.drone and (logicfunction.redcoat or logicfunction.glitch2))],
    "Vision_Lower": [AVLocation("Ukkin-Na - Definetely a Boss Room", BASE_ID+73, logic=logicfunction.trenchcoat and logicfunction.drone)],
    "Peak": [AVLocation("Ukkin-Na - Turbine Pulse", BASE_ID+74, logic=logicfunction.drill)],
    "Bioflux Shaft 1_Upper": [AVLocation("Mar-Uru - After Sentinel", BASE_ID+75, logic=logicfunction.anyup)],
    "Bioflux 2 Secret": [
        AVLocation("Mar-Uru - Quantum Turret", BASE_ID+76, logic=logicfunction.glitch2),
        AVLocation("Mar-Uru - Quantum Turret Basement", BASE_ID+77, logic=logicfunction.glitch2 and logicfunction.redcoat),
        AVLocation("Mar-Uru - Quantum Turret Secret", BASE_ID+78, logic=logicfunction.glitch2 and logicfunction.redcoat)
    ],
    "Hybrid Room": [AVLocation("Mar-Uru - Hallway Floor", BASE_ID+79, logic=logicfunction.redcoat)],
    "Blue and Purple Corridor_West": [AVLocation("Mar-Uru - Before Reverse Slicer", BASE_ID+80)],
    "Secret Item": [AVLocation("Mar-Uru - Reverse Slicer", BASE_ID+81)],
    "Athetos Foyer Shaft_Center": [AVLocation("Mar-Uru - Before Athetos", BASE_ID+82, logic=logicfunction.drone)]
}

av_locations_unpacked = {}
for locationgroup in axiom_verge_locations.values():
    for location in locationgroup:
        assert location.name not in av_locations_unpacked
        av_locations_unpacked[location.name] = location
