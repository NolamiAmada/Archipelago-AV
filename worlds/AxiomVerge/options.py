from dataclasses import dataclass
import Options


class ProgressiveCoats(Options.DefaultOnToggle):
    """Whether Coats should behave as in Vanilla or as Progressive Items
    (Modified Labcoat -> Trenchcoat -> Redcoat)"""
    display_name = "Progressive Coats"


class ProgressiveGlitch(Options.DefaultOnToggle):
    """Whether Glitch Items should behave as in Vanilla or as Progressive Items
    (Address Disruptor -> Address Disruptor 2 -> Address Bomb)"""
    display_name = "Progressive Glitch"


class ProgressiveDrone(Options.Toggle):
    """Whether Drone Items should behave as Vanilla or as Progressive Items
    (Remote Drone -> Enhanced Drone Launch -> Drone Teleport)"""
    display_name = "Progressive Drone"


class GrappleClips(Options.Choice):
    """Whether Grapple Clips should be considered for logic
    standard: only require clips within the room
    advanced: grappling into unloaded rooms can be required"""
    display_name = "Grapple Clips"
    option_off = 0
    option_standard = 1
    option_advanced = 2
    alias_false = 0
    default = 0


class RocketJumps(Options.Choice):
    """Whether Rocket Jumps should be considered for logic
    standard: simple vertical rocket jumps in logic
    advanced: all rocket jumps, including disco hell"""
    display_name = "Rocket Jumps"
    option_off = 0
    option_standard = 1
    option_advanced = 2
    alias_false = 0
    default = 0


class SecretWorlds(Options.Choice):
    """Generates Secret Worlds and the items contained within"""
    display_name = "Secret Worlds"
    option_off = 0
    option_minors_only = 1
    option_on = 2
    alias_true = 2
    alias_false = 0
    default = 0


@dataclass
class AVOptions(Options.PerGameCommonOptions):
    progressive_coats: ProgressiveCoats
    progressive_glitch: ProgressiveGlitch
    progressive_drone: ProgressiveDrone
    grapple_clips: GrappleClips
    rocket_jumps: RocketJumps
    secret_worlds: SecretWorlds
