import sc2
from sc2.bot_ai import BotAI, Race
from sc2.data import *
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.ids.upgrade_id import UpgradeId
from sc2.ids.buff_id import *
from sc2.unit import *
from sc2.units import *
from sc2.position import Point2
from sc2.player import Bot, Computer
from sc2.constants import UnitTypeId
import random
import time


    
class CompetitiveBot(BotAI):
    NAME: str = "gasless"

    RACE: Race = Race.Zerg
    
    latest_enemy_units = False
    
    closestdronesptag = False
    closestdronerwtag = False
    closestdronee1tag = False
    closestdronee2tag = False
    closestdronee2 = False

    overlord1 = False
    overlord2 = False
    overlord3 = False
    overlord4 = False
    overlord5 = False
    overlord6 = False
    overlord7 = False
    overlord8 = False
    overlord9 = False
    overlord10 = False
    overlord11 = False
    overlord12 = False
    overlord13 = False
    overlord14 = False
    overlord15 = False
    overlord16 = False
    overlord17 = False
    overlord18 = False
    overlord19 = False
    overlord20 = False
    overlord1tag = False
    overlord2tag = False
    overlord3tag = False
    overlord4tag = False
    overlord5tag = False
    overlord6tag = False
    overlord7tag = False
    overlord8tag = False
    overlord9tag = False
    overlord10tag = False
    overlord11tag = False
    overlord12tag = False
    overlord13tag = False
    overlord14tag = False
    overlord15tag = False
    overlord16tag = False
    overlord17tag = False
    overlord18tag = False
    overlord19tag = False
    overlord20tag = False
    
    async def on_start(self):
        """
        This code runs once at the start of the game
        Do things here before the game starts
        """
        print("Game started")
        self.larva.random.train(UnitTypeId.DRONE)
        global possible_base_locations
        possible_base_locations = sorted(self.expansion_locations.keys(), key=lambda p: p.distance_to(self.start_location), reverse=True)
        global scouts
        scouts = {UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}

        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(self.start_location, 2.5))
        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(possible_base_locations[1], -2.5), queue = True)
        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(self.start_location, 2.5), queue = True)
        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(possible_base_locations[1], -2.5), queue = True)
        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(self.start_location, 2.5), queue = True)
        self.units(UnitTypeId.OVERLORD).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(possible_base_locations[1], -35))
        self.overlord1tag = self.units(UnitTypeId.OVERLORD).closest_to(possible_base_locations[0]).tag
        self.overlord1 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord1tag)


    async def on_step(self, iteration: int):
        await self.distribute_workers()
        await self.build_workers()
        await self.build_overlords()
        await self.expand()
        await self.build_spawningpool()
        await self.build_zerglings()
        await self.build_gas()
        await self.attack()
        await self.build_roachwarren()
        await self.build_roaches()
        await self.build_queens()
        await self.queen_inject()
        await self.split_queens()
        await self.enemy_units_check()
        

    async def distribute_workers(self):
        if not self.mineral_field or not self.workers or not self.townhalls.ready:
            return
        idle_workers = self.workers.idle
        bases = self.townhalls.ready
        gas_buildings = self.gas_buildings.ready
        spare_mineral_workers = False

        for base in bases:
            local_minerals_tags = {mineral.tag for mineral in self.mineral_field if mineral.distance_to(base) <= 8}
            local_mineral_workers = self.workers.filter(lambda unit: unit.order_target in local_minerals_tags or (unit.is_carrying_minerals and unit.order_target == base.tag))
#worker balance
            if base.surplus_harvesters > 0:
                del local_mineral_workers[:16]
                spare_mineral_workers = local_mineral_workers
            if base.surplus_harvesters < 0 and spare_mineral_workers:
                for worker in spare_mineral_workers:
                    worker.gather(self.mineral_field.closest_to(base))
                if base.surplus_harvesters > -1:
                    del spare_mineral_workers[:]
#idle worker                    
            for worker in self.workers.idle:
                if base.surplus_harvesters < 0:
                    worker.gather(self.mineral_field.closest_to(base))
                elif base.surplus_harvesters >= 0:
                    worker.gather(self.mineral_field.closest_to(base))
#fill gas first
            for gas in gas_buildings:
                if gas.surplus_harvesters < 0:
                    print(self.time_formatted, "need more workers")
                    for worker in local_mineral_workers.take(abs(gas.surplus_harvesters)):
                        print(self.time_formatted, gas.surplus_harvesters)
                        print(self.time_formatted, worker)
                        worker.gather(gas)
                        print(self.time_formatted, gas.surplus_harvesters)
                        print(self.time_formatted, "gathering gas")
                if gas.surplus_harvesters > 0:
                    local_gas_workers = self.workers.filter(lambda unit:  unit.order_target == gas.tag or (unit.is_carrying_vespene and unit.order_target == gas.tag))
                    for worker in local_gas_workers.take(abs(gas.surplus_harvesters)):
                        print(self.time_formatted, gas.surplus_harvesters)
                        print(self.time_formatted, worker)
                        worker.gather(self.mineral_field.closest_to(base))
                    print(self.time_formatted, "Too many gas workers here")
                

    async def build_workers(self):
        if not self.larva:
            return
        if not self.units(UnitTypeId.DRONE):
            return
        larva = self.larva.random
        if (
            self.can_afford(UnitTypeId.DRONE)
            and self.structures(UnitTypeId.HATCHERY).amount < 2
            and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 16
            ):
            if (
                self.supply_left > self.structures(UnitTypeId.HATCHERY).amount
                or self.already_pending(UnitTypeId.OVERLORD) >= 1
                and not self.supply_left == 0
                ):
                larva.train(UnitTypeId.DRONE)
                print(self.time_formatted, "16 hatch")
#After drone scout determine enemy build and react
        if self.time > 45:
