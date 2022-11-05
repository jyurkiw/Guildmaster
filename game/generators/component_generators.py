import esper

from game.lib import RandomEntryRoller, CurveRoller
from game.components import *
from random import choice, choices, randint


class HeroIdentityGenerator(object):
    def __init__(self):
        """Generate HeroIdentity and ActorIdentity components."""
        self.ident = RandomEntryRoller("data/HeroIdentity.csv")
        self.races = RandomEntryRoller("data/Races.csv")

    def __next__(self):
        sex = choice(["male", "female"])
        race = next(self.races)["race"]

        first_name = next(self.ident)[
            "male_first_name" if sex == "male" else "female_first_name"
        ]
        family_name = next(self.ident)["family_name"]

        return ActorIdentity(race=race, sex=sex), HeroIdentity(
            first_name=first_name, family_name=family_name
        )


class StatsGenerator(object):
    def __init__(self, base_stats=2, bonus_curve_file_name='data/average_bonus_stats_roll_curve.yaml'):
        """Generate a random stats component.
        All stats are set to the base_stats value, and then a random
        number of additional stat points are added between the min and
        max bonus_stats values.
        """
        self.base_stats = base_stats
        self.bonus_roller = CurveRoller(bonus_curve_file_name, autocast=int)

    def __next__(self):
        s_line = ["body", "speed", "mind", "soul", "faith", "luck"]
        s = {k: self.base_stats for k in s_line}
        for sb in choices(
            s_line, k=next(self.bonus_roller)
        ):
            s[sb] += 1
        return Stats(**s)


class ProfessionGenerator(object):
    def __init__(self):
        """Generate a random profession component."""
        self.professions = RandomEntryRoller("data/professions.csv")

    def __next__(self):
        prof = Profession(**next(self.professions))
        prof.level = int(prof.level)
        prof.experience = int(prof.experience)
        prof.experience_per_level = int(prof.experience_per_level)

        return prof


class CombatStatsGenerator(object):
    def __init__(self):
        """Generate combat stats based on stats and profession."""
        self.combat_stats_rollers = {
            "lesser": CurveRoller("data/lesser_stats_roll_curve.yaml", autocast=int),
            "average": CurveRoller("data/average_stats_roll_curve.yaml", autocast=int),
            "greater": CurveRoller("data/greater_stats_roll_curve.yaml", autocast=int),
        }

        self._profession = None
        self._stats = None

    def profession(self, p):
        self._profession = p
        return self

    def stats(self, s):
        self._stats = s
        return self

    def __next__(self):
        if not self._profession or not self._stats:
            raise Exception('Profession and Stats components must be set. Call with "next(gen.profession(p).stats(s))"')
        cs = CombatStats()

        # Initial Rolls
        cs.physical_attack = next(
            self.combat_stats_rollers[self._profession.physical_attack_increase]
        )
        cs.physical_defense = next(
            self.combat_stats_rollers[self._profession.physical_defense_increase]
        )

        cs.mental_attack = next(
            self.combat_stats_rollers[self._profession.mental_attack_increase]
        )
        cs.mental_defense = next(
            self.combat_stats_rollers[self._profession.mental_defense_increase]
        )

        cs.spiritual_attack = next(
            self.combat_stats_rollers[self._profession.spiritual_attack_increase]
        )
        cs.spiritual_defense = next(
            self.combat_stats_rollers[self._profession.spiritual_defense_increase]
        )
        cs.health = next(
            self.combat_stats_rollers[self._profession.health_increase]
        )

        # Stat bonuses
        cs.physical_attack += (
            (max(self._stats.body, self._stats.speed) * 2)
            + self._stats.mind
            + self._stats.faith
        )
        cs.physical_defense += (
            self._stats.body
            + self._stats.speed
            + (max(self._stats.faith, self._stats.luck) * 2)
        )

        cs.mental_attack += (
            (max(self._stats.mind, self._stats.faith) * 2)
            + self._stats.body
            + self._stats.luck
        )
        cs.mental_defense += (
            self._stats.mind
            + self._stats.faith
            + max(self._stats.speed, self._stats.luck)
            + self._stats.soul
        )

        cs.spiritual_attack += (
            (max(self._stats.faith, self._stats.soul) * 2)
            + self._stats.body
            + self._stats.mind
        )
        cs.spiritual_defense += (
            (self._stats.soul * 2)
            + self._stats.faith
            + max(self._stats.body, self._stats.luck)
        )
        cs.health += (
            (self._stats.body * 2)
            + (self._stats.soul * 2)
        )

        self._profession = None
        self._stats = None

        return cs


class HeroGenerator(object):
    def __init__(self, world: esper.World, base_stats=1, max_level=5):
        """Create a full hero in the passed world.

        :param world: An esper.World object
        :param base_stats: base value of stats
        :param min_bonus_stats: minimum bonus stat points
        :param max_bonus_stats: maximum bonus stat points
        """
        self.world = world
        self.base_stats = base_stats
        self.max_level = max_level

        self.hero_identity_generator = HeroIdentityGenerator()
        self.profession_generator = ProfessionGenerator()
        self.stats_generator = StatsGenerator(base_stats=self.base_stats)
        self.combat_stats_generator = CombatStatsGenerator()

    def __next__(self):
        actor_identity, hero_identity = next(self.hero_identity_generator)
        profession = next(self.profession_generator)
        stats = next(self.stats_generator)
        combat_stats = next(self.combat_stats_generator.stats(stats).profession(profession))

        return self.world.create_entity(
            hero_identity,
            actor_identity,
            profession,
            stats,
            combat_stats,
            CombatInventory(),
            Target(),
            CombatMessages()
        )

    def add_experience(self, c_id: int, experience_award: int):
        """Add experience to an entity.

        :param c_id: The hero's entity id in the world
        :param experience_award: The experience to award
        :return: True if the entity can have a level-up applied
        """
        profession = self.world.component_for_entity(c_id, Profession)
        profession.experience += experience_award

        return profession.experience >= profession.experience_per_level and profession.level >= self.max_level

    def apply_level_up(self, c_id: int):
        """Apply a level-up to an entity with stats and a profession.

        :param c_id: The entity id.
        :param world: The esper world object.
        :param gen: A CombatStatsGenerator object.
        :return: None
        """
        profession = self.world.component_for_entity(c_id, Profession)

        if profession.experience < profession.experience_per_level or profession.level >= self.max_level:
            return False

        stats = self.world.component_for_entity(c_id, Stats)
        combat_stats = self.world.component_for_entity(c_id, CombatStats)

        level_stats = next(self.combat_stats_generator.stats(stats).profession(profession))

        combat_stats += level_stats
        profession.level += 1
        profession.experience -= profession.experience_per_level

        return True
