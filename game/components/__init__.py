from dataclasses import dataclass as component
from dataclasses import field


@component
class HeroIdentity:
    first_name: str = ''
    family_name: str = ''


@component
class ActorIdentity:
    race: str = ''
    sex: str = ''


@component
class Stats:
    body: int = 3
    speed: int = 3

    mind: int = 3
    soul: int = 3

    faith: int = 3
    luck: int = 3


@component
class Location:
    location: str = 'home'


@component
class Destination:
    destination: str = ''
    distance: int = 0


@component
class CombatStats:
    physical_attack: int = 0
    physical_defense: int = 0

    mental_attack: int = 0
    mental_defense: int = 0

    spiritual_attack: int = 0
    spiritual_defense: int = 0

    health: int = 0

    def __iadd__(self, other):
        self.physical_attack += other.physical_attack
        self.physical_defense += other.physical_defense
        self.mental_attack += other.mental_attack
        self.mental_defense += other.mental_defense
        self.spiritual_attack += other.spiritual_attack
        self.spiritual_defense += other.spiritual_defense
        self.health += other.health


@component
class Profession:
    name: str = ''
    level: int = 1
    experience: int = 0
    experience_per_level: int = 100

    physical_attack_increase: str = 'average'
    physical_defense_increase: str = 'average'

    mental_attack_increase: str = 'average'
    mental_defense_increase: str = 'average'

    spiritual_attack_increase: str = 'average'
    spiritual_defense_increase: str = 'average'

    health_increase: str = 'average'


@component
class Target:
    t_id: int = 0
    t_combat_stats: CombatStats = None
    t_hero_identity: HeroIdentity = None


@component
class AgroTarget:
    id: int = None      # id = entity id
    hate: int = 0


@component
class Agro:
    hate_table: list = field(default_factory=list)


@component
class CombatMessages:
    messages: list = field(default_factory=list)


@component
class Weapon:
    name: str = None
    min_damage: int = 0
    max_damage: int = 0


@component
class Armor:
    name: str = None
    damage_reduction: int = 0


@component
class CombatInventory:
    main_weapon: Weapon = None
    secondary_weapon: Weapon = None

    shield: Armor = None
    head_armor: Armor = None
    torso_armor: Armor = None
    arm_armor: Armor = None
    leg_armor: Armor = None
    foot_armor: Armor = None

    @property
    def damage_reduction(self):
        return (
            self.shield.damage_reduction if self.shield else 0
            + self.head_armor.damage_reduction if self.head_armor else 0
            + self.torso_armor.damage_reduction if self.torso_armor else 0
            + self.arm_armor.damage_reduction if self.arm_armor else 0
            + self.leg_armor.damage_reduction if self.leg_armor else 0
            + self.foot_armor.damage_reduction if self.foot_armor else 0
        )

    @property
    def damage(self):
        return (
            self.main_weapon.min_damage if self.main_weapon else 0
            + self.secondary_weapon.min_damage if self.secondary_weapon else 0,
            self.main_weapon.max_damage if self.main_weapon else 0
            + self.secondary_weapon.max_damage if self.secondary_weapon else 0

        )