#if macro
            if (
                self.enemy_units(UnitTypeId.DRONE).amount > 14
                or self.enemy_units(UnitTypeId.SCV).amount > 14
                or self.enemy_units(UnitTypeId.PROBE).amount > 14
                ):
                print(self.time_formatted, "Enemy is playing macro")
                if (
                    self.supply_left > self.structures(UnitTypeId.HATCHERY).amount
                    or self.already_pending(UnitTypeId.OVERLORD) >= 1
                    and not self.supply_left == 0
                    ):
                    if (
                        self.can_afford(UnitTypeId.DRONE)
                        and self.structures(UnitTypeId.HATCHERY).amount > 1
                        and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 17
                        and self.supply_left > self.structures(UnitTypeId.HATCHERY).amount
                        ):
                        larva.train(UnitTypeId.DRONE)
                        print(self.time_formatted, "17 pool")
                if (
                    not self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
                    and self.can_afford(UnitTypeId.DRONE)
                    and self.structures(UnitTypeId.HATCHERY).amount > 1
                    and self.structures(UnitTypeId.SPAWNINGPOOL).amount > 0
                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 19
                    ):
                    larva.train(UnitTypeId.DRONE)
                    print(self.time_formatted, "19 hatch")
                if (
                    self.can_afford(UnitTypeId.DRONE)
                    and self.structures(UnitTypeId.HATCHERY).amount > 2
                    and self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) > 1
                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (self.structures(UnitTypeId.HATCHERY).amount * 16) + (self.structures(UnitTypeId.EXTRACTOR).amount * 3)
                    and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
                    ):
                    if (
                        self.already_pending(UnitTypeId.ZERGLING) + self.units(UnitTypeId.ZERGLING).amount > 0
                        or self.enemy_structures(UnitTypeId.EXTRACTOR).amount < 1
                        and self.enemy_structures(UnitTypeId.REFINERY).amount < 1
                        and self.enemy_structures(UnitTypeId.ASSIMILATOR).amount < 1
                        ):
                        larva.train(UnitTypeId.DRONE)
                        print(self.time_formatted, "building enough drones to match base count")
#pre move drones
                if (
                    self.minerals > 200
                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 17
                    and not self.structures(UnitTypeId.HATCHERY).amount > 1
                    ):
                    if not self.closestdronee1tag:
                        self.closestdronee1tag = self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[14]).tag
                    if self.closestdronee1tag:
                        self.closestdronee1 = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronee1tag)
                        self.closestdronee1.move(possible_base_locations[14])
                    print(self.time_formatted, "16 hatch drone moving to new expansion location")
                if (
                    self.minerals > 150
                    and not self.structures(UnitTypeId.SPAWNINGPOOL)
                    and self.structures(UnitTypeId.HATCHERY).amount > 1
                    ):
                    if not self.closestdronesptag:
                        self.closestdronesptag = self.units(UnitTypeId.DRONE).closest_to(self.start_location.position.towards(possible_base_locations[0], -10)).tag
                    if self.closestdronesptag:
                        self.closestdronesp = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronesptag)
                        self.closestdronesp.move(self.start_location.position.towards(possible_base_locations[0], -10))
                        print(self.time_formatted, "17 pool drone moving to pool build location")
                if (
                    self.minerals > 100
                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) > 18
                    and not self.structures(UnitTypeId.HATCHERY).amount > 2
                    ):
                    if not self.closestdronee2tag:
                        self.closestdronee2tag = self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[13]).tag
                    if self.closestdronee2tag:
                        self.closestdronee2 = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronee2tag)
                        self.closestdronee2.move(possible_base_locations[13])
                        print(self.time_formatted, "19 hatch drone moving to new expansion location")
                    if self.closestdronee2:
                        if (
                            self.supply_left > self.structures(UnitTypeId.HATCHERY).amount
                            or self.already_pending(UnitTypeId.OVERLORD) >= 1
                            and not self.supply_left == 0
                            ):
                            if (
                                self.can_afford(UnitTypeId.DRONE)
                                and self.structures(UnitTypeId.HATCHERY).amount < 3
                                and self.enemy_structures(UnitTypeId.EXTRACTOR).amount < 1
                                and self.enemy_structures(UnitTypeId.REFINERY).amount < 1
                                and self.enemy_structures(UnitTypeId.ASSIMILATOR).amount < 1
                                and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 20
                                ):
                                larva.train(UnitTypeId.DRONE)
                                print(self.time_formatted, "19 hatch up to 20 drones")
#early aggression back to droning after ling scout if we overbuilt units
            if (
                self.supply_left > self.structures(UnitTypeId.HATCHERY).amount
                or self.already_pending(UnitTypeId.OVERLORD) >= 1
                and not self.supply_left == 0
                ):
                if (
                    self.can_afford(UnitTypeId.DRONE)
                    and self.time > 134
                    and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (self.structures(UnitTypeId.HATCHERY).amount * 16) + (self.structures(UnitTypeId.EXTRACTOR).amount * 3)
                    and self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount > self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount
                    ):
                    larva.train(UnitTypeId.DRONE)
                    print(self.time_formatted, "our combat units =", self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                    print(self.time_formatted, "enemy combat units =", self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                    print(self.time_formatted, "Switching from anti aggression to drones")

#if early aggression
            if (
                self.enemy_units(UnitTypeId.DRONE).amount < 15
                and self.enemy_units(UnitTypeId.SCV).amount < 15
                and self.enemy_units(UnitTypeId.PROBE).amount < 15
                ):
                if (
                    self.minerals > 150
                    and not self.structures(UnitTypeId.SPAWNINGPOOL)
                    ):
                    if not self.closestdronesptag:
                        self.closestdronesptag = self.units(UnitTypeId.DRONE).closest_to(self.start_location.position.towards(possible_base_locations[0], -10)).tag
                    if self.closestdronesptag:
                        self.closestdronesp = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronesptag)
                        self.closestdronesp.move(self.start_location.position.towards(possible_base_locations[0], -10))
                        print(self.time_formatted, "Emergency pool drone moving to pool build location")
                if (
                    self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) > 0
                    and self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) < 0.2
                    ):
                    larva.train(UnitTypeId.DRONE)
                    print(self.time_formatted, "Drone while emergency pool starts")
                if (
                    self.minerals > 100
                    and self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) > 0.95
                    and not self.structures(UnitTypeId.ROACHWARREN)
                    and not self.already_pending(UnitTypeId.ROACHWARREN)
                    and self.time < 120
                    ):
                    if (
                        self.enemy_structures(UnitTypeId.EXTRACTOR).amount > 0
                        or self.enemy_structures(UnitTypeId.REFINERY).amount > 0
                        or self.enemy_structures(UnitTypeId.ASSIMILATOR).amount > 0
                        ):
                        if (
                            self.enemy_units(UnitTypeId.DRONE).amount < 15
                            and self.enemy_units(UnitTypeId.SCV).amount < 15
                            and self.enemy_units(UnitTypeId.PROBE).amount < 15
                            ):
                            if not self.closestdronerwtag:
                                self.closestdronerwtag = self.units(UnitTypeId.DRONE).closest_to(self.start_location.position.towards(possible_base_locations[14], -10)).tag
                            if self.closestdronerwtag:
                                self.closestdronerw = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronerwtag)
                                self.closestdronerw.move(self.start_location.position.towards(possible_base_locations[14], -10))
                                print(self.time_formatted, "Emergency roach warren drone moving to roach warren location")

    async def build_overlords(self):
