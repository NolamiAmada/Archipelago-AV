from BaseClasses import Region, Location, CollectionState, Entrance
from typing import TYPE_CHECKING, NamedTuple, List, Callable, Dict
from .locations import axiom_verge_locations
from . import logicfunction
from .items import axiom_verge_items, item_name_groups
import enum
if TYPE_CHECKING:
    from . import AVWorld


class Orientation(enum.Enum):
    Up = enum.auto()
    Down = enum.auto()
    Left = enum.auto()
    Right = enum.auto()
    What = enum.auto()
    Save = enum.auto()


class BossDoor(enum.Enum):  # would rename to doortype but im too lazy, areatrans for area rando, inner and outer for boss rando
    Regular = enum.auto()
    Outer = enum.auto()
    Inner = enum.auto()
    Areatrans = enum.auto()


class AVDoor(NamedTuple):
    name: str
    orientation: Orientation = Orientation.What
    bossdoor: BossDoor = BossDoor.Regular
    logic: Callable[[CollectionState], bool] = Entrance.access_rule

    def is_real_door(self) -> bool:  # if true is actual door, # otherwise connects two regions part of same room, also used for some edge cases
        return self.orientation != Orientation.What or Orientation.Save

    def find_mirror_face(self) -> Orientation:
        assert self.is_real_door()
        if self.orientation == Orientation.Right:
            return Orientation.Left
        elif self.orientation == Orientation.Left:
            return Orientation.Right
        elif self.orientation == Orientation.Up:
            return Orientation.Down
        else:
            return Orientation.Up


