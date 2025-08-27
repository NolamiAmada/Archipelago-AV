from .items import axiom_verge_items, item_name_groups
from BaseClasses import CollectionState, Location
from typing import TYPE_CHECKING, NamedTuple, Callable

if TYPE_CHECKING:
    from . import AVWorld


class LogicInfo(NamedTuple):
    player: int
    yamldronefly: bool
    yamlroomrando: bool


def anycoat(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _anycoat(state: CollectionState) -> bool:
        return state.has("Modified Lab Coat", logic_info.player) or state.has("Trenchcoat", logic_info.player) or state.has("Red Coat", logic_info.player) or state.has("Progressive Coat", logic_info.player)
    return _anycoat


def trenchcoat(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _trenchcoat(state: CollectionState) -> bool:
        return state.has("Trenchcoat", logic_info.player) or state.has("Red Coat", logic_info.player) or state.has("Progressive Coat", logic_info.player, count=2)
    return _trenchcoat


def redcoat(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _redcoat(state: CollectionState) -> bool:
        return state.has("Red Coat", logic_info.player) or state.has("Progressive Coat", logic_info.player, count=3)
    return _redcoat


def drone(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _drone(state: CollectionState) -> bool:
        return state.has("Remote Drone", logic_info.player) or state.has("Progressive Drone", logic_info.player)
    return _drone


def dronelaunch(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _dronelaunch(state: CollectionState) -> bool:
        return (state.has("Enhanced Drone Launch", logic_info.player) and state.has("Remote Drone", logic_info.player)) or state.has("Progressive Drone", logic_info.player, count=2)
    return _dronelaunch


def dronetp(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _dronetp(state: CollectionState) -> bool:
        return state.has("Drone Teleport", logic_info.player) or state.has("Progressive Drone", logic_info.player, count=3)
    return _dronetp


def anyglitch(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _anyglitch(state: CollectionState) -> bool:
        return state.has("Address Disruptor", logic_info.player) or state.has("Address Disruptor 2", logic_info.player) or state.has("Address Bomb", logic_info.player) or state.has("Progressive Glitch", logic_info.player)
    return _anyglitch


def glitch2(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _glitch2(state: CollectionState) -> bool:
        return state.has("Address Disruptor 2", logic_info.player) or state.has("Address Bomb", logic_info.player) or state.has("Progressive Glitch", logic_info.player, count=2)
    return _glitch2


def glitchnades(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _glitchnades(state: CollectionState) -> bool:
        return state.has("Address Bomb", logic_info.player) or state.has("Progressive Glitch", logic_info.player, count=3)
    return _glitchnades


def drill(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _drill(state: CollectionState) -> bool:
        return justdrill(logic_info)(state) or drone(logic_info)(state) or redcoat(logic_info)(state)
    return _drill


def breakblock(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _breakblock(state: CollectionState) -> bool:
        return anyweapon(logic_info)(state) or drill(logic_info)(state) or redcoat(logic_info)(state)
    return _breakblock


def longwarp(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _longwarp(state: CollectionState) -> bool:
        return fielddisruptor(logic_info)(state) and trenchcoat(logic_info)(state) or redcoat(logic_info)(state)
    return _longwarp


def verylongwarp(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _verylongwarp(state: CollectionState) -> bool:
        return fielddisruptor(logic_info)(state) and redcoat(logic_info)(state)
    return _verylongwarp


def shortdrone(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _shortdrone(state: CollectionState) -> bool:
        return drone(logic_info)(state) and dronetp(logic_info)(state)
    return _shortdrone


def longdrone(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _longdrone(state: CollectionState) -> bool:
        return shortdrone(logic_info)(state) and dronelaunch(logic_info)(state)
    return _longdrone


def anyup(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _anyup(state: CollectionState) -> bool:
        return anyupnoceiling(logic_info)(state) or grapple(logic_info)(state)
    return _anyup


def anyupnoceiling(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _anyupnoceiling(state: CollectionState) -> bool:
        return fielddisruptor(logic_info)(state) or trenchcoat(logic_info)(state) or shortdrone(logic_info)(state)
    return _anyupnoceiling


def anyupnodrone(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _anyupnodrone(state: CollectionState) -> bool:
        return fielddisruptor(logic_info)(state) or trenchcoat(logic_info)(state) or grapple(logic_info)(state)
    return _anyupnodrone


def sevenblockup(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _sevenblockup(state: CollectionState) -> bool:
        return grapple(logic_info)(state) or trenchcoat(logic_info)(state) or shortdrone(logic_info)(state)
    return _sevenblockup


def tempup(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _tempup(state: CollectionState) -> bool:
        return anyup(logic_info)(state)
    return _tempup


def dronefly(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _dronefly(state: CollectionState) -> bool:
        return shortdrone(logic_info)(state) and (state.has("Address Disruptor", logic_info.player) or state.has("Address Disruptor 2", logic_info.player) or state.has("Progressive Glitch", logic_info.player) or justdrill(logic_info)(state)) and logic_info.yamldronefly
    return _dronefly


def dronequest(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _dronequest(state: CollectionState) -> bool:
        return drone(logic_info)(state) and ((not logic_info.yamlroomrando) or dronetp(logic_info)(state))
    return _dronequest


def infectiondone(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _infectiondone(state: CollectionState) -> bool:
        return state.has("Infection Cleared", logic_info.player)
    return _infectiondone


def passcodetool(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _passcodetool(state: CollectionState) -> bool:
        return state.has("Passcode Tool", logic_info.player)
    return _passcodetool


def grapple(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _grapple(state: CollectionState) -> bool:
        return state.has("Grapple", logic_info.player)
    return _grapple


def fielddisruptor(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _fielddisruptor(state: CollectionState) -> bool:
        return state.has("Field Disruptor", logic_info.player)
    return _fielddisruptor


def justdrill(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _justdrill(state: CollectionState) -> bool:
        return state.has("Laser Drill", logic_info.player)
    return _justdrill


def anyweapon(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _anyweapon(state: CollectionState) -> bool:
        return state.has_group("Weapon", logic_info.player)
    return _anyweapon


def fatbeam(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _fatbeam(state: CollectionState) -> bool:
        return state.has("Fat Beam", logic_info.player)
    return _fatbeam


def scissorbeam(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _scissorbeam(state: CollectionState) -> bool:
        return state.has("Scissor Beam", logic_info.player)
    return _scissorbeam


def shortpierce(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _shortpierce(state: CollectionState) -> bool:
        return state.has_group("ShortPierce", logic_info.player)
    return _shortpierce


def longpierce(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _longpierce(state: CollectionState) -> bool:
        return state.has_group("LongPierce", logic_info.player)
    return _longpierce


def longweapon(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _longweapon(state: CollectionState) -> bool:
        return state.has_group("LongWeapon", logic_info.player)
    return _longweapon


def rangeweapon(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _rangeweapon(state: CollectionState) -> bool:
        return state.has_group("RangeWeapon", logic_info.player)
    return _rangeweapon


def cornercut(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _cornercut(state: CollectionState) -> bool:
        return state.has_group("CornerCut", logic_info.player)
    return _cornercut


def girtabweapon(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _girtabweapon(state: CollectionState) -> bool:
        return state.has_group("GirTabWeapon", logic_info.player)
    return _girtabweapon


def sudrankey(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _sudrankey(state: CollectionState) -> bool:
        return state.has("Sudran Key", logic_info.player) or redcoat(logic_info)(state)
    return _sudrankey


def no(logic_info: LogicInfo) -> Callable[[CollectionState], bool]:
    def _no(state: CollectionState) -> bool:
        return False
    return _no