#overlordscout
        if (
            self.time > 179
            and self.time < 181
            ):
            print(self.time_formatted, "overlord scout 3min")
            if (
                self.enemy_structures(UnitTypeId.EXTRACTOR).amount < 1
                and self.enemy_structures(UnitTypeId.REFINERY).amount < 1
                and self.enemy_structures(UnitTypeId.ASSIMILATOR).amount < 1
                ):
                self.overlord1.move(possible_base_locations[0].position.towards(possible_base_locations[1], -4.5))
                self.overlord1.move(possible_base_locations[0].position.towards(possible_base_locations[1], -35), queue = True)
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -4.5))
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -24), queue = True)
                print(self.time_formatted, "Overlord scout initiated 3:00")
        if (
            self.time > 164
            and self.time < 166
            ):
            print(self.time_formatted, "overlord scout 2:45")
            if (
                self.enemy_structures(UnitTypeId.EXTRACTOR).amount > 0
                or self.enemy_structures(UnitTypeId.REFINERY).amount > 0
                or self.enemy_structures(UnitTypeId.ASSIMILATOR).amount > 0
                ):
                self.overlord1.move(possible_base_locations[0].position.towards(possible_base_locations[1], -4.5))
                self.overlord1.move(possible_base_locations[0].position.towards(possible_base_locations[1], -35), queue = True)
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -4.5))
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -24), queue = True)
                print(self.time_formatted, "Overlord scout initiated 2:45")
#position overlords
        if not self.units(UnitTypeId.OVERLORD):
            return

#overlord 1
        if self.overlord1tag:
            self.overlord1 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord1tag)
        if not self.overlord1 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord3:
            print(self.time_formatted, "overlord1 =", self.overlord1)
            self.overlord1tag = self.overlord3tag
            self.overlord1 = self.overlord3
            self.overlord3 = False
            print(self.time_formatted, "overlord1 replaced by overlord3")
            print(self.time_formatted, "overlord1 =", self.overlord1)
        if self.overlord1 and self.time > 210:
            self.overlord1.move(possible_base_locations[0].position.towards(possible_base_locations[1], -35))
            
#overlord 2
        if not self.overlord2 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord3:
            print(self.time_formatted, "overlord2 =", self.overlord2)
            self.overlord2tag = self.overlord3tag
            self.overlord2 = self.overlord3
            self.overlord3 = False
            print(self.time_formatted, "overlord2 replaced by overlord3")
            print(self.time_formatted, "overlord2 =", self.overlord2)
        if self.units(UnitTypeId.OVERLORD).amount == 2:
            self.overlord2tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord2tag:
            self.overlord2 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord2tag)
        if self.overlord2:
            if (
                self.enemy_structures(UnitTypeId.HATCHERY).amount > 1
                or self.enemy_structures(UnitTypeId.COMMANDCENTER).amount > 1
                or self.enemy_structures(UnitTypeId.NEXUS).amount > 1
                ):
                if (
                    self.units(UnitTypeId.OVERLORD).idle.closer_than(19, possible_base_locations[1].position)
                    ):
                    self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -24))
            if self.time < 60:
                    self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -10))
            if (
                self.enemy_structures(UnitTypeId.EXTRACTOR).amount > 0
                or self.enemy_structures(UnitTypeId.REFINERY).amount > 0
                or self.enemy_structures(UnitTypeId.ASSIMILATOR).amount > 0
                ):
                if self.time < 120:
                    self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -10))
            elif (
                self.enemy_structures(UnitTypeId.EXTRACTOR).amount < 1
                and self.enemy_structures(UnitTypeId.REFINERY).amount < 1
                and self.enemy_structures(UnitTypeId.ASSIMILATOR).amount < 1
                and self.time > 210
                ):
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -24))
                
#overlord 3        
        if not self.overlord3 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord4:
            print(self.time_formatted, "overlord3 =", self.overlord3)
            self.overlord3tag = self.overlord4tag
            self.overlord3 = self.overlord4
            self.overlord4 = False
            print(self.time_formatted, "overlord3 replaced by overlord4")
            print(self.time_formatted, "overlord3 =", self.overlord3)
        if self.units(UnitTypeId.OVERLORD).amount == 3:
            self.overlord3tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord3tag:
            self.overlord3 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord3tag)
        if self.overlord3:
            self.overlord3.move(possible_base_locations[1].position.towards(self.start_location, 40))
            
#overlord 4
        if not self.overlord4 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord5:
            print(self.time_formatted, "overlord4 =", self.overlord4)
            self.overlord4tag = self.overlord5tag
            self.overlord4 = self.overlord5
            self.overlord5 = False
            print(self.time_formatted, "overlord4 replaced by overlord5")
            print(self.time_formatted, "overlord4 =", self.overlord4)
        if self.units(UnitTypeId.OVERLORD).amount == 4:
            self.overlord4tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord4tag:
            self.overlord4 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord4tag)
        if self.overlord4:
            self.overlord4.move(possible_base_locations[2].position.towards(self.start_location, 10))
            
#overlord 5
        if not self.overlord5 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord6:
            print(self.time_formatted, "overlord4 =", self.overlord4)
            self.overlord5tag = self.overlord6tag
            self.overlord5 = self.overlord6
            self.overlord6 = False
            print(self.time_formatted, "overlord5 replaced by overlord6")
            print(self.time_formatted, "overlord5 =", self.overlord5)
        if self.units(UnitTypeId.OVERLORD).amount == 5:
            self.overlord5tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord5tag:
            self.overlord5 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord5tag)
        if self.overlord5:
            self.overlord5.move(possible_base_locations[3].position.towards(self.start_location, 10))