class AVRegion(enum.Enum):

    def __init__(self, name: str, doors: List[AVDoor]) -> None:
        self.title = name
        self.doors = doors

    # non location regions
    MENU = "Menu", [AVDoor("To Start")]
    SLUG = "Slug", [AVDoor("Enemy Slug")]

    # eribusave1: 2 regions
    ERIBU_SAVE1_WEST = "Eribu Save 1_West", [
        AVDoor("Eribu Save 1 Left Door", Orientation.Left),
        AVDoor("Eribu Save 1 Inner WE", logic=lambda state: logicfunction.breakblock(state) or logicfunction.anycoat(state)),
        AVDoor("Eribu Save 1 Save", Orientation.Save)
    ]
    ERIBU_SAVE1_EAST = "Eribu Save 1_East", [
        AVDoor("Eribu Save 1 Right Door", Orientation.Right),
        AVDoor("Eribu Save 1 Inner EW", logic=lambda state: logicfunction.breakblock(state) or logicfunction.anycoat(state))
    ]

    ERIBU_SAVE2 = "Eribu Save 2", [
        AVDoor("Eribu Save 2 Right Door", Orientation.Right),
        AVDoor("Eribu Save 2 Save", Orientation.Save)
    ]

    # disruptorroom: 2 regions
    DISRUPTOR_ROOM_EAST = "Disruptor Room_East", [
        AVDoor("Disruptor Room Right Door", Orientation.Right),
        AVDoor("Disruptor Room Inner EW", logic=lambda state: logicfunction.drill(state) and logicfunction.longwarp(state) or logicfunction.drill(state) and state.has("Grapple") or logicfunction.shortdrone(state))
    ]
    DISRUPTOR_ROOM_WEST = "Disruptor Room_West", [
        AVDoor("Disruptor Room Left Door", Orientation.Left),
        AVDoor("Disruptor Room Up Door", Orientation.Up),
        AVDoor("Disruptor Room Inner WE", logic=lambda state: logicfunction.drill(state))
    ]

    BUBBLE_WALL = "Bubble Wall", [
        AVDoor("Bubble Wall Left Door", Orientation.Left, logic=lambda state: logicfunction.breakblock(state)),
        AVDoor("Bubble Wall Right Door", Orientation.Right, logic=lambda state: logicfunction.breakblock(state))
    ]

    # brinstarshaft: 3 regions
    BRINSTAR_SHAFT_LOWER = "Brinstar Shaft_Lower", [
        AVDoor("Brinstar Shaft Lower Left Door", Orientation.Left),
        AVDoor("Brinstar Shaft Lower Right Door", Orientation.Right),
        AVDoor("Brinstar Shaft Center Right Door", Orientation.Right),
        AVDoor("Brinstar Shaft Upper Right Door", Orientation.Right),
        AVDoor("Brinstar Shaft Inner BC", logic=lambda state: state.has("CornerCut") or logicfunction.tempup(state) or logicfunction.trenchcoat(state) or logicfunction.drone(state))
    ]
    BRINSTAR_SHAFT_CENTER = "Brinstar Shaft_Center", [
        AVDoor("Brinstar Shaft Center Left Door", Orientation.Left),
        AVDoor("Brinstar Shaft Inner CB"),
        AVDoor("Brinstar Shaft Inner CU", logic=lambda state: logicfunction.drill(state))
    ]
    BRINSTAR_SHAFT_UPPER = "Brinstar Shaft_Upper", [
        AVDoor("Brinstar Shaft Upper Left Door", Orientation.Left),
        AVDoor("Brinstar Shaft Inner UC", logic=lambda state: logicfunction.drill(state))
    ]

    NOVA_GATE = "Nova Gate", [
        AVDoor("Nova Gate Left Door", Orientation.Left, logic=lambda state: state.has("CornerCut") or logicfunction.anycoat(state)),
        AVDoor("Nova Gate Right Door", Orientation.Right, logic=lambda state: state.has("Weapon") or logicfunction.trenchcoat(state) or logicfunction.drone(state) or state.has("Laser Drill"))
    ]

    # spitbughall: 2 regions
    SPITBUG_HALL_WEST = "Spitbug Hall_West", [
        AVDoor("Spitbug Hall Left Door", Orientation.Left),
        AVDoor("Spitbug Hall Left Up Door", Orientation.Up),
        AVDoor("Spitbug Hall Inner WE", logic=lambda state: state.has("Weapon") or logicfunction.drone(state) or state.has("Laser Drill") or logicfunction.anycoat(state))
    ]
    SPITBUG_HALL_EAST = "Spitbug Hall_East", [
        AVDoor("Spitbug Hall Right Up Door", Orientation.Up),
        AVDoor("Spitbug Hall Inner EW", logic=lambda state: state.has("CornerCut") or logicfunction.anycoat(state))
    ]

    WRONG_TOWER = "Wrong Tower", [
        AVDoor("Wrong Tower Up Door", Orientation.Up),
        AVDoor("Wrong Tower Down Door", Orientation.Down)
    ]

    FALSE_REFLECTOR_ACCESS = "False Reflector Access", [
        AVDoor("False Reflector Access Down Door", Orientation.Down, logic=lambda state: logicfunction.glitchnades(state)),
        AVDoor("False Reflector Access Up Door", Orientation.Up, logic=lambda state: logicfunction.glitchnades(state) and logicfunction.anyupnoceiling(state))
    ]

    FALSE_REFLECTOR = "False Reflector", [
        AVDoor("False Reflector Down Door", Orientation.Down)
    ]

    NOVA_ACCESS = "Nova Access", [
        AVDoor("Nova Access Up Door", Orientation.Up),
        AVDoor("Nova Access Down Door")
    ]

    NOVA_ROOM = "Nova Room", [
        AVDoor("Nova Room Down Door", Orientation.Down)
    ]

    BUBBLED_ALTAR = "Bubbled Altar", [
        AVDoor("Bubbled Altar Right Door", Orientation.Right)
    ]

    BUOYG_HALL = "Buoyg Hall", [
        AVDoor("Buoyg Hall Right Door", Orientation.Right),
        AVDoor("Buoyg Hall Left Door", Orientation.Left)
    ]

    # multidisruptor: 2 regions
    MULTI_DISRUPTOR_LOWER = "Multi Disruptor_Lower", [
        AVDoor("Multi Disruptor Right Door", Orientation.Right),
        AVDoor("Multi Disruptor Inner BU", logic=lambda state: state.has("Grapple") or logicfunction.dronefly(state))
    ]
    MULTI_DISRUPTOR_UPPER = "Multi Disruptor_Upper", [
        AVDoor("Multi Disruptor Left Door", Orientation.Left),
        AVDoor("Multi Disruptor Up Door", Orientation.Up),
        AVDoor("Multi Disruptor Inner UB")
    ]

    #left door wonky in door rando
    CRYPTOGRAPHY = "Cryptography", [
        AVDoor("Cryptography Down Door", Orientation.Down),
        AVDoor("Cryptography Left Door", Orientation.Left, logic=lambda state: state.has("Passcode Tool"))
    ]

    THRILLER = "Thriller", [
        AVDoor("Thriller Right Door", Orientation.Right, logic=lambda state: logicfunction.anyup(state)),
        AVDoor("Thriller Left Door", Orientation.Left, logic=lambda state: logicfunction.anyup(state))
    ]

    FORBIDDEN_SHAFT = "Forbidden Shaft", [
        AVDoor("Forbidden Shaft Up Door", Orientation.Right),
        AVDoor("Forbidden Shaft Down Door", Orientation.Right)
    ]

    # forbiddencorridor: 2 regions
    FORBIDDEN_CORRIDOR_WEST = "Forbidden Corridor_West", [
        AVDoor("Forbidden Corridor Left Door", Orientation.Left),
        AVDoor("Forbidden Corridor Inner WE", logic=lambda state: logicfunction.breakblock(state))
    ]
    FORBIDDEN_CORRIDOR_EAST = "Forbidden Corridor_East", [
        AVDoor("Forbidden Corridor Right Door", Orientation.Right),
        AVDoor("Forbidden Corridor Inner EW", logic=lambda state: state.has("Fat Beam"))
    ]

    XEDUR_FOYER = "Xedur Foyer", [
        AVDoor("Xedur Foyer Lower Left Door", Orientation.Left),
        AVDoor("Xedur Foyer Upper Left Door", Orientation.Left),
        AVDoor("Xedur Foyer Lower Right Door", Orientation.Right),
        AVDoor("Xedur Foyer Upper Right Door", Orientation.Right)
    ]

    XEDUR_ACCESS = "Xedur Access", [
        AVDoor("Xedur Access Left Door", Orientation.Left),
        AVDoor("Xedur Access Right Door", Orientation.Right, BossDoor.Outer)
    ]

    XEDUR = "Xedur", [
        AVDoor("Xedur Left Door", Orientation.Left, BossDoor.Inner, logic=lambda state: state.has("Weapon")),
        AVDoor("Xedur Right Door", Orientation.Right, BossDoor.Inner, logic=lambda state: state.has("Weapon"))
    ]

    # drillroom: 2 regions
    DRILL_ROOM_UPPER = "Drill Room_Upper", [
        AVDoor("Drill Room Up Door", Orientation.Left, BossDoor.Outer, logic=lambda state: logicfunction.shortdrone(state) or logicfunction.longwarp(state) or (state.has('Field Disruptor') and state.has("Grapple"))),
        AVDoor("Drill Room Inner UB", logic=lambda state: logicfunction.drill(state))
    ]
    DRILL_ROOM_LOWER = "Drill Room_Lower", [
        AVDoor("Drill Room Down Door", Orientation.Left),
        AVDoor("Drill Room Inner BU", logic=lambda state: logicfunction.dronefly(state) or (logicfunction.longdrone(state)))
    ]

    # drillsecret: 2 regions
    XEDUR_BASEMENT_EAST = "Xedur Basement_East", [
        AVDoor("Xedur Basement Right Door", Orientation.Right),
        AVDoor("Xedur Basement Inner EW", logic=lambda state: logicfunction.drill(state) and (state.has("CornerCut") or (state.has("Weapon") and logicfunction.tempup(state)) or state.has("LongKilver") or logicfunction.anycoat(state)))
    ]
    XEDUR_BASEMENT_WEST = "Xedur Basement_West", [
        AVDoor("Xedur Basement Left Door", Orientation.Left, logic=lambda state: logicfunction.drill(state)),
        AVDoor("Xedur Basement Inner WE", logic=lambda state: logicfunction.drill(state) and state.has("Fat Beam"))
    ]

    DIGGY_HOLE = "Diggy Hole", [
        AVDoor("Diggy Hole Up Door", Orientation.Left, logic=lambda state: logicfunction.drill(state)),
        AVDoor("Diggy Hole Down Door", Orientation.Right, logic=lambda state: logicfunction.drill(state))
    ]

    # thedrop: 2 regions
    THE_DROP_MAIN = "The Drop_Main", [
        AVDoor("The Drop Upper Left Door", Orientation.Left),
        AVDoor("The Drop Upper Right Door", Orientation.Right),
        AVDoor("The Drop Lower Right Door", Orientation.Right),
        AVDoor("The Drop Down Door", Orientation.Down),
        AVDoor("The Drop Inner MS", logic=lambda state: (logicfunction.dronequest(state) or logicfunction.trenchcoat(state)) and logicfunction.glitchnades(state))
    ]
    THE_DROP_SECRET = "The Drop_Secret", [
        AVDoor("The Drop Lower Left Door", Orientation.Left),
        AVDoor("The Drop Inner SM", logic=lambda state: (logicfunction.dronequest(state) or logicfunction.trenchcoat(state)) and logicfunction.glitchnades(state))
    ]

    WEAPONS_VAULT = "Weapons Vault", [
        AVDoor("Weapons Vault Right Door", Orientation.Right)
    ]

    BUBBLEWRAP = "Bubblewrap", [
        AVDoor("Bubblewrap Up Door", Orientation.Up),
        AVDoor("Bubblewrap Left Door", Orientation.Left),
        AVDoor("Bubblewrap Right Door", Orientation.Right)
    ]

    ERIBU_TO_ABSU = "Eribu to Absu", [
        AVDoor("Eribu to Absu Left Door", Orientation.Left),
        AVDoor("Eribu to Absu Down Door", Orientation.Down, BossDoor.Areatrans)
    ]

    # secretchamber: 2 regions
    SECRET_CHAMBER_LOWER = "Secret Chamber_Lower", [
        AVDoor("Secret Chamber Right Door", Orientation.Right),
        AVDoor("Secret Chamber Inner BU", logic=lambda state: (logicfunction.anyglitch(state) and (logicfunction.breakblock(state) or logicfunction.trenchcoat(state))) or state.has("Grapple") or logicfunction.shortdrone(state) or logicfunction.longwarp(state))
    ]
    # up door is weird
    SECRET_CHAMBER_UPPER = "Secret Chamber_Upper", [
        AVDoor("Secret Chamber Up Door", Orientation.Up, logic=lambda state: state.has("Passcode Tool") and logicfunction.anyup(state)),
        AVDoor("Secret Chamber Inner UB")
    ]

    DISCHARGE_CHAMBER = "Discharge Chamber", [
        AVDoor("Discharge Chamber Down Door", Orientation.Down)
    ]

    ERIBU_TO_UKKINNA = "Eribu to Ukkin-Na", [
        AVDoor("Eribu to Ukkin-Na Left Door", Orientation.Left, logic=lambda state: logicfunction.glitch2(state) or logicfunction.redcoat(state)),
        AVDoor("Eribu to Ukkin-Na Right Door", Orientation.Right, BossDoor.Areatrans, logic=lambda state: logicfunction.glitch2(state) or logicfunction.redcoat(state))
    ]

    # eributoindi: 2 regions
    ERIBU_TO_INDI_WEST = "Eribu to Indi_West", [
        AVDoor("Eribu to Indi Left Door", Orientation.Left),
        AVDoor("Eribu to Indi Inner WE", logic=lambda state: logicfunction.trenchcoat(state) or logicfunction.shortdrone(state) or state.has("Grapple"))
    ]
    ERIBU_TO_INDI_EAST = "Eribu to Indi_East", [
        AVDoor("Eribu to Indi Right Door", Orientation.Right, BossDoor.Areatrans),
        AVDoor("Eribu to Indi Inner EW", logic=lambda state: logicfunction.anyup(state))
    ]

    PRIMORDIAL_ACCESS = "Primordial Access", [
        AVDoor("Primordial Access Left Door", Orientation.Left, logic=lambda state: logicfunction.anyup(state) and logicfunction.glitch2(state) or logicfunction.redcoat(state)),
        AVDoor("Primordial Access Right Door", Orientation.Right, logic=lambda state: logicfunction.anyup(state) and logicfunction.glitch2(state) or logicfunction.redcoat(state))
    ]

    # primordialcavern: 3 regions
    PRIMORDIAL_CAVERN_EAST = "Primordial Cavern_East", [
        AVDoor("Primordial Cavern Right Door", Orientation.Right, logic=lambda state: logicfunction.anyup(state)),
        AVDoor("Primordial Cavern Inner EW", logic=lambda state: logicfunction.redcoat(state)),
        AVDoor("Primordial Cavern Inner EC", logic=lambda state: logicfunction.drone(state) and logicfunction.trenchcoat(state) or logicfunction.drone(state) and state.has("Grapple") or logicfunction.shortdrone(state))
    ]
    PRIMORDIAL_CAVERN_CENTER = "Primordial Cavern_Center", [
        AVDoor("Primordial Cavern Inner CW", logic=lambda state: logicfunction.drone(state)),
        AVDoor("Primordial Cavern Inner CE", logic=lambda state: logicfunction.drone(state))
    ]
    PRIMORDIAL_CAVERN_WEST = "Primordial Cavern_West", [
        AVDoor("Primordial Cavern Up Door", Orientation.Up, logic=lambda state: logicfunction.redcoat(state) or logicfunction.shortdrone(state) or logicfunction.trenchcoat(state) and state.has("Grapple") or logicfunction.longwarp(state) or state.has("Grapple") and state.has("Field Disruptor")),
        AVDoor("Primordial Cavern Inner WE", logic=lambda state: logicfunction.redcoat(state)),
        AVDoor("Primordial Cavern Inner WC", logic=lambda state: logicfunction.drone(state))
    ]

    # flamethrower access: 2 regions
    FLAMETHROWER_ACCESS_WEST = "Flamethrower Access_West", [
        AVDoor("Flamethrower Access Down Door", Orientation.Down),
        AVDoor("Flamethrower Access Inner WE", logic=lambda state: logicfunction.trenchcoat(state) and state.has("Grapple") or state.has("Grapple") and logicfunction.trenchcoat(state) or logicfunction.longdrone(state) or logicfunction.redcoat(state) and state.has("Grapple") and state.has("Field Disruptor"))
    ]
    FLAMETHROWER_ACCESS_EAST = "Flamethrower Access_East", [
        AVDoor("Flamethrower Access Up Door", Orientation.Up),
        AVDoor("Flamethrower Access Inner EW", logic=lambda state: logicfunction.longdrone(state) or state.has("Grapple")),
        AVDoor("Flamethrower Access - Slug in Room")
    ]

    FLAMETHROWER_ROOM = "Flamethrower Room", [AVDoor("Flamethrower Room Down Door", Orientation.Down)]

    BUBBLE_MAZE = "Bubble Maze", [
        AVDoor("Bubble Maze Down Door", Orientation.Down, logic=lambda state: logicfunction.anycoat(state) and logicfunction.shortdrone(state)),
        AVDoor("Bubble Maze Right Door", Orientation.Right, logic=lambda state: logicfunction.anycoat(state) and logicfunction.shortdrone(state))
    ]

    WHEELCHAIR = "Wheelchair", [AVDoor("Wheelchair Left Door", Orientation.Left)]

    ABSU_SAVE1 = "Absu Save 1", [
        AVDoor("Absu Save 1 Right Door", Orientation.Right),
        AVDoor("Absu Save 1 Save", Orientation.Save)
    ]

    # absu shaft: 3 regions
    ABSU_SHAFT_UPPER = "Absu Shaft_Upper", [
        AVDoor("Absu Shaft Up Door", Orientation.Up, BossDoor.Areatrans),
        AVDoor("Absu Shaft Upper Left Door", Orientation.Left),
        AVDoor("Absu Shaft Upper Right Door", Orientation.Right),
        AVDoor("Absu Shaft Upper Center Left Door", Orientation.Left),
        AVDoor("Absu Shaft Lower Right Door", Orientation.Right),
        AVDoor("Absu Shaft Inner UC", logic=lambda state: logicfunction.dronequest(state))
    ]
    ABSU_SHAFT_CENTER = "Absu Shaft_Center", [
        AVDoor("Absu Shaft Lower Center Left Door", Orientation.Left),
        AVDoor("Absu Shaft Inner CU", logic=lambda state: logicfunction.dronequest(state)),
        AVDoor("Absu Shaft Inner CB", logic=lambda state: logicfunction.trenchcoat(state))
    ]
    ABSU_SHAFT_LOWER = "Absu Shaft_Lower", [
        AVDoor("Absu Shaft Lower Left Door", Orientation.Left),
        AVDoor("Absu Shaft Inner BC", logic=lambda state: logicfunction.trenchcoat(state))
    ]

    DONUT_VAULT = "Donut Vault", [AVDoor("Donut Vault Right Door", Orientation.Right)]

    UPPER_SHAFT_BASEMENT = "Upper Shaft Basement", [AVDoor("Upper Shaft Basement Right Door", Orientation.Right)]

    LOWER_SHAFT_BASEMENT = "Lower Shaft Basement", [AVDoor("Lower Shaft Basement Right Door", Orientation.Right)]

    # ventilation: 3 regions
    VENTILATION_WEST = "Ventilation_West", [
        AVDoor("Ventilation Left Door", Orientation.Left),
        AVDoor("Ventilation Inner WC", logic=lambda state: logicfunction.drill(state) or logicfunction.trenchcoat(state))
    ]
    VENTILATION_CENTER = "Ventilation_Center", [
        AVDoor("Ventilation Up Door", Orientation.Up),
        AVDoor("Ventilation Inner CW", logic=lambda state: logicfunction.drill(state) or logicfunction.trenchcoat(state)),
        AVDoor("Ventilation Inner CE", logic=lambda state: logicfunction.drill(state))
    ]
    VENTILATION_EAST = "Ventilation_East", [
        AVDoor("Ventilation Right Door", Orientation.Up),
        AVDoor("Ventilation Inner EC", logic=lambda state: logicfunction.drill(state))
    ]

    ATTIC_ACCESS = "Attic Access", [
        AVDoor("Attic Access Down Door", Orientation.Down),
        AVDoor("Attic Access Right Door", Orientation.Right, logic=lambda state: logicfunction.tempup(state))
    ]

    # attic: 5 regions
    ATTIC_WEST = "Attic_West", [
        AVDoor("Attic Left Door", Orientation.Left, logic=lambda state: logicfunction.anyup(state)),
        AVDoor("Attic Inner WCW", logic=lambda state: logicfunction.glitchnades(state))
    ]
    ATTIC_CENTER_WEST = "Attic_Center West", [
        AVDoor("Attic Inner CWW", logic=lambda state: logicfunction.glitchnades(state)),
        AVDoor("Attic Inner CWCE", logic=lambda state: logicfunction.glitchnades(state))
    ]
    ATTIC_CENTER_EAST = "Attic_Center East", [
        AVDoor("Attic Inner CECW", logic=lambda state: logicfunction.glitchnades(state)),
        AVDoor("Attic Inner CELE")
    ]
    ATTIC_LOWER_EAST = "Attic_Lower East", [
        AVDoor("Attic Down Door", Orientation.Down),
        AVDoor("Attic Inner LECE", logic=lambda state: logicfunction.tempup(state)),
        AVDoor("Attic Inner LEUE", logic=lambda state: logicfunction.tempup(state))
    ]
    ATTIC_UPPER_EAST = "Attic_Upper East", [
        AVDoor("Attic Inner UELE")
    ]

    # pinkdiatoms2: 2 regions
    PINK_DIATOMS2_WEST = "Pink Diatoms 2_West", [
        AVDoor("Pink Diatoms 2 Left Door", Orientation.Left),
        AVDoor("Pink Diatoms 2 Down Door", Orientation.Down),
        AVDoor("Pink Diatoms 2 Inner WE", logic=lambda state: logicfunction.glitch2(state))
    ]
    PINK_DIATOMS2_EAST = "Pink Diatoms 2_East", [
        AVDoor("Pink Diatoms 2 Up Door", Orientation.Up),
        AVDoor("Pink Diatoms 2 Inner EW", logic=lambda state: logicfunction.glitch2(state))
    ]

    OVERGROWN_PRISON = "Overgrown Prison", [
        AVDoor("Overgrown Prison Up Door", Orientation.Up, logic=lambda state: logicfunction.tempup(state)),
        AVDoor("Overgrown Prison Upper Left Door", Orientation.Left),
        AVDoor("Overgrown Prison Lower Left Door", Orientation.Left),
        AVDoor("Overgrown Prison Right Door", Orientation.Right)
    ]

    ABSU_SAVE2 = "Absu Save 2", [
        AVDoor("Absu Save 2 Left Door", Orientation.Left),
        AVDoor("Absu Save 2 Save", Orientation.Save)
    ]

    DINING_HALL = "Dining Hall", [
        AVDoor("Dining Hall Right Door", Orientation.Right, logic=lambda state: logicfunction.anyup(state) and logicfunction.anycoat(state)),
        AVDoor("Dining Hall Left Door", Orientation.Left, logic=lambda state: logicfunction.anyup(state) and logicfunction.anycoat(state))
    ]

    PINK_DIATOMS_ACCESS = "Pink Diatoms Access", [
        AVDoor("Pink Diatoms Access Left Door", Orientation.Left),
        AVDoor("Pink Diatoms Access Right Door", Orientation.Right)
    ]

    # pinkdiatoms1: 3 regions
    PINK_DIATOMS1_UPPER = "Pink Diatoms 1_Upper", [
        AVDoor("Pink Diatoms 1 Upper Right Door", Orientation.Right),
        AVDoor("Pink Diatoms 1 Inner UC", logic=lambda state: logicfunction.drill(state))
    ]
    PINK_DIATOMS1_CENTER = "Pink Diatoms 1_Center", [
        AVDoor("Pink Diatoms 1 Left Door", Orientation.Left),
        AVDoor("Pink Diatoms 1 Center Right Door", Orientation.Right),
        AVDoor("Pink Diatoms 1 Inner CU", logic=lambda state: logicfunction.drill(state)),
        AVDoor("Pink Diatoms 1 Inner CB", logic=lambda state: logicfunction.glitch2(state) and logicfunction.anycoat(state))
    ]
    PINK_DIATOMS1_LOWER = "Pink Diatoms 1_Lower", [
        AVDoor("Pink Diatoms 1 Lower Right Door", Orientation.Right),
        AVDoor("Pink Diatoms 1 Inner BC", logic=lambda state: logicfunction.glitch2(state) and logicfunction.anycoat(state) and logicfunction.anyupnoceiling(state))
    ]

    PRISON_CELLAR = "Prison Cellar", [
        AVDoor("Prison Cellar Left Door", Orientation.Left, logic=lambda state: logicfunction.dronequest(state)),
        AVDoor("Prison Cellar Up Door", Orientation.Up, logic=lambda state: logicfunction.dronequest(state))
    ]

    PRISON_CELLAR_SECRET = "Prison Cellar Secret", [AVDoor("Prison Cellar Down Door", Orientation.Down)]

    ELSENOVA = "Elsenova", [
        AVDoor("Elsenova Right Door", Orientation.Right),
        AVDoor("Elsenova Left Door", Orientation.Left)
    ]

    # prison1: 2 regions
    PRISON1_UPPER = "Prison Tower_Upper", [
        AVDoor("Prison Tower Upper Right Door", Orientation.Right, logic=lambda state: state.has("ShortPierce") or logicfunction.anycoat(state)),
        AVDoor("Prison Tower Left Door", Orientation.Left, logic=lambda state: state.has("ShortPierce") or logicfunction.anycoat(state)),
        AVDoor("Prison Tower Inner UB", logic=lambda state: state.has("ShortPierce") or logicfunction.anycoat(state))
    ]

    PRISON1_LOWER = "Prison Tower_Lower", [
        AVDoor("Prison Tower Lower Right Door"),
        AVDoor("Prison Tower Inner BU", Orientation.Right, logic=lambda state: logicfunction.breakblock(state) or logicfunction.anycoat(state))
    ]

    MAINTENANCE = "Maintenance", [
        AVDoor("Maintenance Left Door", Orientation.Left),
        AVDoor("Maintenance Right Door", Orientation.Right)
    ]

    STORAGE1 = "Storage 1", [
        AVDoor("Storage 1 Left Door", Orientation.Left),
        AVDoor("Storage 1 Down Door", Orientation.Down),
        AVDoor("Storage 1 Up Door", Orientation.Up)
    ]

    STORAGE2 = "Storage 2", [
        AVDoor("Storage 2 Down Door", Orientation.Down),
        AVDoor("Storage 2 Up Door", Orientation.Up)
    ]

    TELAL_ACCESS_SHAFT = "Telal Access Shaft", [
        AVDoor("Telal Access Shaft Down Door", Orientation.Down),
        AVDoor("Telal Access Shaft Up Door", Orientation.Up)
    ]

    ABSU_SAVE3 = "Absu Save 3", [
        AVDoor("Absu Save 3 Right Door", Orientation.Right),
        AVDoor("Absu Save 3 Save", Orientation.Save)
    ]

    TELAL_FOYER = "Telal Foyer", [
        AVDoor("Telal Foyer Down Door", Orientation.Down),
        AVDoor("Telal Foyer Left Door", Orientation.Left),
        AVDoor("Telal Foyer Right Door", Orientation.Right, BossDoor.Outer)
    ]

    TELAL = "Telal", [
        AVDoor("Telal Left Door", Orientation.Left, BossDoor.Inner, logic=lambda state: (logicfunction.anycoat(state) and state.has("Weapon")) or state.has("Fat Beam")),
        AVDoor("Telal Down Door", Orientation.Down, BossDoor.Inner, logic=lambda state: state.has("LongWeapon"))
    ]

    # telaltreasury: 4 regions
    TELAL_TREASURY_UPPER = "Telal Treasury_Upper", [
        AVDoor("Telal Treasury Up Door", Orientation.Up, BossDoor.Outer),
        AVDoor("Telal Treasury Inner UW"),
        AVDoor("Telal Treasury Inner UE", logic=lambda state: logicfunction.trenchcoat(state) or logicfunction.anycoat(state) and state.has("Scissor Beam") or state.has("Fat Beam"))
    ]
    TELAL_TREASURY_EAST = "Telal Treasury_East", [
        AVDoor("Telal Treasury Right Door", Orientation.Right),
        AVDoor("Telal Treasury Inner EU", logic=lambda state: (logicfunction.anyglitch(state) and logicfunction.anyupnoceiling(state) and logicfunction.breakblock(state)) or logicfunction.redcoat(state) or (logicfunction.trenchcoat(state) and (state.has("Grapple") or state.has("Field Disruptor") or logicfunction.shortdrone(state)))),
        AVDoor("Telal Treasury Inner ES")
    ]
    TELAL_TREASURY_WEST = "Telal Treasury_West", [
        AVDoor("Telal Treasury Inner WU", logic=lambda state: logicfunction.dronefly(state)),
        AVDoor("Telal Treasury Inner WS", logic=lambda state: logicfunction.anyglitch(state) or logicfunction.tempup(state))
    ]
    TELAL_TREASURY_SOUTH = "Telal Treasury_South", [
        AVDoor("Telal Treasury Inner SW"),
        AVDoor("Telal Treasury Inner SE", logic=lambda state: logicfunction.dronefly(state) or logicfunction.anyglitch(state))
    ]

    TELAL_SECRET_ACCESS1 = "Telal Secret Access 1", [
        AVDoor("Telal Secret Access 1 Left Door", Orientation.Left),
        AVDoor("Telal Secret Access 1 Down Door", Orientation.Down),
        AVDoor("Telal Secret Access 1 Up Door", Orientation.Up, logic=lambda state: logicfunction.sevenblockup(state))
    ]

    TELAL_SECRET_ACCESS2 = "Telal Secret Access 2", [
        AVDoor("Telal Secret Access 2 Down Door", Orientation.Down),
        AVDoor("Telal Secret Access 2 Up Door", Orientation.Up, logic=lambda state: logicfunction.sevenblockup(state))
    ]

    TELAL_SECRET_ACCESS3 = "Telal Secret Access 3", [
        AVDoor("Telal Secret Access 3 Down Door", Orientation.Down),
        AVDoor("Telal Secret Access 3 Left Door", Orientation.Left)
    ]

    ABSU_TO_INDI_UPPER = "Absu to Indi_Upper", [
        AVDoor("Absu to Indi Up Door", Orientation.Up, BossDoor.Areatrans, logic=lambda state: logicfunction.anyup(state)),
        AVDoor("Absu to Indi Upper Right Door", Orientation.Right, logic=lambda state: logicfunction.anyup(state)),
        AVDoor("Abso to Indi Inner UB", logic=lambda state: logicfunction.anycoat(state))
    ]

    ABSU_TO_INDI_LOWER = "Absu to Indi_Lower", [
        AVDoor("Absu to Indi Lower Right Door", Orientation.Right),
        AVDoor("Absu to Indi Inner BU", logic=lambda state: logicfunction.sevenblockup(state) and logicfunction.anycoat(state))
    ]

    TELAL_SECRET_ACCESS4 = "Telal Secret Access 4", [AVDoor("Telal Secret Access 4 Left Door", Orientation.Left)]

    TELAL_EXIT = "Telal Exit", [
        AVDoor("Telal Exit Up Door", Orientation.Up, logic=lambda state: logicfunction.anyup(state)),
        AVDoor("Telal Exit Down Door", Orientation.Down)
    ]

    # ducts1: 3 regions
    DUCTS1_WEST = "Ducts 1_West", [
        AVDoor("Ducts 1 Up Door", Orientation.Up),
        AVDoor("Ducts 1 Inner WE", logic=lambda state: logicfunction.drill(state) or logicfunction.trenchcoat(state)),
        AVDoor("Ducts 1 Inner WS", logic=lambda state: logicfunction.anycoat(state))
    ]
    DUCTS1_EAST = "Ducts 1_East", [
        AVDoor("Ducts 1 Right Door", Orientation.Right),
        AVDoor("Ducts 1 Inner EW", logic=lambda state: logicfunction.drill(state) or logicfunction.trenchcoat(state))
    ]
    DUCTS1_SECRET = "Ducts 1_Secret", [
        AVDoor("Ducts 1 Down Door", Orientation.Down),
        AVDoor("Ducts 1 Inner SW", logic=lambda state: logicfunction.anycoat(state))
    ]

    DUCTS1_SECRET1 = "Ducts 1 Secret 1", [
        AVDoor("Ducts 1 Secret 1 Up Door", Orientation.Up),
        AVDoor("Ducts 1 Secret 1 Left Door", Orientation.Left)
    ]

    DUCTS1_SECRET2 = "Ducts 1 Secret 2", [
        AVDoor("Ducts 1 Secret 2 Right Door", Orientation.Right),
        AVDoor("Ducts 1 Secret 2 Left Door", Orientation.Left)
    ]

    DUCTS1_SECRET3 = "Ducts 1 Secret 3", [AVDoor("Ducts 1 Secret 3 Right Door", Orientation.Right)]

    DUCTS2 = "Ducts 2", [
        AVDoor("Ducts 2 Left Door", Orientation.Left, logic=lambda state: logicfunction.drill(state) or logicfunction.trenchcoat(state)),
        AVDoor("Ducts 2 Right Door", Orientation.Right, logic=lambda state: logicfunction.drill(state) or logicfunction.trenchcoat(state))
    ]

    # purplediatoms1: 3 regions
    PURPLE_DIATOMS1_UPPER = "Purple Diatoms 1_Upper", [
        AVDoor("Purple Diatoms 1 Up Door", Orientation.Up),
        AVDoor("Purple Diatoms 1 Right Door", Orientation.Right),
        AVDoor("Purple Diatoms 1 Upper Left Door", Orientation.Left),
        AVDoor('Purple Diatoms 1 Inner UW'),
        AVDoor("Purple Diatoms 1 Inner UE", logic=lambda state: logicfunction.anycoat(state))
    ]
    PURPLEDIATOMS1_WEST = "Purple Diatoms 1_West", [
        AVDoor("Purple Diatoms 1 Lower Left Door", Orientation.Left),
        AVDoor("Purple Diatoms 1 Inner WU", logic=lambda state: logicfunction.anyglitch(state) or logicfunction.sevenblockup(state)),
        AVDoor("Purple Diatoms 1 Inner WE", logic=lambda state: logicfunction.anycoat(state))
    ]
    PURPLEDIATOMS1_EAST = "Purple Diatoms 1_East", [
        AVDoor("Purple Diatoms 1 Down Door", Orientation.Down),
        AVDoor("Purple Diatoms 1 Inner EW", logic=lambda state: logicfunction.anycoat(state)),
        AVDoor("Purple Diatoms 1 Inner EU", logic=lambda state: logicfunction.trenchcoat(state))
    ]

    ABSU_SAVE4 = "Absu Save 4", [
        AVDoor("Absu Save 4 Right Door", Orientation.Right),
        AVDoor("Absu Save 4 Save", Orientation.Save)
    ]

    PURPLEDIATOMS1_HIDDENACCESS1 = "Purple Diatoms 1 Hidden Access 1", [
        AVDoor("Purple Diatoms 1 Hidden Access 1 Up Door", Orientation.Up),
        AVDoor("Purple Diatoms 1 Hidden Access 1 Right Door", Orientation.Right)
    ]

    PURPLEDIATOMS1_HIDDENACCESS2 = "Purple Diatoms 1 Hidden Access 2", [
        AVDoor("Purple Diatoms 1 Hidden Access 2 Left Door", Orientation.Left, logic=lambda state: logicfunction.anyup(state) and logicfunction.anycoat(state)),
        AVDoor("Purple Diatoms 1 Hidden Access 2 Right Door", Orientation.Right, logic=lambda state: logicfunction.trenchcoat(state) and (logicfunction.redcoat(state) or state.has("Grapple") or state.has("Field Disruptor") or logicfunction.shortdrone(state)))
    ]

    LAVATUNNEL = "Lava Tunnel", [
        AVDoor("Lava Tunnel Left Door", Orientation.Left, logic=lambda state: state.has("Weapon")),
        AVDoor("Lava Tunnel Right Door", Orientation.Right, logic=lambda state: state.has("Weapon"))
    ]

    LAVASECRET = "Lava Secret", [AVDoor("Lava Secret Left Door", Orientation.Left)]

    # greenfungus1: 2 regions
    GREEN_FUNGUS1_UPPER = "Green Fungus 1_Upper", [
        AVDoor("Green Fungus 1 Left Door", Orientation.Left),
        AVDoor("Green Fungus 1 Right Door", Orientation.Right),
        AVDoor("Green Fungus 1 Inner UB", logic=lambda state: logicfunction.anycoat(state) or logicfunction.dronequest(state))
    ]
    GREEN_FUNGUS1_LOWER = "Green Fungus 1_Lower", [
        AVDoor("Green Fungus 1 Down Door", Orientation.Down),
        AVDoor("Green Fungus 1 Inner BU")
    ]

    GREEN_FUNGUS1_SECRET1 = "Green Fungus 1 Secret 1", [AVDoor("Green Fungus 1 Secret 1 Up Door", Orientation.Up)]

    CHASMS = "Chasms", [
        AVDoor("Chasms Left Door", Orientation.Left),
        AVDoor("Chasms Right Door", Orientation.Right)
    ]

    FUNGUS_FOREST = "Fungus Forest", [
        AVDoor("Fungus Forest Lower Left Door", Orientation.Left),
        AVDoor("Fungus Forest Upper Left Door", Orientation.Left),
        AVDoor("Fungus Forest Upper Right Door", Orientation.Right),
        AVDoor("Fungus Forest Lower Right Door", Orientation.Right)
    ]

    ABSU_SAVE5 = "Absu Save 5", [
        AVDoor("Absu Save 5 Right Door", Orientation.Right),
        AVDoor("Absu Save 5 Save", Orientation.Save)
    ]

    FUNGUS_SHRINE = "Fungus Shrine", [AVDoor("Fungus Shrine Left Door", Orientation.Left)]

    VINE_SHAFT = "Vine Shaft", [
        AVDoor("Vine Shaft Left Door", Orientation.Left),
        AVDoor("Vine Shaft Right Door", Orientation.Right)
    ]

    ABSU_TO_ZI = "Absu to Zi", [
        AVDoor("Absu to Zi Left Door", Orientation.Left),
        AVDoor("Absu to Zi Right Door", Orientation.Right, BossDoor.Areatrans)
    ]

    ZI_TO_ABSU = "Zi to Absu", [
        AVDoor("Zi to Absu Left Door", Orientation.Left, BossDoor.Areatrans),
        AVDoor("Zi to Absu Right Door", Orientation.Right)
    ]

    STEAM_ROOM1 = "Steam Room 1", [
        AVDoor("Steam Room 1 Left Door", Orientation.Left),
        AVDoor("Steam Room 1 Right Door", Orientation.Right)
    ]

    # steamroom2: 3 regions
    STEAM_ROOM2_WEST = "Steam Room 2_West", [
        AVDoor("Steam Room 2 Lower Left Door", Orientation.Left),
        AVDoor("Steam Room 2 Inner WE")
    ]
    STEAM_ROOM2_EAST = "Steam Room 2_East", [
        AVDoor("Steam Room 2 Right Door", Orientation.Right),
        AVDoor("Steam Room 2 Inner EW"),
        AVDoor("Steam Room 2 Inner EU")
    ]
    STEAM_ROOM2_UPPER = "Steam Room 2_Upper", [
        AVDoor("Steam Room 2 Upper Left Door", Orientation.Left),
        AVDoor("Steam Room 2 Inner UE")
    ]

    HIDDEN_MUTANTS = "Hidden Mutants", [
        AVDoor('Hidden Mutants Lower Right Door', Orientation.Right),
        AVDoor("Hidden Mutants Upper Right Door", Orientation.Right)
    ]

    STEAM1_SECRET = "Steam 1 Secret", [AVDoor("Steam 1 Secret Left Door", Orientation.Left)]

    ZI_SAVE1 = "Zi Save 1", [
        AVDoor("Zi Save 1 Left Door", Orientation.Left),
        AVDoor("Zi Save 1 Right Door", Orientation.Right),
        AVDoor("Zi Save 1 Save", Orientation.Save)
    ]

    CENTRAL_ACCESS = "Central Access", [
        AVDoor("Central Access Left Door", Orientation.Left),
        AVDoor("Central Access Right Door", Orientation.Right)
    ]

    #centraltube: 3 regions
    CENTRAL_TUBE_LOWER = "Central Tube_Lower", [
        AVDoor("Central Tube Lower Left Door", Orientation.Left),
        AVDoor("Central Tube Right Door", Orientation.Right),
        AVDoor("Central Tube Inner BS"),
        AVDoor("Central Tube Inner BU")
    ]
    CENTRAL_TUBE_UPPER = "Central Tube_Upper", [
        AVDoor("Central Tube Up Door", Orientation.Up),
        AVDoor("Central Tube Inner UB")
    ]
    CENTRAL_TUBE_SECRET = "Central Tube_Secret", [
        AVDoor("Central Tube Upper Left Door", Orientation.Left),
        AVDoor("Central Tube Inner SB")
    ]

    EYE_STALK_TUNNEL = "Eye Stalk Tunnel", [
        AVDoor("Eye Stalk Tunnel Left Door", Orientation.Left),
        AVDoor("Eye Stalk Tunnel Right Door", Orientation.Right)
    ]

    EYE_STALK_SECRET1 = "Eye Stalk Secret 1", [
        AVDoor("Eye Stalk Secret 1 Left Door", Orientation.Left),
        AVDoor("Eye Stalk Secret 1 Right Door", Orientation.Right)
    ]

    EYE_STALK_SECRET2 = "Eye Stalk Secret 2", [AVDoor("Eye Stalk Secret 2 Right Door", Orientation.Right)]

    ARTERIAL_ACCESS = "Arterial Access", [
        AVDoor("Arterial Access Left Door", Orientation.Left),
        AVDoor("Arterial Access Right Door", Orientation.Right)
    ]

    ARTERIAL_SHAFT = "Arterial Shaft", [
        AVDoor("Arterial Shaft Lower Left Door", Orientation.Left),
        AVDoor("Arterial Shaft Lower Right Door", Orientation.Right),
        AVDoor("Arterial Shaft Upper Left Door", Orientation.Left),
        AVDoor("Arterial Shaft Upper Right Door", Orientation.Right)
    ]

    VERUSKA_ACCESS = "Veruska Access", [  # prison was too generic, so I changed it to not conflict with other rooms
        AVDoor("Veruska Access Upper Left Door", Orientation.Left),
        AVDoor("Veruska Access Lower Left Door", Orientation.Left)
    ]

    VERUSKA = "Veruska", [
        AVDoor("Veruska Right Door", Orientation.Right),
        AVDoor("Veruska Left Door", Orientation.Left)
    ]

    VERUSKA_STORAGE = "Veruska Storage", [
        AVDoor("Veruska Storage Right Door", Orientation.Right),
        AVDoor("Veruska Storage Down Door", Orientation.Down)
    ]

    VERUSKA_BASEMENT = "Veruska Basement", [
        AVDoor("Veruska Basement Up Door", Orientation.Up),
        AVDoor("Veruska Basement Left Door", Orientation.Left)
    ]

    VERUSKA_SECRET = "Veruska Secret", [AVDoor("Veruska Secret Right Door", Orientation.Right)]

    ZI_SAVE3 = "Zi Save 3", [
        AVDoor("Zi Save 3 Left Door", Orientation.Left),
        AVDoor("Zi Save 3 Right Door", Orientation.Right),
        AVDoor("Zi Save 3 Save", Orientation.Save)
    ]

    ARTERIAL_MAIN = "Arterial Main", [
        AVDoor("Arterial Main Lower Left Door", Orientation.Left),
        AVDoor("Arterial Main Upper Left Door", Orientation.Left),
        AVDoor("Arterial Main Right Door", Orientation.Right)
    ]

    ZI_TO_KUR = "Zi to Kur", [
        AVDoor("Zi to Kur Left Door", Orientation.Left),
        AVDoor("Zi to Kur Right Door", Orientation.Right, BossDoor.Areatrans)
    ]

    ARTERIAL_BYPASS = "Arterial Bypass", [
        AVDoor("Arterial Bypass Right Door", Orientation.Right),
        AVDoor("Arterial Bypass Left Door", Orientation.Left),
        AVDoor("Arterial Bypass Down Door", Orientation.Down)
    ]

    # arterialfiltration: technically 2 regions
    ARTERIAL_FILTRATION = "Arterial Filtration", [
        AVDoor("Arterial Filtration Right Door", Orientation.Right),
        AVDoor("Arterial Filtration Inner MS")
    ]

    ARTERIAL_FILTRATION_UPPER = "Arterial Filtration_Upper", [
        AVDoor("Arterial Filtration Up Door", Orientation.Up),
        AVDoor("Arterial Filtration Inner SM")
    ]

    ARTERIAL_BYPASS_ENTRANCE = "Arterial Bypass Entrance", [
        AVDoor("Arterial Bypass Entrance Right Door", Orientation.Right),
        AVDoor("Arterial Bypass Entrance Left Door", Orientation.Left),
    ]

    # uppertube: 4 regions
    UPPER_TUBE_LOWER = "Upper Tube_Lower", [
        AVDoor("Upper Tube Down Door", Orientation.Down),
        AVDoor("Upper Tube Inner BC")
    ]

    UPPER_TUBE_CENTER = "Upper Tube_Center", [
        AVDoor("Upper Tube Lower Right Door", Orientation.Right),
        AVDoor("Upper Tube Inner CB"),
        AVDoor("Upper Tube Inner CS"),
        AVDoor("Upper Tube Inner CU")
    ]

    UPPER_TUBE_SECRET = "Upper Tube_Secret", [
        AVDoor("Upper Tube Lower Left Door", Orientation.Left),
        AVDoor("Upper Tube Inner SC")
    ]

    UPPER_TUBE_UPPER = "Upper Tube_Upper", [
        AVDoor("Upper Tube Upper Left Door", Orientation.Left),
        AVDoor("Upper Tube Upper Right Door", Orientation.Right),
        AVDoor("Upper Tube Inner UC")
    ]

    VENOUS_FILTRATION_ACCESS = "Venous Filtration Access", [
        AVDoor("Venous Filtration Access Right Door", Orientation.Right),
        AVDoor("Venous Filtration Access Left Door", Orientation.Left)
    ]

    VENOUS_FILTRATION = "Venous Filtration", [
        AVDoor("Venous Filtration Right Door", Orientation.Right),
        AVDoor("Venous Filtration Left Door", Orientation.Left)
    ]

    VENOUS_MAINTENANCE_ACCESS = "Venous Maintenance Access", [
        AVDoor("Venous Maintenance Access Right Door", Orientation.Right),
        AVDoor("Venous Maintenance Access Left Door", Orientation.Left)
    ]

    VENOUS_MAINTENANCE1 = "Venous Maintenance 1", [
        AVDoor("Venous Maintenance 1 Right Door", Orientation.Right),
        AVDoor("Venous Maintenance 1 Left Door", Orientation.Left)
    ]

    # venousmaintenance2: 3 regions
    VENOUS_MAINTENANCE2_UPPER = "Venous Maintenance 2_Upper", [
        AVDoor("Venous Maintenance 2 Upper Right Door", Orientation.Right),
        AVDoor("Venous Maintenance 2 Inner UC"),
        AVDoor("Venous Maintenance 2 Inner UB")
    ]

    VENOUS_MAINTENANCE2_CENTER = "Venous Maintenance 2_Center", [
        AVDoor("Venous Maintenance 2 Center Right Door", Orientation.Right),
        AVDoor("Venous Maintenance 2 Inner CU"),
        AVDoor("Venous Maintenance 2 Inner CB")
    ]

    VENOUS_MAINTENANCE2_LOWER = "Venous Maintenance 2_Lower", [
        AVDoor("Venous Maintenance 2 Lower Right Door", Orientation.Right),
        AVDoor("Venous Maintenance 2 Inner BC"),
        AVDoor("Venous Maintenance 2 Inner BU")
    ]

    VENOUS_MAINTENANCE3 = "Venous Maintenance 3", [
        AVDoor("Venous Maintenance 3 Left Door", Orientation.Left)
    ]

    VENOUS_MAINTENANCE4 = "Venous Maintenance 4", [
        AVDoor("Venous Maintenance 4 Right Door", Orientation.Right),
        AVDoor("Venous Maintenance 4 Left Door", Orientation.Left)
    ]

    VENOUS_MAINTENANCE_SECRET = "Venous Maintenance Secret", [
        AVDoor("Venous Maintenance Secret Left Door", Orientation.Left)
    ]

    ZI_SAVE2 = "Zi Save 2", [
        AVDoor("Zi Save 2 Left Door", Orientation.Left),
        AVDoor("Zi Save 2 Right Door", Orientation.Right),
        AVDoor("Zi Save 2 Save", Orientation.Save)
    ]

    ZI_TO_INDI = "Zi to Indi", [
        AVDoor("Zi to Indi Up Door", Orientation.Up, BossDoor.Areatrans),
        AVDoor("Zi to Indi Right Door", Orientation.Right)
    ]

    URUKU_FOYER = "Uruku Foyer", [
        AVDoor("Uruku Foyer Left Door", Orientation.Left),
        AVDoor("Uruki Foyer Right Door", Orientation.Right, BossDoor.Outer)
    ]

    # uruku: 2 regions
    URUKU_MAIN = "Uruku_Main", [
        AVDoor("Uruku Left Door", Orientation.Left, BossDoor.Inner),
        AVDoor("Uruku Upper Right Door", Orientation.Right, BossDoor.Inner),
        AVDoor("Uruku Inner MS")
    ]

    URUKU_SECRET = "Uruku_Secret", [
        AVDoor("Uruku Lower Right Door", Orientation.Right, BossDoor.Inner),
        AVDoor("Uruku Inner SM")
    ]

    # filtration: 3 regions
    FILTRATION_UPPER = "Filtration_Upper", [
        AVDoor("Filtration Upper Left Door", Orientation.Left, BossDoor.Outer),
        AVDoor("Filtration Inner UE")
    ]

    FILTRATION_EAST = "Filtration_East", [
        AVDoor("Filtration Right Door", Orientation.Right),
        AVDoor("Filtration Inner EW"),
        AVDoor("Filtration Inner EU")
    ]

    FILTRATION_WEST = "Filtration_West", [
        AVDoor("Filtration Lower Left Door", Orientation.Left, BossDoor.Outer),
        AVDoor("Filtration Inner WE")
    ]

    LABCOAT = "Labcoat Room", [
        AVDoor("Labcoat Room Left Door", Orientation.Left)
    ]

    #kurshaft: 5 regions
    KUR_SHAFT_LOWER = "Kur Shaft_Lower", [
        AVDoor("Kur Shaft Lower Left Door", Orientation.Left, BossDoor.Areatrans),
        AVDoor("Kur Shaft Lower Right Door", Orientation.Right),
        AVDoor("Kur Shaft Lower Center Right Door", Orientation.Right),
        AVDoor("Kur Shaft Upper Center Right Door", Orientation.Right),
        AVDoor("Kur Shaft Upper Right Door", Orientation.Right),
        AVDoor("Kur Shaft Inner BC", logic=lambda state: logicfunction.anycoat(state)),
        AVDoor("Kur Shaft Inner BT", logic=lambda state: logicfunction.tempup(state) and logicfunction.anycoat(state))
    ]

    KUR_SHAFT_CENTER = "Kur Shaft_Center", [
        AVDoor("Kur Shaft Center Left Door", Orientation.Left),
        AVDoor("Kur Shaft Inner CB", logic=lambda state: logicfunction.anycoat(state)),
        AVDoor("Kur Shaft Inner CT", logic=lambda state: logicfunction.tempup(state) and logicfunction.anycoat(state))
    ]

    KUR_SHAFT_TRANSIT = "Kur Shaft_Transit", [
        AVDoor("Kur Shaft Inner TB", logic=lambda state: logicfunction.anycoat(state)),
        AVDoor("Kur Shaft Inner TC", logic=lambda state: logicfunction.anycoat(state)),
        AVDoor("Kur Shaft Inner TU", logic=lambda state: logicfunction.tempup(state))
    ]

    KUR_SHAFT_UPPER = "Kur Shaft_Upper", [
        AVDoor("Kur Shaft Up Door", Orientation.Up),
        AVDoor("Kur Shaft Inner UT"),
        AVDoor("Kur Shaft Inner US", logic=lambda state: logicfunction.glitch2(state) or logicfunction.trenchcoat(state))
    ]

    KUR_SHAFT_SECRET = "Kur Shaft_Secret", [
        AVDoor("Kur Shaft Upper Left Door", Orientation.Left),
        AVDoor("Kur Shaft Inner SU", logic=lambda state: logicfunction.glitch2(state) or logicfunction.trenchcoat(state))
    ]

    KUR_SAVE1 = "Kur Save 1", [
        AVDoor("Kur Save 1 Left Door", Orientation.Left),
        AVDoor("Kur Save 1 Save", Orientation.Save)
    ]

    TO_ADDRESS_DISRUPTOR = "To Address Disruptor", [
        AVDoor("To Address Disruptor Left Door", Orientation.Left, logic=lambda state: logicfunction.trenchcoat(state) and logicfunction.breakblock(state)),
        AVDoor("To Address Disruptor Down Door", Orientation.Down, logic=lambda state: logicfunction.anycoat(state) and (state.has("Fat Beam") or logicfunction.drone(state) or logicfunction.trenchcoat(state)))
    ]

    #addressdisruptor2: 3 regions
    ADDRESS_DISRUPTOR2_MAIN = "Address Disruptor 2_Main", [
        AVDoor("Address Disruptor 2 Up Door", Orientation.Up),
        AVDoor("Address Disruptor 2 Inner MS", logic=lambda state: logicfunction.anycoat(state) and (state.has("Fat Beam") or logicfunction.drone(state) or logicfunction.trenchcoat(state)))
    ]

    ADDRESS_DISRUPTOR2_SECRET = "Address Disruptor 2_Secret", [
        AVDoor("Address Disruptor 2 Inner SW", logic=lambda state: logicfunction.redcoat(state) or (logicfunction.glitch2(state) and logicfunction.breakblock(state))),
        AVDoor("Address Disruptor 2 Inner SM", logic=lambda state: logicfunction.tempup(state) and logicfunction.anycoat(state) and (state.has("Fat Beam") or logicfunction.drone(state) or logicfunction.trenchcoat(state)))
    ]

    ADDRESS_DISRUPTOR2_WEST = "Address Disruptor 2_West", [
        AVDoor("Address Disruptor 2 Left Door", Orientation.Left),
        AVDoor("Address Disruptor 2 Inner WS", logic=lambda state: logicfunction.redcoat(state) or (logicfunction.glitch2(state) and logicfunction.breakblock(state)))

    ]

    SURFACE_SHAFT = "Surface Shaft", [
        AVDoor("Surface Shaft Left Door", Orientation.Left),
        AVDoor("Surface Shaft Right Door", Orientation.Right)
    ]

    #cavernaccess: 2 regions
    CAVERN_ACCESS_MAIN = "Cavern Access_Main", [
        AVDoor("Cavern Access Left Door", Orientation.Left),
        AVDoor("Cavern Access Down Door", Orientation.Down),
        AVDoor("Cavern Access Inner MS", logic=lambda state: logicfunction.tempup(state) and logicfunction.breakblock(state) and logicfunction.anycoat(state))
    ]

    CAVERN_ACCESS_SECRET = "Cavern Access_Secret", [
        AVDoor("Cavern Access Right Door", Orientation.Right),
        AVDoor("Cavern Access Inner SM", logic=lambda state: logicfunction.breakblock(state) and logicfunction.anycoat(state))
    ]
    
    #highjumpaccess: 2 regions
    HIGH_JUMP_ACCESS_UPPER = "High Jump Access_Upper", [
        AVDoor("High Jump Access Up Door", Orientation.Up),
        AVDoor("High Jump Access Inner UB")
    ]

    HIGH_JUMP_ACCESS_LOWER = "Hight Jump Access_Lower", [
        AVDoor("High Jump Access Right Door", Orientation.Right),
        AVDoor("High Jump Access Inner BU", logic=lambda state: logicfunction.anyup(state))
    ]

    HIGH_JUMP_ROOM_MAIN = "High Jump Room_Main", [
        AVDoor("High Jump Room Left Door", Orientation.Left, logic=lambda state: logicfunction.anyup(state)),
        AVDoor("High Jump Room Inner MS", logic=lambda state: logicfunction.trenchcoat(state))
    ]

    HIGH_JUMP_ROOM_SECRET = "High Jump Room_Secret", [
        AVDoor("High Jump Room Right Door", Orientation.Right),
        AVDoor("High Jumpt Room Inner SM", logic=lambda state: logicfunction.trenchcoat(state))
    ]

    #this room blows
    STALAGMITE_MAZE = "Stalagmite Maze", [
        AVDoor("Stalagmite Maze Left Door", Orientation.Left, logic=lambda state: logicfunction.dronefly(state) or ((logicfunction.shortdrone(state) and logicfunction.verylongwarp(state)) or (logicfunction.longdrone(state) and logicfunction.longwarp(state)))),
        AVDoor("Stalagmite Maze Down Door", Orientation.Down, logic=lambda state: logicfunction.dronefly(state) or (logicfunction.anyglitch(state) and (logicfunction.drone(state) or logicfunction.redcoat(state))))
    ]

    TETHERED_CHARGE = "Tethered Charge", [
        AVDoor("Tethered Charge Up Door", Orientation.Up, logic=lambda state: logicfunction.dronefly(state) and logicfunction.trenchcoat(state)),
        AVDoor("Tethered Charge Left Door", Orientation.Left)
    ]

    SECRET_PASSAGE_TO_TETHERED_CHARGE = "Secret Passage To Tethered Charge", [
        AVDoor("Secret Passage to Tethered Charge Right Door", Orientation.Right, logic=lambda state: state.has("Fat Beam")),
        AVDoor("Secret Passage to Tethered Charge Left Door", Orientation.Left, logic=lambda state: logicfunction.breakblock(state))
    ]


