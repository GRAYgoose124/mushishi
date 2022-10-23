import json
from discord.ext.commands import Cog


class Raid(Cog):
    pass


class Gear:
    def __init__(self, geartype: str, base_stat: str):
        self.type = geartype
        self.faction = None
        self.star = None
        self.level = None
        self.stats = {'HP': None,
                      'DEF': None,
                      'ATK': None,
                      'SPD': None,
                      'CRATE': None,
                      'CDMG': None,
                      'ACC': None,
                      'RES': None}
        self.base_stat = base_stat

    def setstats(self, hp, deff, atk, spd, crate, cdmg, acc, res):
            stats = [hp, deff, atk, spd, crate, cdmg, acc, res]
            for stat, k in zip(stats, self.stats.keys()):
                self.stats[k] = stat
            return self

    def __repr__(self):
        return f'{self.stats}'

class Aura:
    def __init__(self, auratype, location, stats):
        self.type = auratype
        self.location = location
        self.stats = stats

    def __repr__(self):
        return f'Aura | type: {self.type}, location: {self.location}, stats: {self.stats}'


class Skill:
    type_effects = {'ability1': ['AoEAttack', 'ExtraHit', 'MultipleAttack'],
              'aura': ['Accuracy', 'Attack', 'CriticalRate', 'Defense', 'HealthPoints', 'Resistance', 'Speed'],
              'buff': ['AllyProtection', 'BlockDamage', 'BlockDebuff', 'ContinuousHeal',
                       'Counterattack', 'IncreaseAttack', 'IncreaseCritical', 'IncreaseDefense',
                       'IncreaseSpeed', 'ReflectDamage', 'Reviveon', 'Shield', 'Unkillable', 'Veil'],
              'debuff': ['BlockBuff', 'BlockCooldown', 'BlockRevive', 'Bomb', 'DecreaseAccuracy', 'DecreaseAttack',
                         'DecreaseDefense', 'DecreaseSpeed', 'Fear', 'Freeze', 'HealReduction',
                         'HPBurn', 'Leech', 'Poison', 'Provoke', 'Sleep', 'SpreadDebuff', 'Stun', 'Weaken'],
              'instant': ['AllyJoin', 'DecreaseBuff', 'DecreaseMAX', 'DecreaseSkill',
                          'DecreaseTurn', 'EnemyMAX', 'EqualizeHP', 'ExchangeHP', 'ExtraTurn',
                          'Heal', 'IgnoreBlock', 'IgnoreDefense', 'IgnoreShield',
                          'IncreaseBuff', 'IncreaseDamage', 'IncreaseDebuff', 'IncreaseSkill',
                          'IncreaseTurn', 'PutSkill', 'RemoveBuff', 'RemoveDebuff', 'ResetSkill',
                          'Revive', 'SelfHeal', 'StealBuff'],
              'passive': ['PartnerSkill', 'UnlockSecret']}

    base_effects = ['DMG', 'duration', 'debuffchance', 'buffchance', 'boostmeteronkill', 'extracritchance']

    def __init__(self, name, base, effects, level, levels, cooldown):
        self.level = level
        self.levels = levels
        self.name = name
        self.base = base
        self.effects = effects
        self.stats = {'DMG': 1.00}
        self.cooldown = cooldown

        for stat, value in levels[:level-1]:
                if stat == 'DMG':
                    self.stats[stat] += value
                if stat == 'debuffchance':
                    for effect in self.effects:
                        if isinstance(effect, list):
                            for n, effect in enumerate(self.effects):
                                if effect[0] == 'Poison' or effect[0] == 'extracritchance':
                                    self.effects[n][1] += value
                if stat == 'cooldown':
                    self.cooldown += value
                                 
    def _use(self, source, target):
        remaining_hp = target.base_stats['HP'] - source.base_stats[self.base] * self.stats['DMG']
        for n, effect in enumerate(self.effects):
            if isinstance(effect, list):
                if effect[0] == 'boostmeteronkill':
                    if remaining_hp < 0:
                        source.turnmeter += effect[1]
        return

    def __repr__(self):
        return f'{self.name}'


class Champion:
    def __init__(self, name: str, faction, skills: [Skill], aura: Aura):
        self.name = name
        self.skills = skills
        self.aura = aura
        self.faction = faction
        self.level = 1
        self.rank = 1
        self.turnmeter = 0.0

        self.base_stats = {'HP': None,
                           'DEF': None,
                           'ATK': None,
                           'SPD': None,
                           'CRATE': None,
                           'CDMG': None,
                           'ACC': None,
                           'RES': None}

        self.gear = {'Weapon': None,
                     'Gauntlets': None,
                     'Helmet': None,
                     'Armor': None,
                     'Shield': None,
                     'Boots': None,
                     'Ring': None,
                     'Amulet': None,
                     'Banner': None}

        self.masteries = []

    def addgear(self, gear):
        self.gear[gear.type] = gear
        return self

    def addskill(self, skill):
        self.skills.append(skill)
        return self

    def rmskill(self, skill_name):
        del(self.skills[skill_name])

    def useskill(self, skill, target):
        remaining_hp =  self.skills[skill]._use(self, target)
        return remaining_hp

    def setstats(self, hp, deff, atk, spd, crate, cdmg, acc, res):
        stats = [hp, deff, atk, spd, crate, cdmg, acc, res]
        for stat, k in zip(stats, self.base_stats.keys()):
            self.base_stats[k] = stat
        return self
    
    def setlvl(self, level):
        if level > self.rank * 10:
            level = self.rank * 10
        self.level = level
        return self

    def setrank(self, rank):
        if rank > 6:
            rank = 6
        self.rank = rank
        return self

    def __repr__(self):
        return f'level: {self.level} rank: {self.rank}\ngear: {self.gear}\nskills: {self.skills}\naura: {self.aura}\nmasteries: {self.masteries}\nfaction: {self.faction}'

class Arena:
    def __init__(self):
        pass


if __name__ == '__main__':
    raid_data = None

    levels = [('DMG', .05),
              ('debuffchance', .10),
              ('DMG', .05),
              ('debuffchance', .10),
              ('DMG', .10)]
    # ['Poison', chance, debuff, duration]
    skill_effects = [['Poison', .80, .025, 2]]
    dark_bolt = Skill('Dark Bolt', 'ATK', skill_effects, 6, levels, 1)

    levels = [('DMG', .05),
              ('DMG', .05),
              ('DMG', .05),
              ('DMG', .05)]     
    # ['extracritchance', chance], ['boostmeteronkill', fillpercent]
    skill_effects = ['AoEAttack', ['extracritchance', .15], ['boostmeteronkill', .25]]
    acid_rain = Skill('Acid Rain', 'ATK', skill_effects, 5, levels, 3)

    levels =  [('DMG', .10),
              ('buffdebuffchance', .05),
              ('DMG', .10),
              ('buffdebuffchance', .05),
              ('cooldown', -1)]
    skill_effects = [['MultipleAttack', 4], ['Poison', .40, .05, 2]]
    disintegrate = Skill('Disintegrate', 'ATK', skill_effects, 6, levels, 4)

    aura = Aura('allyhp', 'all', 1.15)

    kael = Champion('kael', 'Dark Elves', [dark_bolt, acid_rain, disintegrate], aura)
    kael.setrank(6).setlvl(60).setstats(5000, 900, 1200, 120, 50, 65, 75, 50)
 
    gear_stats = []
    kael.addgear(Gear('Helmet', 'HP'))

    print(kael)