#overlord 6            
        if not self.overlord6 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord7:
            print(self.time_formatted, "overlord6 =", self.overlord6)
            self.overlord6tag = self.overlord7tag
            self.overlord6 = self.overlord7
            self.overlord7 = False
            print(self.time_formatted, "overlord6 replaced by overlord7")
            print(self.time_formatted, "overlord6 =", self.overlord6)
        if self.units(UnitTypeId.OVERLORD).amount == 6:
            self.overlord6tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord6tag:
            self.overlord6 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord6tag)
        if self.overlord6:
            self.overlord6.move(possible_base_locations[4].position.towards(self.start_location, 10))

#overlord 7            
        if not self.overlord7 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord8:
            self.overlord7tag = self.overlord8tag
            self.overlord7 = self.overlord8
            self.overlord8 = False
        if self.units(UnitTypeId.OVERLORD).amount == 7:
            self.overlord7tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord7tag:
            self.overlord7 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord7tag)
        if self.overlord7:
            self.overlord7.move(possible_base_locations[5].position.towards(self.start_location, 10))

#overlord 8            
        if not self.overlord8 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord9:
            self.overlord8tag = self.overlord9tag
            self.overlord8 = self.overlord9
            self.overlord9 = False
        if self.units(UnitTypeId.OVERLORD).amount == 8:
            self.overlord8tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord8tag:
            self.overlord8 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord8tag)
        if self.overlord8:
            self.overlord8.move(possible_base_locations[6].position.towards(self.start_location, 10))

#overlord 9            
        if not self.overlord9 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord10:
            self.overlord9tag = self.overlord10tag
            self.overlord9 = self.overlord10
            self.overlord10 = False
        if self.units(UnitTypeId.OVERLORD).amount == 9:
            self.overlord9tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord9tag:
            self.overlord9 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord9tag)
        if self.overlord9:
            self.overlord9.move(possible_base_locations[7].position.towards(self.start_location, 10))

#overlord 10            
        if not self.overlord10 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord11:
            self.overlord10tag = self.overlord11tag
            self.overlord10 = self.overlord11
            self.overlord11 = False
        if self.units(UnitTypeId.OVERLORD).amount == 10:
            self.overlord10tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord10tag:
            self.overlord10 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord10tag)
        if self.overlord10:
            self.overlord10.move(possible_base_locations[8].position.towards(self.start_location, 10))

#overlord 11            
        if not self.overlord11 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord12:
            self.overlord11tag = self.overlord12tag
            self.overlord11 = self.overlord12
            self.overlord12 = False
        if self.units(UnitTypeId.OVERLORD).amount == 11:
            self.overlord11tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord11tag:
            self.overlord11 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord11tag)
        if self.overlord11:
            self.overlord11.move(possible_base_locations[9].position.towards(self.start_location, 10))

#overlord 12            
        if not self.overlord12 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord13:
            self.overlord12tag = self.overlord13tag
            self.overlord12 = self.overlord13
            self.overlord13 = False
        if self.units(UnitTypeId.OVERLORD).amount == 12:
            self.overlord12tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord12tag:
            self.overlord12 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord12tag)
        if self.overlord12:
            self.overlord12.move(possible_base_locations[10].position.towards(self.start_location, 10))

#overlord 13            
        if not self.overlord13 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord14:
            self.overlord13tag = self.overlord14tag
            self.overlord13 = self.overlord14
            self.overlord14 = False
        if self.units(UnitTypeId.OVERLORD).amount == 13:
            self.overlord13tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord13tag:
            self.overlord13 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord13tag)
        if self.overlord13:
            self.overlord13.move(possible_base_locations[11].position.towards(self.start_location, 10))
            
#overlord 14            
        if not self.overlord14 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord15:
            self.overlord14tag = self.overlord15tag
            self.overlord14 = self.overlord15
            self.overlord15 = False
        if self.units(UnitTypeId.OVERLORD).amount == 14:
            self.overlord14tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord14tag:
            self.overlord14 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord14tag)
        if self.overlord14:
            self.overlord14.move(possible_base_locations[12].position.towards(self.start_location, 10))
            
#overlord 15            
        if not self.overlord15 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord16:
            self.overlord15tag = self.overlord16tag
            self.overlord15 = self.overlord16
            self.overlord16 = False
        if self.units(UnitTypeId.OVERLORD).amount == 15:
            self.overlord15tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord15tag:
            self.overlord15 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord15tag)
        if self.overlord15:
            self.overlord15.move(possible_base_locations[13].position.towards(self.start_location, 10))
            
#overlord 16            
        if not self.overlord16 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord17:
            self.overlord16tag = self.overlord17tag
            self.overlord16 = self.overlord17
            self.overlord17 = False
        if self.units(UnitTypeId.OVERLORD).amount == 16:
            self.overlord16tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord16tag:
            self.overlord16 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord16tag)
        if self.overlord16:
            self.overlord16.move(possible_base_locations[14].position.towards(self.start_location, 10))
            
#overlord 17            
        if not self.overlord17 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord18:
            self.overlord17tag = self.overlord18tag
            self.overlord17 = self.overlord18
            self.overlord18 = False
        if self.units(UnitTypeId.OVERLORD).amount == 17:
            self.overlord17tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord17tag:
            self.overlord17 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord17tag)
        if self.overlord17:
            self.overlord17.move(possible_base_locations[15].position.towards(self.start_location, 10))
            
#overlord 18            
        if not self.overlord18 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord19:
            self.overlord18tag = self.overlord19tag
            self.overlord18 = self.overlord19
            self.overlord19 = False
        if self.units(UnitTypeId.OVERLORD).amount == 18:
            self.overlord18tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord18tag:
            self.overlord18 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord18tag)
            