class AVDoorID(NamedTuple):
    region: AVRegion
    index: int


class AVConnection(NamedTuple):
    enter: AVDoorID
    exit: AVDoorID
    twoway: bool = True


axiom_verge_connections = [
    AVConnection(AVDoorID(AVRegion.MENU, 0), AVDoorID(AVRegion.ERIBU_SAVE1_WEST, 2)),  # REWORK WHEN/IF SPAWN RANDO
    AVConnection(AVDoorID(AVRegion.ERIBU_SAVE1_WEST, 1), AVDoorID(AVRegion.ERIBU_SAVE1_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.DISRUPTOR_ROOM_EAST, 1), AVDoorID(AVRegion.DISRUPTOR_ROOM_WEST, 2)),
    AVConnection(AVDoorID(AVRegion.BRINSTAR_SHAFT_LOWER, 4), AVDoorID(AVRegion.BRINSTAR_SHAFT_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.BRINSTAR_SHAFT_CENTER, 2), AVDoorID(AVRegion.BRINSTAR_SHAFT_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.SPITBUG_HALL_WEST, 2), AVDoorID(AVRegion.SPITBUG_HALL_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.MULTI_DISRUPTOR_LOWER, 1), AVDoorID(AVRegion.MULTI_DISRUPTOR_UPPER, 2)),
    AVConnection(AVDoorID(AVRegion.FORBIDDEN_CORRIDOR_EAST, 1), AVDoorID(AVRegion.FORBIDDEN_CORRIDOR_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.DRILL_ROOM_UPPER, 1), AVDoorID(AVRegion.DRILL_ROOM_LOWER, 1)),
    AVConnection(AVDoorID(AVRegion.XEDUR_BASEMENT_EAST, 1), AVDoorID(AVRegion.XEDUR_BASEMENT_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.THE_DROP_MAIN, 4), AVDoorID(AVRegion.THE_DROP_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.SECRET_CHAMBER_LOWER, 1), AVDoorID(AVRegion.SECRET_CHAMBER_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.ERIBU_TO_INDI_EAST, 1), AVDoorID(AVRegion.ERIBU_TO_INDI_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.PRIMORDIAL_CAVERN_EAST, 2), AVDoorID(AVRegion.PRIMORDIAL_CAVERN_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.PRIMORDIAL_CAVERN_WEST, 2), AVDoorID(AVRegion.PRIMORDIAL_CAVERN_CENTER, 0)),
    AVConnection(AVDoorID(AVRegion.PRIMORDIAL_CAVERN_EAST, 1), AVDoorID(AVRegion.PRIMORDIAL_CAVERN_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.FLAMETHROWER_ACCESS_EAST, 1), AVDoorID(AVRegion.FLAMETHROWER_ACCESS_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.FLAMETHROWER_ACCESS_EAST, 2), AVDoorID(AVRegion.SLUG, 0)),
    AVConnection(AVDoorID(AVRegion.ABSU_SHAFT_UPPER, 5), AVDoorID(AVRegion.ABSU_SHAFT_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.ABSU_SHAFT_LOWER, 1), AVDoorID(AVRegion.ABSU_SHAFT_CENTER, 2)),
    AVConnection(AVDoorID(AVRegion.VENTILATION_EAST, 1), AVDoorID(AVRegion.VENTILATION_CENTER, 2)),
    AVConnection(AVDoorID(AVRegion.VENTILATION_CENTER, 1), AVDoorID(AVRegion.VENTILATION_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.ATTIC_WEST, 1), AVDoorID(AVRegion.ATTIC_CENTER_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.ATTIC_CENTER_WEST, 1), AVDoorID(AVRegion.ATTIC_CENTER_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.ATTIC_CENTER_EAST, 1), AVDoorID(AVRegion.ATTIC_LOWER_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.ATTIC_UPPER_EAST, 0), AVDoorID(AVRegion.ATTIC_LOWER_EAST, 2)),
    AVConnection(AVDoorID(AVRegion.PINK_DIATOMS2_EAST, 1), AVDoorID(AVRegion.PINK_DIATOMS2_WEST, 2)),
    AVConnection(AVDoorID(AVRegion.PINK_DIATOMS1_UPPER, 1), AVDoorID(AVRegion.PINK_DIATOMS1_CENTER, 2)),
    AVConnection(AVDoorID(AVRegion.PINK_DIATOMS1_CENTER, 3), AVDoorID(AVRegion.PINK_DIATOMS1_LOWER, 1)),
    AVConnection(AVDoorID(AVRegion.PRISON1_UPPER, 2), AVDoorID(AVRegion.PRISON1_LOWER, 1)),
    AVConnection(AVDoorID(AVRegion.TELAL_TREASURY_UPPER, 1), AVDoorID(AVRegion.TELAL_TREASURY_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.TELAL_TREASURY_UPPER, 2), AVDoorID(AVRegion.TELAL_TREASURY_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.TELAL_TREASURY_SOUTH, 0), AVDoorID(AVRegion.TELAL_TREASURY_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.TELAL_TREASURY_SOUTH, 1), AVDoorID(AVRegion.TELAL_TREASURY_EAST, 2)),
    AVConnection(AVDoorID(AVRegion.DUCTS1_WEST, 1), AVDoorID(AVRegion.DUCTS1_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.DUCTS1_WEST, 2), AVDoorID(AVRegion.DUCTS1_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.PURPLE_DIATOMS1_UPPER, 3), AVDoorID(AVRegion.PURPLEDIATOMS1_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.PURPLEDIATOMS1_WEST, 2), AVDoorID(AVRegion.PURPLEDIATOMS1_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.PURPLEDIATOMS1_EAST, 2), AVDoorID(AVRegion.PURPLE_DIATOMS1_UPPER, 4)),
    AVConnection(AVDoorID(AVRegion.GREEN_FUNGUS1_UPPER, 2), AVDoorID(AVRegion.GREEN_FUNGUS1_LOWER, 1)),
    AVConnection(AVDoorID(AVRegion.STEAM_ROOM2_WEST, 1), AVDoorID(AVRegion.STEAM_ROOM2_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.STEAM_ROOM2_EAST, 2), AVDoorID(AVRegion.STEAM_ROOM2_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.CENTRAL_TUBE_LOWER, 2), AVDoorID(AVRegion.CENTRAL_TUBE_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.CENTRAL_TUBE_LOWER, 3), AVDoorID(AVRegion.CENTRAL_TUBE_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.ARTERIAL_FILTRATION, 1), AVDoorID(AVRegion.ARTERIAL_FILTRATION_UPPER, 1), False),
    AVConnection(AVDoorID(AVRegion.UPPER_TUBE_LOWER, 1), AVDoorID(AVRegion.UPPER_TUBE_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.UPPER_TUBE_CENTER, 2), AVDoorID(AVRegion.UPPER_TUBE_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.UPPER_TUBE_CENTER, 3), AVDoorID(AVRegion.UPPER_TUBE_UPPER, 2)),
    AVConnection(AVDoorID(AVRegion.VENOUS_MAINTENANCE2_UPPER, 1), AVDoorID(AVRegion.VENOUS_MAINTENANCE2_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.VENOUS_MAINTENANCE2_UPPER, 2), AVDoorID(AVRegion.VENOUS_MAINTENANCE2_LOWER, 2)),
    AVConnection(AVDoorID(AVRegion.VENOUS_MAINTENANCE2_CENTER, 2), AVDoorID(AVRegion.VENOUS_MAINTENANCE2_LOWER, 1)),
    AVConnection(AVDoorID(AVRegion.URUKU_MAIN, 2), AVDoorID(AVRegion.URUKU_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.FILTRATION_EAST, 1), AVDoorID(AVRegion.FILTRATION_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.FILTRATION_EAST, 2), AVDoorID(AVRegion.FILTRATION_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_LOWER, 5), AVDoorID(AVRegion.KUR_SHAFT_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_LOWER, 6), AVDoorID(AVRegion.KUR_SHAFT_TRANSIT, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_CENTER, 2), AVDoorID(AVRegion.KUR_SHAFT_TRANSIT, 1)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_TRANSIT, 2), AVDoorID(AVRegion.KUR_SHAFT_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_UPPER, 2), AVDoorID(AVRegion.KUR_SHAFT_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.ADDRESS_DISRUPTOR2_MAIN, 1), AVDoorID(AVRegion.ADDRESS_DISRUPTOR2_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.ADDRESS_DISRUPTOR2_WEST, 1), AVDoorID(AVRegion.ADDRESS_DISRUPTOR2_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.CAVERN_ACCESS_MAIN, 2), AVDoorID(AVRegion.CAVERN_ACCESS_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.HIGH_JUMP_ACCESS_UPPER, 1), AVDoorID(AVRegion.HIGH_JUMP_ACCESS_LOWER, 1)),
    AVConnection(AVDoorID(AVRegion.HIGH_JUMP_ROOM_MAIN, 1), AVDoorID(AVRegion.HIGH_JUMP_ROOM_SECRET, 1))
]

