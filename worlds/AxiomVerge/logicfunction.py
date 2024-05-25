from .items import axiom_verge_items, item_name_groups
from BaseClasses import CollectionState
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import AVWorld


def anycoat(state: CollectionState) -> bool:
    return state.has("Modified Lab Coat") or state.has("Trenchcoat") or state.has("Red Coat") or state.has("Progressive Coat")


def trenchcoat(state: CollectionState) -> bool:
    return state.has("Trenchcoat") or state.has("Red Coat") or state.has("Progressive Coat", count=2)


def redcoat(state: CollectionState) -> bool:
    return state.has("Red Coat") or state.has("Progressive Coat", count=3)


def drone(state: CollectionState) -> bool:
    return state.has("Remote Drone") or state.has("Progressive Drone")


def dronelaunch(state:CollectionState) -> bool:
    return state.has("Enhanced Drone Launch") or state.has("Progressive Drone", count=2)


def dronetp(state:CollectionState) -> bool:
    return state.has("Drone Teleport") or state.has("Progressive Drone", count=3)


def anyglitch(state: CollectionState) -> bool:
    return state.has("Address Disruptor") or state.has("Address Disruptor 2") or state.has("Address Bomb") or state.has("Progressive Glitch")


def glitch2(state:CollectionState) -> bool:
    return state.has("Address Disruptor 2") or state.has("Address Bomb") or state.has("Progressive Glitch", count=2)


def glitchnades(state: CollectionState) -> bool:
    return state.has("Address Bomb") or state.has("Progressive Glitch", count=3)


def drill(state: CollectionState) -> bool:
    return state.has("Laser Drill") or drone(state) or redcoat(state)


def breakblock(state: CollectionState) -> bool:
    return state.has("Weapon") or drill(state)


def longwarp(state: CollectionState) -> bool:
    return state.has("Field Disruptor") and trenchcoat(state) or redcoat(state)


def verylongwarp(state: CollectionState) -> bool:
    return state.has("Field Disruptor") and redcoat(state)


def shortdrone(state: CollectionState) -> bool:
    return drone(state) and dronetp(state)


def longdrone(state: CollectionState) -> bool:
    return shortdrone(state) and dronelaunch(state)


def anyup(state: CollectionState) -> bool:
    return state.has("Field Disruptor") or state.has("Grapple") or trenchcoat(state) or shortdrone(state)