#overlord 19            
        if not self.overlord19 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord20:
            self.overlord19tag = self.overlord20tag
            self.overlord19 = self.overlord20
            self.overlord20 = False
        if self.units(UnitTypeId.OVERLORD).amount == 19:
            self.overlord19tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord19tag:
            self.overlord19 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord19tag)
            
#overlord 20            
        if self.units(UnitTypeId.OVERLORD).amount == 20:
            self.overlord20tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord20tag:
            self.overlord20 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord20tag)
    
#spawn more overlords
        if not self.larva:
            return
        larva = self.larva.random
        if self.supply_cap < 200:
            if (
                self.supply_left < self.structures(UnitTypeId.HATCHERY).amount + 1
                and self.already_pending(UnitTypeId.OVERLORD) < self.structures(UnitTypeId.HATCHERY).ready.amount
                and self.can_afford(UnitTypeId.OVERLORD)
                ):
                larva.train(UnitTypeId.OVERLORD)
            if (
                self.already_pending(UnitTypeId.ROACHWARREN)
                or self.structures(UnitTypeId.ROACHWARREN).ready
                ):
                if (
                    self.supply_left <= self.structures(UnitTypeId.HATCHERY).ready.amount * 5
                    and self.already_pending(UnitTypeId.OVERLORD) < self.structures(UnitTypeId.HATCHERY).ready.amount
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    larva.train(UnitTypeId.OVERLORD)
            if (
                self.structures(UnitTypeId.HATCHERY).amount > 2
                and self.supply_left < self.structures(UnitTypeId.HATCHERY).ready.amount + 3
                and self.already_pending(UnitTypeId.OVERLORD) < self.structures(UnitTypeId.HATCHERY).ready.amount
                ):
                larva.train(UnitTypeId.OVERLORD)
            if (
                self.time < 80
                and self.can_afford(UnitTypeId.OVERLORD)
                and self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) > 0
                and self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) < 0.5
                and self.supply_left < 5
                and not self.already_pending(UnitTypeId.OVERLORD)
                ):
                if (
                    self.enemy_units(UnitTypeId.DRONE).amount < 15
                    and self.enemy_units(UnitTypeId.SCV).amount < 15
                    and self.enemy_units(UnitTypeId.PROBE).amount < 15
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                
            
    async def expand(self):
        if not self.units(UnitTypeId.DRONE):
            return
#if early gas aggression, don't expand, if non gas aggression, expand
        if (
            self.time > 45
            and self.time < 120
            and self.enemy_structures(UnitTypeId.EXTRACTOR).amount < 1
            and self.enemy_structures(UnitTypeId.REFINERY).amount < 1
            and self.enemy_structures(UnitTypeId.ASSIMILATOR).amount < 1
            ):
            if (
                self.supply_used > 15
                and self.can_afford(UnitTypeId.HATCHERY)
                ):
                if (
                    self.structures(UnitTypeId.HATCHERY).amount <= self.enemy_structures(UnitTypeId.HATCHERY).amount
                    or self.structures(UnitTypeId.HATCHERY).amount <= self.enemy_structures(UnitTypeId.COMMANDCENTER).amount
                    or self.structures(UnitTypeId.HATCHERY).amount <= self.enemy_structures(UnitTypeId.NEXUS).amount
                    ):
                    await self.expand_now()
#stay 1 base ahead of them
        if (
            self.time > 150
            and self.can_afford(UnitTypeId.HATCHERY)
            and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
            and not self.already_pending(UnitTypeId.HATCHERY)
            and self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount > self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount
            ):
            if (
                self.structures(UnitTypeId.HATCHERY).amount <= self.enemy_structures(UnitTypeId.HATCHERY).amount
                or self.structures(UnitTypeId.HATCHERY).amount <= self.enemy_structures(UnitTypeId.COMMANDCENTER).amount
                or self.structures(UnitTypeId.HATCHERY).amount <= self.enemy_structures(UnitTypeId.NEXUS).amount
                ):
                await self.expand_now()


    async def build_spawningpool(self):
        if not self.units(UnitTypeId.DRONE):
            return
        if (
            self.time > 45
            and self.enemy_units(UnitTypeId.DRONE).amount < 15
            and self.enemy_units(UnitTypeId.SCV).amount < 15
            and self.enemy_units(UnitTypeId.PROBE).amount < 15
            ):
            if (
                not self.structures(UnitTypeId.SPAWNINGPOOL).ready
                and not self.already_pending(UnitTypeId.SPAWNINGPOOL)
                and self.can_afford(UnitTypeId.SPAWNINGPOOL)
                ):
                await self.build(UnitTypeId.SPAWNINGPOOL, near = self.start_location.position.towards(possible_base_locations[0], -10))
        if (
            not self.structures(UnitTypeId.SPAWNINGPOOL).ready
            and not self.already_pending(UnitTypeId.SPAWNINGPOOL)
            and self.can_afford(UnitTypeId.SPAWNINGPOOL)
            and self.structures(UnitTypeId.HATCHERY).amount > 1
            ):
            await self.build(UnitTypeId.SPAWNINGPOOL, near = self.start_location.position.towards(possible_base_locations[0], -10))

    async def build_gas(self):
        if not self.units(UnitTypeId.DRONE):
            return
        for hatch in self.structures(UnitTypeId.HATCHERY).ready:
            geysernear = self.vespene_geyser.closer_than(15, hatch).closest_to(hatch)
            geyserfar = self.vespene_geyser.closer_than(15, hatch).furthest_to(hatch)
            local_minerals_tags = {mineral.tag for mineral in self.mineral_field if mineral.distance_to(hatch) <= 8}
            local_mineral_workers = self.workers.filter(lambda unit: unit.order_target in local_minerals_tags or (unit.is_carrying_minerals and unit.order_target == hatch.tag))
            if (
                self.can_afford(UnitTypeId.EXTRACTOR)
                and local_mineral_workers.amount > self.structures(UnitTypeId.EXTRACTOR).amount * 11
                and self.structures(UnitTypeId.EXTRACTOR).amount < self.structures(UnitTypeId.HATCHERY).amount * 2
                and self.structure_type_build_progress(UnitTypeId.ROACHWARREN) > 0
                ):
                if (
                    self.structures(UnitTypeId.EXTRACTOR).amount < self.enemy_structures(UnitTypeId.EXTRACTOR).amount and self.already_pending(UnitTypeId.EXTRACTOR) < self.enemy_structures(UnitTypeId.EXTRACTOR).amount
                    or self.structures(UnitTypeId.EXTRACTOR).amount < self.enemy_structures(UnitTypeId.REFINERY).amount and self.already_pending(UnitTypeId.EXTRACTOR) < self.enemy_structures(UnitTypeId.REFINERY).amount
                    or self.structures(UnitTypeId.EXTRACTOR).amount < self.enemy_structures(UnitTypeId.ASSIMILATOR).amount and self.already_pending(UnitTypeId.EXTRACTOR) < self.enemy_structures(UnitTypeId.ASSIMILATOR).amount
                    ):
                    if (
                        not self.gas_buildings.closer_than(1, geysernear)
                        ):
                        await self.build(UnitTypeId.EXTRACTOR, geysernear)
                        print(self.time_formatted, "Building Gas")
                    elif (
                        not self.gas_buildings.closer_than(1, geyserfar)
                        ):
                        await self.build(UnitTypeId.EXTRACTOR, geyserfar)
                        print(self.time_formatted, "Building Gas")
                    print(self.time_formatted, self.already_pending(UnitTypeId.EXTRACTOR))
                    print(self.time_formatted, "They got more gas than us, that's not allowed!")
                        
    async def enemy_units_check(self):
        if self.time > 1:
            x = self.units.closest_to(self.start_location).type_id
            print(self.time_formatted, "unit type =", self.calculate_unit_value(x))
            print(self.time_formatted, "unit type =", self.units.closest_to(self.start_location).type_id)
            if not self.latest_enemy_units:
                self.latest_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).tags
            if self.latest_enemy_units:
                print("enemy units latest are =", self.latest_enemy_units)
