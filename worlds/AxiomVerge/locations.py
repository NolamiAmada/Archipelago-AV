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
    "Infection Sequence": [AVLocation("Infection Sequence", None, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state) and (logicfunction.trenchcoat(logic_info)(state) or (logicfunction.fielddisruptor(logic_info)(state) and logicfunction.anycoat(logic_info)(state)))))],
    "Athetos": [AVLocation("Athetos Defeated", None, logic=lambda logic_info: (lambda state: logicfunction.longweapon(logic_info)(state) and logicfunction.anyupnoceiling(logic_info)(state)))],
    "Disruptor Room_East": [AVLocation("Eribu - Starter Weapon", BASE_ID+0)],
    "Nova Room": [AVLocation("Eribu - Nova", BASE_ID+1, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state)))],
    "False Reflector": [AVLocation("Eribu - Corrupted Tower", BASE_ID+2, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.grapple(logic_info)(state)))],
    "Bubbled Altar": [AVLocation("Eribu - Bubble Altar", BASE_ID+3, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state)))],
    "Multi Disruptor_Lower": [AVLocation("Eribu - Multi Disruptor", BASE_ID+4)],
    "Forbidden Corridor_West": [AVLocation("Eribu - Password Hall", BASE_ID+5)],
    "Drill Room_Upper": [AVLocation("Eribu - Drill", BASE_ID+6, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state)))],
    "Xedur Basement_West": [AVLocation("Eribu - Under Xedur", BASE_ID+7, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Wheelchair": [AVLocation("Eribu - Faded Note", BASE_ID+8)],
    "Primordial Cavern_Center": [AVLocation("Eribu - Primordial Cavern", BASE_ID+9)],
    "Flamethrower Room": [AVLocation("Eribu - Flamethrower", BASE_ID+10, logic=lambda logic_info: (lambda state: logicfunction.passcodetool(logic_info)(state) and logicfunction.redcoat(logic_info)(state)))],
    "Weapons Vault": [AVLocation("Eribu - Lightning Gun", BASE_ID+11, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))],
    "Eribu to Indi_East": [AVLocation("Eribu - Exit to Indi", BASE_ID+12, logic=lambda logic_info: (lambda state: (logicfunction.shortdrone(logic_info)(state) and logicfunction.anycoat(logic_info)(state)) or (logicfunction.redcoat(logic_info)(state) and logicfunction.grapple(logic_info)(state))))],
    "Bubblewrap": [AVLocation("Eribu - Exit to Absu", BASE_ID+13)],
    "Secret Chamber_Upper": [AVLocation("Eribu - Trapclaw Ledge", BASE_ID+14)],
    "Discharge Chamber": [AVLocation("Eribu - Orbital Discharge", BASE_ID+15, logic=lambda logic_info: (lambda state: logicfunction.grapple(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.longwarp(logic_info)(state)))],
    "Slug": [AVLocation("??? - Glitchy Slug", BASE_ID+16, logic=lambda logic_info: (lambda state: logicfunction.anyglitch(logic_info)(state)))],
    "Absu Shaft_Upper": [AVLocation("Absu - Entrance Shaft", BASE_ID+17, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Ventilation_Center": [AVLocation("Absu - Hallway Vault", BASE_ID+18, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.shortpierce(logic_info)(state)))],
    "Upper Shaft Basement": [AVLocation("Absu - Shaft Basement", BASE_ID+19)],
    "Lower Shaft Basement": [AVLocation("Absu - Data Bomb", BASE_ID + 20)],
    "Donut Vault": [AVLocation("Absu - Glitch the Donuts", BASE_ID+21, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.anyglitch(logic_info)(state) and (logicfunction.anycoat(logic_info)(state) or logicfunction.shortpierce(logic_info)(state)))))],
    "Attic_West": [AVLocation("Absu - Attic Left Altar", BASE_ID+22)],
    "Attic_Center West": [AVLocation("Absu - Attic Glitch Barriers", BASE_ID+23)],
    "Attic_Center East": [AVLocation("Absu - Attic Mushrooms", BASE_ID+24)],
    "Attic_Upper East": [AVLocation("Absu - Attic Right Altar", BASE_ID+25)],
    "Prison Cellar Secret": [AVLocation("Absu - Basement Spiral", BASE_ID+26)],
    "Elsenova": [AVLocation("Absu - Elsenova", BASE_ID+27)],
    "Prison Tower": [AVLocation("Absu - Jail Cell", BASE_ID+28, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state)))],
    "Telal Treasury_West": [AVLocation("Absu - Address Disruptor 1", BASE_ID+29, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state)))],
    "Telal Secret Access 4": [AVLocation("Absu - Spider Hall", BASE_ID+30, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state)))],
    "Telal Exit": [AVLocation("Absu - Behind Telal", BASE_ID+31)],
    "Ducts 1 Secret 3": [AVLocation("Absu - Deep Prison", BASE_ID+32)],
    "Ducts 2": [AVLocation("Absu - A Block too High", BASE_ID+33, logic=lambda logic_info: (lambda state: (logicfunction.drill(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)) and ((logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.grapple(logic_info)(state)) or logicfunction.anyglitch(logic_info)(state))))],
    "Purple Diatoms 1_Upper": [AVLocation("Absu - Donut Shortcut", BASE_ID+34, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) or logicfunction.anyglitch(logic_info)(state)))],
    "Lava Secret": [AVLocation("Absu - Lava Hall", BASE_ID+35)],
    "Green Fungus 1_Upper": [AVLocation("Absu - Inconspicuous Wall", BASE_ID+36, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Green Fungus 1 Secret 1": [AVLocation("Absu - Through the Crags", BASE_ID+37)],
    "Chasms": [AVLocation("Absu - Chasms", BASE_ID+38, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.drone(logic_info)(state)))],
    "Fungus Forest": [AVLocation("Absu - Remote Detonation", BASE_ID+39, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) and (logicfunction.anycoat(logic_info)(state) or (logicfunction.anyglitch(logic_info)(state) and logicfunction.breakblock(logic_info)(state)) or logicfunction.longpierce(logic_info)(state))))],
    "Fungus Shrine": [AVLocation("Absu - Inertial Pulse", BASE_ID+40, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.glitch2(logic_info)(state) and logicfunction.drill(logic_info)(state))))],
    "Absu to Zi": [AVLocation("Absu - Spider Nest", BASE_ID+41, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Steam Room 2_Upper": [AVLocation("Zi - Steam Room", BASE_ID+42, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state)))],
    "Central Access": [AVLocation("Zi - Blue Hall Ceiling", BASE_ID+43, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) and logicfunction.anyupnoceiling(logic_info)(state)))],
    "Eye Stalk Secret 2": [AVLocation("Zi - Sucker Hall", BASE_ID+44, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.anyweapon(logic_info)(state)))],
    "Arterial Access": [AVLocation("Zi - Orange Hall Ceiling", BASE_ID+45, logic=lambda logic_info: (lambda state: (logicfunction.anyup(logic_info)(state) and logicfunction.anyweapon(logic_info)(state)) or logicfunction.trenchcoat(logic_info)(state)))],
    "Arterial Shaft": [AVLocation("Zi - Under the Shaft", BASE_ID+46, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)))],
    "Veruska Basement": [AVLocation("Zi - Veruska Right Item", BASE_ID+47)],
    "Veruska Secret": [AVLocation("Zi - Veruska Left Item", BASE_ID+48)],
    "Steam 1 Secret": [AVLocation("Zi - Lower Bioflux Accelerator", BASE_ID+49)],
    "Arterial Filtration": [AVLocation("Zi - VIP Box", BASE_ID+50, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.anycoat(logic_info)(state)))],
    "Arterial Bypass Entrance": [AVLocation("Zi - Purple Hall Ceiling", BASE_ID+51, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) and logicfunction.anyup(logic_info)(state)))],
    "Venous Maintenance 3": [AVLocation("Zi - Above Voranj", BASE_ID+52)],
    "Venous Maintenance Secret": [AVLocation("Zi - Voranj", BASE_ID+53, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state)))],
    "Uruku_Upper": [AVLocation("Zi - Uruku", BASE_ID+54, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state)))],
    "Filtration_Upper": [AVLocation("Zi - Filter Ceiling", BASE_ID+55, logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or logicfunction.grapple(logic_info)(state) or (logicfunction.longdrone(logic_info)(state) and (logicfunction.redcoat(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state))))))],
    "Labcoat Room": [AVLocation("Zi - Labcoat", BASE_ID+56, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))],
    "Kur Shaft_Transit": [AVLocation("Kur - Main Shaft", BASE_ID+57)],
    "Address Disruptor 2_Secret": [AVLocation("Kur - Address Disruptor 2", BASE_ID+58)],
    "Cavern Access_Main": [AVLocation("Kur - Tunnel Bore", BASE_ID+59, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))],
    "High Jump Access_Upper": [AVLocation("Kur - Firewall", BASE_ID+60, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) or logicfunction.drone(logic_info)(state)))],
    "Tethered Charge": [AVLocation("Kur - Tethered Charge", BASE_ID+61)],
    "Indi to Eribu": [AVLocation("Indi - Ceiling", BASE_ID+62, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))],
    "Indi to Edin": [AVLocation("Indi - Box", BASE_ID+63, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state)))],
    "Left Leg Shaft_Lower_Upper": [AVLocation("Ukkin-Na - Robot Step Stool", BASE_ID+64)],
    "Left Leg Shaft_Transit": [AVLocation("Ukkin-Na - A Long Fall", BASE_ID+65, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state) or logicfunction.infectiondone(logic_info)(state)))],
    "Left Leg Shaft_Upper_Center": [AVLocation("Ukkin-Na - After Infection", BASE_ID+66, logic=lambda logic_info: (lambda state: logicfunction.infectiondone(logic_info)(state)))],
    "Ophelia's Attic": [AVLocation("Ukkin-Na - Above Ophelia", BASE_ID+67, logic=lambda logic_info: (lambda state: logicfunction.infectiondone(logic_info)(state) and (logicfunction.redcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.longwarp(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and (logicfunction.fielddisruptor(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)))))))],
    "Entrance to Madness_Lower": [AVLocation("Ukkin-Na - Start of Infection", BASE_ID+68, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state) and (logicfunction.scissorbeam(logic_info)(state) or logicfunction.fatbeam(logic_info)(state))))],
    "Ukkin-Na Hidden Item": [AVLocation("Ukkin-Na - Past the Slugs", BASE_ID+69, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))],
    "Trenchcoat Chamber_Upper": [AVLocation("Ukkin-Na - Trenchcoat", BASE_ID+70)],
    "Trenchcoat Chamber_Lower": [AVLocation("Ukkin-Na - Under Trenchcoat", BASE_ID+71, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state)))],
    "Living Room of Illusion": [AVLocation("Ukkin-Na - Floorbreakers", BASE_ID+72, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.drone(logic_info)(state) and (logicfunction.redcoat(logic_info)(state) or logicfunction.glitch2(logic_info)(state))))],
    "Vision_Lower": [AVLocation("Ukkin-Na - Definetely a Boss Room", BASE_ID+73, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.drone(logic_info)(state)))],
    "Peak": [AVLocation("Ukkin-Na - Turbine Pulse", BASE_ID+74, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Bioflux Shaft 1_Upper": [AVLocation("Mar-Uru - After Sentinel", BASE_ID+75, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))],
    "Bioflux 2 Secret": [
        AVLocation("Mar-Uru - Quantum Turret", BASE_ID+76, logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state))),
        AVLocation("Mar-Uru - Quantum Turret Basement", BASE_ID+77, logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) and logicfunction.redcoat(logic_info)(state))),
        AVLocation("Mar-Uru - Quantum Turret Secret", BASE_ID+78, logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) and logicfunction.redcoat(logic_info)(state))
    )],
    "Hybrid Room": [AVLocation("Mar-Uru - Hallway Floor", BASE_ID+79, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state)))],
    "Blue and Purple Corridor_West": [AVLocation("Mar-Uru - Before Reverse Slicer", BASE_ID+80)],
    "Secret Item": [AVLocation("Mar-Uru - Reverse Slicer", BASE_ID+81)],
    "Athetos Foyer Shaft_Center": [AVLocation("Mar-Uru - Before Athetos", BASE_ID+82, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))],
    "Edin to Ukkin-Na_West": [AVLocation("Edin - Near Ukkin-Na", BASE_ID+83, logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.tempup(logic_info)(state) and logicfunction.grapple(logic_info)(state))))],
    "Edin to Ukkin-Na_East": [AVLocation("Edin - Shards", BASE_ID+84, logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state)))],
    "Edin to Ukkin-Na_Center": [AVLocation("Edin - Upper Bioflux Accellerator", BASE_ID+85, logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state)))],
    "Edin to Ukkin-Na_Secret": [AVLocation("Edin - Near Indi", BASE_ID+86)],
    "Hangar Basement Entrance_Upper": [AVLocation("Edin - Near Hangar", BASE_ID+87, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.anyglitch(logic_info)(state) and logicfunction.sevenblockup(logic_info)(state))))],
    "Western Hangar Entrance_Upper": [AVLocation("Edin - West of Distortion Field Upper", BASE_ID+88, logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state))))],
    "Western Hangar Entrance_Center": [AVLocation("Edin - West of Distortion Field Lower", BASE_ID+89, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Hangar Foyer": [AVLocation("Edin - Distortion Field", BASE_ID+90, logic=lambda logic_info: (lambda state: logicfunction.anyglitch(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state) and (logicfunction.dronefly(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.shortdrone(logic_info)(state) and (logicfunction.redcoat(logic_info)(state) or logicfunction.longdrone(logic_info)(state))))))], # item not present sometimes? maybe give command related?
    "Hangar_East": [AVLocation("Edin - Address Bomb", BASE_ID+91)],
    "Hangar Attic Right Door": [
        AVLocation("Edin - Wisp Chamber Right Item", BASE_ID+92, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))), # these both need combat logic realistically
        AVLocation("Edin - Wisp Chamber Left Item", BASE_ID+93, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state)))
    ],
    "West Tower Level 1_Upper": [AVLocation("Edin - Hidden Ceiling", BASE_ID+94, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)))],
    "Level 1 Secret": [AVLocation("Edin - Very Real Wall", BASE_ID+95)],
    "Distortion Field Room": [AVLocation("Edin - Drone Teleport Challenge", BASE_ID+96, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)))],
    "West Tower Level 3_East": [AVLocation("Edin - Hole in the Wall", BASE_ID+97, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state))))],
    "Drone Teleport Room_Lower": [AVLocation("Edin - Drone Teleport", BASE_ID+98)],
    "Thorn Maze Secret": [AVLocation("Kur - Hypo Atomizer", BASE_ID+99)],
    "High Jump Room_Main": [AVLocation("Kur - Field Disruptor", BASE_ID+100)],
    "Lair Vestibule": [AVLocation("Kur - Laser Friend", BASE_ID+101, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state) and (logicfunction.anyglitch(logic_info)(state) or logicfunction.redcoat(logic_info)(state)) and (logicfunction.grapple(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.longwarp(logic_info)(state))))],
    "Mountain Back_East": [
        AVLocation("Kur - Grapple", BASE_ID+102),
        AVLocation("Kur - Hidden Above Grapple", BASE_ID+103, logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state)))
    ],
    "Mountain Back_Upper": [AVLocation("Kur - Grapple Room Ledge", BASE_ID+104, logic=lambda logic_info: (lambda state: logicfunction.grapple(logic_info)(state) or logicfunction.dronelaunch(logic_info)(state) or (logicfunction.shortdrone(logic_info)(state) and logicfunction.anycoat(logic_info)(state) and (logicfunction.anyupnodrone(logic_info)(state) or logicfunction.dronefly(logic_info)(state)))))],
    "Secret Lair Shortcut": [AVLocation("Kur - Gir-Tab Bypass", BASE_ID+105, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))]
}

av_locations_unpacked = {}
for locationgroup in axiom_verge_locations.values():
    for location in locationgroup:
        assert location.name not in av_locations_unpacked
        av_locations_unpacked[location.name] = location
