from BaseClasses import Item, ItemClassification
from typing import NamedTuple


class AVItem(NamedTuple):
    name: str
    classification: ItemClassification
    code: int
    quantity: int


BASE_ID = 332200000
axiom_verge_items = [
    AVItem("Axiom Disruptor", ItemClassification.progression, BASE_ID+0, 1),
    AVItem("Nova", ItemClassification.progression, BASE_ID+1, 1),
    AVItem("Multi-Disruptor", ItemClassification.progression, BASE_ID + 2, 1),
    AVItem("Orbital Discharge", ItemClassification.progression, BASE_ID + 3, 1),
    AVItem("Lightning Gun", ItemClassification.progression, BASE_ID + 4, 1),
    AVItem("Flamethrower", ItemClassification.progression, BASE_ID + 5, 1),
    AVItem("Kilver", ItemClassification.progression, BASE_ID + 6, 1),
    AVItem("Inertial Pulse", ItemClassification.progression, BASE_ID + 7, 1),
    AVItem("Data Bomb", ItemClassification.progression, BASE_ID + 8, 1),
    AVItem("Voranj", ItemClassification.progression, BASE_ID + 9, 1),
    AVItem("Firewall", ItemClassification.progression, BASE_ID + 10, 1),
    AVItem("Hypo-Atomizer", ItemClassification.progression, BASE_ID + 11, 1),
    AVItem("Reflector", ItemClassification.progression, BASE_ID + 12, 1),
    AVItem("Ion Beam", ItemClassification.progression, BASE_ID + 13, 1),
    AVItem("Tethered Charge", ItemClassification.progression, BASE_ID + 14, 1),
    AVItem("Turbine Pulse", ItemClassification.progression, BASE_ID + 15, 1),
    AVItem("Shards", ItemClassification.progression, BASE_ID + 16, 1),
    AVItem("Distortion Field", ItemClassification.progression, BASE_ID + 17, 1),
    AVItem("Quantum Variegator", ItemClassification.progression, BASE_ID + 18, 1),
    AVItem("Reverse Slicer", ItemClassification.progression, BASE_ID + 19, 1),
    AVItem("Heat Seekers", ItemClassification.progression, BASE_ID + 20, 1),
    AVItem("Scissor Beam", ItemClassification.progression, BASE_ID + 21, 1),
    AVItem("Fat Beam", ItemClassification.progression, BASE_ID + 22, 1),
    AVItem("Laser Drill", ItemClassification.progression, BASE_ID + 23, 1),
    AVItem("Passcode Tool", ItemClassification.progression, BASE_ID + 29, 1),
    AVItem("Field Disruptor", ItemClassification.progression, BASE_ID + 30, 1),
    AVItem("Grapple", ItemClassification.progression, BASE_ID + 32, 1),
    AVItem("Sudran Key", ItemClassification.progression, BASE_ID + 36, 1),
    AVItem("Bioflux Accelerator (upper)", ItemClassification.useful, BASE_ID + 37, 1),
    AVItem("Bioflux Accelerator (lower)", ItemClassification.useful, BASE_ID + 38, 1),
    AVItem("Health Node", ItemClassification.useful, BASE_ID+39, 9),  # should be 9
    AVItem("Health Node Fragment", ItemClassification.filler, BASE_ID + 40, 25),  # should be 25
    AVItem("Power Node", ItemClassification.useful, BASE_ID + 41, 6),  # should be 6
    AVItem("Power Node Fragment", ItemClassification.filler, BASE_ID + 42, 18),  # should be 18
    AVItem("Range Node", ItemClassification.filler, BASE_ID + 43, 6),  # should be 6
    AVItem("Size Node", ItemClassification.filler, BASE_ID + 44, 6),  # should be 6
]

# Items can be grouped using their names to allow easy checking if any item
# from that group has been collected. Group names can also be used for !hint
item_name_groups = {
    "LongPierce": {
        "Fat Beam", "Scissor Beam", "Flamethrower"
    },  # DON'T USE THIS FOR THE SWITCH AFTER TELAL, HARDCODE THAT ONE
    "ShortPierce": {
        "Kilver", "Distortion Field", "Reverse Slicer",
        "Fat Beam", "Scissor Beam", "Flamethrower"
    },
    "CornerCut": {
        "Nova", "Orbital Discharge", "Hypo-Atomizer", "Reflector",
        "Kilver", "Distortion Field", "Reverse Slicer",
        "Fat Beam", "Scissor Beam", "Flamethrower"
    },
    "Weapon": {
        "Axiom Disruptor", "Multi Disruptor", "Lightning Gun", "Inertial Pulse", "Data Bomb",
        "Voranj", "Firewall", "Ion Beam", "Tethered Charge", "Turbine Pulse", "Shards",
        "Quantum Variegator", "Heat Seekers",
        "Nova", "Orbital Discharge", "Hypo-Atomizer", "Reflector",
        "Kilver", "Distortion Field", "Reverse Slicer",
        "Fat Beam", "Scissor Beam", "Flamethrower"
    },
    "LongWeapon": {
        "Axiom Disruptor", "Inertial Pulse", "Data Bomb", "Voranj", "Ion Beam", "Tethered Charge", "Turbine Pulse",
        "Heat Seekers", "Nova", "Orbital Discharge", "Hypo-Atomizer", "Reflector", "Fat Beam", "Scissor Beam",
        "Flamethrower", "Multi Disruptor", "Lightning Gun", "Shards", "Quantum Variegator", "Reverse Slicer"
    },
    "RangeWeapon": {
        "Axiom Disruptor", "Inertial Pulse", "Data Bomb", "Ion Beam", "Turbine Pulse",
        "Heat Seekers", "Nova", "Orbital Discharge", "Hypo-Atomizer", "Reflector", "Fat Beam"
    }
}