#                print(self.time_formatted, "enemy units =", self.enemy_units.by_tag(self.enemy_units.tags[1:]))
                if self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).tags > self.latest_enemy_units:
                    self.latest_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).tags
                    print(self.time_formatted, "New enemy units =", self.latest_enemy_units)
                if self.state.dead_units:
                    print(self.time_formatted, "enemies before deaths =", self.latest_enemy_units)
                    print(self.time_formatted, "enemies that died =", self.state.dead_units)
                    self.latest_enemy_units = (set(self.latest_enemy_units) - set(self.state.dead_units))
                    print(self.time_formatted, "enemies after deaths =", self.latest_enemy_units)
                
    
    async def build_zerglings(self):
        if not self.larva:
            return
        larva = self.larva.random
        if (
            self.supply_left > self.structures(UnitTypeId.HATCHERY).amount
            or self.already_pending(UnitTypeId.OVERLORD) >= 1
            and not self.supply_left == 0
            or self.supply_cap > 199
            ):
#emergency lings:
            if (
                self.time > 45
                and self.enemy_units(UnitTypeId.DRONE).amount < 15
                and self.enemy_units(UnitTypeId.SCV).amount < 15
                and self.enemy_units(UnitTypeId.PROBE).amount < 15
                ):
                if (
                    self.can_afford(UnitTypeId.ZERGLING)
                    and self.structures(UnitTypeId.SPAWNINGPOOL).ready
                    and not self.structures(UnitTypeId.ROACHWARREN).ready
                    ):
                    if (
                        self.time < 120
                        or self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
                        ):
                        larva.train(UnitTypeId.ZERGLING)
                        print(self.time_formatted, "emergency lings")
#defensive lings:
            if (
                self.enemy_units.not_flying.closer_than(50, self.start_location).amount > 1
                and self.can_afford(UnitTypeId.ZERGLING)
                and self.structures(UnitTypeId.SPAWNINGPOOL).ready
                and self.vespene < 25
                and self.time > 149
                and self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount <= self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount
                ):
                larva.train(UnitTypeId.ZERGLING)
                print(self.time_formatted, "defensive lings")
#macro lings:
            if (
                self.structures(UnitTypeId.SPAWNINGPOOL).ready
                and self.can_afford(UnitTypeId.ZERGLING)
                and self.supply_workers > 65
                and self.vespene < 25
                ):
                larva.train(UnitTypeId.ZERGLING)
                print(self.time_formatted, "macro lings")
#scout lings:
            if (
                self.structures(UnitTypeId.SPAWNINGPOOL).ready
                and self.can_afford(UnitTypeId.ZERGLING)
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) < 1
                ):
                if (
                    self.enemy_units(UnitTypeId.DRONE).amount > 14
                    or self.enemy_units(UnitTypeId.SCV).amount > 14
                    or self.enemy_units(UnitTypeId.PROBE).amount > 14
                    ):
                    if (
                        self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) > 1
                        ):
                        larva.train(UnitTypeId.ZERGLING)
                        print(self.time_formatted, "scout ling created")
                elif (
                    self.enemy_units(UnitTypeId.DRONE).amount < 15
                    and self.enemy_units(UnitTypeId.SCV).amount < 15
                    and self.enemy_units(UnitTypeId.PROBE).amount < 15
                    ):
                    larva.train(UnitTypeId.ZERGLING)
                    print(self.time_formatted, "scout ling created")
