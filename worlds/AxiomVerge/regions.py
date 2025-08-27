from BaseClasses import Region, Location, CollectionState, Entrance
from typing import TYPE_CHECKING, NamedTuple, List, Callable, Dict
from .locations import axiom_verge_locations, av_locations_unpacked
from . import logicfunction
from .logicfunction import LogicInfo
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
    logic: Callable[[LogicInfo], Callable[[CollectionState], bool]] = lambda logic_info: Entrance.access_rule

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
    SLUG = "Slug", [
        AVDoor("Slug in Eribu", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state))),
        AVDoor("Slug in Indi", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state))),
        AVDoor("Slug in Lower Ukkin-Na", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state))),
        AVDoor("Slug in Upper Ukkin-Na", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state))
    )]

    # eribusave1: 2 regions
    ERIBU_SAVE1_WEST = "Eribu Save 1_West", [
        AVDoor("Eribu Save 1 Left Door", Orientation.Left),
        AVDoor("Eribu Save 1 Inner WE", logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state) or logicfunction.anycoat(logic_info)(state))),
        AVDoor("Eribu Save 1 Save", Orientation.Save)
    ]
    ERIBU_SAVE1_EAST = "Eribu Save 1_East", [
        AVDoor("Eribu Save 1 Right Door", Orientation.Right),
        AVDoor("Eribu Save 1 Inner EW", logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state) or logicfunction.anycoat(logic_info)(state))
    )]

    ERIBU_SAVE2 = "Eribu Save 2", [
        AVDoor("Eribu Save 2 Right Door", Orientation.Right),
        AVDoor("Eribu Save 2 Save", Orientation.Save)
    ]

    # disruptorroom: 2 regions
    DISRUPTOR_ROOM_EAST = "Disruptor Room_East", [
        AVDoor("Disruptor Room Right Door", Orientation.Right),
        AVDoor("Disruptor Room Inner EW", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) and logicfunction.longwarp(logic_info)(state) or logicfunction.drill(logic_info)(state) and logicfunction.grapple(logic_info)(state) or logicfunction.shortdrone(logic_info)(state))
    )]
    DISRUPTOR_ROOM_WEST = "Disruptor Room_West", [
        AVDoor("Disruptor Room Left Door", Orientation.Left),
        AVDoor("Disruptor Room Up Door", Orientation.Up),
        AVDoor("Disruptor Room Inner WE", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]

    BUBBLE_WALL = "Bubble Wall", [
        AVDoor("Bubble Wall Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state))),
        AVDoor("Bubble Wall Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state))
    )]

    # brinstarshaft: 3 regions
    BRINSTAR_SHAFT_LOWER = "Brinstar Shaft_Lower", [
        AVDoor("Brinstar Shaft Lower Left Door", Orientation.Left),
        AVDoor("Brinstar Shaft Lower Right Door", Orientation.Right),
        AVDoor("Brinstar Shaft Center Right Door", Orientation.Right),
        AVDoor("Brinstar Shaft Upper Right Door", Orientation.Right),
        AVDoor("Brinstar Shaft Inner BC", logic=lambda logic_info: (lambda state: logicfunction.cornercut(logic_info)(state) or logicfunction.tempup(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state) or logicfunction.drone(logic_info)(state))
    )]
    BRINSTAR_SHAFT_CENTER = "Brinstar Shaft_Center", [
        AVDoor("Brinstar Shaft Center Left Door", Orientation.Left),
        AVDoor("Brinstar Shaft Inner CB"),
        AVDoor("Brinstar Shaft Inner CU", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]
    BRINSTAR_SHAFT_UPPER = "Brinstar Shaft_Upper", [
        AVDoor("Brinstar Shaft Upper Left Door", Orientation.Left),
        AVDoor("Brinstar Shaft Inner UC", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]

    NOVA_GATE = "Nova Gate", [
        AVDoor("Nova Gate Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.cornercut(logic_info)(state) or logicfunction.anycoat(logic_info)(state))),
        AVDoor("Nova Gate Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state) or logicfunction.drone(logic_info)(state) or logicfunction.justdrill(logic_info)(state))
    )]

    # spitbughall: 2 regions
    SPITBUG_HALL_WEST = "Spitbug Hall_West", [
        AVDoor("Spitbug Hall Left Door", Orientation.Left),
        AVDoor("Spitbug Hall Left Up Door", Orientation.Up),
        AVDoor("Spitbug Hall Inner WE", logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state) or logicfunction.drone(logic_info)(state) or logicfunction.justdrill(logic_info)(state) or logicfunction.anycoat(logic_info)(state))
    )]
    SPITBUG_HALL_EAST = "Spitbug Hall_East", [
        AVDoor("Spitbug Hall Right Up Door", Orientation.Up),
        AVDoor("Spitbug Hall Inner EW", logic=lambda logic_info: (lambda state: logicfunction.cornercut(logic_info)(state) or logicfunction.anycoat(logic_info)(state))
    )]

    WRONG_TOWER = "Wrong Tower", [
        AVDoor("Wrong Tower Up Door", Orientation.Up),
        AVDoor("Wrong Tower Down Door", Orientation.Down)
    ]

    FALSE_REFLECTOR_ACCESS = "False Reflector Access", [
        AVDoor("False Reflector Access Down Door", Orientation.Down, logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state))),
        AVDoor("False Reflector Access Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state) and logicfunction.anyupnoceiling(logic_info)(state))
    )]

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
        AVDoor("Multi Disruptor Inner BU", logic=lambda logic_info: (lambda state: logicfunction.grapple(logic_info)(state) or logicfunction.dronefly(logic_info)(state))
    )]
    MULTI_DISRUPTOR_UPPER = "Multi Disruptor_Upper", [
        AVDoor("Multi Disruptor Left Door", Orientation.Left),
        AVDoor("Multi Disruptor Up Door", Orientation.Up),
        AVDoor("Multi Disruptor Inner UB")
    ]

    #left door wonky in door rando
    CRYPTOGRAPHY = "Cryptography", [
        AVDoor("Cryptography Down Door", Orientation.Down),
        AVDoor("Cryptography Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.passcodetool(logic_info)(state))
    )]

    THRILLER = "Thriller", [
        AVDoor("Thriller Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Thriller Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))
    )]

    FORBIDDEN_SHAFT = "Forbidden Shaft", [
        AVDoor("Forbidden Shaft Up Door", Orientation.Right),
        AVDoor("Forbidden Shaft Down Door", Orientation.Right)
    ]

    # forbiddencorridor: 2 regions
    FORBIDDEN_CORRIDOR_WEST = "Forbidden Corridor_West", [
        AVDoor("Forbidden Corridor Left Door", Orientation.Left),
        AVDoor("Forbidden Corridor Inner WE", logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state))
    )]
    FORBIDDEN_CORRIDOR_EAST = "Forbidden Corridor_East", [
        AVDoor("Forbidden Corridor Right Door", Orientation.Right),
        AVDoor("Forbidden Corridor Inner EW", logic=lambda logic_info: (lambda state: logicfunction.fatbeam(logic_info)(state))
    )]

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
        AVDoor("Xedur Left Door", Orientation.Left, BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state))),
        AVDoor("Xedur Right Door", Orientation.Right, BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state))
    )]

    # drillroom: 2 regions
    DRILL_ROOM_UPPER = "Drill Room_Upper", [
        AVDoor("Drill Room Up Door", Orientation.Left, BossDoor.Outer, logic=lambda logic_info: (lambda state: logicfunction.shortdrone(logic_info)(state) or logicfunction.longwarp(logic_info)(state) or (logicfunction.fielddisruptor(logic_info)(state) and logicfunction.grapple(logic_info)(state)))),
        AVDoor("Drill Room Inner UB", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]
    DRILL_ROOM_LOWER = "Drill Room_Lower", [
        AVDoor("Drill Room Down Door", Orientation.Left),
        AVDoor("Drill Room Inner BU", logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.longdrone(logic_info)(state)))
    )]

    # drillsecret: 2 regions
    XEDUR_BASEMENT_EAST = "Xedur Basement_East", [
        AVDoor("Xedur Basement Right Door", Orientation.Right),
        AVDoor("Xedur Basement Inner EW", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) and (logicfunction.cornercut(logic_info)(state) or (logicfunction.anyweapon(logic_info)(state) and logicfunction.tempup(logic_info)(state)) or logicfunction.longpierce(logic_info)(state) or logicfunction.anycoat(logic_info)(state)))
    )]
    XEDUR_BASEMENT_WEST = "Xedur Basement_West", [
        AVDoor("Xedur Basement Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))),
        AVDoor("Xedur Basement Inner WE", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) and logicfunction.fatbeam(logic_info)(state))
    )]

    DIGGY_HOLE = "Diggy Hole", [
        AVDoor("Diggy Hole Up Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))),
        AVDoor("Diggy Hole Down Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]

    # thedrop: 2 regions
    THE_DROP_MAIN = "The Drop_Main", [
        AVDoor("The Drop Upper Left Door", Orientation.Left),
        AVDoor("The Drop Upper Right Door", Orientation.Right),
        AVDoor("The Drop Lower Right Door", Orientation.Right),
        AVDoor("The Drop Down Door", Orientation.Down),
        AVDoor("The Drop Inner MS", logic=lambda logic_info: (lambda state: (logicfunction.dronequest(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)) and logicfunction.glitchnades(logic_info)(state))
    )]
    THE_DROP_SECRET = "The Drop_Secret", [
        AVDoor("The Drop Lower Left Door", Orientation.Left),
        AVDoor("The Drop Inner SM", logic=lambda logic_info: (lambda state: (logicfunction.dronequest(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)) and logicfunction.glitchnades(logic_info)(state))
    )]

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
        AVDoor("Secret Chamber Inner BU", logic=lambda logic_info: (lambda state: (logicfunction.anyglitch(logic_info)(state) and (logicfunction.breakblock(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))) or logicfunction.grapple(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.longwarp(logic_info)(state))
    )]
    # up door is weird
    SECRET_CHAMBER_UPPER = "Secret Chamber_Upper", [
        AVDoor("Secret Chamber Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.passcodetool(logic_info)(state) and logicfunction.anyup(logic_info)(state))),
        AVDoor("Secret Chamber Inner UB")
    ]

    DISCHARGE_CHAMBER = "Discharge Chamber", [
        AVDoor("Discharge Chamber Down Door", Orientation.Down)
    ]

    ERIBU_TO_UKKINNA = "Eribu to Ukkin-Na", [
        AVDoor("Eribu to Ukkin-Na Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) or logicfunction.redcoat(logic_info)(state))),
        AVDoor("Eribu to Ukkin-Na Right Door", Orientation.Right, BossDoor.Areatrans, logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) or logicfunction.redcoat(logic_info)(state))
    )]

    # eributoindi: 2 regions
    ERIBU_TO_INDI_WEST = "Eribu to Indi_West", [
        AVDoor("Eribu to Indi Left Door", Orientation.Left),
        AVDoor("Eribu to Indi Inner WE", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.grapple(logic_info)(state))
    )]
    ERIBU_TO_INDI_EAST = "Eribu to Indi_East", [
        AVDoor("Eribu to Indi Right Door", Orientation.Right, BossDoor.Areatrans),
        AVDoor("Eribu to Indi Inner EW", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))
    )]

    PRIMORDIAL_ACCESS = "Primordial Access", [
        AVDoor("Primordial Access Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.glitch2(logic_info)(state) or logicfunction.redcoat(logic_info)(state))),
        AVDoor("Primordial Access Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.glitch2(logic_info)(state) or logicfunction.redcoat(logic_info)(state))
    )]

    # primordialcavern: 3 regions
    PRIMORDIAL_CAVERN_EAST = "Primordial Cavern_East", [
        AVDoor("Primordial Cavern Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Primordial Cavern Inner EW", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state))),
        AVDoor("Primordial Cavern Inner EC", logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state) or logicfunction.drone(logic_info)(state) and logicfunction.grapple(logic_info)(state) or logicfunction.shortdrone(logic_info)(state))
    )]
    PRIMORDIAL_CAVERN_CENTER = "Primordial Cavern_Center", [
        AVDoor("Primordial Cavern Inner CW", logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state))),
        AVDoor("Primordial Cavern Inner CE", logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state))
    )]
    PRIMORDIAL_CAVERN_WEST = "Primordial Cavern_West", [
        AVDoor("Primordial Cavern Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state) and logicfunction.grapple(logic_info)(state) or logicfunction.longwarp(logic_info)(state) or logicfunction.grapple(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state))),
        AVDoor("Primordial Cavern Inner WE", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state))),
        AVDoor("Primordial Cavern Inner WC", logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state))
    )]

    # flamethrower access: 2 regions
    FLAMETHROWER_ACCESS_WEST = "Flamethrower Access_West", [
        AVDoor("Flamethrower Access Down Door", Orientation.Down),
        AVDoor("Flamethrower Access Inner WE", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.grapple(logic_info)(state) or logicfunction.grapple(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state) or logicfunction.longdrone(logic_info)(state) or logicfunction.redcoat(logic_info)(state) and logicfunction.grapple(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state))
    )]
    FLAMETHROWER_ACCESS_EAST = "Flamethrower Access_East", [
        AVDoor("Flamethrower Access Up Door", Orientation.Up),
        AVDoor("Flamethrower Access Inner EW", logic=lambda logic_info: (lambda state: logicfunction.longdrone(logic_info)(state) or logicfunction.grapple(logic_info)(state))),
        AVDoor("Flamethrower Access - Slug in Room")
    ]

    FLAMETHROWER_ROOM = "Flamethrower Room", [AVDoor("Flamethrower Room Down Door", Orientation.Down)]

    BUBBLE_MAZE = "Bubble Maze", [
        AVDoor("Bubble Maze Down Door", Orientation.Down, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state))),
        AVDoor("Bubble Maze Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state))
    )]

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
        AVDoor("Absu Shaft Inner UC", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state))
    )]
    ABSU_SHAFT_CENTER = "Absu Shaft_Center", [
        AVDoor("Absu Shaft Lower Center Left Door", Orientation.Left),
        AVDoor("Absu Shaft Inner CU", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state))),
        AVDoor("Absu Shaft Inner CB", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))
    )]
    ABSU_SHAFT_LOWER = "Absu Shaft_Lower", [
        AVDoor("Absu Shaft Lower Left Door", Orientation.Left),
        AVDoor("Absu Shaft Inner BC", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))
    )]

    DONUT_VAULT = "Donut Vault", [AVDoor("Donut Vault Right Door", Orientation.Right)]

    UPPER_SHAFT_BASEMENT = "Upper Shaft Basement", [AVDoor("Upper Shaft Basement Right Door", Orientation.Right)]

    LOWER_SHAFT_BASEMENT = "Lower Shaft Basement", [AVDoor("Lower Shaft Basement Right Door", Orientation.Right)]

    # ventilation: 3 regions
    VENTILATION_WEST = "Ventilation_West", [
        AVDoor("Ventilation Left Door", Orientation.Left),
        AVDoor("Ventilation Inner WC", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))
    )]
    VENTILATION_CENTER = "Ventilation_Center", [
        AVDoor("Ventilation Up Door", Orientation.Up),
        AVDoor("Ventilation Inner CW", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Ventilation Inner CE", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]
    VENTILATION_EAST = "Ventilation_East", [
        AVDoor("Ventilation Right Door", Orientation.Up),
        AVDoor("Ventilation Inner EC", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]

    ATTIC_ACCESS = "Attic Access", [
        AVDoor("Attic Access Down Door", Orientation.Down),
        AVDoor("Attic Access Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))
    )]

    # attic: 5 regions
    ATTIC_WEST = "Attic_West", [
        AVDoor("Attic Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Attic Inner WCW", logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state))
    )]
    ATTIC_CENTER_WEST = "Attic_Center West", [
        AVDoor("Attic Inner CWW", logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state))),
        AVDoor("Attic Inner CWCE", logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state))
    )]
    ATTIC_CENTER_EAST = "Attic_Center East", [
        AVDoor("Attic Inner CECW", logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state))),
        AVDoor("Attic Inner CELE")
    ]
    ATTIC_LOWER_EAST = "Attic_Lower East", [
        AVDoor("Attic Down Door", Orientation.Down),
        AVDoor("Attic Inner LECE", logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))),
        AVDoor("Attic Inner LEUE", logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))
    )]
    ATTIC_UPPER_EAST = "Attic_Upper East", [
        AVDoor("Attic Inner UELE")
    ]

    # pinkdiatoms2: 2 regions
    PINK_DIATOMS2_WEST = "Pink Diatoms 2_West", [
        AVDoor("Pink Diatoms 2 Left Door", Orientation.Left),
        AVDoor("Pink Diatoms 2 Down Door", Orientation.Down),
        AVDoor("Pink Diatoms 2 Inner WE", logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state))
    )]
    PINK_DIATOMS2_EAST = "Pink Diatoms 2_East", [
        AVDoor("Pink Diatoms 2 Up Door", Orientation.Up),
        AVDoor("Pink Diatoms 2 Inner EW", logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state))
    )]

    OVERGROWN_PRISON = "Overgrown Prison", [
        AVDoor("Overgrown Prison Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))),
        AVDoor("Overgrown Prison Upper Left Door", Orientation.Left),
        AVDoor("Overgrown Prison Lower Left Door", Orientation.Left),
        AVDoor("Overgrown Prison Right Door", Orientation.Right)
    ]

    ABSU_SAVE2 = "Absu Save 2", [
        AVDoor("Absu Save 2 Left Door", Orientation.Left),
        AVDoor("Absu Save 2 Save", Orientation.Save)
    ]

    DINING_HALL = "Dining Hall", [
        AVDoor("Dining Hall Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.anycoat(logic_info)(state))),
        AVDoor("Dining Hall Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.anycoat(logic_info)(state))
    )]

    PINK_DIATOMS_ACCESS = "Pink Diatoms Access", [
        AVDoor("Pink Diatoms Access Left Door", Orientation.Left),
        AVDoor("Pink Diatoms Access Right Door", Orientation.Right)
    ]

    # pinkdiatoms1: 3 regions
    PINK_DIATOMS1_UPPER = "Pink Diatoms 1_Upper", [
        AVDoor("Pink Diatoms 1 Upper Right Door", Orientation.Right),
        AVDoor("Pink Diatoms 1 Inner UC", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]
    PINK_DIATOMS1_CENTER = "Pink Diatoms 1_Center", [
        AVDoor("Pink Diatoms 1 Left Door", Orientation.Left),
        AVDoor("Pink Diatoms 1 Center Right Door", Orientation.Right),
        AVDoor("Pink Diatoms 1 Inner CU", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))),
        AVDoor("Pink Diatoms 1 Inner CB", logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) and logicfunction.anycoat(logic_info)(state))
    )]
    PINK_DIATOMS1_LOWER = "Pink Diatoms 1_Lower", [
        AVDoor("Pink Diatoms 1 Lower Right Door", Orientation.Right),
        AVDoor("Pink Diatoms 1 Inner BC", logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) and logicfunction.anycoat(logic_info)(state) and logicfunction.anyupnoceiling(logic_info)(state))
    )]

    PRISON_CELLAR = "Prison Cellar", [
        AVDoor("Prison Cellar Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state))),
        AVDoor("Prison Cellar Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state))
    )]

    PRISON_CELLAR_SECRET = "Prison Cellar Secret", [AVDoor("Prison Cellar Down Door", Orientation.Down)]

    ELSENOVA = "Elsenova", [
        AVDoor("Elsenova Right Door", Orientation.Right),
        AVDoor("Elsenova Left Door", Orientation.Left)
    ]

    # prison1: 2 regions
    PRISON1_UPPER = "Prison Tower_Upper", [
        AVDoor("Prison Tower Upper Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.shortpierce(logic_info)(state) or logicfunction.anycoat(logic_info)(state))),
        AVDoor("Prison Tower Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.shortpierce(logic_info)(state) or logicfunction.anycoat(logic_info)(state))),
        AVDoor("Prison Tower Inner UB", logic=lambda logic_info: (lambda state: logicfunction.shortpierce(logic_info)(state) or logicfunction.anycoat(logic_info)(state))
    )]

    PRISON1_LOWER = "Prison Tower_Lower", [
        AVDoor("Prison Tower Lower Right Door"),
        AVDoor("Prison Tower Inner BU", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state) or logicfunction.anycoat(logic_info)(state))
    )]

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
        AVDoor("Telal Left Door", Orientation.Left, BossDoor.Inner, logic=lambda logic_info: (lambda state: (logicfunction.anycoat(logic_info)(state) and logicfunction.anyweapon(logic_info)(state)) or logicfunction.fatbeam(logic_info)(state))),
        AVDoor("Telal Down Door", Orientation.Down, BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.longweapon(logic_info)(state))
    )]

    # telaltreasury: 4 regions
    TELAL_TREASURY_UPPER = "Telal Treasury_Upper", [
        AVDoor("Telal Treasury Up Door", Orientation.Up, BossDoor.Outer),
        AVDoor("Telal Treasury Inner UW"),
        AVDoor("Telal Treasury Inner UE", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.anycoat(logic_info)(state) and logicfunction.scissorbeam(logic_info)(state) or logicfunction.fatbeam(logic_info)(state))
    )]
    TELAL_TREASURY_EAST = "Telal Treasury_East", [
        AVDoor("Telal Treasury Right Door", Orientation.Right),
        AVDoor("Telal Treasury Inner EU", logic=lambda logic_info: (lambda state: (logicfunction.anyglitch(logic_info)(state) and logicfunction.anyupnoceiling(logic_info)(state) and logicfunction.breakblock(logic_info)(state)) or logicfunction.redcoat(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and (logicfunction.grapple(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state) or logicfunction.shortdrone(logic_info)(state))))),
        AVDoor("Telal Treasury Inner ES")
    ]
    TELAL_TREASURY_WEST = "Telal Treasury_West", [
        AVDoor("Telal Treasury Inner WU", logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state))),
        AVDoor("Telal Treasury Inner WS", logic=lambda logic_info: (lambda state: logicfunction.anyglitch(logic_info)(state) or logicfunction.tempup(logic_info)(state))
    )]
    TELAL_TREASURY_SOUTH = "Telal Treasury_South", [
        AVDoor("Telal Treasury Inner SW"),
        AVDoor("Telal Treasury Inner SE", logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or logicfunction.anyglitch(logic_info)(state))
    )]

    TELAL_SECRET_ACCESS1 = "Telal Secret Access 1", [
        AVDoor("Telal Secret Access 1 Left Door", Orientation.Left),
        AVDoor("Telal Secret Access 1 Down Door", Orientation.Down),
        AVDoor("Telal Secret Access 1 Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.sevenblockup(logic_info)(state))
    )]

    TELAL_SECRET_ACCESS2 = "Telal Secret Access 2", [
        AVDoor("Telal Secret Access 2 Down Door", Orientation.Down),
        AVDoor("Telal Secret Access 2 Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.sevenblockup(logic_info)(state))
    )]

    TELAL_SECRET_ACCESS3 = "Telal Secret Access 3", [
        AVDoor("Telal Secret Access 3 Down Door", Orientation.Down),
        AVDoor("Telal Secret Access 3 Left Door", Orientation.Left)
    ]

    ABSU_TO_INDI_UPPER = "Absu to Indi_Upper", [
        AVDoor("Absu to Indi Up Door", Orientation.Up, BossDoor.Areatrans, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Absu to Indi Upper Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Abso to Indi Inner UB", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]

    ABSU_TO_INDI_LOWER = "Absu to Indi_Lower", [
        AVDoor("Absu to Indi Lower Right Door", Orientation.Right),
        AVDoor("Absu to Indi Inner BU", logic=lambda logic_info: (lambda state: logicfunction.sevenblockup(logic_info)(state) and logicfunction.anycoat(logic_info)(state))
    )]

    TELAL_SECRET_ACCESS4 = "Telal Secret Access 4", [AVDoor("Telal Secret Access 4 Left Door", Orientation.Left)]

    TELAL_EXIT = "Telal Exit", [
        AVDoor("Telal Exit Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Telal Exit Down Door", Orientation.Down)
    ]

    # ducts1: 3 regions
    DUCTS1_WEST = "Ducts 1_West", [
        AVDoor("Ducts 1 Up Door", Orientation.Up),
        AVDoor("Ducts 1 Inner WE", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Ducts 1 Inner WS", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]
    DUCTS1_EAST = "Ducts 1_East", [
        AVDoor("Ducts 1 Right Door", Orientation.Right),
        AVDoor("Ducts 1 Inner EW", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))
    )]
    DUCTS1_SECRET = "Ducts 1_Secret", [
        AVDoor("Ducts 1 Down Door", Orientation.Down),
        AVDoor("Ducts 1 Inner SW", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]

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
        AVDoor("Ducts 2 Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Ducts 2 Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))
    )]

    # purplediatoms1: 3 regions
    PURPLE_DIATOMS1_UPPER = "Purple Diatoms 1_Upper", [
        AVDoor("Purple Diatoms 1 Up Door", Orientation.Up),
        AVDoor("Purple Diatoms 1 Right Door", Orientation.Right),
        AVDoor("Purple Diatoms 1 Upper Left Door", Orientation.Left),
        AVDoor('Purple Diatoms 1 Inner UW'),
        AVDoor("Purple Diatoms 1 Inner UE", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]
    PURPLEDIATOMS1_WEST = "Purple Diatoms 1_West", [
        AVDoor("Purple Diatoms 1 Lower Left Door", Orientation.Left),
        AVDoor("Purple Diatoms 1 Inner WU", logic=lambda logic_info: (lambda state: logicfunction.anyglitch(logic_info)(state) or logicfunction.sevenblockup(logic_info)(state))),
        AVDoor("Purple Diatoms 1 Inner WE", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]
    PURPLEDIATOMS1_EAST = "Purple Diatoms 1_East", [
        AVDoor("Purple Diatoms 1 Down Door", Orientation.Down),
        AVDoor("Purple Diatoms 1 Inner EW", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))),
        AVDoor("Purple Diatoms 1 Inner EU", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))
    )]

    ABSU_SAVE4 = "Absu Save 4", [
        AVDoor("Absu Save 4 Right Door", Orientation.Right),
        AVDoor("Absu Save 4 Save", Orientation.Save)
    ]

    PURPLEDIATOMS1_HIDDENACCESS1 = "Purple Diatoms 1 Hidden Access 1", [
        AVDoor("Purple Diatoms 1 Hidden Access 1 Up Door", Orientation.Up),
        AVDoor("Purple Diatoms 1 Hidden Access 1 Right Door", Orientation.Right)
    ]

    PURPLEDIATOMS1_HIDDENACCESS2 = "Purple Diatoms 1 Hidden Access 2", [
        AVDoor("Purple Diatoms 1 Hidden Access 2 Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.anycoat(logic_info)(state))),
        AVDoor("Purple Diatoms 1 Hidden Access 2 Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and (logicfunction.redcoat(logic_info)(state) or logicfunction.grapple(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state) or logicfunction.shortdrone(logic_info)(state)))
    )]

    LAVATUNNEL = "Lava Tunnel", [
        AVDoor("Lava Tunnel Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state))),
        AVDoor("Lava Tunnel Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state))
    )]

    LAVASECRET = "Lava Secret", [AVDoor("Lava Secret Left Door", Orientation.Left)]

    # greenfungus1: 2 regions
    GREEN_FUNGUS1_UPPER = "Green Fungus 1_Upper", [
        AVDoor("Green Fungus 1 Left Door", Orientation.Left),
        AVDoor("Green Fungus 1 Right Door", Orientation.Right),
        AVDoor("Green Fungus 1 Inner UB", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.dronequest(logic_info)(state))
    )]
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
        AVDoor("Steam Room 2 Inner EW", logic=lambda logic_info: (lambda state: logicfunction.grapple(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state))),
        AVDoor("Steam Room 2 Inner EU", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))
    )]
    STEAM_ROOM2_UPPER = "Steam Room 2_Upper", [
        AVDoor("Steam Room 2 Upper Left Door", Orientation.Left),
        AVDoor("Steam Room 2 Inner UE")
    ]

    HIDDEN_MUTANTS = "Hidden Mutants", [
        AVDoor('Hidden Mutants Lower Right Door', Orientation.Right),
        AVDoor("Hidden Mutants Upper Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))
    )]

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
        AVDoor("Central Tube Inner BS", logic=lambda logic_info: (lambda state: (logicfunction.anyup(logic_info)(state) and logicfunction.glitch2(logic_info)(state)) or logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Central Tube Inner BU", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))
    )]
    CENTRAL_TUBE_UPPER = "Central Tube_Upper", [
        AVDoor("Central Tube Up Door", Orientation.Up),
        AVDoor("Central Tube Inner UB")
    ]
    CENTRAL_TUBE_SECRET = "Central Tube_Secret", [
        AVDoor("Central Tube Upper Left Door", Orientation.Left),
        AVDoor("Central Tube Inner SB", logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) or logicfunction.anycoat(logic_info)(state))
    )]

    EYE_STALK_TUNNEL = "Eye Stalk Tunnel", [
        AVDoor("Eye Stalk Tunnel Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.anyweapon(logic_info)(state))),
        AVDoor("Eye Stalk Tunnel Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.anyweapon(logic_info)(state))
    )]

    EYE_STALK_SECRET1 = "Eye Stalk Secret 1", [
        AVDoor("Eye Stalk Secret 1 Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.anyweapon(logic_info)(state))),
        AVDoor("Eye Stalk Secret 1 Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.anyweapon(logic_info)(state))
    )]

    EYE_STALK_SECRET2 = "Eye Stalk Secret 2", [AVDoor("Eye Stalk Secret 2 Right Door", Orientation.Right)]

    ARTERIAL_ACCESS = "Arterial Access", [
        AVDoor("Arterial Access Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Arterial Access Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))
    )]

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
        AVDoor("Veruska Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.shortdrone(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Veruska Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))
    )]

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
        AVDoor("Arterial Main Upper Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))),
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
        AVDoor("Arterial Filtration Inner MS", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) and logicfunction.grapple(logic_info)(state))
    )]

    ARTERIAL_FILTRATION_UPPER = "Arterial Filtration_Upper", [
        AVDoor("Arterial Filtration Up Door", Orientation.Up),
        AVDoor("Arterial Filtration Inner SM", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state))
    )]

    ARTERIAL_BYPASS_ENTRANCE = "Arterial Bypass Entrance", [
        AVDoor("Arterial Bypass Entrance Right Door", Orientation.Right),
        AVDoor("Arterial Bypass Entrance Left Door", Orientation.Left),
    ]

    # uppertube: 4 regions
    UPPER_TUBE_LOWER = "Upper Tube_Lower", [
        AVDoor("Upper Tube Down Door", Orientation.Down),
        AVDoor("Upper Tube Inner BC", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))
    )]

    UPPER_TUBE_CENTER = "Upper Tube_Center", [
        AVDoor("Upper Tube Lower Right Door", Orientation.Right),
        AVDoor("Upper Tube Inner CB"),
        AVDoor("Upper Tube Inner CS", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state))),
        AVDoor("Upper Tube Inner CU", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))
    )]

    UPPER_TUBE_SECRET = "Upper Tube_Secret", [
        AVDoor("Upper Tube Lower Left Door", Orientation.Left),
        AVDoor("Upper Tube Inner SC", logic=lambda logic_info: (lambda state: logicfunction.shortdrone(logic_info)(state))
    )]

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
        AVDoor("Venous Filtration Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))),
        AVDoor("Venous Filtration Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]

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
        AVDoor("Venous Maintenance 2 Inner CU", logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state)))),
        AVDoor("Venous Maintenance 2 Inner CB")
    ]

    VENOUS_MAINTENANCE2_LOWER = "Venous Maintenance 2_Lower", [
        AVDoor("Venous Maintenance 2 Lower Right Door", Orientation.Right),
        AVDoor("Venous Maintenance 2 Inner BC", logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.redcoat(logic_info)(state)))),
        AVDoor("Venous Maintenance 2 Inner BU", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]

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
        AVDoor("Zi to Indi Up Door", Orientation.Up, BossDoor.Areatrans, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.fielddisruptor(logic_info)(state) and (logicfunction.trenchcoat(logic_info)(state) or logicfunction.grapple(logic_info)(state))))),
        AVDoor("Zi to Indi Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))
    )]

    URUKU_FOYER = "Uruku Foyer", [
        AVDoor("Uruku Foyer Left Door", Orientation.Left),
        AVDoor("Uruki Foyer Right Door", Orientation.Right, BossDoor.Outer)
    ]

    # uruku: 3 regions
    URUKU_MAIN = "Uruku_Main", [
        AVDoor("Uruku Left Door", Orientation.Left, BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.rangeweapon(logic_info)(state))),
        AVDoor("Uruku Inner MU", logic=lambda logic_info: (lambda state: ((logicfunction.trenchcoat(logic_info)(state) or (logicfunction.fielddisruptor(logic_info)(state) and logicfunction.rangeweapon(logic_info)(state))) and logicfunction.anyglitch(logic_info)(state)) or logicfunction.longwarp(logic_info)(state) or (logicfunction.shortdrone(logic_info)(state) and logicfunction.rangeweapon(logic_info)(state)))),
        AVDoor("Uruku Inner MS", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.anycoat(logic_info)(state) and logicfunction.anyglitch(logic_info)(state))
    )]

    URUKU_UPPER = "Uruku_Upper", [
        AVDoor("Uruku Upper Right Door", Orientation.Right, BossDoor.Inner),
        AVDoor("Uruku Inner UM", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]

    URUKU_SECRET = "Uruku_Secret", [
        AVDoor("Uruku Lower Right Door", Orientation.Right, BossDoor.Inner),
        AVDoor("Uruku Inner SM", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]

    # filtration: 4 regions
    FILTRATION_UPPER = "Filtration_Upper", [
        AVDoor("Filtration Upper Left Door", Orientation.Left, BossDoor.Outer),
        AVDoor("Filtration Inner UC")
    ]

    FILTRATION_CENTER = "Filtration_Center", [
        AVDoor("Filtration Inner CE", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.breakblock(logic_info)(state))),
        AVDoor("Filtration Inner CW", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))),
        AVDoor("Filtration Inner CU", logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.longdrone(logic_info)(state) and (logicfunction.redcoat(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state)) or logicfunction.grapple(logic_info)(state))))
    )]

    FILTRATION_WEST = "Filtration_West", [
        AVDoor("Filtration Lower Left Door", Orientation.Left, BossDoor.Outer),
        AVDoor("Filtration Inner WC", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]

    FILTRATION_EAST = "Filtration_East", [
        AVDoor("Filtration Right Door", Orientation.Right),
        AVDoor("Filtration Inner EC", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.fatbeam(logic_info)(state))
    )]

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
        AVDoor("Kur Shaft Inner BC", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))),
        AVDoor("Kur Shaft Inner BT", logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state) and logicfunction.anycoat(logic_info)(state))
    )]

    KUR_SHAFT_CENTER = "Kur Shaft_Center", [
        AVDoor("Kur Shaft Center Left Door", Orientation.Left, BossDoor.Areatrans),
        AVDoor("Kur Shaft Inner CB", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))),
        AVDoor("Kur Shaft Inner CT", logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state) and logicfunction.anycoat(logic_info)(state))
    )]

    KUR_SHAFT_TRANSIT = "Kur Shaft_Transit", [
        AVDoor("Kur Shaft Inner TB", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))),
        AVDoor("Kur Shaft Inner TC", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))),
        AVDoor("Kur Shaft Inner TU", logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))
    )]

    KUR_SHAFT_UPPER = "Kur Shaft_Upper", [
        AVDoor("Kur Shaft Up Door", Orientation.Up),
        AVDoor("Kur Shaft Inner UT"),
        AVDoor("Kur Shaft Inner US", logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))
    )]

    KUR_SHAFT_SECRET = "Kur Shaft_Secret", [
        AVDoor("Kur Shaft Upper Left Door", Orientation.Left, BossDoor.Areatrans),
        AVDoor("Kur Shaft Inner SU", logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))
    )]

    KUR_SAVE1 = "Kur Save 1", [
        AVDoor("Kur Save 1 Left Door", Orientation.Left),
        AVDoor("Kur Save 1 Save", Orientation.Save)
    ]

    TO_ADDRESS_DISRUPTOR = "To Address Disruptor", [
        AVDoor("To Address Disruptor Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.breakblock(logic_info)(state))),
        AVDoor("To Address Disruptor Down Door", Orientation.Down, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) and (logicfunction.fatbeam(logic_info)(state) or logicfunction.drone(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)))
    )]

    #addressdisruptor2: 3 regions
    ADDRESS_DISRUPTOR2_MAIN = "Address Disruptor 2_Main", [
        AVDoor("Address Disruptor 2 Up Door", Orientation.Up),
        AVDoor("Address Disruptor 2 Inner MS", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) and (logicfunction.fatbeam(logic_info)(state) or logicfunction.drone(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)))
    )]

    ADDRESS_DISRUPTOR2_SECRET = "Address Disruptor 2_Secret", [
        AVDoor("Address Disruptor 2 Inner SW", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.glitch2(logic_info)(state) and logicfunction.breakblock(logic_info)(state)))),
        AVDoor("Address Disruptor 2 Inner SM", logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state) and logicfunction.anycoat(logic_info)(state) and (logicfunction.fatbeam(logic_info)(state) or logicfunction.drone(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)))
    )]

    ADDRESS_DISRUPTOR2_WEST = "Address Disruptor 2_West", [
        AVDoor("Address Disruptor 2 Left Door", Orientation.Left),
        AVDoor("Address Disruptor 2 Inner WS", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.glitch2(logic_info)(state) and logicfunction.breakblock(logic_info)(state)))

    )]

    SURFACE_SHAFT = "Surface Shaft", [
        AVDoor("Surface Shaft Left Door", Orientation.Left),
        AVDoor("Surface Shaft Right Door", Orientation.Right)
    ]

    #cavernaccess: 2 regions
    CAVERN_ACCESS_MAIN = "Cavern Access_Main", [
        AVDoor("Cavern Access Left Door", Orientation.Left),
        AVDoor("Cavern Access Down Door", Orientation.Down),
        AVDoor("Cavern Access Inner MS", logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state) and logicfunction.breakblock(logic_info)(state) and logicfunction.anycoat(logic_info)(state))
    )]

    CAVERN_ACCESS_SECRET = "Cavern Access_Secret", [
        AVDoor("Cavern Access Right Door", Orientation.Right),
        AVDoor("Cavern Access Inner SM", logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state) and logicfunction.anycoat(logic_info)(state))
    )]
    
    #highjumpaccess: 2 regions
    HIGH_JUMP_ACCESS_UPPER = "High Jump Access_Upper", [
        AVDoor("High Jump Access Up Door", Orientation.Up),
        AVDoor("High Jump Access Inner UB")
    ]

    HIGH_JUMP_ACCESS_LOWER = "Hight Jump Access_Lower", [
        AVDoor("High Jump Access Right Door", Orientation.Right),
        AVDoor("High Jump Access Inner BU", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))
    )]

    HIGH_JUMP_ROOM_MAIN = "High Jump Room_Main", [
        AVDoor("High Jump Room Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("High Jump Room Inner MS", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))
    )]

    HIGH_JUMP_ROOM_SECRET = "High Jump Room_Secret", [
        AVDoor("High Jump Room Right Door", Orientation.Right),
        AVDoor("High Jumpt Room Inner SM", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))
    )]

    #this room blows
    STALAGMITE_MAZE = "Stalagmite Maze", [
        AVDoor("Stalagmite Maze Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or ((logicfunction.shortdrone(logic_info)(state) and logicfunction.verylongwarp(logic_info)(state)) or (logicfunction.longdrone(logic_info)(state) and logicfunction.longwarp(logic_info)(state))))),
        AVDoor("Stalagmite Maze Down Door", Orientation.Down, logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.anyglitch(logic_info)(state) and (logicfunction.drone(logic_info)(state) or logicfunction.redcoat(logic_info)(state))))
    )]

    TETHERED_CHARGE = "Tethered Charge", [
        AVDoor("Tethered Charge Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Tethered Charge Left Door", Orientation.Left)
    ]

    SECRET_PASSAGE_TO_TETHERED_CHARGE = "Secret Passage to Tethered Charge", [
        AVDoor("Secret Passage to Tethered Charge Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.fatbeam(logic_info)(state))),
        AVDoor("Secret Passage to Tethered Charge Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.breakblock(logic_info)(state))
    )]

    INDI_TO_ERIBU = "Indi to Eribu", [
        AVDoor("Indi to Eribu Left Door", Orientation.Left, BossDoor.Areatrans),
        AVDoor("Indi to Eribu Right Door", Orientation.Right)
    ]

    INDI_TO_ABSU = "Indi to Absu", [
        AVDoor("Indi to Absu Down Door", Orientation.Down, BossDoor.Areatrans),
        AVDoor("Indi to Absu Up Door", Orientation.Up)
    ]

    INDI_TO_UKKINNA = "Indi to Ukkin-Na", [
        AVDoor("Indi to Ukkin-Na Up Door", Orientation.Up, BossDoor.Areatrans, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Indi to Ukkin-Na Down Door", Orientation.Down, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]

    INDI_TO_ZI = "Indi to Zi", [
        AVDoor("Indi to Zi Down Door", Orientation.Down, BossDoor.Areatrans),
        AVDoor("Indi to Zi Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))
    )]

    INDI_TO_EDIN = "Indi to Edin", [
        AVDoor("Indi to Edin Up Door", Orientation.Up, BossDoor.Areatrans, logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))),
        AVDoor("Indi to Edin Down Door", Orientation.Down),
        AVDoor("Indi to Edin Right Door", Orientation.Right)
    ]

    INDI_SAVE = "Indi Save", [
        AVDoor("Indi Save Left Door", Orientation.Left),
        AVDoor("Indi Save Save", Orientation.Save)
    ]

    INDI_TO_KUR = "Indi to Kur", [
        AVDoor("Indi to Kur Right Door", Orientation.Right, BossDoor.Areatrans),
        AVDoor("Indi to Kur Left Door", Orientation.Left)
    ]

    #oracaroom: 5 regions
    ORACA_ROOM_EAST = "Oraca Room_East", [
        AVDoor("Oraca Room Right Door", Orientation.Right),
        AVDoor("Oraca Room Inner EU", logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))
    )]

    ORACA_ROOM_UPPER = "Oraca Room_Upper", [
        AVDoor("Oraca Room Right Up Door", Orientation.Up),
        AVDoor("Oraca Room Left Up Door", Orientation.Up),
        AVDoor("Oraca Room - Slug in Room"),
        AVDoor("Oraca Room Inner UE"),
        AVDoor("Oraca Room Inner ULE"),
        AVDoor("Oraca Room Inner ULW"),
        AVDoor("Oraca Room Inner UW", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))
    )]

    ORACA_ROOM_LOWEREAST = "Oraca Room_Lower_East", [
        AVDoor("Oraca Room Right Down Door", Orientation.Down),
        AVDoor("Oraca Room Inner LEU", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))
    )]

    ORACA_ROOM_LOWERWEST = "Oraca Room_Lower_West", [
        AVDoor("Oraca Room Left Down Door", Orientation.Down),
        AVDoor("Oraca Room Inner LWU", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))
    )]

    ORACA_ROOM_WEST = "Oraca Room_West", [
        AVDoor("Oraca Room Left Door", Orientation.Left),
        AVDoor("Oraca Room Inner WU", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))
    )]

    UKKINNA_TO_ERIBU = "Ukkin-Na to Eribu", [
        AVDoor("Ukkin-Na to Eribu Left Door", Orientation.Left, BossDoor.Areatrans, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Ukkin-Na to Eribu Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]

    INFECTION_SEQUENCE = "Infection Sequence", [
        AVDoor("Infection Beginning")
    ]

    #leftlegshaft: 7 regions
    LEFT_LEG_SHAFT_LOWER_LOWER = "Left Leg Shaft_Lower_Lower", [
        AVDoor("Left Leg Shaft Lower Left Door", Orientation.Left),
        AVDoor("Left Leg Shaft Lower Right Door", Orientation.Right),
        AVDoor("Left Leg Shaft Inner LlLu", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and (logicfunction.grapple(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state))) or (logicfunction.grapple(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state) and logicfunction.anyglitch(logic_info)(state)))
    )]

    LEFT_LEG_SHAFT_LOWER_UPPER = "Left Leg Shaft_Lower_Upper", [
        AVDoor("Left Leg Shaft Inner LuLl"),
        AVDoor("Left Leg Shaft Inner LuT", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))
    )]

    LEFT_LEG_SHAFT_TRANSIT = "Left Leg Shaft_Transit", [
        AVDoor("Left Leg Shaft Inner TLU", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Left Leg Shaft Inner TUl", logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) and logicfunction.redcoat(logic_info)(state) and logicfunction.grapple(logic_info)(state))
    )]

    LEFT_LEG_SHAFT_UPPER_LOWER = "Left Leg Shaft_Upper_Lower", [
        AVDoor("Left Leg Shaft Center Left Door", Orientation.Left),
        AVDoor("Left Leg Shaft Center Right Door", Orientation.Right),
        AVDoor("Left Leg Shaft Inner UlT", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Left Leg Shaft Inner UlUc", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state) and (logicfunction.grapple(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state) or logicfunction.infectiondone(logic_info)(state)) or ((logicfunction.grapple(logic_info)(state) or logicfunction.infectiondone(logic_info)(state)) and logicfunction.fielddisruptor(logic_info)(state)))
    )]

    LEFT_LEG_SHAFT_UPPER_SECRET = "Left Leg Shaft_Upper_Secret", [
        AVDoor("Left Leg Shaft Upper Left Door", Orientation.Left),
        AVDoor("Left Leg Shaft Inner UsUc")
    ]

    LEFT_LEG_SHAFT_UPPER_CENTER = "Left Leg Shaft_Upper_Center", [
        AVDoor("Left Leg Shaft Inner UcUl"),
        AVDoor("Left Leg Shaft Inner UcUs", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.grapple(logic_info)(state))),
        AVDoor("Left Leg Shaft Inner UcUu", logic=lambda logic_info: (lambda state: logicfunction.longwarp(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.redcoat(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and (logicfunction.trenchcoat(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state))) or (logicfunction.infectiondone(logic_info)(state) and (logicfunction.trenchcoat(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state))))
    )]

    LEFT_LEG_SHAFT_UPPER_UPPER = "Left Leg Shaft_Upper_Upper", [
        AVDoor("Left Leg Shaft Upper Right Door", Orientation.Right),
        AVDoor("Left Leg Shaft Inner UuUc")
    ]

    OPHELIAS_ATTIC = "Ophelia's Attic", [
        AVDoor("Ophelias Attic Right Door", Orientation.Right)
    ]

    OPHELIA = "Ophelia", [
        AVDoor("Ophelia Right Door", Orientation.Right)
    ]

    UKKINNA_SAVE_3 = "Ukkin-Na Save 3", [
        AVDoor("Ukkin-Na Save 3 Left Door", Orientation.Left),
        AVDoor("Ukkin-Na Save 3 Save", Orientation.Save)
    ]

    VISON_EXIT = "Vision Exit", [
        AVDoor("Vision Exit Left Door", Orientation.Left),
        AVDoor("Vision Exit Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.longwarp(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and (logicfunction.fielddisruptor(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)))) or (logicfunction.infectiondone(logic_info)(state) and (logicfunction.trenchcoat(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state))))
    )]

    FEETCONNECTOR = "Feet Connector", [
        AVDoor("Feet Connector Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Feet Connector Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]

    # ukkinnasave1: 2 regions
    UKKINNA_SAVE_1_LOWER = "Ukkin-Na Save 1_Lower", [
        AVDoor("Ukkin-Na Save 1 Lower Left Door", Orientation.Left),
        AVDoor("Ukkin-Na Save 1 Right Door", Orientation.Right),
        AVDoor("Ukkin-Na Save 1 Inner BU", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state) or (logicfunction.shortdrone(logic_info)(state) and logicfunction.infectiondone(logic_info)(state)))),
        AVDoor("Ukkin-Na Save 1 Save", Orientation.Save)
    ]

    UKKINNA_SAVE_1_UPPER = "Ukkin-Na Save 1_Upper", [
        AVDoor("Ukkin-Na Save 1 Upper Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.infectiondone(logic_info)(state))),
        AVDoor("Ukkin-Na Save 1 Inner UB"),
        AVDoor("Into Infection")
    ]

    # rightlegbottomshaft: 4 regions
    RIGHT_LEG_BOTTOM_SHAFT_WEST = "Right Leg Bottom Shaft_West", [
        AVDoor("Right Leg Bottom Shaft Left Door", Orientation.Left),
        AVDoor("Right Leg Bottom Shaft Inner WE"),
        AVDoor("Right Leg Bottom Shaft Inner WC", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state) and logicfunction.infectiondone(logic_info)(state))
    )]

    RIGHT_LEG_BOTTOM_SHAFT_EAST = "Right Leg Bottom Shaft_East", [
        AVDoor("Right Leg Bottom Shaft Lower Right Door", Orientation.Right),
        AVDoor("Right Leg Bottom Shaft Inner EW", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state) or logicfunction.grapple(logic_info)(state) or (logicfunction.shortdrone(logic_info)(state) and logicfunction.infectiondone(logic_info)(state)))
    )]

    RIGHT_LEG_BOTTOM_SHAFT_CENTER = "Right Leg Bottom Shaft_Center", [
        AVDoor("Right Leg Bottom Shaft Center Right Door", Orientation.Right),
        AVDoor("Right Leg Bottom Shaft Inner CW", logic=lambda logic_info: (lambda state: logicfunction.infectiondone(logic_info)(state))),
        AVDoor("Right Leg Bottom Shaft Inner CU", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state) and logicfunction.infectiondone(logic_info)(state))
    )]

    RIGHT_LEG_BOTTOM_SHAFT_UPPER = "Right Leg Bottom Shaft_Upper", [
        AVDoor("Right Leg Bottom Shaft Upper Right Door", Orientation.Right),
        AVDoor("Right Leg Bottom Shaft Inner UC")
    ]

    # ukkinnatoindi: 2 regions
    UKKINNA_TO_INDI_WEST = "Ukkin-Na to Indi_West", [
        AVDoor("Ukkin-Na to Indi Left Door", Orientation.Left),
        AVDoor("Ukkin-Na to Indi Inner WE", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))
    )]

    UKKINNA_TO_INDI_EAST = "Ukkin-Na to Indi_East", [
        AVDoor("Ukkin-Na to Indi Down Door", Orientation.Down, BossDoor.Areatrans),
        AVDoor("Ukkin-Na to Indi Right Door", Orientation.Right),
        AVDoor("Ukkin-Na to Indi Inner EW", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]

    UKKINNA_TO_EDIN = "Ukkin-Na to Edin", [
        AVDoor("Ukkin-Na to Edin Right Door", Orientation.Right, BossDoor.Areatrans, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Ukkin-Na to Edin Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))
    )]

    MUDROOM_OF_NEUROSIS = "Mudroom of Neurosis", [
        AVDoor("Mudroom of Neurosis Left Door", Orientation.Left),
        AVDoor("Mudroom of Neurosis Right Door", Orientation.Right)
    ]

    # entrancetomadness: 3 regions
    ENTRANCE_TO_MADNESS_LOWER = "Entrance to Madness_Lower", [
        AVDoor("Entrance to Madness Lower Left Door", Orientation.Left),
        AVDoor("Entrance to Madness Inner BU", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))
    )]

    ENTRANCE_TO_MADNESS_UPPER = "Entrance to Madness_Upper", [
        AVDoor("Entrance to Madness Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Entrance to Madness Inner US", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Entrance to Madness Inner UB")
    ]

    ENTRANCE_TO_MADNESS_SECRET = "Entrance to Madness_Secret", [
        AVDoor("Entrance to Madness Upper Left Door", Orientation.Left),
        AVDoor("Entrance to Madness Inner SU", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))
    )]

    UKKINNA_HIDDEN_ITEM = "Ukkin-Na Hidden Item", [
        AVDoor("Ukkin-Na Hidden Item Right Door", Orientation.Right),
        AVDoor("Ukkin-Na Hidden Item - Slug in Room")
    ]

    FOYER_OF_INSANITY = "Foyer of Insanity", [
        AVDoor("Foyer of Insanity Down Door", Orientation.Down),
        AVDoor("Foyer of Insanity Left Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))),
        AVDoor("Foyer of Insanity Right Up Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))
    )]

    # trenchcoatchamber: 2 regions
    TRENCHCOAT_CHAMBER_LOWER = "Trenchcoat Chamber_Lower", [
        AVDoor("Trenchcoat Chamber Down Door", Orientation.Down),
        AVDoor("Trenchcoat Chamber Inner BU", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))
    )]

    TRENCHCOAT_CHAMBER_UPPER = "Trenchcoat Chamber_Upper", [
        AVDoor("Trenchcoat Chamber Right Door", Orientation.Right),
        AVDoor("Trenchcoat Chamber Inner UB")
    ]

    # shaftoflaughingfaces: 3 regions
    SHAFT_OF_LAUGHING_FACES_LOWER = "Shaft of Laughing Faces_Lower", [
        AVDoor("Shaft of Laughing Faces Down Door", Orientation.Down),
        AVDoor("Shaft of Laughing Faces Inner BU", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))
    )]

    SHAFT_OF_LAUGHING_FACES_UPPER = "Shaft of Laughing Faces_Upper", [
        AVDoor("Shaft of Laughing Faces Up Door", Orientation.Up),
        AVDoor("Shaft of Laughing Faces Inner UB"),
        AVDoor("Shaft of Laughing Faces Inner US", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))
    )]

    SHAFT_OF_LAUGHING_FACES_SECRET = "Shaft of Laughing Faces_Secret", [
        AVDoor("Shaft of Laughing Faces Left Door", Orientation.Left),
        AVDoor("Shaft of Laughing Faces Inner SU", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))
    )]

    CORRIDOR_OF_PSYCHOSIS = "Corridor of Psychosis", [
        AVDoor("Corridor of Psychosis Down Door", Orientation.Down),
        AVDoor("Corridor of Psychosis Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyupnodrone(logic_info)(state))
    )]

    LIVING_ROOM_OF_ILLUSION = "Living Room of Illusion", [
        AVDoor('Living Room of Illusion Down Door', Orientation.Down, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Living Room of Illusion Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))
    )]

    GUEST_ROOM_OF_MENTAL_ILLNESS = "Guest Room of Mental Illness", [
        AVDoor("Guest Room of Mental Illness Down Door", Orientation.Down),
        AVDoor("Guest Room of Mental Illness Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))
    )]

    VISION_FOYER = "Vision Foyer", [
        AVDoor("Vision Foyer Down Door", Orientation.Down),
        AVDoor("Vision Foyer Right Door", Orientation.Right),
        AVDoor("Vision Foyer Left Door", Orientation.Left)  # DOES THIS COUNT AS A BOSS DOOR??????
    ]

    UKKINNA_SAVE_2 = "Ukkin-Na Save 2", [
        AVDoor("Ukkin-Na Save 2 Left Door", Orientation.Left),
        AVDoor("Ukkin-Na Save 2 Save", Orientation.Save)
    ]

    # vison: 2 regions
    VISION_LOWER = "Vision_Lower", [
        AVDoor("Vision Left Door", Orientation.Left),  # DOES THIS COUNT AS A BOSS DOOR??????
        AVDoor("Vision Lower Right Door", Orientation.Right),  # DOES THIS COUNT AS A BOSS DOOR??????
        AVDoor("Vision Inner BU", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state))  # assuming the head stays after redcoat
    )]

    VISION_UPPER = "Vision_Upper", [
        AVDoor('Vision Upper Right Door', Orientation.Right),  # DOES THIS COUNT AS A BOSS DOOR??????
        AVDoor("Vision Inner UB")
    ]

    # ukkinnatomaruru: 2 regions
    UKKINNA_TO_MARURU_LOWER = "Ukkin-Na to Mar-Uru_Lower", [
        AVDoor("Ukkin-Na to Mar-Uru Right Door", Orientation.Right),  # DOES THIS COUNT AS A BOSS DOOR??????
        AVDoor("Ukkin-Na to Mar-Uru Left Door", Orientation.Left),
        AVDoor("Ukkin-Na to Mar-Uru Inner BU", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) and ((logicfunction.shortdrone(logic_info)(state) and logicfunction.grapple(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state)) or logicfunction.longdrone(logic_info)(state)))
    )]

    UKKINNA_TO_MARURU_UPPER = "Ukkin-Na to Mar-Uru_Upper", [
        AVDoor("Ukkin-Na to Mar-Uru Up Door", Orientation.Up, BossDoor.Areatrans),
        AVDoor("Ukkin-Na to Mar-Uru Inner UB", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state))
    )]

    PEAK = "Peak", [
        AVDoor("Peak Left Door", Orientation.Left),
        AVDoor("Peak - Slug in Room", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))
    )]

    MARURU_TO_UKKINNA = "Mar-Uru to Ukkin-Na", [
        AVDoor("Mar-Uru to Ukkin-Na Down Door", Orientation.Down, BossDoor.Areatrans),
        AVDoor("Mar-Uru to Ukkin-Na Left Door", Orientation.Left)
    ]

    ATHETOS_FOYER1 = "Athetos Foyer 1", [
        AVDoor("Athetos Foyer 1 Lower Right Door", Orientation.Right),
        AVDoor("Athetos Foyer 1 Upper Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: (logicfunction.trenchcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)) or logicfunction.longdrone(logic_info)(state) or logicfunction.dronefly(logic_info)(state))
    )]

    #athetosfoyer2: 2 regions
    ATHETOS_FOYER2_LOWER = "Athetos Foyer 2_Lower", [
        AVDoor("Athetos Foyer 2 Lower Left Door", Orientation.Left),
        AVDoor("Athetos Foyer 2 Right Door", Orientation.Right),
        AVDoor("Athetos Foyer 2 Inner BU", logic=lambda logic_info: (lambda state: logicfunction.shortdrone(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))
    )]

    ATHETOS_FOYER2_UPPER = "Athetos Foyer 2_Upper", [
        AVDoor("Athetos Foyer 2 Upper Left Door", Orientation.Left),
        AVDoor("Athetos Foyer 2 Inner UB")
    ]

    MARURU_SAVE1 = "Mar-Uru Save 1", [
        AVDoor("Mar-Uru Save 1 Right Door", Orientation.Right),
        AVDoor("Mar-Uru Save 1 Save", Orientation.Save)
    ]

    ATHETOS_FOYER3 = "Athetos Foyer 3", [
        AVDoor("Athetos Foyer 3 Lower Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state))),
        AVDoor("Athetos Foyer 3 Upper Left Door", Orientation.Left, BossDoor.Outer, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state))
    )]

    SENTINEL_SHAFT = "Sentinel Shaft", [
        AVDoor("Sentinel Shaft Right Door", Orientation.Right, BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state))),
        AVDoor("Sentinel Shaft Left Door", Orientation.Left, BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state) and ((((logicfunction.redcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)) or (logicfunction.longdrone(logic_info)(state))) and logicfunction.grapple(logic_info)(state)) or (logicfunction.trenchcoat(logic_info)(state) and logicfunction.longdrone(logic_info)(state)) or logicfunction.dronefly(logic_info)(state)))
    )]

    #biofluxshaft1: 2 regions
    BIOFLUX_SHAFT1_LOWER = "Bioflux Shaft 1_Lower", [
        AVDoor("Bioflux Shaft 1 Lower Right Door", Orientation.Right, BossDoor.Outer),
        AVDoor("Bioflux Shaft 1 Inner BU", logic=lambda logic_info: (lambda state: logicfunction.longdrone(logic_info)(state) or ((logicfunction.longwarp(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and logicfunction.grapple(logic_info)(state))) and logicfunction.shortdrone(logic_info)(state)))),
    ]

    BIOFLUX_SHAFT1_UPPER = "Bioflux Shaft 1_Upper", [
        AVDoor("Bioflux Shaft 1 Upper Right Door", Orientation.Right),
        AVDoor("Bioflux Shaft 1 Inner UB")
    ]

    BIOFLUX_SHAFT2 = "Bioflux Shaft 2", [
        AVDoor("Bioflux Shaft 2 Left Door", Orientation.Left),
        AVDoor("Bioflux Shaft 2 Right Door", Orientation.Right),
        AVDoor("Bioflux Shaft 2 Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: (logicfunction.redcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)) or ((logicfunction.grapple(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state) or logicfunction.longdrone(logic_info)(state)) and logicfunction.trenchcoat(logic_info)(state)))
    )]

    BIOFLUX2_SECRET = "Bioflux 2 Secret", [
        AVDoor("Bioflux 2 Secret Left Door", Orientation.Left)
    ]

    #redgooroom: 2 regions
    RED_GOO_ROOM_LOWER = "Red Goo Room_Lower", [
        AVDoor("Red Goo Room Down Door", Orientation.Down),
        AVDoor("Red Goo Room Inner BU", logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))
    )]

    RED_GOO_ROOM_UPPER = "Red Goo Room_Upper", [
        AVDoor("Red Goo Room Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))),
        AVDoor("Red Goo Room Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))),
        AVDoor("Red Goo Room Inner UB")
    ]

    MARURU_SAVE2 = "Mar-Uru Save 2", [
        AVDoor("Mar-Uru Save 2 Right Door", Orientation.Right),
        AVDoor("Mar-Uru Save 2 Save", Orientation.Save)
    ]

    HYBRID_ROOM = "Hybrid Room", [
        AVDoor('Hybrid Room Left Door', Orientation.Left),
        AVDoor("Hybrid Room Right Door", Orientation.Right)
    ]

    ORANGE_NICKNACKS = "Orange Nicknacks", [
        AVDoor("Orange Nicknacks Lower Left Door", Orientation.Left),
        AVDoor("Orange Nicknacks Upper Left Door", Orientation.Left, BossDoor.Outer, logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))),
    ]

    XEDUR_HUL = "Xedur Hul", [
        AVDoor("Xedur Hul Right Door", Orientation.Right, BossDoor.Inner),
        AVDoor("Xedur Hul Left Door", Orientation.Left, BossDoor.Inner)
    ]

    #blueandpurplecorridor: 2 regions
    BLUE_AND_PURPLE_CORRIDOR_EAST = "Blue and Purple Corridor_East", [
        AVDoor("Blue and Purple Corridor Right Door", Orientation.Right),
        AVDoor("Blue and Purple Corridor Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Blue and Purple Corridor Inner EW", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state))
    )]

    BLUE_AND_PURPLE_CORRIDOR_WEST = "Blue and Purple Corridor_West", [
        AVDoor("Blue and Purple Corridor Left Door", Orientation.Left),
        AVDoor("Blue and Purple Corridor Inner WE", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state))
    )]

    HIDDEN_AREA_ENTRANCE = "Hidden Area Entrance", [
        AVDoor("Hidden Area Entrance Right Door", Orientation.Right),
        AVDoor("Hidden Area Entrance Left Door", Orientation.Left)
    ]

    HIDDEN_AREA_SHAFT = "Hidden Area Shaft", [
        AVDoor("Hidden Area Shaft Upper Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and (logicfunction.shortdrone(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state))))),
        AVDoor("Hidden Area Shaft Lower Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and ((logicfunction.anyglitch(logic_info)(state) and logicfunction.anyweapon(logic_info)(state)) or logicfunction.fatbeam(logic_info)(state)))
    )]

    SECRET_ITEM = "Secret Item", [
        AVDoor("Secret Item Left Door", Orientation.Left)
    ]

    # athetosfoyershaft: 3 regions
    ATHETOS_FOYER_SHAFT_LOWER = "Athetos Foyer Shaft_Lower", [
        AVDoor("Athetos Foyer Shaft Down Door", Orientation.Down),
        AVDoor("Athetos Foyer Shaft Inner BC", logic=lambda logic_info: (lambda state: logicfunction.tempup(logic_info)(state))
    )]

    ATHETOS_FOYER_SHAFT_CENTER = "Athetos Foyer Shaft_Center", [
        AVDoor("Athetos Foyer Shaft Left Door", Orientation.Left),
        AVDoor("Athetos Foyer Shaft Inner CB"),
        AVDoor("Athetos Foyer Shaft Inner CU", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and logicfunction.grapple(logic_info)(state)))
    )]

    ATHETOS_FOYER_SHAFT_UPPER = "Athetos Foyer Shaft_Upper", [
        AVDoor("Athetos Foyer Up Door", Orientation.Up, BossDoor.Outer),
        AVDoor("Athetos Foyer Inner UC", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state))
    )]

    MARURU_SAVE3 = "Mar-Uru Save 3", [
        AVDoor("Mar-Uru Save 3 Right Door", Orientation.Right),
        AVDoor("Mar-Uru Save 3 Save", Orientation.Save)
    ]

    ATHETOS = "Athetos", [
        AVDoor("Athetos Down Door", Orientation.Down)
    ]

    # edintoukkinna: 5 regions
    EDIN_TO_UKKINNA_WEST = "Edin to Ukkin-Na_West", [
        AVDoor("Edin to Ukkin-Na Left Door", Orientation.Left, BossDoor.Areatrans),
        AVDoor("Edin to Ukkin-Na Inner WC", logic=lambda logic_info: (lambda state: logicfunction.longwarp(logic_info)(state) or logicfunction.shortdrone(logic_info)(state)))
    ]

    EDIN_TO_UKKINNA_CENTER = "Edin to Ukkin-Na_Center", [
        AVDoor("Edin to Ukkin-Na Inner CW"),
        AVDoor("Edin to Ukkin-Na Inner CE"),
        AVDoor("Edin to Ukkin-Na Inner CU", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.glitchnades(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state))))
    ]

    EDIN_TO_UKKINNA_UPPER = "Edin to Ukkin-Na_Upper", [
        AVDoor("Edin to Ukkin-Na Up Door", Orientation.Up),
        AVDoor("Edin to Ukkin-Na Inner UC", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state) or logicfunction.glitchnades(logic_info)(state)))
    ]

    EDIN_TO_UKKINNA_EAST = "Edin to Ukkin-Na_East", [
        AVDoor("Edin to Ukkin-Na Upper Right Door", Orientation.Right),
        AVDoor("Edin to Ukkin-Na Inner EC", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.longdrone(logic_info)(state) or logicfunction.dronefly(logic_info)(state) or logicfunction.grapple(logic_info)(state) or (logicfunction.shortdrone(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state))))
    ]

    EDIN_TO_UKKINNA_SECRET = "Edin to Ukkin-Na_Secret", [
        AVDoor("Edin to Ukkin-Na Lower Right Door", Orientation.Right)
    ]

    #edintoindi: 2 regions
    EDIN_TO_INDI_MAIN = "Edin to Indi_Main", [
        AVDoor("Edin to Indi Down Door", Orientation.Down, BossDoor.Areatrans),
        AVDoor("Edin to Indi Right Door", Orientation.Right),
        AVDoor("Edin to Indi Upper Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Edin to Indi Inner MS", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state)))
    ]

    EDIN_TO_INDI_SECRET = "Edin to Indi_Secret", [
        AVDoor("Edin to Indi Lower Left Door", Orientation.Left),
        AVDoor("Edin to Indi Inner SM", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state)))
    ]

    #hangarbasemententrance: 3 regions
    HANGAR_BASEMENT_ENTRANCE_WEST = "Hangar Basement Entrance_West", [
        AVDoor("Hangar Basement Entrance Lower Left Door", Orientation.Left),
        AVDoor("Hangar Basement Entrance Inner WE", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state) and logicfunction.glitchnades(logic_info)(state))),
        AVDoor("Hangar Basement Entrance Inner WU", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and (logicfunction.shortdrone(logic_info)(state) or logicfunction.grapple(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state))))
    ]

    HANGAR_BASEMENT_ENTRANCE_EAST = "Hangar Basement Entrance_East", [
        AVDoor("Hangar Basement Entrance Right Door", Orientation.Right),
        AVDoor("Hangar Basement Entrance Inner EW", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.glitchnades(logic_info)(state))),
        AVDoor("Hangar Basement Entrance Inner EU", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and (logicfunction.shortdrone(logic_info)(state) or logicfunction.grapple(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state))))
    ]

    HANGAR_BASEMENT_ENTRANCE_UPPER = "Hangar Basement Entrance_Upper", [
        AVDoor("Hangar Basement Entrance Upper Left Door", Orientation.Left),
        AVDoor("Hangar Basement Entrance Inner UW", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Hangar Basement Entrance Inner UE", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.glitchnades(logic_info)(state)))
    ]

    #westernhangarentrance: 3 regions
    WESTERN_HANGAR_ENTRANCE_LOWER = "Western Hangar Entrace_Lower", [
        AVDoor("Western Hangar Entrance Lower Right Door", Orientation.Right),
        AVDoor("Western Hangar Entrance Inner BC", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state)))
    ]

    WESTERN_HANGAR_ENTRANCE_CENTER = "Western Hangar Entrance_Center", [
        AVDoor("Western Hangar Entrance Inner CB"),
        AVDoor("Western Hangar Entrance Inner CU", logic=lambda logic_info: (lambda state: logicfunction.longwarp(logic_info)(state) or logicfunction.shortdrone(logic_info)(state)))
    ]

    WESTERN_HANGAR_ENTRANCE_UPPER = "Western Hangar Entrance_Upper", [
        AVDoor("Western Hangar Entrance Upper Right Door", Orientation.Right),
        AVDoor("Western Hangar Entrance Inner UC")
    ]

    HANGAR_FOYER = "Hangar Foyer", [
        AVDoor("Hangar Foyer Left Door", Orientation.Left),
        AVDoor("Hangar Foyer Right Door", Orientation.Right)
    ]

    EDIN_SAVE1 = "Edin Save 1", [
        AVDoor("Edin Save 1 Left Door", Orientation.Left),
        AVDoor("Edin Save 1 Right Door", Orientation.Right),
        AVDoor("Edin Save 1 Save", Orientation.Save)
    ]

    DEFORMED_TRACE_BOSS_FOYER = "Deformed Trace Boss Foyer", [
        AVDoor("Deformed Trace Boss Foyer Left Door", Orientation.Left),
        AVDoor("Deformed Trace Boss Foyer Down Door", Orientation.Down, bossdoor=BossDoor.Outer)
    ]

    DEFORMED_TRACE_BOSS_ROOM = "Deformed Trace Boss Room", [
        AVDoor("Deformed Trace Boss Room Up Door", Orientation.Up, bossdoor=BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.anyweapon(logic_info)(state) and (logicfunction.trenchcoat(logic_info)(state) and logicfunction.dronefly(logic_info)(state)) or (logicfunction.longdrone(logic_info)(state) and logicfunction.redcoat(logic_info)(state)))),
        AVDoor("Deformed Trace Boss Room Left Door", Orientation.Left, bossdoor=BossDoor.Inner)
    ]

    HANGAR_ACCESS = "Hangar Access", [
        AVDoor("Hangar Access Right Door", Orientation.Right, bossdoor=BossDoor.Outer, logic=lambda logic_info: (lambda state: logicfunction.longwarp(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.anyupnoceiling(logic_info)(state)))),
        AVDoor("Hangar Access Down Door", Orientation.Down)
    ]

    #hangar: 3 regions
    HANGAR_EAST = "Hangar_East", [
        AVDoor("Hangar Right Door", Orientation.Right),
        AVDoor("Hangar Inner EW", logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state))),
        AVDoor("Hangar Inner EU", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state)))
    ]

    HANGAR_WEST = "Hangar_West", [
        AVDoor("Hangar Left Door", Orientation.Left),
        AVDoor("Hangar Inner WE", logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state)))
    ]

    HANGAR_UPPER = "Hangar_Upper", [
        AVDoor("Hangar Up Door", Orientation.Up),
        AVDoor("Hangar Inner UE")
    ]

    #edintokur: 3 regions
    EDIN_TO_KUR_WEST = "Edin to Kur_West", [
        AVDoor("Edin to Kur Lower Left Door", Orientation.Left),
        AVDoor("Edin to Kur Inner WE", logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state)))
    ]

    EDIN_TO_KUR_EAST = "Edin to Kur_East", [
        AVDoor("Edin to Kur Right Door", Orientation.Right, bossdoor=BossDoor.Areatrans),
        AVDoor("Edin to Kur Inner EW", logic=lambda logic_info: (lambda state: logicfunction.glitchnades(logic_info)(state))),
        AVDoor("Edin to Kur Inner EU", logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.glitchnades(logic_info)(state) and (logicfunction.shortdrone(logic_info)(state) or logicfunction.longwarp(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state))))))
    ]

    EDIN_TO_KUR_UPPER = "Edin to Kur_Upper", [
        AVDoor("Edin to Kur Upper Left Door", Orientation.Left),
        AVDoor("Edin to Kur Inner UE", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state)))
    ]

    HANGAR_ATTIC = "Hangar Attic", [
        AVDoor("Hangar Attic Right Door", Orientation.Right)
    ]

    #westtowerlevel1: 2 regions
    WEST_TOWER_LEVEL1_LOWER = "West Tower Level 1_Lower", [
        AVDoor("West Tower Level 1 Down Door", Orientation.Down),
        AVDoor("West Tower Level 1 Lower Left Door", Orientation.Left),
        AVDoor("West Tower Level 1 Right Door", Orientation.Right),
        AVDoor("West Tower Level 1 Inner BU", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))
    ]

    WEST_TOWER_LEVEL1_UPPER = "West Tower Level 1_Upper", [
        AVDoor("West Tower Level 1 Upper Left Door", Orientation.Left),
        AVDoor("West Tower Level 1 Inner UB")
    ]

    EDIN_SAVE2 = "Edin Save 2", [
        AVDoor("Edin Save 2 Right Door", Orientation.Right),
        AVDoor("Edin Save 2 Save", Orientation.Save)
    ]

    LEVEL1_SECRET = "Level 1 Secret", [
        AVDoor("Level 1 Secret Left Door", Orientation.Left)
    ]

    WEST_TOWER_LEVEL2 = "West Tower Level 2", [
        AVDoor("West Tower Level 2 Right Door", Orientation.Right),
        AVDoor("West Tower Level 2 Left Door", Orientation.Left),
        AVDoor("West Tower Level 2 Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state)))
    ]

    DistortionFieldRoom = "Distortion Field Room", [
        AVDoor("Distortion Field Room Right Door", Orientation.Right)
    ]

    #westtowerlevel3: 4 regions
    WEST_TOWER_LEVEL3_LOWER = "West Tower Level 3_Lower", [
        AVDoor("West Tower Level 3 Down Door", Orientation.Down),
        AVDoor("West Tower level 3 Inner BE", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state)))
    ]

    WEST_TOWER_LEVEL3_EAST = "West Tower Level 3_East", [
        AVDoor("West Tower Level 3 Inner EB"),
        AVDoor("West Tower Level 3 Inner EU", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state)))
    ]

    WEST_TOWER_LEVEL3_UPPER = "West Tower Level 3_Upper", [
        AVDoor("West Tower Level 3 Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state))),
        AVDoor("West Tower Level 3 Inner UE", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("West Tower Level 3 Inner UW", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)))
    ]

    WEST_TOWER_LEVEL3_WEST = "West Tower Level 3_West", [
        AVDoor("West Tower Level 3 Left Door", Orientation.Left),
        AVDoor("West Tower Level 3 Inner WU", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)))
    ]

    SPITBUG_BOSS_FOYER = "Spitbug Boss Foyer", [
        AVDoor("Spitbug Boss Foyer Down Door", Orientation.Down),
        AVDoor("Spitbug Boss Foyer Right Door", Orientation.Right),
        AVDoor("Spitbug Boss Foyer Left Door", Orientation.Left, bossdoor=BossDoor.Outer)
    ]

    EDIN_SAVE3 = "EDIN Save 3", [
        AVDoor("EDIN Save 3 Left Door", Orientation.Left),
        AVDoor("EDIN Save 3 Save", Orientation.Save)
    ]

    SPITBUG_BOSS_ROOM = "Spitbug Boss Room", [
        AVDoor("Spitbug Boss Room Right Door", Orientation.Right, bossdoor=BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.rangeweapon(logic_info)(state))), # this room DEFINITELY needs combat logic
        AVDoor("Spitbug Boss Room Left Door", Orientation.Left, bossdoor=BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.rangeweapon(logic_info)(state)))
    ]

    #droneteleportroom: 2 regions
    DRONE_TELEPORT_ROOM_UPPER = "Drone Teleport Room_Upper", [
        AVDoor("Drone Teleport Room Upper Right Door", Orientation.Right, bossdoor=BossDoor.Outer),
        AVDoor("Drone Teleport Room Inner UB", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state)))
    ]

    DRONE_TELEPORT_ROOM_LOWER = "Drone Teleport Room_Lower", [
        AVDoor("Drone Teleport Room Lower Right Door", Orientation.Right),
        AVDoor("Drone Teleport Room Inner BU", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state)))
    ]

    #foothills: 5 regions
    FOOTHILLS_WEST = "Foothills_West", [
        AVDoor("Foothills Down Door", Orientation.Down),
        AVDoor("Foothills Inner WM", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or (logicfunction.anycoat(logic_info)(state) and logicfunction.drill(logic_info)(state)) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state)))),
        AVDoor("Foothills Inner WU", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state)))
    ]

    FOOTHILLS_MAIN = "Foothills_Main", [
        AVDoor("Foothills Inner MW", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or (logicfunction.anycoat(logic_info)(state) and logicfunction.drill(logic_info)(state)) or logicfunction.shortdrone(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state) or logicfunction.grapple(logic_info)(state))),
        AVDoor("Foothills Inner ME", logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Foothills Inner MS", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and logicfunction.dronequest(logic_info)(state))),
        AVDoor("Foothills Inner MU", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))
    ]

    FOOTHILLS_UPPER = "Foothills Upper", [
        AVDoor("Foothills Up Door", Orientation.Up),
        AVDoor("Foothills Inner UM"),
        AVDoor("Foothills Inner UW"),
        AVDoor("Foothills Inner US", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state)))
    ]
    
    FOOTHILLS_SECRET = "Foothills_Secret", [
        AVDoor("Foothills Upper Right Door", Orientation.Right),
        AVDoor("Foothills Inner SM", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state))),
        AVDoor("Foothills Inner SU", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state)))
    ]
    
    FOOTHILLS_EAST = "Foothills_East", [
        AVDoor("Foothills Lower Right Door", Orientation.Right),
        AVDoor("Foothills Inner EM", logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state)))
    ]

    THORN_MAZE = "Thorn Maze", [
        AVDoor("Thorn Maze Left Door", Orientation.Left),
        AVDoor("Thorn Maze Right Door", Orientation.Right)
    ]

    THORN_MAZE_SECRET = "Thorn Maze Secret", [
        AVDoor("Thorn Maze Secret Left Door", Orientation.Left)
    ]

    LAIR_ENTRANCE = "Lair Entrance", [
        AVDoor("Lair Entrance Left Door", Orientation.Left),
        AVDoor("Lair Entrance Right Door", Orientation.Right)
    ]

    ELEVATED_POOLS = "Elevated Pools", [
        AVDoor("Elevated Pools Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Elevated Pools Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.fielddisruptor(logic_info)(state) and logicfunction.anyglitch(logic_info)(state))))
    ]

    LAIR_VESTIBULE = "Lair Vestibule", [
        AVDoor("Lair Vestibule Left Door", Orientation.Left), # probably needs combat logic
        AVDoor("Lair Vestibule Right Door", Orientation.Right)
    ]

    #girtabfoyer: 2 regions
    GIRTAB_FOYER_LOWER = "Gir-Tab Foyer_Lower", [
        AVDoor("Gir-Tab Foyer Lower Left Door", Orientation.Left),
        AVDoor("Gir-Tab Foyer Inner BU", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))
    ]

    GIRTAB_FOYER_UPPER = "Gir=Tab Foyer_Upper", [
        AVDoor("Gir-Tab Foyer Upper Left Door", Orientation.Left),
        AVDoor("Gir-Tab Foyer Right Door", Orientation.Right, bossdoor=BossDoor.Outer, logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))),
        AVDoor("Gir-Tab Foyer Innner UB")
    ]

    KUR_SAVE2 = "Kur Save 2", [
        AVDoor("Kur Save 2 Right Door", Orientation.Right),
        AVDoor("Kur Save 2 Save", Orientation.Save)
    ]

    GIRTAB = "Gir-Tab", [
        AVDoor("Gir-Tab Left Door", Orientation.Left, bossdoor=BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.girtabweapon(logic_info)(state))),
        AVDoor("Gir-Tab Right Door", Orientation.Right, bossdoor=BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.girtabweapon(logic_info)(state))),
        AVDoor("Gir-Tab Up Door", Orientation.Up, bossdoor=BossDoor.Inner, logic=lambda logic_info: (lambda state: logicfunction.girtabweapon(logic_info)(state) and logicfunction.no(logic_info)(state))) # this is possible but i cannot be bothered to figure out how right now
    ]

    KATRAHASKA = "Katrahaska", [
        AVDoor("Katrahaska Left Door", Orientation.Left),
        AVDoor("Katrahaska Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))
    ]

    #maintenanceentrance: 2 regions

    MAINTENANCE_ENTRANCE_LOWER = "Maintenance Entrance_Lower", [
        AVDoor("Maintenance Entrance Down Door", Orientation.Down),
        AVDoor("Maintenance Entrance Inner BU", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state)))
    ]

    MAINTENANCE_ENTRANCE_UPPER = "Maintenance Entrance_Upper", [
        AVDoor("Maintenance Entrance Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Maintenance Entrance Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Maintenance Entrance Inner UB")
    ]

    DRONE_CONTROL = "Drone Control", [
        AVDoor("Drone Control Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) and logicfunction.breakblock(logic_info)(state))),
        AVDoor("Drone Control Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) and logicfunction.breakblock(logic_info)(state)))
    ]

    #secretkurtoekurmah: 2 regions
    SECRET_KUR_TO_EKURMAH_WEST = "Secret Kur to E-Kur-Mah_West", [
        AVDoor("Secret Kur to E-Kur-Mah Left Door", Orientation.Left),
        AVDoor("Secret Kur to E-Kur-Mah Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.fielddisruptor(logic_info)(state))),
        AVDoor("Secret Kur to E-Kur-Mah Inner WE", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state)))
    ]

    SECRET_KUR_TO_EKURMAH_EAST = "Secret Kur to E-Kur-Mah_East", [
        AVDoor("Secret Kur to E-Kur-Mah Right Door", Orientation.Right, bossdoor=BossDoor.Areatrans),
        AVDoor("Secret Kur to E-Kur-Mah Inner EW", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.drill(logic_info)(state)))
    ]

    #mountainback: 4 regions

    MOUNTAIN_BACK_LOWER = "Mountain Back_Lower", [
        AVDoor("Mountain Back Down Door", Orientation.Down),
        AVDoor("Mountain Back Inner BW", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state) and (logicfunction.drone(logic_info)(state) or logicfunction.longpierce(logic_info)(state) or logicfunction.trenchcoat(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.anycoat(logic_info)(state))))),
        AVDoor("Mountain Back Inner BE", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) and (logicfunction.shortdrone(logic_info)(state) or (logicfunction.anyupnoceiling(logic_info)(state) and logicfunction.grapple(logic_info)(state)))))
    ]

    MOUNTAIN_BACK_WEST = "Mountain Back_West", [
        AVDoor("Mountain Back Left Door", Orientation.Left),
        AVDoor("Mountain Back Inner WB", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.breakblock(logic_info)(state) or (logicfunction.anyup(logic_info) and logicfunction.anycoat(logic_info)(state)))),
        AVDoor("Mountain Back Inner WU", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))
    ]

    MOUNTAIN_BACK_UPPER = "Mountain Back_Upper", [
        AVDoor("Mountain Back Inner UW", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Mountain Back Inner UE")
    ]

    MOUNTAIN_BACK_EAST = "Mountain Back_East", [
        AVDoor("Mountain Back Inner EB", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) and logicfunction.sevenblockup(logic_info)(state))),
        AVDoor("Mountain Back Inner EU", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) and logicfunction.sevenblockup(logic_info)(state)))
    ]

    KUR_SAVE5 = "Kur Save 5", [
        AVDoor("Kur Save 5 Right Door", Orientation.Right),
        AVDoor("Kur Save 5 Save", Orientation.Save)
    ]

    #secretlairruins: 3 regions
    SECRET_LAIR_RUINS_LOWER = "Secret Lair Ruins_Lower", [
        AVDoor("Secret Lair Ruins Down Door", Orientation.Down),
        AVDoor("Secret Lair Ruins Inner BE", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state)))
    ]

    SECRET_LAIR_RUINS_EAST = "Secret Lair Ruins_East", [
        AVDoor("Secret Lair Ruins Right Door", Orientation.Right),
        AVDoor("Secret Lair Ruins Inner EB"),
        AVDoor("Secret Lair Ruins Inner EW", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state)))
    ]

    SECRET_LAIR_RUINS_WEST = "Secret Lair Ruins_West", [
        AVDoor("Secret Lair Ruins Left Door", Orientation.Left),
        AVDoor("Secret Lair Ruins Inner WE", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) and logicfunction.anyupnoceiling(logic_info)(state)))
    ]

    SECRET_LAIR_SHORTCUT = "Secret Lair Shortcut", [
        AVDoor("Secret Lair Shortcut Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Secret Lair Shortcut Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))
    ]

    #droneroom: 5 regions
    DRONE_ROOM_WEST = "Drone Room_West", [
        AVDoor("Drone Room Upper Left Door", Orientation.Left, logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.fatbeam(logic_info)(state) or (logicfunction.breakblock(logic_info)(state) and (logicfunction.sevenblockup(logic_info)(state) or logicfunction.drone(logic_info)(state))))),
        AVDoor("Drone Room Inner WB", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state) or logicfunction.fatbeam(logic_info)(state))),
        AVDoor("Drone Room Inner WC", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and (logicfunction.anycoat(logic_info)(state) or logicfunction.fatbeam(logic_info)(state))))
    ]

    DRONE_ROOM_LOWER = "Drone Room_Lower", [
        AVDoor("Drone Room Inner BW", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state)))),
        AVDoor("Drone Room Inner BS", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state) and (logicfunction.trenchcoat(logic_info)(state) or logicfunction.breakblock(logic_info)(state) or logicfunction.drone(logic_info)(state)))),
        AVDoor("Drone Room Inner BC", logic=lambda logic_info: (lambda state: logicfunction.shortdrone(logic_info)(state)))
    ]

    DRONE_ROOM_SECRET = "Drone Room_Secret", [
        AVDoor("Drone Room Lower Left Door", Orientation.Left),
        AVDoor("Drone Room Inner SB", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state)))
    ]

    DRONE_ROOM_CENTER = "Drone Room_Center", [
        AVDoor("Drone Room Inner CB", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Drone Room Inner CW"),
        AVDoor("Drone Room Inner CE", logic=lambda logic_info: (lambda state: logicfunction.sevenblockup(logic_info)(state) and logicfunction.drill(logic_info)(state)))
    ]

    DRONE_ROOM_EAST = "Drone Room_East", [
        AVDoor("Drone Room Right Door", Orientation.Right),
        AVDoor("Drone Room Inner EC", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state)))
    ]

    #mountainslope: 6 regions
    MOUNTAIN_SLOPE_LOWER = "Mountain Slope_Lower", [
        AVDoor("Mountain Slope Down Door", Orientation.Down),
        AVDoor("Mountain Slope Lower Right Door", Orientation.Right),
        AVDoor("Mountain Slope Inner BM", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Mountain Slope Inner BE", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.fielddisruptor(logic_info)(state) and (logicfunction.drone(logic_info)(state) or logicfunction.longpierce(logic_info)(state))))),
        AVDoor("Mountain Slope Inner BU", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state)))
    ]

    MOUNTAIN_SLOPE_MAIN = "Mountain Slope_Main", [
        AVDoor("Mountain Slope Inner MS", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Mountain Slope Inner MB"),
        AVDoor("Mountain Slope Inner ME"),
        AVDoor("Mountain Slope Inner MU", logic=lambda logic_info: (lambda state: logicfunction.verylongwarp(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.anyupnoceiling(logic_info)(state) and logicfunction.grapple(logic_info)(state)))),
        AVDoor("Mountain Slope Inner MI", logic=lambda logic_info: (lambda state: logicfunction.grapple(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or logicfunction.redcoat(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and logicfunction.drone(logic_info)(state))))
    ]

    MOUNTAIN_SLOPE_SECRET = "Mountain Slope_Secret", [
        AVDoor("Mountain Slope Upper Right Door", Orientation.Right, logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Mountain Slope Inner SM", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state)))
    ]

    MOUNTAIN_SLOPE_EAST = "Mountain Slope_East", [
        AVDoor("Mountain Slope Center Right Door", Orientation.Right),
        AVDoor("Mountain Slope Inner EM", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))),
        AVDoor("Mountain Slope Inner EB", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.breakblock(logic_info)(state)))
    ]

    MOUNTAIN_SLOPE_UPPER = "Mountain Slope_Upper", [
        AVDoor("Mountain Slope Up Door", Orientation.Up),
        AVDoor("Mountain Slope Inner UM", logic=lambda logic_info: (lambda state: logicfunction.drill(logic_info)(state))),
        AVDoor("Mountain Slope Inner UB"),
        AVDoor("Mountain Slope Inner UI", logic=lambda logic_info: (lambda state: logicfunction.drone(logic_info)(state)))
    ]

    MOUNTAIN_SLOPE_ITEM = "Mountain Slope_Item", [
        AVDoor("Mountain Slope IU", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state))),
        AVDoor("Mountain Slope IM", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state)))
    ]

    KUR_SAVE3 = "Kur Save 3", [
        AVDoor("Kur Save 3 Left Door", Orientation.Left),
        AVDoor("Kur Save 3 Save", Orientation.Save)
    ]

    #icecrags: 12 regions dear god
    ICECRAGS_LOWERWEST = "Ice Crags_LowerWest", [
        AVDoor("Ice Crags Down Door", Orientation.Down),
        AVDoor("Ice Crags Inner BwW", logic=lambda logic_info: (lambda state: logicfunction.shortdrone(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state)) or (logicfunction.fielddisruptor(logic_info)(state) and (logicfunction.trenchcoat(logic_info)(state) or logicfunction.grapple(logic_info)(state))))),
        AVDoor("Ice Crags Inner BwBe", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state)))
    ]

    ICECRAGS_WEST = "Ice Crags_West", [
        AVDoor("Ice Crags Inner WBw"),
        AVDoor("Ice Crags Inner WE", logic=lambda logic_info: (lambda state: logicfunction.sevenblockup(logic_info)(state) and logicfunction.anycoat(logic_info)(state))),
        AVDoor("Ice Crags Inner WC"),
        AVDoor("Ice Crags Inner WUw", logic=lambda logic_info: (lambda state: logicfunction.shortdrone(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state)) or (logicfunction.fielddisruptor(logic_info)(state) and (logicfunction.trenchcoat(logic_info)(state) or logicfunction.grapple(logic_info)(state))))),
        AVDoor("Ice Crags Inner WSw", logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or (logicfunction.shortdrone(logic_info)(state) and logicfunction.grapple(logic_info)(state))))
    ]

    ICECRAGS_LOWEREAST = "Ice Crags_LowerEast", [
        AVDoor("Ice Crags Inner BeBw", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state))),
        AVDoor("Ice Crags Inner BeE", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))),
        AVDoor("Ice Crags Inner BeSe", logic=lambda logic_info: (lambda state: logicfunction.dronequest(logic_info)(state)))
    ]

    ICECRAGS_EAST = "Ice Crags_East", [
        AVDoor("Ice Crags Inner EBe"),
        AVDoor("Ice Crags Inner EW", logic=lambda logic_info: (lambda state: logicfunction.anycoat(logic_info)(state))),
        AVDoor("Ice Crags Inner EC", logic=lambda logic_info: (lambda state: logicfunction.grapple(logic_info)(state) or logicfunction.longdrone(logic_info)(state) or ((logicfunction.shortdrone(logic_info)(state) and logicfunction.longwarp(logic_info)(state)))))
    ]

    ICECRAGS_SECRETEAST = "Ice Crags_SecretEast", [
        AVDoor("Ice Crags Inner SeBe", logic=lambda logic_info: (lambda state: logicfunction.shortdrone(logic_info)(state))),
        AVDoor("Ice Crags Inner SeSb")
    ]

    ICECRAGS_SECRETLOWER = "Ice Crags_SecretLower", [
        AVDoor("Ice Crags Lower Right Door", Orientation.Right),
        AVDoor("Ice Crags Inner SbSe", logic=lambda logic_info: (lambda state: logicfunction.grapple(logic_info)(state) or (logicfunction.drone(logic_info)(state) and (logicfunction.anyupnodrone(logic_info)(state) or logicfunction.dronelaunch(logic_info)(state)))))
    ]

    ICECRAGS_UPPER = "Ice Crags_Upper", [
        AVDoor("Ice Crags Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.anyupnodrone(logic_info)(state))),
        AVDoor("Ice Crags Upper Right Door", Orientation.Right),
        AVDoor("Ice Crags Inner UUe")
    ]

    ICECRAGS_CENTER = "Ice Crags_Center", [
        AVDoor("Ice Crags Inner CE"),
        AVDoor("Ice Crags Inner CW", logic=lambda logic_info: (lambda state: logicfunction.anyupnoceiling(logic_info)(state))),
        AVDoor("Ice Crags Inner CUe", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state) or (logicfunction.fielddisruptor(logic_info)(state) and logicfunction.grapple(logic_info)(state))))
    ]

    ICECRAGS_UPPEREAST = "Ice Crags_UpperEast", [
        AVDoor("Ice Crags Inner UeU", logic=lambda logic_info: (lambda state: logicfunction.anyup(logic_info)(state))),
        AVDoor("Ice Crags Inner UeC"),
        AVDoor("Ice Crags Inner UeUw", logic=lambda logic_info: (lambda state: logicfunction.shortdrone(logic_info)(state) or (logicfunction.grapple(logic_info)(state) and logicfunction.trenchcoat(logic_info)(state)) or (logicfunction.fielddisruptor(logic_info)(state) and (logicfunction.trenchcoat(logic_info)(state) or logicfunction.grapple(logic_info)(state)))))
    ]

    ICECRAGS_UPPERWEST = "Ice Crags_UpperWest", [
        AVDoor("Ice Crags Inner UwW"),
        AVDoor("Ice Crags Inner UwUe", logic=lambda logic_info: (lambda state: logicfunction.sevenblockup(logic_info)(state))),
        AVDoor("Ice Crags Inner UwSu", logic=lambda logic_info: (lambda state: logicfunction.glitch2(logic_info)(state) and (logicfunction.grapple(logic_info)(state) or (logicfunction.drill(logic_info)(state) and (logicfunction.shortdrone(logic_info)(state) or (logicfunction.trenchcoat(logic_info)(state) and logicfunction.fielddisruptor(logic_info)(state)))))))
    ]

    ICECRAGS_SECRETUPPER = "Ice Crags_SecretUpper", [
        AVDoor("Ice Crags Inner SuSw"),
        AVDoor("Ice Crags Inner SuUw", logic=lambda logic_info: (lambda state: logicfunction.no(logic_info)(state)))
    ]

    ICECRAGS_SECRETWEST = "Ice Crags_SecretWest", [
        AVDoor("Ice Crags Inner SwSu", logic=lambda logic_info: (lambda state: logicfunction.dronefly(logic_info)(state) or logicfunction.longdrone(logic_info)(state) or ((logicfunction.shortdrone(logic_info)(state) or logicfunction.redcoat(logic_info)(state)) and logicfunction.grapple(logic_info)(state)))),
        AVDoor("Ice Crags Inner SwW")
    ]

    CAVERN_OF_THE_ROSES1 = "Cavern of the Roses", [
        AVDoor("Cavern of the Roses Left Door", Orientation.Left),
        AVDoor("Cavern of the Roses Right Door", Orientation.Right)
    ]

    FLORAL_CLOSET = "Floral Closet", [
        AVDoor("Floral Closet Left Door", Orientation.Left),
        AVDoor("Floral Closet Up Door", Orientation.Up)
    ]

    HIDDEN_STALAGMITE = "Hidden Stalagmite", [
        AVDoor("Hidden Stalagmite Down Door", Orientation.Down),
        AVDoor("Hidden Stalagmite Right Door", Orientation.Right)
    ]

    SUSPENSION_OF_THE_GILL = "Suspension of the Gill", [
        AVDoor("Suspension of the Gill Left Door", Orientation.Left),
        AVDoor("Suspension of the Gill Up Door", Orientation.Up)
    ]

    REFLECTOR_ROOM = "Reflector Room", [
        AVDoor("Reflector Room Down Door", Orientation.Down)
    ]

    IMPROVED_LAUNCH_ROOM = "Improved Launch Room", [
        AVDoor("Improved Launch Room Left Door", Orientation.Left)
    ]

    #kurtoekurmah: 2 regions

    KUR_TO_EKURMAH_WEST = "Kur to E-Kur-Mah_West", [
        AVDoor("Kur to E-Kur-Mah Down Door", Orientation.Down),
        AVDoor("Kur to E-Kur-Mah Left Door", Orientation.Left),
        AVDoor("Kur to E-Kur-Mah Inner WE", logic=lambda logic_info: (lambda state: (logicfunction.verylongwarp(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)) or ((logicfunction.longdrone(logic_info)(state) or logicfunction.dronefly(logic_info)(state)) and logicfunction.trenchcoat(logic_info)(state))))
    ]

    KUR_TO_EKURMAH_EAST = "Kur to E-Kur-Mah_East", [
        AVDoor("Kur to E-Kur-Mah Right Door", Orientation.Right),
        AVDoor("Kur to E-Kur-Mah Inner EW", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)))
    ]

    KUR_SAVE4 = "Kur Save 4", [
        AVDoor("Kur Save 4 Right Door", Orientation.Right),
        AVDoor("Kur Save 4 Save", Orientation.Save)
    ]

    #ekurmahtokur: 5 regions
    EKURMAH_TO_KUR_WEST = "E-Kur-Mah to Kur_West", [
        AVDoor("E-Kur-Mah to Kur Left Door", Orientation.Left),
        AVDoor("E-Kur-Mah to Kur Inner WC", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("E-Kur-Mah to Kur Inner WU", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and (logicfunction.longdrone(logic_info)(state) or logicfunction.dronefly(logic_info)(state) or (logicfunction.fielddisruptor(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)))))
    ]

    EKURMAH_TO_KUR_CENTER = "E-Kur-Mah to Kur_Center", [
        AVDoor("E-Kur-Mah to Kur Inner CW", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("E-Kur-Mah to Kur Inner CE", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and (logicfunction.shortdrone(logic_info)(state) or logicfunction.grapple(logic_info)(state) or logicfunction.verylongwarp(logic_info)(state)))),
        AVDoor("E-Kur-Mah to Kur Inner CU", logic=lambda logic_info: (lambda state: (logicfunction.trenchcoat(logic_info)(state) and logicfunction.grapple(logic_info)(state)) or logicfunction.redcoat(logic_info)(state)))
    ]

    EKURMAH_TO_KUR_EAST = "E-Kur-Mah to Kur_East", [
        AVDoor("E-Kur-Mah to Kur Inner EC", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("E-Kur-Mah to Kur Inner EU", logic=lambda logic_info: (lambda state: ((logicfunction.trenchcoat(logic_info)(state) or logicfunction.shortdrone(logic_info)(state)) and logicfunction.grapple(logic_info)(state)) or (logicfunction.longwarp(logic_info)(state) and logicfunction.shortdrone(logic_info)(state)) or logicfunction.longdrone(logic_info)(state) or logicfunction.dronefly(logic_info)(state))),
        AVDoor("E-Kur-Mah to Kur Inner EB", logic=lambda logic_info: (lambda state: logicfunction.sudrankey(logic_info)(state)))
    ]

    EKURMAH_TO_KUR_UPPER = "E-Kur-Mah to Kur_Upper", [
        AVDoor("E-Kur-Mah to Kur Up Door", Orientation.Up),
        AVDoor("E-Kur-Mah to Kur Inner UE", logic=lambda logic_info: (lambda state: logicfunction.shortdrone(logic_info)(state))),
        AVDoor("E-Kur-Mah to Kur Inner UW", logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("E-Kur-Mah to Kur Inner UC", logic=lambda logic_info: (lambda state: logicfunction.redcoat(logic_info)(state)))
    ]

    EKURMAH_TO_KUR_LOWER = "E-Kur-Mah to Kur_Lower", [
        AVDoor("E-Kur-Mah to Kur Right Door", Orientation.Right),
        AVDoor("E-Kur-Mah to Kur Inner BE", logic=lambda logic_info: (lambda state: logicfunction.sudrankey(logic_info)(state) and (logicfunction.longwarp(logic_info)(state) or logicfunction.shortdrone(logic_info)(state))))
    ]

    ARCADE_ATTIC = "Arcade Attic", [
        AVDoor("Arcade Attic Down Door", Orientation.Down, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state))),
        AVDoor("Arcade Attic Up Door", Orientation.Up, logic=lambda logic_info: (lambda state: logicfunction.trenchcoat(logic_info)(state) and (logicfunction.longwarp(logic_info)(state) or logicfunction.grapple(logic_info)(state) or logicfunction.shortdrone(logic_info)(state)))),
    ]

    TRANSITION_ROOM = "Transition Room", [
        AVDoor("Transition Room Down Door", Orientation.Down),
        AVDoor("Transition Room Right Door", Orientation.Right)
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
    AVConnection(AVDoorID(AVRegion.URUKU_MAIN, 1), AVDoorID(AVRegion.URUKU_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.FILTRATION_CENTER, 0), AVDoorID(AVRegion.FILTRATION_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.FILTRATION_CENTER, 1), AVDoorID(AVRegion.FILTRATION_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.FILTRATION_CENTER, 2), AVDoorID(AVRegion.FILTRATION_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_LOWER, 5), AVDoorID(AVRegion.KUR_SHAFT_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_LOWER, 6), AVDoorID(AVRegion.KUR_SHAFT_TRANSIT, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_CENTER, 2), AVDoorID(AVRegion.KUR_SHAFT_TRANSIT, 1)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_TRANSIT, 2), AVDoorID(AVRegion.KUR_SHAFT_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_UPPER, 2), AVDoorID(AVRegion.KUR_SHAFT_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.ADDRESS_DISRUPTOR2_MAIN, 1), AVDoorID(AVRegion.ADDRESS_DISRUPTOR2_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.ADDRESS_DISRUPTOR2_WEST, 1), AVDoorID(AVRegion.ADDRESS_DISRUPTOR2_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.CAVERN_ACCESS_MAIN, 2), AVDoorID(AVRegion.CAVERN_ACCESS_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.HIGH_JUMP_ACCESS_UPPER, 1), AVDoorID(AVRegion.HIGH_JUMP_ACCESS_LOWER, 1)),
    AVConnection(AVDoorID(AVRegion.HIGH_JUMP_ROOM_MAIN, 1), AVDoorID(AVRegion.HIGH_JUMP_ROOM_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_UPPER, 3), AVDoorID(AVRegion.ORACA_ROOM_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_UPPER, 4), AVDoorID(AVRegion.ORACA_ROOM_LOWEREAST, 1)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_UPPER, 5), AVDoorID(AVRegion.ORACA_ROOM_LOWERWEST, 1)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_UPPER, 6), AVDoorID(AVRegion.ORACA_ROOM_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_UPPER, 2), AVDoorID(AVRegion.SLUG, 1), False),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_LOWER_LOWER, 2), AVDoorID(AVRegion.LEFT_LEG_SHAFT_LOWER_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_LOWER_UPPER, 1), AVDoorID(AVRegion.LEFT_LEG_SHAFT_TRANSIT, 0)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_TRANSIT, 1), AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_LOWER, 2)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_LOWER, 3), AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_CENTER, 0)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_CENTER, 1), AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_CENTER, 2), AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_SAVE_1_LOWER, 2), AVDoorID(AVRegion.UKKINNA_SAVE_1_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_SAVE_1_UPPER, 2), AVDoorID(AVRegion.INFECTION_SEQUENCE, 0)),
    AVConnection(AVDoorID(AVRegion.RIGHT_LEG_BOTTOM_SHAFT_WEST, 1), AVDoorID(AVRegion.RIGHT_LEG_BOTTOM_SHAFT_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.RIGHT_LEG_BOTTOM_SHAFT_WEST, 2), AVDoorID(AVRegion.RIGHT_LEG_BOTTOM_SHAFT_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.RIGHT_LEG_BOTTOM_SHAFT_CENTER, 2), AVDoorID(AVRegion.RIGHT_LEG_BOTTOM_SHAFT_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_TO_INDI_WEST, 1), AVDoorID(AVRegion.UKKINNA_TO_INDI_EAST, 2)),
    AVConnection(AVDoorID(AVRegion.ENTRANCE_TO_MADNESS_LOWER, 1), AVDoorID(AVRegion.ENTRANCE_TO_MADNESS_UPPER, 2)),
    AVConnection(AVDoorID(AVRegion.ENTRANCE_TO_MADNESS_SECRET, 1), AVDoorID(AVRegion.ENTRANCE_TO_MADNESS_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_HIDDEN_ITEM, 1), AVDoorID(AVRegion.SLUG, 2), False),
    AVConnection(AVDoorID(AVRegion.SHAFT_OF_LAUGHING_FACES_LOWER, 1), AVDoorID(AVRegion.SHAFT_OF_LAUGHING_FACES_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.SHAFT_OF_LAUGHING_FACES_UPPER, 2), AVDoorID(AVRegion.SHAFT_OF_LAUGHING_FACES_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.VISION_LOWER, 2), AVDoorID(AVRegion.VISION_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.ATHETOS_FOYER2_LOWER, 2), AVDoorID(AVRegion.ATHETOS_FOYER2_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.BIOFLUX_SHAFT1_LOWER, 1), AVDoorID(AVRegion.BIOFLUX_SHAFT1_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.RED_GOO_ROOM_LOWER, 1), AVDoorID(AVRegion.RED_GOO_ROOM_UPPER, 2)),
    AVConnection(AVDoorID(AVRegion.BLUE_AND_PURPLE_CORRIDOR_EAST, 2), AVDoorID(AVRegion.BLUE_AND_PURPLE_CORRIDOR_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.ATHETOS_FOYER_SHAFT_LOWER, 1), AVDoorID(AVRegion.ATHETOS_FOYER_SHAFT_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.ATHETOS_FOYER_SHAFT_CENTER, 2), AVDoorID(AVRegion.ATHETOS_FOYER_SHAFT_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_TO_MARURU_LOWER, 2), AVDoorID(AVRegion.UKKINNA_TO_MARURU_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_UKKINNA_WEST, 1), AVDoorID(AVRegion.EDIN_TO_UKKINNA_CENTER, 0)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_UKKINNA_CENTER, 2), AVDoorID(AVRegion.EDIN_TO_UKKINNA_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_UKKINNA_CENTER, 1), AVDoorID(AVRegion.EDIN_TO_UKKINNA_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_INDI_MAIN, 3), AVDoorID(AVRegion.EDIN_TO_INDI_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.HANGAR_BASEMENT_ENTRANCE_WEST, 1), AVDoorID(AVRegion.HANGAR_BASEMENT_ENTRANCE_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.HANGAR_BASEMENT_ENTRANCE_WEST, 2), AVDoorID(AVRegion.HANGAR_BASEMENT_ENTRANCE_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.HANGAR_BASEMENT_ENTRANCE_EAST, 2), AVDoorID(AVRegion.HANGAR_BASEMENT_ENTRANCE_UPPER, 2)),
    AVConnection(AVDoorID(AVRegion.WESTERN_HANGAR_ENTRANCE_LOWER, 1), AVDoorID(AVRegion.WESTERN_HANGAR_ENTRANCE_CENTER, 0)),
    AVConnection(AVDoorID(AVRegion.WESTERN_HANGAR_ENTRANCE_CENTER, 1), AVDoorID(AVRegion.WESTERN_HANGAR_ENTRANCE_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.HANGAR_EAST, 1), AVDoorID(AVRegion.HANGAR_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.HANGAR_EAST, 2), AVDoorID(AVRegion.HANGAR_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_KUR_EAST, 1), AVDoorID(AVRegion.EDIN_TO_KUR_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_KUR_EAST, 2), AVDoorID(AVRegion.EDIN_TO_KUR_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL1_LOWER, 3), AVDoorID(AVRegion.WEST_TOWER_LEVEL1_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL3_LOWER, 1), AVDoorID(AVRegion.WEST_TOWER_LEVEL3_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL3_EAST, 1), AVDoorID(AVRegion.WEST_TOWER_LEVEL3_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL3_UPPER, 2), AVDoorID(AVRegion.WEST_TOWER_LEVEL3_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.DRONE_TELEPORT_ROOM_UPPER, 1), AVDoorID(AVRegion.DRONE_TELEPORT_ROOM_LOWER, 1)),
    AVConnection(AVDoorID(AVRegion.FOOTHILLS_WEST, 1), AVDoorID(AVRegion.FOOTHILLS_MAIN, 0)),
    AVConnection(AVDoorID(AVRegion.FOOTHILLS_EAST, 1), AVDoorID(AVRegion.FOOTHILLS_MAIN, 1)),
    AVConnection(AVDoorID(AVRegion.FOOTHILLS_SECRET, 1), AVDoorID(AVRegion.FOOTHILLS_MAIN, 2)),
    AVConnection(AVDoorID(AVRegion.FOOTHILLS_UPPER, 1), AVDoorID(AVRegion.FOOTHILLS_MAIN, 3)),
    AVConnection(AVDoorID(AVRegion.FOOTHILLS_UPPER, 2), AVDoorID(AVRegion.FOOTHILLS_WEST, 2), False),
    AVConnection(AVDoorID(AVRegion.FOOTHILLS_UPPER, 3), AVDoorID(AVRegion.FOOTHILLS_SECRET, 2), False),
    AVConnection(AVDoorID(AVRegion.GIRTAB_FOYER_LOWER, 1), AVDoorID(AVRegion.GIRTAB_FOYER_UPPER, 2)),
    AVConnection(AVDoorID(AVRegion.MAINTENANCE_ENTRANCE_LOWER, 1), AVDoorID(AVRegion.MAINTENANCE_ENTRANCE_UPPER, 2)),
    AVConnection(AVDoorID(AVRegion.SECRET_KUR_TO_EKURMAH_WEST, 2), AVDoorID(AVRegion.SECRET_KUR_TO_EKURMAH_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_BACK_LOWER, 1), AVDoorID(AVRegion.MOUNTAIN_BACK_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_BACK_LOWER, 2), AVDoorID(AVRegion.MOUNTAIN_BACK_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_BACK_WEST, 2), AVDoorID(AVRegion.MOUNTAIN_BACK_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_BACK_UPPER, 1), AVDoorID(AVRegion.MOUNTAIN_BACK_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.SECRET_LAIR_RUINS_LOWER, 1), AVDoorID(AVRegion.SECRET_LAIR_RUINS_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.SECRET_LAIR_RUINS_EAST, 2), AVDoorID(AVRegion.SECRET_LAIR_RUINS_WEST, 1)),
    AVConnection(AVDoorID(AVRegion.DRONE_ROOM_WEST, 1), AVDoorID(AVRegion.DRONE_ROOM_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.DRONE_ROOM_WEST, 2), AVDoorID(AVRegion.DRONE_ROOM_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.DRONE_ROOM_LOWER, 1), AVDoorID(AVRegion.DRONE_ROOM_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.DRONE_ROOM_LOWER, 2), AVDoorID(AVRegion.DRONE_ROOM_CENTER, 0)),
    AVConnection(AVDoorID(AVRegion.DRONE_ROOM_CENTER, 2), AVDoorID(AVRegion.DRONE_ROOM_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_LOWER, 2), AVDoorID(AVRegion.MOUNTAIN_SLOPE_MAIN, 1)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_LOWER, 3), AVDoorID(AVRegion.MOUNTAIN_SLOPE_EAST, 2)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_UPPER, 2), AVDoorID(AVRegion.MOUNTAIN_SLOPE_LOWER, 4), False),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_MAIN, 0), AVDoorID(AVRegion.MOUNTAIN_SLOPE_SECRET, 1)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_MAIN, 2), AVDoorID(AVRegion.MOUNTAIN_SLOPE_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_MAIN, 3), AVDoorID(AVRegion.MOUNTAIN_SLOPE_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_MAIN, 4), AVDoorID(AVRegion.MOUNTAIN_SLOPE_ITEM, 1), False),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_UPPER, 3), AVDoorID(AVRegion.MOUNTAIN_SLOPE_ITEM, 0), False),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_LOWERWEST, 1), AVDoorID(AVRegion.ICECRAGS_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_LOWERWEST, 2), AVDoorID(AVRegion.ICECRAGS_LOWEREAST, 0)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_WEST, 1), AVDoorID(AVRegion.ICECRAGS_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_WEST, 2), AVDoorID(AVRegion.ICECRAGS_CENTER, 1)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_WEST, 3), AVDoorID(AVRegion.ICECRAGS_UPPERWEST, 0)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_WEST, 4), AVDoorID(AVRegion.ICECRAGS_SECRETWEST, 1)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_LOWEREAST, 1), AVDoorID(AVRegion.ICECRAGS_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_LOWEREAST, 2), AVDoorID(AVRegion.ICECRAGS_SECRETEAST, 0)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_EAST, 2), AVDoorID(AVRegion.ICECRAGS_CENTER, 0)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_SECRETEAST, 1), AVDoorID(AVRegion.ICECRAGS_SECRETLOWER, 1)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_UPPER, 2), AVDoorID(AVRegion.ICECRAGS_UPPEREAST, 0)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_CENTER, 2), AVDoorID(AVRegion.ICECRAGS_UPPEREAST, 1)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_UPPEREAST, 2), AVDoorID(AVRegion.ICECRAGS_UPPERWEST, 1)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_UPPERWEST, 2), AVDoorID(AVRegion.ICECRAGS_SECRETUPPER, 1)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_SECRETUPPER, 0), AVDoorID(AVRegion.ICECRAGS_SECRETWEST, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_TO_EKURMAH_WEST, 2), AVDoorID(AVRegion.KUR_TO_EKURMAH_EAST, 1)),
    AVConnection(AVDoorID(AVRegion.EKURMAH_TO_KUR_WEST, 1), AVDoorID(AVRegion.EKURMAH_TO_KUR_CENTER, 0)),
    AVConnection(AVDoorID(AVRegion.EKURMAH_TO_KUR_WEST, 2), AVDoorID(AVRegion.EKURMAH_TO_KUR_UPPER, 2)),
    AVConnection(AVDoorID(AVRegion.EKURMAH_TO_KUR_CENTER, 1), AVDoorID(AVRegion.EKURMAH_TO_KUR_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.EKURMAH_TO_KUR_CENTER, 2), AVDoorID(AVRegion.EKURMAH_TO_KUR_UPPER, 3)),
    AVConnection(AVDoorID(AVRegion.EKURMAH_TO_KUR_EAST, 1), AVDoorID(AVRegion.EKURMAH_TO_KUR_UPPER, 1)),
    AVConnection(AVDoorID(AVRegion.EKURMAH_TO_KUR_EAST, 2), AVDoorID(AVRegion.EKURMAH_TO_KUR_LOWER, 1))
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
    AVConnection(AVDoorID(AVRegion.FILTRATION_UPPER, 0), AVDoorID(AVRegion.URUKU_UPPER, 0)),
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
    AVConnection(AVDoorID(AVRegion.HIGH_JUMP_ROOM_SECRET, 0), AVDoorID(AVRegion.SECRET_PASSAGE_TO_TETHERED_CHARGE, 1)),
    AVConnection(AVDoorID(AVRegion.ERIBU_TO_INDI_EAST, 0), AVDoorID(AVRegion.INDI_TO_ERIBU, 0)),
    AVConnection(AVDoorID(AVRegion.ABSU_TO_INDI_UPPER, 0), AVDoorID(AVRegion.INDI_TO_ABSU, 0)),
    AVConnection(AVDoorID(AVRegion.ZI_TO_INDI, 0), AVDoorID(AVRegion.INDI_TO_ZI, 0)),
    AVConnection(AVDoorID(AVRegion.INDI_TO_EDIN, 2), AVDoorID(AVRegion.INDI_SAVE, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_CENTER, 0), AVDoorID(AVRegion.INDI_TO_KUR, 0)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_EAST, 0), AVDoorID(AVRegion.INDI_TO_KUR, 1)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_UPPER, 0), AVDoorID(AVRegion.INDI_TO_EDIN, 1)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_UPPER, 1), AVDoorID(AVRegion.INDI_TO_UKKINNA, 1)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_LOWEREAST, 0), AVDoorID(AVRegion.INDI_TO_ZI, 1)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_LOWERWEST, 0), AVDoorID(AVRegion.INDI_TO_ABSU, 1)),
    AVConnection(AVDoorID(AVRegion.ORACA_ROOM_WEST, 0), AVDoorID(AVRegion.INDI_TO_ERIBU, 1)),
    AVConnection(AVDoorID(AVRegion.ERIBU_TO_UKKINNA, 1), AVDoorID(AVRegion.UKKINNA_TO_ERIBU, 0)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_LOWER_LOWER, 0), AVDoorID(AVRegion.UKKINNA_TO_ERIBU, 1)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_SECRET, 0), AVDoorID(AVRegion.OPHELIAS_ATTIC, 0)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_LOWER, 0), AVDoorID(AVRegion.OPHELIA, 0)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_LOWER, 1), AVDoorID(AVRegion.UKKINNA_SAVE_3, 0)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_UPPER_UPPER, 0), AVDoorID(AVRegion.VISON_EXIT, 0)),
    AVConnection(AVDoorID(AVRegion.LEFT_LEG_SHAFT_LOWER_LOWER, 1), AVDoorID(AVRegion.FEETCONNECTOR, 0)),
    AVConnection(AVDoorID(AVRegion.FEETCONNECTOR, 1), AVDoorID(AVRegion.RIGHT_LEG_BOTTOM_SHAFT_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_SAVE_1_LOWER, 0), AVDoorID(AVRegion.RIGHT_LEG_BOTTOM_SHAFT_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_SAVE_1_UPPER, 0), AVDoorID(AVRegion.RIGHT_LEG_BOTTOM_SHAFT_CENTER, 0)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_SAVE_1_LOWER, 1), AVDoorID(AVRegion.UKKINNA_TO_INDI_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.INDI_TO_UKKINNA, 0), AVDoorID(AVRegion.UKKINNA_TO_INDI_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_TO_INDI_EAST, 1), AVDoorID(AVRegion.UKKINNA_TO_EDIN, 1)),
    AVConnection(AVDoorID(AVRegion.RIGHT_LEG_BOTTOM_SHAFT_UPPER, 0), AVDoorID(AVRegion.MUDROOM_OF_NEUROSIS, 0)),
    AVConnection(AVDoorID(AVRegion.MUDROOM_OF_NEUROSIS, 1), AVDoorID(AVRegion.ENTRANCE_TO_MADNESS_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.ENTRANCE_TO_MADNESS_SECRET, 0), AVDoorID(AVRegion.UKKINNA_HIDDEN_ITEM, 0)),
    AVConnection(AVDoorID(AVRegion.ENTRANCE_TO_MADNESS_UPPER, 0), AVDoorID(AVRegion.FOYER_OF_INSANITY, 0)),
    AVConnection(AVDoorID(AVRegion.FOYER_OF_INSANITY, 1), AVDoorID(AVRegion.TRENCHCOAT_CHAMBER_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.FOYER_OF_INSANITY, 2), AVDoorID(AVRegion.SHAFT_OF_LAUGHING_FACES_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.SHAFT_OF_LAUGHING_FACES_SECRET, 0), AVDoorID(AVRegion.TRENCHCOAT_CHAMBER_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.SHAFT_OF_LAUGHING_FACES_UPPER, 0), AVDoorID(AVRegion.CORRIDOR_OF_PSYCHOSIS, 0)),
    AVConnection(AVDoorID(AVRegion.CORRIDOR_OF_PSYCHOSIS, 1), AVDoorID(AVRegion.LIVING_ROOM_OF_ILLUSION, 0)),
    AVConnection(AVDoorID(AVRegion.LIVING_ROOM_OF_ILLUSION, 1), AVDoorID(AVRegion.GUEST_ROOM_OF_MENTAL_ILLNESS, 0)),
    AVConnection(AVDoorID(AVRegion.GUEST_ROOM_OF_MENTAL_ILLNESS, 1), AVDoorID(AVRegion.VISION_FOYER, 0)),
    AVConnection(AVDoorID(AVRegion.VISION_FOYER, 1), AVDoorID(AVRegion.UKKINNA_SAVE_2, 0)),
    AVConnection(AVDoorID(AVRegion.VISION_FOYER, 2), AVDoorID(AVRegion.VISION_LOWER, 1)),
    AVConnection(AVDoorID(AVRegion.VISION_LOWER, 0), AVDoorID(AVRegion.UKKINNA_TO_MARURU_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_TO_MARURU_LOWER, 1), AVDoorID(AVRegion.VISON_EXIT, 1)),
    AVConnection(AVDoorID(AVRegion.MARURU_TO_UKKINNA, 0), AVDoorID(AVRegion.UKKINNA_TO_MARURU_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.MARURU_TO_UKKINNA, 1), AVDoorID(AVRegion.ATHETOS_FOYER1, 0)),
    AVConnection(AVDoorID(AVRegion.ATHETOS_FOYER1, 1), AVDoorID(AVRegion.ATHETOS_FOYER2_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.ATHETOS_FOYER2_UPPER, 0), AVDoorID(AVRegion.MARURU_SAVE1, 0)),
    AVConnection(AVDoorID(AVRegion.ATHETOS_FOYER2_LOWER, 1), AVDoorID(AVRegion.ATHETOS_FOYER3, 0)),
    AVConnection(AVDoorID(AVRegion.ATHETOS_FOYER3, 1), AVDoorID(AVRegion.SENTINEL_SHAFT, 0)),
    AVConnection(AVDoorID(AVRegion.BIOFLUX_SHAFT1_LOWER, 0), AVDoorID(AVRegion.SENTINEL_SHAFT, 1)),
    AVConnection(AVDoorID(AVRegion.BIOFLUX_SHAFT1_UPPER, 0), AVDoorID(AVRegion.BIOFLUX_SHAFT2, 0)),
    AVConnection(AVDoorID(AVRegion.BIOFLUX_SHAFT2, 1), AVDoorID(AVRegion.BIOFLUX2_SECRET, 0)),  # exempt from room rando?
    AVConnection(AVDoorID(AVRegion.BIOFLUX_SHAFT2, 2), AVDoorID(AVRegion.RED_GOO_ROOM_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.RED_GOO_ROOM_UPPER, 1), AVDoorID(AVRegion.MARURU_SAVE2, 0)),
    AVConnection(AVDoorID(AVRegion.RED_GOO_ROOM_UPPER, 0), AVDoorID(AVRegion.HYBRID_ROOM, 0)),
    AVConnection(AVDoorID(AVRegion.HYBRID_ROOM, 1), AVDoorID(AVRegion.ORANGE_NICKNACKS, 0)),
    AVConnection(AVDoorID(AVRegion.ORANGE_NICKNACKS, 1), AVDoorID(AVRegion.XEDUR_HUL, 0)),
    AVConnection(AVDoorID(AVRegion.XEDUR_HUL, 1), AVDoorID(AVRegion.BLUE_AND_PURPLE_CORRIDOR_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.BLUE_AND_PURPLE_CORRIDOR_WEST, 0), AVDoorID(AVRegion.HIDDEN_AREA_ENTRANCE, 0)),
    AVConnection(AVDoorID(AVRegion.HIDDEN_AREA_ENTRANCE, 1), AVDoorID(AVRegion.HIDDEN_AREA_SHAFT, 0)),
    AVConnection(AVDoorID(AVRegion.HIDDEN_AREA_SHAFT, 1), AVDoorID(AVRegion.SECRET_ITEM, 0)),
    AVConnection(AVDoorID(AVRegion.BLUE_AND_PURPLE_CORRIDOR_EAST, 1), AVDoorID(AVRegion.ATHETOS_FOYER_SHAFT_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.ATHETOS_FOYER_SHAFT_CENTER, 0), AVDoorID(AVRegion.MARURU_SAVE3, 0)),
    AVConnection(AVDoorID(AVRegion.ATHETOS_FOYER_SHAFT_UPPER, 0), AVDoorID(AVRegion.ATHETOS, 0)),
    AVConnection(AVDoorID(AVRegion.PEAK, 0), AVDoorID(AVRegion.VISION_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.UKKINNA_TO_EDIN, 0), AVDoorID(AVRegion.EDIN_TO_UKKINNA_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_UKKINNA_EAST, 0), AVDoorID(AVRegion.EDIN_TO_INDI_MAIN, 2)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_INDI_SECRET, 0), AVDoorID(AVRegion.EDIN_TO_UKKINNA_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_INDI_MAIN, 0), AVDoorID(AVRegion.INDI_TO_EDIN, 0)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_INDI_MAIN, 1), AVDoorID(AVRegion.HANGAR_BASEMENT_ENTRANCE_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.HANGAR_BASEMENT_ENTRANCE_UPPER, 0), AVDoorID(AVRegion.WESTERN_HANGAR_ENTRANCE_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.WESTERN_HANGAR_ENTRANCE_UPPER, 0), AVDoorID(AVRegion.HANGAR_FOYER, 0)),
    AVConnection(AVDoorID(AVRegion.HANGAR_FOYER, 1), AVDoorID(AVRegion.EDIN_SAVE1, 0)),
    AVConnection(AVDoorID(AVRegion.EDIN_SAVE1, 1), AVDoorID(AVRegion.DEFORMED_TRACE_BOSS_FOYER, 0)),
    AVConnection(AVDoorID(AVRegion.DEFORMED_TRACE_BOSS_FOYER, 1), AVDoorID(AVRegion.DEFORMED_TRACE_BOSS_ROOM, 0)),
    AVConnection(AVDoorID(AVRegion.DEFORMED_TRACE_BOSS_ROOM, 1), AVDoorID(AVRegion.HANGAR_ACCESS, 0)),
    AVConnection(AVDoorID(AVRegion.HANGAR_ACCESS, 1), AVDoorID(AVRegion.HANGAR_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.HANGAR_BASEMENT_ENTRANCE_EAST, 0), AVDoorID(AVRegion.HANGAR_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.HANGAR_EAST, 0), AVDoorID(AVRegion.EDIN_TO_KUR_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_KUR_EAST, 0), AVDoorID(AVRegion.KUR_SHAFT_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_KUR_UPPER, 0), AVDoorID(AVRegion.HANGAR_ATTIC, 0)),
    AVConnection(AVDoorID(AVRegion.EDIN_TO_UKKINNA_UPPER, 0), AVDoorID(AVRegion.WEST_TOWER_LEVEL1_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL1_LOWER, 1), AVDoorID(AVRegion.EDIN_SAVE2, 0)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL1_LOWER, 2), AVDoorID(AVRegion.LEVEL1_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL1_UPPER, 0), AVDoorID(AVRegion.WEST_TOWER_LEVEL2, 0)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL2, 1), AVDoorID(AVRegion.DistortionFieldRoom, 0)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL2, 2), AVDoorID(AVRegion.WEST_TOWER_LEVEL3_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL3_UPPER, 0), AVDoorID(AVRegion.SPITBUG_BOSS_FOYER, 0)),
    AVConnection(AVDoorID(AVRegion.SPITBUG_BOSS_FOYER, 1), AVDoorID(AVRegion.EDIN_SAVE3, 0)),
    AVConnection(AVDoorID(AVRegion.SPITBUG_BOSS_FOYER, 2), AVDoorID(AVRegion.SPITBUG_BOSS_ROOM, 0)),
    AVConnection(AVDoorID(AVRegion.SPITBUG_BOSS_ROOM, 1), AVDoorID(AVRegion.DRONE_TELEPORT_ROOM_UPPER, 0)),
    AVConnection(AVDoorID(AVRegion.WEST_TOWER_LEVEL3_WEST, 0), AVDoorID(AVRegion.DRONE_TELEPORT_ROOM_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_SHAFT_UPPER, 0), AVDoorID(AVRegion.FOOTHILLS_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.FOOTHILLS_SECRET, 0), AVDoorID(AVRegion.THORN_MAZE, 0)),
    AVConnection(AVDoorID(AVRegion.THORN_MAZE, 1), AVDoorID(AVRegion.THORN_MAZE_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.FOOTHILLS_EAST, 0), AVDoorID(AVRegion.LAIR_ENTRANCE, 0)),
    AVConnection(AVDoorID(AVRegion.LAIR_ENTRANCE, 1), AVDoorID(AVRegion.ELEVATED_POOLS, 0)),
    AVConnection(AVDoorID(AVRegion.ELEVATED_POOLS, 1), AVDoorID(AVRegion.LAIR_VESTIBULE, 0)),
    AVConnection(AVDoorID(AVRegion.LAIR_VESTIBULE, 1), AVDoorID(AVRegion.GIRTAB_FOYER_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.GIRTAB_FOYER_UPPER, 0), AVDoorID(AVRegion.KUR_SAVE2, 0)),
    AVConnection(AVDoorID(AVRegion.GIRTAB_FOYER_UPPER, 1), AVDoorID(AVRegion.GIRTAB, 0)),
    AVConnection(AVDoorID(AVRegion.GIRTAB, 1), AVDoorID(AVRegion.KATRAHASKA, 0)),
    AVConnection(AVDoorID(AVRegion.KATRAHASKA, 1), AVDoorID(AVRegion.MAINTENANCE_ENTRANCE_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.MAINTENANCE_ENTRANCE_UPPER, 0), AVDoorID(AVRegion.DRONE_CONTROL, 0)),
    AVConnection(AVDoorID(AVRegion.DRONE_CONTROL, 1), AVDoorID(AVRegion.SECRET_KUR_TO_EKURMAH_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.SECRET_KUR_TO_EKURMAH_WEST, 1), AVDoorID(AVRegion.MOUNTAIN_BACK_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_BACK_WEST, 0), AVDoorID(AVRegion.KUR_SAVE5, 0)),
    AVConnection(AVDoorID(AVRegion.SECRET_LAIR_RUINS_LOWER, 0), AVDoorID(AVRegion.GIRTAB, 2)),
    AVConnection(AVDoorID(AVRegion.MAINTENANCE_ENTRANCE_UPPER, 1), AVDoorID(AVRegion.SECRET_LAIR_RUINS_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.SECRET_LAIR_RUINS_WEST, 0), AVDoorID(AVRegion.SECRET_LAIR_SHORTCUT, 0)),
    AVConnection(AVDoorID(AVRegion.SECRET_LAIR_SHORTCUT, 1), AVDoorID(AVRegion.DRONE_ROOM_EAST, 0)),
    AVConnection(AVDoorID(AVRegion.FOOTHILLS_UPPER, 0), AVDoorID(AVRegion.MOUNTAIN_SLOPE_LOWER, 0)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_EAST, 0), AVDoorID(AVRegion.DRONE_ROOM_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_SECRET, 0), AVDoorID(AVRegion.DRONE_ROOM_SECRET, 0)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_LOWER, 1), AVDoorID(AVRegion.KUR_SAVE3, 0)),
    AVConnection(AVDoorID(AVRegion.MOUNTAIN_SLOPE_UPPER, 0), AVDoorID(AVRegion.ICECRAGS_LOWERWEST, 0)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_SECRETLOWER, 0), AVDoorID(AVRegion.CAVERN_OF_THE_ROSES1, 0)),
    AVConnection(AVDoorID(AVRegion.CAVERN_OF_THE_ROSES1, 1), AVDoorID(AVRegion.FLORAL_CLOSET, 0)),
    AVConnection(AVDoorID(AVRegion.FLORAL_CLOSET, 1), AVDoorID(AVRegion.HIDDEN_STALAGMITE, 0)),
    AVConnection(AVDoorID(AVRegion.HIDDEN_STALAGMITE, 1), AVDoorID(AVRegion.SUSPENSION_OF_THE_GILL, 0)),
    AVConnection(AVDoorID(AVRegion.SUSPENSION_OF_THE_GILL, 1), AVDoorID(AVRegion.REFLECTOR_ROOM, 0)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_UPPER, 1), AVDoorID(AVRegion.IMPROVED_LAUNCH_ROOM, 0)),
    AVConnection(AVDoorID(AVRegion.ICECRAGS_UPPER, 0), AVDoorID(AVRegion.KUR_TO_EKURMAH_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_TO_EKURMAH_WEST, 1), AVDoorID(AVRegion.KUR_SAVE4, 0)),
    AVConnection(AVDoorID(AVRegion.KUR_TO_EKURMAH_EAST, 0), AVDoorID(AVRegion.EKURMAH_TO_KUR_WEST, 0)),
    AVConnection(AVDoorID(AVRegion.EKURMAH_TO_KUR_UPPER, 0), AVDoorID(AVRegion.ARCADE_ATTIC, 0)),
    AVConnection(AVDoorID(AVRegion.ARCADE_ATTIC, 1), AVDoorID(AVRegion.TRANSITION_ROOM, 0))
]

