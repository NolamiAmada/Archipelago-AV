import settings
import typing
from .options import AVOptions
from .items import axiom_verge_items, AVItem, BASE_ID  # data used below to add items to the World
from .locations import axiom_verge_locations, av_locations_unpacked  # same as above
from .regions import create_region
from worlds.AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, ItemClassification


class AVWorld(World):
    """Insert description of the world/game here."""
    game = "Axiom Verge"  # name of the game/world
    options_dataclass = AVOptions  # options the player can set
    options: AVOptions
    topology_present = False  # show path to required location checks in spoiler

    item_name_to_id = {axiom_verge_item.name: axiom_verge_item.code for
                       axiom_verge_item in axiom_verge_items}
    location_name_to_id = av_locations_unpacked

    def create_regions(self) -> None:
        create_region(self)
        print(f"Locations: {self.multiworld.regions.location_cache}")
        print(f"Regions: {self.multiworld.regions.region_cache}")

    def create_items(self) -> None:
        if self.options.progressive_coats:
            axiom_verge_items.append(AVItem("Progressive Coat", ItemClassification.progression, BASE_ID + 45, 3))
        else:
            axiom_verge_items.append(AVItem("Modified Lab Coat", ItemClassification.progression, BASE_ID + 26, 1))
            axiom_verge_items.append(AVItem("Trenchcoat", ItemClassification.progression, BASE_ID + 27, 1))
            axiom_verge_items.append(AVItem("Red Coat", ItemClassification.progression, BASE_ID + 28, 1))
        if self.options.progressive_glitch:
            axiom_verge_items.append(AVItem("Progressive Glitch", ItemClassification.progression, BASE_ID + 46, 3))
        else:
            axiom_verge_items.append(AVItem("Address Disruptor", ItemClassification.progression, BASE_ID + 24, 1))
            axiom_verge_items.append(AVItem("Address Disruptor 2", ItemClassification.progression, BASE_ID + 25, 1))
            axiom_verge_items.append(AVItem("Address Bomb", ItemClassification.progression, BASE_ID + 34, 1))
        if self.options.progressive_drone:
            axiom_verge_items.append(AVItem("Progressive Drone", ItemClassification.progression, BASE_ID + 47, 3))
        else:
            axiom_verge_items.append(AVItem("Remote Drone", ItemClassification.progression, BASE_ID + 31, 1))
            axiom_verge_items.append(AVItem("Enhanced Drone Launch", ItemClassification.progression, BASE_ID + 33, 1))
            axiom_verge_items.append(AVItem("Drone Teleport", ItemClassification.progression, BASE_ID + 35, 1))

        itempool_data = []
        for item in axiom_verge_items:
            for _ in range(item.quantity):
                itempool_data.append(item)
        items = [Item(item.name, item.classification, item.code, self.player) for item in itempool_data]
        self.multiworld.itempool += items