#lings to match enemy lings if aggression
            if (
                self.can_afford(UnitTypeId.ZERGLING)
                and self.time > 90
                and self.vespene < 25
                and self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount <= self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount
                ):
                larva.train(UnitTypeId.ZERGLING)
                print(self.time_formatted, "our combat units =", self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                print(self.time_formatted, "enemy combat units =", self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                print(self.time_formatted, "Switching from drones to defensive lings")


    async def attack(self):
        roaches = self.units(UnitTypeId.ROACH).ready
        roachcount = self.units(UnitTypeId.ROACH).amount
        lingcount = self.units(UnitTypeId.ZERGLING).amount
        lings = self.units(UnitTypeId.ZERGLING).ready
        airunits = {UnitTypeId.OVERLORD, UnitTypeId.OVERSEER, UnitTypeId.MUTALISK, UnitTypeId.CORRUPTOR, UnitTypeId.BROODLORD, UnitTypeId.MEDIVAC}
        scouts = {UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}
        queens = self.units(UnitTypeId.QUEEN).ready
#defend against the worker rush!
        for drone in self.units(UnitTypeId.DRONE).ready:
            if (
                self.structures(UnitTypeId.SPAWNINGPOOL).not_ready
                ):
                if (
                    self.enemy_units.not_flying.closer_than(10, self.start_location).amount > 1
                    ):
                    drone.attack(self.enemy_units.not_flying.closest_to(drone))
                elif (
                    self.enemy_structures.not_flying.closer_than(20, self.start_location).amount > 0
                    ):
                    drone.attack(self.enemy_structures.not_flying.closer_than(10, self.start_location).closest_to(drone))
            if (
                self.alert(Alert.UnitUnderAttack)
                and self.time < 100
                ):
                drone.attack(self.enemy_units.not_flying.closest_to(drone))

#queens have an attack too
        for queen in queens:
            if (
                self.enemy_units.not_flying.closer_than(5, queen).amount > 0
                or self.enemy_units.flying.closer_than(7, queen).amount > 0
                ):
                queen.attack(self.enemy_units.closest_to(queen))
                
        for roach in roaches:
#defend
            if (
                roachcount > 0
                and self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
                ):
                if (
                    roach.weapon_cooldown == 0
                    ):
                    roach.attack(self.enemy_units.not_flying.closest_to(roach))
                    roach.attack(possible_base_locations[0], queue = True)
                else:
                    roach.move(self.enemy_units.not_flying.closest_to(roach).position)
            elif (
                roachcount > 0
                and self.enemy_structures.not_flying.closer_than(50, self.start_location).amount > 0
                ):
                if (
                    roach.weapon_cooldown == 0
                    ):
                    roach.attack(self.enemy_structures.not_flying.closest_to(roach))
                    roach.attack(possible_base_locations[0], queue = True)
                else:
                    roach.move(self.enemy_structures.not_flying.closest_to(roach).position)
#group
            if (
                roachcount > 0
                and not self.enemy_units.not_flying.closer_than(50, self.start_location)
                and not self.enemy_structures.closer_than(50, self.start_location)
                and roachcount < self.structures(UnitTypeId.HATCHERY).amount * 10
                ):
                roach.move(possible_base_locations[14].towards(self.enemy_start_locations[0], 10))
#attack units first
            if (
                roachcount > self.structures(UnitTypeId.HATCHERY).amount * 10
                and self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).amount > 0
                ):
                if (
                    roach.weapon_cooldown == 0
                    ):
                    roach.attack(self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).closest_to(roach))
                else:
                    roach.move(self.enemy_units.not_flying.closest_to(roach).position)
#attack structures second
            elif (
                roachcount > 50
                and self.enemy_structures.amount > 0
                and not self.enemy_units.not_flying.amount > 0
                ):
                if (
                    roach.weapon_cooldown == 0
                    ):
                    roach.attack(self.enemy_structures.not_flying.closest_to(roach))
                else:
                    roach.move(self.enemy_structures.not_flying.closest_to(roach).position)
#attack locations last
            elif (
                roachcount > 50
                and self.enemy_structures.amount == 0
                and self.enemy_units.not_flying.amount == 0
                and len(roach.orders) < 3
                ):
                roach.attack(possible_base_locations[1])
                roach.attack(possible_base_locations[0], queue = True)
                roach.attack(possible_base_locations[2], queue = True)
                roach.attack(possible_base_locations[3], queue = True)
                roach.attack(possible_base_locations[4], queue = True)
                roach.attack(possible_base_locations[5], queue = True)

        for ling in lings:
#group
            if (
                lingcount > 0
                and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
                and not self.enemy_structures.not_flying.closer_than(50, self.start_location)
                and lingcount < self.structures(UnitTypeId.HATCHERY).amount * 10
                and not ling.is_moving
                ):
                ling.move(possible_base_locations[14].towards(self.enemy_start_locations[0], 4))
#defend
            if (
                lingcount > 0
                and self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
                ):
                ling.attack(self.enemy_units.not_flying.closest_to(ling))
            elif (
                lingcount > 0
                and self.enemy_structures.not_flying.closer_than(50, self.start_location)
                ):
                ling.attack(self.enemy_structures.not_flying.closest_to(ling))
#attack
            if (
                lingcount > self.structures(UnitTypeId.HATCHERY).amount * 20
                and self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).amount > 0
                ):
                ling.attack(self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).closest_to(ling))
            elif (
                lingcount > self.structures(UnitTypeId.HATCHERY).amount * 20
                and self.enemy_structures.amount > 0
                ):
                ling.attack(self.enemy_structures.not_flying.closest_to(ling))
            if (
                roachcount > 50
                and len(ling.orders) < 3
                and self.enemy_structures.amount == 0
                and self.enemy_units.not_flying.amount == 0
                ):
                ling.attack(possible_base_locations[1], queue = True)
                ling.attack(possible_base_locations[0], queue = True)
#lingscoutdeep
        if (
            lingcount > 0
            and self.time < 180
            and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
            ):
            lings.closest_to(possible_base_locations[0]).move(possible_base_locations[0])
