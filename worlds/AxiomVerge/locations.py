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
    "Nova Room": [AVLocation("Eribu - Right Tower", BASE_ID+1, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state)))],
    "False Reflector": [AVLocation("Eribu - Left Tower", BASE_ID+2, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.grapple(logic_info)(state)))],
    "Bubbled Altar": [AVLocation("Eribu - Bubble Shrine", BASE_ID+3, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state)))],
    "Multi Disruptor_Lower": [AVLocation("Eribu - Outside Upper Passcode Room", BASE_ID+4)],
    "Forbidden Corridor_West": [AVLocation("Eribu - Upper Passcode Room", BASE_ID+5)],
    "Drill Room_Upper": [AVLocation("Eribu - Xedur Reward", BASE_ID+6, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state)))],
    "Xedur Basement_West": [AVLocation("Eribu - Under Xedur", BASE_ID+7, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Wheelchair": [AVLocation("Eribu - Wheelchair Room", BASE_ID+8)],
    "Primordial Cavern_Center": [AVLocation("Eribu - Primordial Cavern", BASE_ID+9)],
    "Flamethrower Room": [AVLocation("Eribu - Flamethrower", BASE_ID+10, logic=lambda logic_info: (lambda state: logicfunction.passcodetool(logic_info)(state) and logicfunction.redcoat(logic_info)(state)))],
    "Weapons Vault": [AVLocation("Eribu - Sentry Bot Tunnel", BASE_ID+11, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))],
    "Eribu to Indi_East": [AVLocation("Eribu - Path to Indi Ceiling", BASE_ID+12, logic=lambda logic_info: (lambda state: (logicfunction.shortdrone(logic_info)(state) and logicfunction.anycoat(logic_info)(state)) or (logicfunction.redcoat(logic_info)(state) and logicfunction.grapple(logic_info)(state))))],
    "Bubblewrap": [AVLocation("Eribu - Path to Absu", BASE_ID+13)],
    "Secret Chamber_Upper": [AVLocation("Eribu - Outside Lower Passcode Room", BASE_ID+14)],
    "Discharge Chamber": [AVLocation("Eribu - Lower Passcode Room", BASE_ID+15, logic=lambda logic_info: (lambda state: logicfunction.grapple(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.longwarp(logic_info)(state)))],
    "Slug": [AVLocation("Glitched Slug Item", BASE_ID+16, logic=lambda logic_info: (lambda state: logicfunction.anyglitch(logic_info)(state)))],
    "Absu Shaft_Upper": [AVLocation("Absu - Entrance Shaft", BASE_ID+17, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Ventilation_Center": [AVLocation("Absu - Switch Cage", BASE_ID+18, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.shortpierce(logic_info)(state)))],
    "Upper Shaft Basement": [AVLocation("Absu - Under Entrance Shaft", BASE_ID+19)],
    "Lower Shaft Basement": [AVLocation("Absu - Deep Under Entrance Shaft", BASE_ID + 20)],
    "Donut Vault": [AVLocation("Absu - Entrance Shaft Vault", BASE_ID+21, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.anyglitch(logic_info)(state) and (logicfunction.anycoat(logic_info)(state) or logicfunction.shortpierce(logic_info)(state)))))],
    "Attic_West": [AVLocation("Absu - Attic Left Shrine", BASE_ID+22)],
    "Attic_Center West": [AVLocation("Absu - Attic Between Glitch Barriers", BASE_ID+23)],
    "Attic_Center East": [AVLocation("Absu - Attic Upper Alcove", BASE_ID+24)],
    "Attic_Upper East": [AVLocation("Absu - Attic Right Shrine", BASE_ID+25)],
    "Prison Cellar Secret": [AVLocation("Absu - Behind Glitch Barrier", BASE_ID+26)],
    "Elsenova": [AVLocation("Absu - Elsenova", BASE_ID+27)],
    "Prison Tower": [AVLocation("Absu - Cell Near Elsenova", BASE_ID+28, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state)))],
    "Telal Treasury_West": [AVLocation("Absu - Telal Reward", BASE_ID+29, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state)))],
    "Telal Secret Access 4": [AVLocation("Absu - Path to Indi Side Room", BASE_ID+30, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state)))],
    "Telal Exit": [AVLocation("Absu - Shaft Behind Telal", BASE_ID+31)],
    "Ducts 1 Secret 3": [AVLocation("Absu - Lowest Point", BASE_ID+32)],
    "Ducts 2": [AVLocation("Absu - Floating Platform", BASE_ID+33, logic=lambda logic_info: (lambda state: (logicfunction.drill(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)) and ((logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.grapple(logic_info)(state)) or logicfunction.anyglitch(logic_info)(state))))],
    "Purple Diatoms 1_Upper": [AVLocation("Absu - Trapped Diatoms", BASE_ID+34, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) or logicfunction.anyglitch(logic_info)(state)))],
    "Lava Secret": [AVLocation("Absu - Lava Hall", BASE_ID+35)],
    "Green Fungus 1_Upper": [AVLocation("Absu - Green Wall Alcove", BASE_ID+36, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Green Fungus 1 Secret 1": [AVLocation("Absu - Hidden Shrine", BASE_ID+37)],
    "Chasms": [AVLocation("Absu - Chasm Room Tunnel", BASE_ID+38, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.drone(logic_info)(state)))],
    "Fungus Forest": [AVLocation("Absu - Gated Alcove", BASE_ID+39, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) and (logicfunction.anycoat(logic_info)(state) or (logicfunction.anyglitch(logic_info)(state) and logicfunction.breakblock(logic_info)(state)) or logicfunction.longpierce(logic_info)(state))))],
    "Fungus Shrine": [AVLocation("Absu - Shrine Behind Glitch", BASE_ID+40, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.glitch2(logic_info)(state) and logicfunction.drill(logic_info)(state))))],
    "Absu to Zi": [AVLocation("Absu - Path to Zi", BASE_ID+41, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Steam Room 2_Upper": [AVLocation("Zi - False Wall Near Lower Save", BASE_ID+42, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state)))],
    "Central Access": [AVLocation("Zi - Ceiling Secret Near Lower Save", BASE_ID+43, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) and logicfunction.anyupnoceiling(logic_info)(state)))],
    "Eye Stalk Secret 2": [AVLocation("Zi - Furglot Tunnel", BASE_ID+44, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.anyweapon(logic_info)(state)))],
    "Arterial Access": [AVLocation("Zi - False Ceiling Alcove", BASE_ID+45, logic=lambda logic_info: (lambda state: (logicfunction.anyup(logic_info)(state) and logicfunction.anyweapon(logic_info)(state)) or logicfunction.trenchcoat(logic_info)(state)))],
    "Arterial Shaft": [AVLocation("Zi - Above Veruska", BASE_ID+46, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)))],
    "Veruska Basement": [AVLocation("Zi - Below Veruska Right", BASE_ID+47)],
    "Veruska Secret": [AVLocation("Zi - Below Veruska Left", BASE_ID+48)],
    "Steam 1 Secret": [AVLocation("Zi - Disappointment Hill", BASE_ID+49)],
    "Arterial Filtration": [AVLocation("Zi - Preview Room", BASE_ID+50, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.anycoat(logic_info)(state)))],
    "Arterial Bypass Entrance": [AVLocation("Zi - Ceiling Secret Near Preview Room", BASE_ID+51, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) and logicfunction.anyup(logic_info)(state)))],
    "Venous Maintenance 3": [AVLocation("Zi - Drone Quest Upper", BASE_ID+52)],
    "Venous Maintenance Secret": [AVLocation("Zi - Drone Quest Lower", BASE_ID+53, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state)))],
    "Uruku_Upper": [AVLocation("Zi - Uruku Cage", BASE_ID+54, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state)))],
    "Filtration_Upper": [AVLocation("Zi - Behind Uruku Ceiling Ledge", BASE_ID+55, logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or logicfunction.grapple(logic_info)(state) or (logicfunction.longdrone(logic_info)(state) and (logicfunction.redcoat(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state))))))],
    "Labcoat Room": [AVLocation("Zi - Uruku Reward", BASE_ID+56, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))],
    "Kur Shaft_Transit": [AVLocation("Kur - Main Shaft", BASE_ID+57)],
    "Address Disruptor 2_Secret": [AVLocation("Kur - Address Disruptor 2", BASE_ID+58)],
    "Cavern Access_Main": [AVLocation("Kur - Drone Tunnel Before Gauntlet", BASE_ID+59, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))],
    "High Jump Access_Upper": [AVLocation("Kur - High Jump Shrine False Wall", BASE_ID+60, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) or logicfunction.drone(logic_info)(state)))],
    "Tethered Charge": [AVLocation("Kur - Gauntlet Reward", BASE_ID+61)],
    "Indi to Eribu": [AVLocation("Indi - Path to Eribu", BASE_ID+62, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))],
    "Indi to Edin": [AVLocation("Indi - Outside Save", BASE_ID+63, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state)))],
    "Left Leg Shaft_Lower_Upper": [AVLocation("Ukkin-Na - Below Long Fall", BASE_ID+64)],
    "Left Leg Shaft_Transit": [AVLocation("Ukkin-Na - Long Fall", BASE_ID+65, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state) or logicfunction.infectiondone(logic_info)(state)))],
    "Left Leg Shaft_Upper_Center": [AVLocation("Ukkin-Na - Outside Ophelia", BASE_ID+66, logic=lambda logic_info: (lambda state: logicfunction.infectiondone(logic_info)(state)))],
    "Ophelia's Attic": [AVLocation("Ukkin-Na - Above Ophelia", BASE_ID+67, logic=lambda logic_info: (lambda state: logicfunction.infectiondone(logic_info)(state) and (logicfunction.redcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.longwarp(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and (logicfunction.fielddisruptor(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)))))))],
    "Entrance to Madness_Lower": [AVLocation("Ukkin-Na - Secret Room Above Lower Save", BASE_ID+68, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state) and (logicfunction.scissorbeam(logic_info)(state) or logicfunction.fatbeam(logic_info)(state))))],
    "Ukkin-Na Hidden Item": [AVLocation("Ukkin-Na - Past the Slugs", BASE_ID+69, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))],
    "Trenchcoat Chamber_Upper": [AVLocation("Ukkin-Na - Midway Shaft Upper", BASE_ID+70)],
    "Trenchcoat Chamber_Lower": [AVLocation("Ukkin-Na - Midway Shaft Lower", BASE_ID+71, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state)))],
    "Living Room of Illusion": [AVLocation("Ukkin-Na - Secret Room Below Upper Save", BASE_ID+72, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.drone(logic_info)(state) and (logicfunction.redcoat(logic_info)(state) or logicfunction.glitch2(logic_info)(state))))],
    "Vision_Lower": [AVLocation("Ukkin-Na - Vision Room Tunnel", BASE_ID+73, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.drone(logic_info)(state)))],
    "Peak": [AVLocation("Ukkin-Na - Turbine Pulse", BASE_ID+74, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Bioflux Shaft 1_Upper": [AVLocation("Mar-Uru - Sentinel Reward", BASE_ID+75, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))],
    "Bioflux 2 Secret": [
        AVLocation("Mar-Uru - Quantum Sentinel", BASE_ID+76, logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state))),
        AVLocation("Mar-Uru - Quantum Sentinel Basement", BASE_ID+77, logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) and logicfunction.redcoat(logic_info)(state))),
        AVLocation("Mar-Uru - Quantum Sentinel Basement Secret", BASE_ID+78, logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) and logicfunction.redcoat(logic_info)(state))
    )],
    "Hybrid Room": [AVLocation("Mar-Uru - Inside Corridor Block", BASE_ID+79, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state)))],
    "Blue and Purple Corridor_West": [AVLocation("Mar-Uru - Before Laser Bot Puzzle", BASE_ID+80)],
    "Secret Item": [AVLocation("Mar-Uru - Laser Bot Puzzle", BASE_ID+81)],
    "Athetos Foyer Shaft_Center": [AVLocation("Mar-Uru - Athetos Ascent Drone Tunnel", BASE_ID+82, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))],
    "Edin to Ukkin-Na_West": [AVLocation("Edin - Ceiling Near Ukkin-Na", BASE_ID+83, logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.tempup(logic_info)(state) and logicfunction.grapple(logic_info)(state))))],
    "Edin to Ukkin-Na_East": [AVLocation("Edin - Central Ruins Glitch Alcove", BASE_ID+84, logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state)))],
    "Edin to Ukkin-Na_Center": [AVLocation("Edin - Sky Cage", BASE_ID+85, logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state)))],
    "Edin to Ukkin-Na_Secret": [AVLocation("Edin - Near Indi", BASE_ID+86)],
    "Hangar Basement Entrance_Upper": [AVLocation("Edin - Near Hangar", BASE_ID+87, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.anyglitch(logic_info)(state) and logicfunction.sevenblockup(logic_info)(state))))],
    "Western Hangar Entrance_Upper": [AVLocation("Edin - Clone Path Rooftop Ledge", BASE_ID+88, logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state))))],
    "Western Hangar Entrance_Center": [AVLocation("Edin - Clone Path Inside Blocks", BASE_ID+89, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Hangar Foyer": [AVLocation("Edin - Clone Path Before Save", BASE_ID+90, logic=lambda logic_info: (lambda state: logicfunction.anyglitch(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state) and (logicfunction.dronefly(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.shortdrone(logic_info)(state) and (logicfunction.redcoat(logic_info)(state) or logicfunction.longdrone(logic_info)(state))))))], # item not present sometimes? maybe give command related?
    "Hangar_East": [AVLocation("Edin - Main Hangar", BASE_ID+91)],
    "Hangar Attic Right Door": [
        AVLocation("Edin - Double Check Tunnel Right", BASE_ID+92, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))), # these both need combat logic realistically
        AVLocation("Edin - Double Check Tunnel Left", BASE_ID+93, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state)))
    ],
    "West Tower Level 1_Upper": [AVLocation("Edin - Ukhu Path Drone Tunnel", BASE_ID+94, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)))],
    "Level 1 Secret": [AVLocation("Edin - False Wall Shrine", BASE_ID+95)],
    "Distortion Field Room": [AVLocation("Edin - Ukhu Path Side Room", BASE_ID+96, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)))],
    "West Tower Level 3_East": [AVLocation("Edin - Ukhu Path Ruins", BASE_ID+97, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state))))],
    "Drone Teleport Room_Lower": [AVLocation("Edin - Ukhu Reward", BASE_ID+98)],
    "Thorn Maze Secret": [AVLocation("Kur - Drone Side Quest", BASE_ID+99)],
    "High Jump Room_Main": [AVLocation("Kur - High Jump Shrine", BASE_ID+100)],
    "Lair Vestibule": [AVLocation("Kur - Gir-Tab Lower Entrance Drone Tunnel", BASE_ID+101, logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state) and (logicfunction.anyglitch(logic_info)(state) or logicfunction.redcoat(logic_info)(state)) and (logicfunction.grapple(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.longwarp(logic_info)(state))))],
    "Mountain Back_East": [
        AVLocation("Kur - Cliffs Behind Gir-Tab Shrine", BASE_ID+102),
        AVLocation("Kur - Cliffs Behind Gir-Tab Above Shrine", BASE_ID+103, logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state)))
    ],
    "Mountain Back_Upper": [AVLocation("Kur - Cliffs Behind Gir-Tab Near Crumble Floor", BASE_ID+104, logic=lambda logic_info: (lambda state: logicfunction.grapple(logic_info)(state) or logicfunction.dronelaunch(logic_info)(state) or (logicfunction.shortdrone(logic_info)(state) and logicfunction.anycoat(logic_info)(state) and (logicfunction.anyupnodrone(logic_info)(state) or logicfunction.dronefly(logic_info)(state)))))],
    "Secret Lair Shortcut": [AVLocation("Kur - Gir-Tab Upper Entrance", BASE_ID+105, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))],
    "Mountain Slope_Item": [AVLocation("Kur - Watch for Rolling Rocks", BASE_ID+106)],
    "Mountain Slope_East": [AVLocation("Kur - Inside Cliff", BASE_ID+107, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state)))],
    "Drone Room_Lower": [AVLocation("Kur - Above Twin Save Rooms", BASE_ID+108)],
    "Ice Crags_SecretEast": [AVLocation("Kur - Shrine Before Drone Odyssey", BASE_ID+109)],
    "Ice Crags_SecretWest": [AVLocation("Kur - Snowy Cliffs Ledge Lower", BASE_ID+110)],
    "Ice Crags_SecretUpper": [AVLocation("Kur - Snowy Cliffs Ledge Upper", BASE_ID+111)],
    "Reflector Room": [AVLocation("Kur - Drone Odyssey Reward", BASE_ID+112)],
    "Hidden Stalagmite": [AVLocation("Kur - Drone Odyssey Secret", BASE_ID+113, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Improved Launch Room": [AVLocation("Kur - Loop Room", BASE_ID+114)],
    "Kur to E-Kur-Mah_West": [AVLocation("Kur - Peak Cliff Ledge", BASE_ID+115, logic=lambda logic_info: (lambda state: (logicfunction.longdrone(logic_info)(state) or logicfunction.dronefly(logic_info)(state)) or (logicfunction.grapple(logic_info)(state) and (logicfunction.verylongwarp(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state))))))],
    "E-Kur-Mah to Kur_Center": [AVLocation("E-Kur-Mah - Entry Chamber Breakable Wall", BASE_ID+116, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))],
    "Transition Room": [AVLocation("E-Kur-Mah - Key Door on Quarry Path", BASE_ID+117, logic=lambda logic_info: (lambda state: logicfunction.sudrankey(logic_info)(state)))]
}

av_locations_unpacked = {}
for locationgroup in axiom_verge_locations.values():
    for location in locationgroup:
        assert location.name not in av_locations_unpacked
        av_locations_unpacked[location.name] = location
