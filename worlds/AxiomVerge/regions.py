from BaseClasses import Region, Location
from typing import TYPE_CHECKING
from .locations import axiom_verge_locations
if TYPE_CHECKING:
    from . import AVWorld

    # menu_region = Region("Menu", world.player, world.multiworld)
    # menu_region.locations += [
    #     Location(world.player, location.name, location.code, menu_region)
    #     for location in axiom_verge_locations.get(menu_region.name, [])
    # ]
    # world.multiworld.regions.append(menu_region)


def define_region(r: Region, w: "AVWorld"):
    # r.locations += [
    #     Location(r.player, location.name, location.code, r)
    #     for location in axiom_verge_locations.get(r.name, [])
    # ]
    r.add_locations({location.name: location.code for location in axiom_verge_locations.get(r.name, {})})
    w.multiworld.regions.append(r)


def create_region(world: "AVWorld") -> None:
    menu_region = Region("Menu", world.player, world.multiworld)
    define_region(menu_region, world)
    eribusave1_region = Region("Eribu Save 1", world.player, world.multiworld)
    define_region(eribusave1_region, world)
    eribusave2_region = Region("Eribu Save 2", world.player, world.multiworld)
    define_region(eribusave2_region, world)
    eriburoom2_region = Region("Disruptor Room", world.player, world.multiworld)
    define_region(eriburoom2_region, world)
    eriburoom3_region = Region("Bubble Wall", world.player, world.multiworld)
    define_region(eriburoom3_region, world)
    eriburoom4_region = Region("Brinstar Shaft", world.player, world.multiworld)
    define_region(eriburoom4_region, world)
    eriburoom5_region = Region("Nova Gate", world.player, world.multiworld)
    define_region(eriburoom5_region, world)
    eriburoom6_region = Region("Spitbug Hall", world.player, world.multiworld)
    define_region(eriburoom6_region, world)
    eriburoom7_region = Region("Wrong Tower", world.player, world.multiworld)
    define_region(eriburoom7_region, world)
    eriburoom8_region = Region("False Reflector Access", world.player, world.multiworld)
    define_region(eriburoom8_region, world)
    reflectorroom_region = Region("False Reflector", world.player, world.multiworld)
    define_region(reflectorroom_region, world)
    eriburoom9_region = Region("Nova Access", world.player, world.multiworld)
    define_region(eriburoom9_region, world)
    eriburoom10_region = Region("Nova Room", world.player, world.multiworld)
    define_region(eriburoom10_region, world)
    eriburoom11_region = Region("Bubbled Altar", world.player, world.multiworld)
    define_region(eriburoom11_region, world)
    eriburoom12_region = Region("Buoyg Hall", world.player, world.multiworld)
    define_region(eriburoom12_region, world)
    eriburoom13_region = Region("Multi Disruptor", world.player, world.multiworld)
    define_region(eriburoom13_region, world)
    eriburoom14_region = Region("Cryptography", world.player, world.multiworld)
    define_region(eriburoom14_region, world)
    eriburoom14a_region = Region("Thriller", world.player, world.multiworld)
    define_region(eriburoom14a_region, world)
    eriburoom14b_region = Region("Forbidden Shaft", world.player, world.multiworld)
    define_region(eriburoom14b_region, world)
    eriburoom14c_region = Region("Forbidden Corridor", world.player, world.multiworld)
    define_region(eriburoom14c_region, world)
    eriburoom15_region = Region("Xedur Foyer", world.player, world.multiworld)
    define_region(eriburoom15_region, world)
    eriburoom17_region = Region("Xedur Access", world.player, world.multiworld)
    define_region(eriburoom17_region, world)
    xedurroom_region = Region("Xedur", world.player, world.multiworld)
    define_region(xedurroom_region, world)
    drillroom_region = Region("Drill Room", world.player, world.multiworld)
    define_region(drillroom_region, world)
    drillsecret_region = Region("Xedur Basement", world.player, world.multiworld)
    define_region(drillsecret_region, world)
    eriburoom20_region = Region("Diggy Hole", world.player, world.multiworld)
    define_region(eriburoom20_region, world)