#lingscoutfront
        if (
            lingcount > 0
            and self.time > 179
            and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
            and self.enemy_units.not_flying.exclude_type(scouts).closer_than(8, lings.closest_to(possible_base_locations[0])).amount < 1
            ):
            lings.closest_to(possible_base_locations[0]).move(possible_base_locations[0])
        elif (
            lingcount > 0
            and self.time > 179
            and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
            and self.enemy_units.not_flying.exclude_type(scouts).closer_than(8, lings.closest_to(possible_base_locations[0])).amount > 0
            ):
            lings.closest_to(possible_base_locations[0]).move(possible_base_locations[14])

    async def build_roachwarren(self):
        if not self.units(UnitTypeId.DRONE):
            return
        roachwarren = self.structures(UnitTypeId.ROACHWARREN)
        if (
            self.can_afford(UnitTypeId.ROACHWARREN)
            and not roachwarren
            and not self.already_pending(UnitTypeId.ROACHWARREN)
            ):
            if (
                self.can_afford(UnitTypeId.ROACHWARREN)
                and not roachwarren
                and not self.already_pending(UnitTypeId.ROACHWARREN)
                and self.time > 150
                ):
                if (
                    self.enemy_structures(UnitTypeId.ROACHWARREN)
                    or self.enemy_structures(UnitTypeId.BANELINGNEST)
                    or self.enemy_units(UnitTypeId.BANELING)
                    or self.enemy_units(UnitTypeId.ROACH)
                    or self.enemy_units(UnitTypeId.HYDRALISK)
                    ):
                    await self.build(UnitTypeId.ROACHWARREN, near = possible_base_locations[14].position.towards(self.enemy_start_locations[0], 10))
        if (
            self.time < 120
            ):
            if (
                self.enemy_structures(UnitTypeId.EXTRACTOR).amount > 0
                or self.enemy_structures(UnitTypeId.REFINERY).amount > 0
                or self.enemy_structures(UnitTypeId.ASSIMILATOR).amount > 0
                ):
                if (
                    self.enemy_units(UnitTypeId.DRONE).amount < 15
                    and self.enemy_units(UnitTypeId.SCV).amount < 15
                    and self.enemy_units(UnitTypeId.PROBE).amount < 15
                    ):
                    if (
                        self.can_afford(UnitTypeId.ROACHWARREN)
                        and not roachwarren
                        and not self.already_pending(UnitTypeId.ROACHWARREN)
                        ):
                        await self.build(UnitTypeId.ROACHWARREN, near = self.start_location.position.towards(possible_base_locations[14], -10))


    async def build_roaches(self):
        if not self.larva:
            return
        larva = self.larva.random
        if (
            self.supply_left > self.structures(UnitTypeId.HATCHERY).amount * 5
            or self.already_pending(UnitTypeId.OVERLORD) >= 1
            and not self.supply_left == 0
            or self.supply_cap > 199
            ):
            if (
                self.can_afford(UnitTypeId.ROACH)
                and self.structures(UnitTypeId.ROACHWARREN).ready
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                and self.enemy_units.not_flying.exclude_type(scouts).closer_than(50, self.start_location).amount > 0
                ):
                larva.train(UnitTypeId.ROACH)
                print(self.time_formatted, "emergency roaches on the way")
            if (
                self.can_afford(UnitTypeId.ROACH)
                and self.structures(UnitTypeId.ROACHWARREN).ready
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                and self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount <= self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount
                ):
                larva.train(UnitTypeId.ROACH)
                print(self.time_formatted, "our combat units =", self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                print(self.time_formatted, "enemy combat units =", self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                print(self.time_formatted, "too many enemies, making roaches")
            if (
                self.supply_workers + self.already_pending(UnitTypeId.DRONE) >= (self.structures(UnitTypeId.HATCHERY).amount * 16) + (self.structures(UnitTypeId.EXTRACTOR).amount * 3)
                and self.can_afford(UnitTypeId.ROACH)
                and self.structures(UnitTypeId.ROACHWARREN).ready
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                ):
                larva.train(UnitTypeId.ROACH)
                print(self.time_formatted, "too many drones, making roaches")
                

    async def build_queens(self):
        if (
            self.structures(UnitTypeId.SPAWNINGPOOL).ready
            and self.can_afford(UnitTypeId.QUEEN)
            and self.structures(UnitTypeId.HATCHERY).ready.idle
            and self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) < self.structures(UnitTypeId.HATCHERY).amount
            ):
            self.train(UnitTypeId.QUEEN, 1)
            
    async def split_queens(self):
        if not self.units(UnitTypeId.QUEEN):
            return
        for hatchery in self.structures(UnitTypeId.HATCHERY).ready:
                if (
                    self.units(UnitTypeId.QUEEN).closer_than(5, hatchery).amount == 1
                    and hatchery.is_using_ability(AbilityId.TRAINQUEEN_QUEEN)
                    and hatchery.has_buff(BuffId.QUEENSPAWNLARVATIMER)
                    ):
                    print(self.time_formatted, "too many queens including trainees")                   
                    sparequeen = self.units(UnitTypeId.QUEEN).closer_than(6, hatchery).furthest_to(hatchery)
                    if sparequeen:
                            print(self.time_formatted, "there is a spare queen now because another is training")
                            for hatch in self.structures(UnitTypeId.HATCHERY):
                                if (
                                    self.units(UnitTypeId.QUEEN).closer_than(5, hatch).amount < 1
                                    and self.structures(UnitTypeId.HATCHERY).ready
                                    and not hatch.is_using_ability(AbilityId.TRAINQUEEN_QUEEN)
                                    ):
                                    sparequeen.move(hatch)
                                    print(self.time_formatted, "spare queen because another is training moving to lonely hatchery")
                                    break
                                elif(
                                    self.units(UnitTypeId.QUEEN).closer_than(5, hatch).amount < 1
                                    and self.structures(UnitTypeId.HATCHERY).not_ready
                                    ):
                                    sparequeen.move(hatch)
                                    print(self.time_formatted, "spare queen because another is training moving to building hatchery")
                                    break
                elif (
                    self.units(UnitTypeId.QUEEN).closer_than(5, hatchery).amount > 1
                    ):
                    sparequeen = self.units(UnitTypeId.QUEEN).closer_than(5, hatchery).furthest_to(hatchery)
                    print(self.time_formatted, "too many queens")                   
                    if sparequeen:
                            for hatch in self.structures(UnitTypeId.HATCHERY):
                                if (
                                    self.units(UnitTypeId.QUEEN).closer_than(5, hatch).amount < 1
                                    ):
                                    sparequeen.move(hatch)
                                    print(self.time_formatted, "spare queen out of 2 moving to lonely hatchery")
                                    break

    async def queen_inject(self):
        if not self.units(UnitTypeId.QUEEN):
            return
        for queen in self.units(UnitTypeId.QUEEN):
            hatch = self.structures(UnitTypeId.HATCHERY).ready.closest_to(queen)
            if (
                self.can_cast(UnitTypeId.QUEEN, AbilityId.EFFECT_INJECTLARVA)
                and not hatch.has_buff(BuffId.QUEENSPAWNLARVATIMER)
                and not queen.is_using_ability(AbilityId.EFFECT_INJECTLARVA)
                and not self.already_pending(AbilityId.EFFECT_INJECTLARVA)
                ):
                queen(AbilityId.EFFECT_INJECTLARVA, hatch)


    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")