axiom_verge_doors = [
    AVConnection(AVDoorID(AVRegion.ERIBU_SAVE1_WEST, 0), AVDoorID(AVRegion.DISRUPTOR_ROOM_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.DISRUPTOR_ROOM_WEST, 1), AVDoorID(AVRegion.BUBBLE_MAZE, 0)),
    AVConnection(AVDoorID(AVRegion.BUBBLE_MAZE, 1), AVDoorID(AVRegion.WHEELCHAIR, 0)),
    AVConnection(AVDoorID(AVRegion.DISRUPTOR_ROOM_WEST, 0), AVDoorID(AVRegion.PRIMORDIAL_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.PRIMORDIAL_ACCESS, 1), AVDoorID(AVRegion.PRIMORDIAL_CAVERN_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.PRIMORDIAL_CAVERN_WEST, 0), AVDoorID(AVRegion.FLAMETHROWER_ACCESS_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.FLAMETHROWER_ACCESS_EAST, 0), AVDoorID(AVRegion.FLAMETHROWER_ROOM, 0)),
    AVConnection(AVDoorID(AVRegion.ERIBU_SAVE1_EAST, 0), AVDoorID(AVRegion.BUBBLE_WALL, 0)),
    AVConnection(AVDoorID(AVRegion.BUBBLE_WALL, 1), AVDoorID(AVRegion.BRINSTAR_SHAFT_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.BRINSTAR_SHAFT_LOWER, 1), AVDoorID(AVRegion.DIGGY_HOLE, 0)),
    AVConnection(AVDoorID(AVRegion.BRINSTAR_SHAFT_LOWER, 2), AVDoorID(AVRegion.NOVA_GATE, 0)),
    AVConnection(AVDoorID(AVRegion.BRINSTAR_SHAFT_LOWER, 3), AVDoorID(AVRegion.SPITBUG_HALL_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.BRINSTAR_SHAFT_CENTER, 0), AVDoorID(AVRegion.BUBBLED_ALTAR, 0)),
    AVConnection(AVDoorID(AVRegion.BRINSTAR_SHAFT_UPPER, 0), AVDoorID(AVRegion.BUOYG_HALL, 0)),
    AVConnection(AVDoorID(AVRegion.SPITBUG_HALL_WEST, 1), AVDoorID(AVRegion.WRONG_TOWER, 0)),
    AVConnection(AVDoorID(AVRegion.WRONG_TOWER, 1), AVDoorID(AVRegion.FALSE_REFLECTOR_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.FALSE_REFLECTOR_ACCESS, 1), AVDoorID(AVRegion.FALSE_REFLECTOR, 0)),
    AVConnection(AVDoorID(AVRegion.SPITBUG_HALL_EAST, 0), AVDoorID(AVRegion.NOVA_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.NOVA_ACCESS, 1), AVDoorID(AVRegion.NOVA_ROOM, 0)),
    AVConnection(AVDoorID(AVRegion.BUOYG_HALL, 1), AVDoorID(AVRegion.MULTI_DISRUPTOR_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.MULTI_DISRUPTOR_UPPER, 0), AVDoorID(AVRegion.FORBIDDEN_CORRIDOR_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.MULTI_DISRUPTOR_UPPER, 1), AVDoorID(AVRegion.CRYPTOGRAPHY, 0)),
    AVConnection(AVDoorID(AVRegion.CRYPTOGRAPHY, 1), AVDoorID(AVRegion.THRILLER, 0), False),
    AVConnection(AVDoorID(AVRegion.THRILLER, 1), AVDoorID(AVRegion.FORBIDDEN_SHAFT, 0)),
    AVConnection(AVDoorID(AVRegion.FORBIDDEN_SHAFT, 1), AVDoorID(AVRegion.FORBIDDEN_CORRIDOR_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.NOVA_GATE, 1), AVDoorID(AVRegion.XEDUR_FOYER, 0)),
    AVConnection(AVDoorID(AVRegion.XEDUR_FOYER, 1), AVDoorID(AVRegion.ERIBU_SAVE2, 0)),
    AVConnection(AVDoorID(AVRegion.XEDUR_FOYER, 2), AVDoorID(AVRegion.XEDUR_BASEMENT_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.XEDUR_FOYER, 3), AVDoorID(AVRegion.XEDUR_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.XEDUR_ACCESS, 1), AVDoorID(AVRegion.XEDUR, 0)),
    AVConnection(AVDoorID(AVRegion.XEDUR, 1), AVDoorID(AVRegion.DRILL_ROOM_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.DRILL_ROOM_LOWER, 0), AVDoorID(AVRegion.XEDUR_BASEMENT_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.DIGGY_HOLE, 1), AVDoorID(AVRegion.THE_DROP_MAIN, 0)),
    AVConnection(AVDoorID(AVRegion.THE_DROP_SECRET, 0), AVDoorID(AVRegion.WEAPONS_VAULT, 0)),
    AVConnection(AVDoorID(AVRegion.THE_DROP_MAIN, 1), AVDoorID(AVRegion.ERIBU_TO_UKKINNA, 0)),
    AVConnection(AVDoorID(AVRegion.THE_DROP_MAIN, 2), AVDoorID(AVRegion.ERIBU_TO_INDI_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.THE_DROP_MAIN, 3), AVDoorID(AVRegion.BUBBLEWRAP, 0)),
    AVConnection(AVDoorID(AVRegion.BUBBLEWRAP, 1), AVDoorID(AVRegion.SECRET_CHAMBER_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.BUBBLEWRAP, 2), AVDoorID(AVRegion.ERIBU_TO_ABSU, 0)),
    AVConnection(AVDoorID(AVRegion.SECRET_CHAMBER_UPPER, 0), AVDoorID(AVRegion.DISCHARGE_CHAMBER, 0), False),
    AVConnection(AVDoorID(AVRegion.ERIBU_TO_ABSU, 1), AVDoorID(AVRegion.ABSU_SHAFT_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.ABSU_SAVE1, 0), AVDoorID(AVRegion.ABSU_SHAFT_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.ABSU_SHAFT_UPPER, 3), AVDoorID(AVRegion.DONUT_VAULT, 0)),
    AVConnection(AVDoorID(AVRegion.ABSU_SHAFT_CENTER, 0), AVDoorID(AVRegion.UPPER_SHAFT_BASEMENT, 0)),
    AVConnection(AVDoorID(AVRegion.ABSU_SHAFT_LOWER, 0), AVDoorID(AVRegion.LOWER_SHAFT_BASEMENT, 0)),
    AVConnection(AVDoorID(AVRegion.ABSU_SHAFT_UPPER, 2), AVDoorID(AVRegion.VENTILATION_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.VENTILATION_CENTER, 0), AVDoorID(AVRegion.ATTIC_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.ATTIC_ACCESS, 1), AVDoorID(AVRegion.ATTIC_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.PINK_DIATOMS2_WEST, 0), AVDoorID(AVRegion.VENTILATION_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.PINK_DIATOMS2_EAST, 0), AVDoorID(AVRegion.ATTIC_LOWER_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.PINK_DIATOMS2_WEST, 1), AVDoorID(AVRegion.OVERGROWN_PRISON, 0)),
    AVConnection(AVDoorID(AVRegion.OVERGROWN_PRISON, 3), AVDoorID(AVRegion.ABSU_SAVE2, 0)),
    AVConnection(AVDoorID(AVRegion.OVERGROWN_PRISON, 1), AVDoorID(AVRegion.DINING_HALL, 0)),
    AVConnection(AVDoorID(AVRegion.ABSU_SHAFT_UPPER, 4), AVDoorID(AVRegion.PINK_DIATOMS_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.PINK_DIATOMS1_UPPER, 0), AVDoorID(AVRegion.DINING_HALL, 1)),
    AVConnection(AVDoorID(AVRegion.PINK_DIATOMS1_CENTER, 0), AVDoorID(AVRegion.PINK_DIATOMS_ACCESS, 1)),
    AVConnection(AVDoorID(AVRegion.PINK_DIATOMS1_LOWER, 0), AVDoorID(AVRegion.PRISON_CELLAR, 0)),
    AVConnection(AVDoorID(AVRegion.PRISON_CELLAR, 1), AVDoorID(AVRegion.PRISON_CELLAR_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.OVERGROWN_PRISON, 2), AVDoorID(AVRegion.ELSENOVA, 0)),
    AVConnection(AVDoorID(AVRegion.ELSENOVA, 1), AVDoorID(AVRegion.PRISON1_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.PINK_DIATOMS1_CENTER, 1), AVDoorID(AVRegion.PRISON1_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.PRISON1_LOWER, 0), AVDoorID(AVRegion.MAINTENANCE, 0)),
    AVConnection(AVDoorID(AVRegion.MAINTENANCE, 1), AVDoorID(AVRegion.STORAGE1, 0)),
    AVConnection(AVDoorID(AVRegion.STORAGE1, 2), AVDoorID(AVRegion.STORAGE2, 0)),
    AVConnection(AVDoorID(AVRegion.STORAGE2, 1), AVDoorID(AVRegion.TELAL_ACCESS_SHAFT, 0)),
    AVConnection(AVDoorID(AVRegion.TELAL_FOYER, 0), AVDoorID(AVRegion.TELAL_ACCESS_SHAFT, 1)),
    AVConnection(AVDoorID(AVRegion.TELAL_FOYER, 1), AVDoorID(AVRegion.ABSU_SAVE3, 0)),
    AVConnection(AVDoorID(AVRegion.TELAL_FOYER, 2), AVDoorID(AVRegion.TELAL, 0)),
    AVConnection(AVDoorID(AVRegion.TELAL, 1), AVDoorID(AVRegion.TELAL_TREASURY_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.TELAL_TREASURY_EAST, 0), AVDoorID(AVRegion.TELAL_SECRET_ACCESS1, 0)),
    AVConnection(AVDoorID(AVRegion.TELAL_SECRET_ACCESS1, 2), AVDoorID(AVRegion.TELAL_SECRET_ACCESS2, 0)),
    AVConnection(AVDoorID(AVRegion.TELAL_SECRET_ACCESS3, 0), AVDoorID(AVRegion.TELAL_SECRET_ACCESS2, 1)),
    AVConnection(AVDoorID(AVRegion.TELAL_SECRET_ACCESS3, 1), AVDoorID(AVRegion.ABSU_TO_INDI_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.ABSU_TO_INDI_UPPER, 1), AVDoorID(AVRegion.TELAL_SECRET_ACCESS4, 0)),
    AVConnection(AVDoorID(AVRegion.TELAL_SECRET_ACCESS1, 1), AVDoorID(AVRegion.TELAL_EXIT, 0)),
    AVConnection(AVDoorID(AVRegion.STORAGE1, 1), AVDoorID(AVRegion.DUCTS1_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.DUCTS1_SECRET, 0), AVDoorID(AVRegion.DUCTS1_SECRET1, 0)),
    AVConnection(AVDoorID(AVRegion.DUCTS1_SECRET1, 1), AVDoorID(AVRegion.DUCTS1_SECRET2, 0)),
    AVConnection(AVDoorID(AVRegion.DUCTS1_SECRET2, 1), AVDoorID(AVRegion.DUCTS1_SECRET3, 0)),
    AVConnection(AVDoorID(AVRegion.DUCTS1_EAST, 0), AVDoorID(AVRegion.DUCTS2, 0)),
    AVConnection(AVDoorID(AVRegion.TELAL_EXIT, 1), AVDoorID(AVRegion.PURPLE_DIATOMS1_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.DUCTS2, 1), AVDoorID(AVRegion.PURPLEDIATOMS1_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.PURPLE_DIATOMS1_UPPER, 2), AVDoorID(AVRegion.ABSU_SAVE4, 0)),
    AVConnection(AVDoorID(AVRegion.PURPLEDIATOMS1_HIDDENACCESS1, 0), AVDoorID(AVRegion.PURPLEDIATOMS1_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.PURPLEDIATOMS1_HIDDENACCESS1, 1), AVDoorID(AVRegion.PURPLEDIATOMS1_HIDDENACCESS2, 0)),
    AVConnection(AVDoorID(AVRegion.PURPLEDIATOMS1_HIDDENACCESS2, 1), AVDoorID(AVRegion.LAVATUNNEL, 0)),
    AVConnection(AVDoorID(AVRegion.LAVATUNNEL, 1), AVDoorID(AVRegion.LAVASECRET, 0)),
    AVConnection(AVDoorID(AVRegion.PURPLE_DIATOMS1_UPPER, 1), AVDoorID(AVRegion.GREEN_FUNGUS1_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.GREEN_FUNGUS1_LOWER, 0), AVDoorID(AVRegion.GREEN_FUNGUS1_SECRET1, 0)),
    AVConnection(AVDoorID(AVRegion.GREEN_FUNGUS1_UPPER, 1), AVDoorID(AVRegion.CHASMS, 0)),
    AVConnection(AVDoorID(AVRegion.CHASMS, 1), AVDoorID(AVRegion.FUNGUS_FOREST, 0)),
    AVConnection(AVDoorID(AVRegion.FUNGUS_FOREST, 1), AVDoorID(AVRegion.ABSU_SAVE5, 0)),
    AVConnection(AVDoorID(AVRegion.FUNGUS_FOREST, 2), AVDoorID(AVRegion.FUNGUS_SHRINE, 0)),
    AVConnection(AVDoorID(AVRegion.FUNGUS_FOREST, 3), AVDoorID(AVRegion.VINE_SHAFT, 0)),
    AVConnection(AVDoorID(AVRegion.VINE_SHAFT, 1), AVDoorID(AVRegion.ABSU_TO_ZI, 0)),
    AVConnection(AVDoorID(AVRegion.ABSU_TO_ZI, 1), AVDoorID(AVRegion.ZI_TO_ABSU, 0)),
    AVConnection(AVDoorID(AVRegion.ZI_TO_ABSU, 1), AVDoorID(AVRegion.STEAM_ROOM1, 0)),
    AVConnection(AVDoorID(AVRegion.STEAM_ROOM1, 1), AVDoorID(AVRegion.STEAM_ROOM2_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.STEAM_ROOM2_UPPER, 0), AVDoorID(AVRegion.HIDDEN_MUTANTS, 0)),
    AVConnection(AVDoorID(AVRegion.HIDDEN_MUTANTS, 1), AVDoorID(AVRegion.STEAM1_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.STEAM_ROOM2_EAST, 0), AVDoorID(AVRegion.ZI_SAVE1, 0)),
    AVConnection(AVDoorID(AVRegion.ZI_SAVE1, 1), AVDoorID(AVRegion.CENTRAL_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.CENTRAL_ACCESS, 1), AVDoorID(AVRegion.CENTRAL_TUBE_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.CENTRAL_TUBE_SECRET, 0), AVDoorID(AVRegion.EYE_STALK_TUNNEL, 1)),
    AVConnection(AVDoorID(AVRegion.EYE_STALK_TUNNEL, 0), AVDoorID(AVRegion.EYE_STALK_SECRET1, 1)),
    AVConnection(AVDoorID(AVRegion.EYE_STALK_SECRET1, 0), AVDoorID(AVRegion.EYE_STALK_SECRET2, 0)),
    AVConnection(AVDoorID(AVRegion.CENTRAL_TUBE_LOWER, 1), AVDoorID(AVRegion.ARTERIAL_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.ARTERIAL_ACCESS, 1), AVDoorID(AVRegion.ARTERIAL_SHAFT, 0)),
    AVConnection(AVDoorID(AVRegion.ARTERIAL_SHAFT, 1), AVDoorID(AVRegion.VERUSKA_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.VERUSKA_ACCESS, 1), AVDoorID(AVRegion.VERUSKA, 0)),
    AVConnection(AVDoorID(AVRegion.VERUSKA, 1), AVDoorID(AVRegion.VERUSKA_STORAGE, 0)),
    AVConnection(AVDoorID(AVRegion.VERUSKA_STORAGE, 1), AVDoorID(AVRegion.VERUSKA_BASEMENT, 0)),
    AVConnection(AVDoorID(AVRegion.VERUSKA_BASEMENT, 1), AVDoorID(AVRegion.VERUSKA_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.ARTERIAL_SHAFT, 3), AVDoorID(AVRegion.ZI_SAVE3, 0)),
    AVConnection(AVDoorID(AVRegion.ZI_SAVE3, 1), AVDoorID(AVRegion.ARTERIAL_MAIN, 0)),
    AVConnection(AVDoorID(AVRegion.ARTERIAL_MAIN, 2), AVDoorID(AVRegion.ZI_TO_KUR, 0)),
    AVConnection(AVDoorID(AVRegion.ARTERIAL_MAIN, 1), AVDoorID(AVRegion.ARTERIAL_BYPASS, 0)),
    AVConnection(AVDoorID(AVRegion.ARTERIAL_SHAFT, 2), AVDoorID(AVRegion.ARTERIAL_FILTRATION, 0)),
    AVConnection(AVDoorID(AVRegion.ARTERIAL_BYPASS, 2), AVDoorID(AVRegion.ARTERIAL_FILTRATION_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.ARTERIAL_BYPASS, 1), AVDoorID(AVRegion.ARTERIAL_BYPASS_ENTRANCE, 0)),
    AVConnection(AVDoorID(AVRegion.UPPER_TUBE_LOWER, 0), AVDoorID(AVRegion.CENTRAL_TUBE_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.UPPER_TUBE_CENTER, 0), AVDoorID(AVRegion.ARTERIAL_BYPASS_ENTRANCE, 1)),
    AVConnection(AVDoorID(AVRegion.UPPER_TUBE_SECRET, 0), AVDoorID(AVRegion.VENOUS_FILTRATION_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.VENOUS_FILTRATION, 0), AVDoorID(AVRegion.VENOUS_FILTRATION_ACCESS, 1)),
    AVConnection(AVDoorID(AVRegion.VENOUS_FILTRATION, 1), AVDoorID(AVRegion.VENOUS_MAINTENANCE_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.VENOUS_MAINTENANCE_ACCESS, 1), AVDoorID(AVRegion.VENOUS_MAINTENANCE1, 0)),
    AVConnection(AVDoorID(AVRegion.VENOUS_MAINTENANCE1, 1), AVDoorID(AVRegion.VENOUS_MAINTENANCE2_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.VENOUS_MAINTENANCE2_CENTER, 0), AVDoorID(AVRegion.VENOUS_MAINTENANCE3, 0)),
    AVConnection(AVDoorID(AVRegion.VENOUS_MAINTENANCE2_LOWER, 0), AVDoorID(AVRegion.VENOUS_MAINTENANCE4, 1)),
    AVConnection(AVDoorID(AVRegion.VENOUS_MAINTENANCE4, 0), AVDoorID(AVRegion.VENOUS_MAINTENANCE_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.UPPER_TUBE_UPPER, 0), AVDoorID(AVRegion.ZI_SAVE2, 1)),
    AVConnection(AVDoorID(AVRegion.ZI_SAVE2, 0), AVDoorID(AVRegion.ZI_TO_INDI, 1)),
    AVConnection(AVDoorID(AVRegion.UPPER_TUBE_UPPER, 1), AVDoorID(AVRegion.URUKU_FOYER, 0)),
    AVConnection(AVDoorID(AVRegion.URUKU_FOYER, 1), AVDoorID(AVRegion.URUKU_MAIN, 0)),
    AVConnection(AVDoorID(AVRegion.FILTRATION_UPPER, 0), AVDoorID(AVRegion.URUKU_MAIN, 1)),
    AVConnection(AVDoorID(AVRegion.FILTRATION_WEST, 0), AVDoorID(AVRegion.URUKU_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.FILTRATION_EAST, 0), AVDoorID(AVRegion.LABCOAT, 0)),
    AVConnection(AVDoorID(AVRegion.ZI_TO_KUR, 1), AVDoorID(AVRegion.KUR_SHAFT_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_LOWER, 1), AVDoorID(AVRegion.KUR_SAVE1, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_LOWER, 3), AVDoorID(AVRegion.TO_ADDRESS_DISRUPTOR, 0)),
    AVConnection(AVDoorID(AVRegion.TO_ADDRESS_DISRUPTOR, 1), AVDoorID(AVRegion.ADDRESS_DISRUPTOR2_MAIN, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_LOWER, 2), AVDoorID(AVRegion.ADDRESS_DISRUPTOR2_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_LOWER, 4), AVDoorID(AVRegion.SURFACE_SHAFT, 0)),
    AVConnection(AVDoorID(AVRegion.SURFACE_SHAFT, 1), AVDoorID(AVRegion.CAVERN_ACCESS_MAIN, 0)),
    AVConnection(AVDoorID(AVRegion.CAVERN_ACCESS_MAIN, 1), AVDoorID(AVRegion.HIGH_JUMP_ACCESS_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.HIGH_JUMP_ACCESS_LOWER, 0), AVDoorID(AVRegion.HIGH_JUMP_ROOM_MAIN, 0)),
    AVConnection(AVDoorID(AVRegion.CAVERN_ACCESS_SECRET, 0), AVDoorID(AVRegion.STALAGMITE_MAZE, 0)),
    AVConnection(AVDoorID(AVRegion.STALAGMITE_MAZE, 1), AVDoorID(AVRegion.TETHERED_CHARGE, 0)),
    AVConnection(AVDoorID(AVRegion.TETHERED_CHARGE, 1), AVDoorID(AVRegion.SECRET_PASSAGE_TO_TETHERED_CHARGE, 0)),
    AVConnection(AVDoorID(AVRegion.HIGH_JUMP_ROOM_SECRET, 0), AVDoorID(AVRegion.SECRET_PASSAGE_TO_TETHERED_CHARGE, 1))
]

