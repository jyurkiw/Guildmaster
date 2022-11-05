import os.path

import esper
from rich import print

from game.lib import CurveRoller
from game.components import CombatStats, Target, HeroIdentity, CombatMessages, CombatInventory


class AttackResolutionSystem(esper.Processor):
    def __init__(self, combat_roller=None):
        """Initiate the combat system.
        """
        if combat_roller:
            self.combat_roller = combat_roller
        else:
            self.combat_roller = CurveRoller('data/attack_roll_curve.yaml', autocast=int)

        self.damage_dealt = []

    def process(self):
        for a_id, (acs, tar, cs, ci) in self.world.get_components(CombatStats, Target, CombatMessages, CombatInventory):
            t_id = tar.t_id
            tcs = self.world.component_for_entity(t_id, CombatStats)
            tci = self.world.component_for_entity(t_id, CombatInventory)
            dmg_mul = self.roll_damage_multiplier(acs, tcs)

            min_dmg, max_dmg = ci.damage
            reduction = tci.damage_reduction
            dmg = round(max(((max_dmg - min_dmg) * dmg_mul) + min_dmg, min_dmg))

            # handle things like passive abilities, skills...anything that can modify damage

            # apply damage
            tcs.health -= dmg
            cs.messages.append((tar.t_hero_identity, dmg))

    def roll_damage_multiplier(self, acs, tcs):
        """Roll an attack and return damage.

        :param acs: Attacker combat stats.
        :param tcs: Target combat stats.
        :return: Damage dealt by attacker
        """
        return round(next(self.combat_roller) / 150 + ((acs.physical_attack - tcs.physical_defense) / 100), 2)


class CombatRecordSystem(esper.Processor):
    def process(self):
        for a_id, (cm, hid) in self.world.get_components(CombatMessages, HeroIdentity):
            for t_ident, dmg in cm.messages:
                print(f'{t_ident.first_name} {t_ident.family_name} took {dmg} damage!')
            cm.messages.clear()

