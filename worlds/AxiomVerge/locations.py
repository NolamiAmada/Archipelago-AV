from BaseClasses import Location
from typing import NamedTuple


class AVLocation(NamedTuple):
    name: str
    code: int


BASE_ID = 332200000
axiom_verge_locations = {
    "Disruptor Room": [
        AVLocation("Eribu - Starter Weapon", BASE_ID+0)
    ]
}

av_locations_unpacked = {}
for locationgroup in axiom_verge_locations.values():
    for location in locationgroup:
        assert location.name not in av_locations_unpacked
        av_locations_unpacked[location.name] = location.code