region_name_to_connection: Dict[str, List[AVConnection]] = {}
for connection in axiom_verge_connections:
    region_name_to_connection.setdefault(connection.enter.region.title, []).append(connection)
    if connection.twoway:
        region_name_to_connection.setdefault(connection.exit.region.title, []).append(
            AVConnection(connection.exit, connection.enter)
        )


def create_connections(avconnection_list: List[AVConnection], world: "AVWorld"):
    for avconnection in avconnection_list:
        source_avregion = avconnection.enter.region
        target_avregion = avconnection.exit.region
        source_region = world.get_region(source_avregion.title)
        target_region = world.get_region(target_avregion.title)
        assert avconnection.enter.index < len(
            source_avregion.doors), f"door index {avconnection.enter.index} is out of bounds for {source_avregion.title}"
        assert avconnection.exit.index < len(
            avconnection.exit.region.doors), f"door index {avconnection.exit.index} is out of bounds for {target_avregion.title}"
        entrance = Entrance(world.player, source_avregion.doors[avconnection.enter.index].name, source_region)
        source_region.exits.append(entrance)
        entrance.connect(target_region)
        print(f"creating connection from {avconnection.enter.region.title} to {target_avregion.title}")
        if avconnection.twoway:
            entrance = Entrance(world.player, target_avregion.doors[avconnection.exit.index].name, target_region)
            target_region.exits.append(entrance)
            entrance.connect(source_region)
            print(
                f"creating back connection from {avconnection.exit.region.title} to {avconnection.enter.region.title}")


def create_region(world: "AVWorld") -> None:
    created_regions = {}
    for avregion in AVRegion:
        region = Region(avregion.title, world.player, world.multiworld)
        created_regions[region.name] = region
        region.add_locations({location.name: location.code for location in axiom_verge_locations.get(region.name, {})})
        world.multiworld.regions.append(region)
    create_connections(axiom_verge_connections, world)
    if not world.options.room_rando:
        create_connections(axiom_verge_doors, world)