region_name_to_connection: Dict[str, List[AVConnection]] = {}
for connection in axiom_verge_connections:
    region_name_to_connection.setdefault(connection.enter.region.title, []).append(connection)
    if connection.twoway:
        region_name_to_connection.setdefault(connection.exit.region.title, []).append(
            AVConnection(connection.exit, connection.enter)
        )


def create_connections(avconnection_list: List[AVConnection], world: "AVWorld"):
    logic_info = LogicInfo(world.player, world.options.drone_fly, world.options.room_rando)
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
        entrance.access_rule = source_avregion.doors[avconnection.enter.index].logic(logic_info)
        source_region.exits.append(entrance)
        entrance.connect(target_region)
        print(f"creating connection from {avconnection.enter.region.title} to {target_avregion.title}")
        if avconnection.twoway:
            entrance = Entrance(world.player, target_avregion.doors[avconnection.exit.index].name, target_region)
            entrance.access_rule = target_avregion.doors[avconnection.exit.index].logic(logic_info)
            target_region.exits.append(entrance)
            entrance.connect(source_region)
            print(f"creating back connection from {avconnection.exit.region.title} to {avconnection.enter.region.title}")


def create_region(world: "AVWorld") -> None:
    created_regions = {}
    logic_info = LogicInfo(world.player, world.options.drone_fly, world.options.room_rando)
    for avregion in AVRegion:
        region = Region(avregion.title, world.player, world.multiworld)
        created_regions[region.name] = region
        region.add_locations({location.name: location.code for location in axiom_verge_locations.get(region.name, {})})
        for loc in region.locations:
            loc.access_rule = av_locations_unpacked[loc.name].logic(logic_info)
            print(f"adding logic to {loc.name}")
        world.locations.extend(region.locations)
        world.multiworld.regions.append(region)
    create_connections(axiom_verge_connections, world)
    if not world.options.room_rando:
        create_connections(axiom_verge_doors, world)
