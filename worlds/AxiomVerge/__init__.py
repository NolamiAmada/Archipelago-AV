import settings
from typing import List
from .options import AVOptions
from .items import axiom_verge_items, AVItem, BASE_ID, setup_events
from .locations import axiom_verge_locations, av_locations_unpacked
from .regions import create_region
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, CollectionState


class VictoryCondition:
    def __init__(self, player: int) -> None:
        self.player = player

    def victory(self, state: CollectionState) -> bool:
        return state.has("Victory", self.player)


class AVWorld(World):
    game = "Axiom Verge"  # name of the game/world
    options_dataclass = AVOptions  # options the player can set
    options: AVOptions
    topology_present = False  # show path to required location checks in spoiler

    item_name_to_id = {axiom_verge_item.name: axiom_verge_item.code for
                       axiom_verge_item in axiom_verge_items}
    location_name_to_id = {name: location.code for name, location in av_locations_unpacked.items()}
    item_name_groups = items.item_name_groups

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.locations: List[Location] = []

    def create_regions(self) -> None:
        create_region(self)
        print(f"Locations: {self.multiworld.regions.location_cache}")
        print(f"Regions: {self.multiworld.regions.region_cache}")

    def create_items(self) -> None:
        world_items = [item for item in axiom_verge_items]
        setup_events(self.player, self.locations)
        if self.options.progressive_coats:
            world_items.append(AVItem("Progressive Coat", ItemClassification.progression, BASE_ID + 45, 3))
        else:
            world_items.append(AVItem("Modified Lab Coat", ItemClassification.progression, BASE_ID + 26, 1))
            world_items.append(AVItem("Trenchcoat", ItemClassification.progression, BASE_ID + 27, 1))
            world_items.append(AVItem("Red Coat", ItemClassification.progression, BASE_ID + 28, 1))
        if self.options.progressive_glitch:
            world_items.append(AVItem("Progressive Glitch", ItemClassification.progression, BASE_ID + 46, 3))
        else:
            world_items.append(AVItem("Address Disruptor", ItemClassification.progression, BASE_ID + 24, 1))
            world_items.append(AVItem("Address Disruptor 2", ItemClassification.progression, BASE_ID + 25, 1))
            world_items.append(AVItem("Address Bomb", ItemClassification.progression, BASE_ID + 34, 1))
        if self.options.progressive_drone:
            world_items.append(AVItem("Progressive Drone", ItemClassification.progression, BASE_ID + 47, 3))
        else:
            world_items.append(AVItem("Remote Drone", ItemClassification.progression, BASE_ID + 31, 1))
            world_items.append(AVItem("Enhanced Drone Launch", ItemClassification.progression, BASE_ID + 33, 1))
            world_items.append(AVItem("Drone Teleport", ItemClassification.progression, BASE_ID + 35, 1))

        itempool_data = []
        for item in world_items:
            for _ in range(item.quantity):
                itempool_data.append(item)
        items2 = [Item(item.name, item.classification, item.code, self.player) for item in itempool_data]
        if self.options.guarantee_starting_weapon and not self.options.room_rando:
            for loc in self.locations:
                if loc.name == "Eribu - Starter Weapon":
                    wepchoice = self.random.choice(["Axiom Disruptor", "Multi-Disruptor", "Lightning Gun", "Inertial Pulse", "Data Bomb", "Voranj", "Firewall", "Ion Beam", "Tethered Charge", "Turbine Pulse", "Shards", "Quantum Variegator", "Heat Seekers", "Nova", "Orbital Discharge", "Hypo-Atomizer", "Reflector", "Kilver", "Distortion Field", "Reverse Slicer", "Fat Beam", "Scissor Beam", "Flamethrower"])
                    print(wepchoice)
                    wep = [item for item in items2 if item.name == wepchoice]
                    assert len(wep) == 1
                    loc.place_locked_item(wep[0])
                    items2.remove(wep[0])
        self.multiworld.itempool += items2

        # should be its own function but im lazy as hell
        self.multiworld.completion_condition[self.player] = VictoryCondition(self.player).victory

