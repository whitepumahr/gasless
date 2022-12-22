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
    nearby_enemy_units = False
    nearby_friendly_units = False
    enemyworkerstags = False
    enemyworkers = False
    totalvalue = 0
    totalvalue_e = 0
    totalvalue_en = 0
    totalvalue_o = 0
    totalvalue_on = 0
    closestlingtag = False
    closestling = False
    closestlingtag2 = False
    closestling2 = False    
    mylings = False

    
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
        print("Game started")
        self.larva.random.train(UnitTypeId.DRONE)
        global possible_base_locations
        possible_base_locations = sorted(self.expansion_locations.keys(), key=lambda p: p.distance_to(self.start_location), reverse=True)
        print("player 1 or 2", self.player_id)
        print("possible base locations for this map =", possible_base_locations)
        print("possible base locations for this map =", self.expansion_locations)
        global scouts
        scouts = {UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}

        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(self.start_location, 2.8))
        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(possible_base_locations[1], -2.8), queue = True)
        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(self.start_location, 2.8), queue = True)
        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(possible_base_locations[1], -2.8), queue = True)
        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(self.start_location, 2.8), queue = True)
        self.units(UnitTypeId.OVERLORD).closest_to(possible_base_locations[0]).move(possible_base_locations[0].position.towards(possible_base_locations[1], -35))
        self.overlord1tag = self.units(UnitTypeId.OVERLORD).closest_to(possible_base_locations[0]).tag
        self.overlord1 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord1tag)

        await self.chat_send("You can thank Ratosh and the rest of the very helpful sc2 botting community for what's about to happen to you, GLHF!")


    async def on_step(self, iteration: int):

        await self.distribute_workers()
        await self.build_workers()
        await self.build_overlords()
        await self.expand()
        await self.build_zerglings()
        await self.build_gas()
        await self.attack()
        await self.build_roachwarren()
        await self.build_roaches()
        await self.build_queens()
        await self.queen_inject()
        await self.split_queens()
        await self.units_value_check()
        await self.building_cancel_check()
        

    async def building_cancel_check(self):
        if self.townhalls.not_ready:
            for hatch in self.townhalls.not_ready:
                print(self.time_formatted, self.supply_used, "health =", hatch.health_percentage)
                if hatch.health_percentage < .05:
                    hatch(AbilityId.CANCEL_BUILDINPROGRESS)

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
                del local_mineral_workers[:base.ideal_harvesters]
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
                    if self.minerals > self.vespene * 2:
                        #print(self.time_formatted, self.supply_used, "need more workers")
                        for worker in local_mineral_workers.take(abs(gas.surplus_harvesters)):
                            #print(self.time_formatted, self.supply_used, gas.surplus_harvesters)
                            #print(self.time_formatted, self.supply_used, worker)
                            worker.gather(gas)
                            #print(self.time_formatted, self.supply_used, gas.surplus_harvesters)
                            #print(self.time_formatted, self.supply_used, "gathering gas")
                if gas.surplus_harvesters > 0:
                    local_gas_workers = self.workers.filter(lambda unit:  unit.order_target == gas.tag or (unit.is_carrying_vespene and unit.order_target == gas.tag))
                    for worker in local_gas_workers.take(abs(gas.surplus_harvesters)):
                        #print(self.time_formatted, self.supply_used, gas.surplus_harvesters)
                        #print(self.time_formatted, self.supply_used, worker)
                        worker.gather(self.mineral_field.closest_to(base))
                    #print(self.time_formatted, self.supply_used, "Too many gas workers here")
                

    async def build_workers(self):

        if not self.larva:
            return
        if not self.units(UnitTypeId.DRONE):
            return
        if not self.supply_workers:
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        larva = self.larva.random
        enemies_near = Units([], self)
                    
        for hatch in self.townhalls:
            if not enemies_near:
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                    enemies_near.extend(
                        self.enemy_units.filter(
                            lambda u: not u.is_flying
                            and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)
                            and u.distance_to(hatch) < 40
                        )
                    )

        if (
            self.can_afford(UnitTypeId.DRONE)
            and self.townhalls.amount < 2
            and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 16
            and self.time < 60
            ):
            if (
                self.supply_left > self.townhalls.amount
                or self.already_pending(UnitTypeId.OVERLORD) >= 1
                and not self.supply_left == 0
                ):
                larva.train(UnitTypeId.DRONE)
                print(self.time_formatted, self.supply_used, "macro 16 hatch")
#After drone scout determine enemy build and react
        if self.time > 45:
            print(self.time_formatted, self.supply_used, "enemy drones = ", self.enemyworkers)
#if macro
            if self.enemyworkers > 14:
                #print(self.time_formatted, self.supply_used, "Enemy is playing macro")
                if (
                    self.supply_left > self.townhalls.amount
                    or self.already_pending(UnitTypeId.OVERLORD) >= 1
                    and not self.supply_left == 0
                    ):
                    if (
                        self.can_afford(UnitTypeId.DRONE)
                        and self.townhalls.amount > 1
                        and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 17
                        and self.supply_left > self.townhalls.amount
                        ):
                        larva.train(UnitTypeId.DRONE)
                        print(self.time_formatted, self.supply_used, "macro 17 pool")
                    if (
                        not enemies_near.amount > 0
                        and self.can_afford(UnitTypeId.DRONE)
                        and self.townhalls.amount > 1
                        and self.structures(UnitTypeId.SPAWNINGPOOL).amount > 0
                        and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 19
                        ):
                        larva.train(UnitTypeId.DRONE)
                        print(self.time_formatted, self.supply_used, "macro 19 hatch")
                if self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount + 1) * 16:
                    if not self.structures(UnitTypeId.EXTRACTOR):
                        if (
                            self.can_afford(UnitTypeId.DRONE)
                            and self.townhalls.amount > 1
                            and not enemies_near.amount > 0
                            and self.totalvalue_o >= self.totalvalue_e
                            ):
                            if (
                                self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) >= self.townhalls.amount
                                or self.already_pending(UnitTypeId.QUEEN) == self.townhalls.ready.amount
                                ):
                                for hatch in self.townhalls:
                                    if (
                                        hatch.assigned_harvesters + self.already_pending(UnitTypeId.DRONE) < hatch.ideal_harvesters
                                        or self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount + 1) * 16
                                        ):
                                        if (
                                            self.already_pending(UnitTypeId.ZERGLING) + self.units(UnitTypeId.ZERGLING).amount > 0
                                            and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 120
                                            ):
                                            if self.townhalls.amount == 2 and self.already_pending(UnitTypeId.HATCHERY) >= 1 and self.time < 180 or self.townhalls.amount == 2 and self.minerals > 349:
                                                if (
                                                    self.supply_used < 36
                                                    or self.already_pending(UnitTypeId.OVERLORD) >= 1
                                                    and not self.supply_left == 0
                                                    ):
                                                    larva.train(UnitTypeId.DRONE)
                                                    print(self.time_formatted, self.supply_used, "macro droning before third overlord")
                                            if (
                                                self.townhalls.amount == 3
                                                and self.already_pending(UnitTypeId.HATCHERY) >= 1
                                                and self.time < 220
                                                or self.townhalls.amount == 3
                                                and self.minerals > 349
                                                ):
                                                if (
                                                    self.supply_used < 39
                                                    or self.already_pending(UnitTypeId.OVERLORD) >= 1
                                                    and not self.supply_left == 0
                                                    ):
                                                    larva.train(UnitTypeId.DRONE)
                                                    print(self.time_formatted, self.supply_used, "macro droning before fourth overlord")
                                            if (
                                                self.townhalls.amount == 4
                                                and self.already_pending(UnitTypeId.HATCHERY) >= 1
                                                or self.townhalls.amount == 4
                                                and self.minerals > 349
                                                or self.townhalls.amount == 3
                                                and self.already_pending(UnitTypeId.HATCHERY) == 2
                                                ):
                                                if (
                                                    self.supply_used < 49
                                                    or self.already_pending(UnitTypeId.OVERLORD) >= 1
                                                    and not self.supply_left == 0
                                                    ):
                                                    larva.train(UnitTypeId.DRONE)
                                                    print(self.time_formatted, self.supply_used, "macro droning before fifth overlord")
                                            if self.townhalls.amount >= 4 and self.townhalls.amount >= enemy_townhalls.amount:
                                                if (
                                                    self.supply_left > self.townhalls.ready.amount + self.units(UnitTypeId.QUEEN).amount * 2
                                                    or self.already_pending(UnitTypeId.OVERLORD) >= 1
                                                    and not self.supply_left == 0
                                                    ):
                                                    larva.train(UnitTypeId.DRONE)
                                                    print(self.time_formatted, self.supply_used, "macro droning after fifth overlord")
                                            if self.townhalls.amount > enemy_townhalls.amount:
                                                if (
                                                    self.already_pending(UnitTypeId.ROACHWARREN)
                                                    or self.structures(UnitTypeId.ROACHWARREN).ready
                                                    ):
                                                    if (
                                                        self.supply_left > self.townhalls.ready.amount + self.units(UnitTypeId.QUEEN).amount * 3
                                                        or self.already_pending(UnitTypeId.OVERLORD) >= 1
                                                        and not self.supply_left == 0
                                                        ):
                                                        larva.train(UnitTypeId.DRONE)
                                                        print(self.time_formatted, self.supply_used, "macro droning after fifth overlord and roach warren")

#pre move drones

#16 hatch
                if (
                    self.minerals > 200
                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 17
                    and not self.townhalls.amount > 1
                    and not self.already_pending(UnitTypeId.HATCHERY)
                    ):
                    if not self.closestdronee1tag or not self.closestdronee1:
                        self.closestdronee1tag = self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[14]).tag
                    if self.closestdronee1tag:
                        self.closestdronee1 = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronee1tag)
                    if self.closestdronee1:
                        if (
                            not self.enemy_units.not_flying.closer_than(5, possible_base_locations[14]).amount > 0
                            and not self.enemy_structures.not_flying.closer_than(5, possible_base_locations[14]).amount > 0
                            and self.closestdronee1
                            ):
                            self.closestdronee1.move(possible_base_locations[14])
                            #print(self.time_formatted, self.supply_used, "16 hatch drone moving to new expansion location")
                            if self.can_afford(UnitTypeId.HATCHERY):
                                self.closestdronee1.build(UnitTypeId.HATCHERY, possible_base_locations[14])
                        if (
                            self.enemy_units.not_flying.closer_than(5, possible_base_locations[14]).amount > 0
                            or self.enemy_structures.not_flying.closer_than(5, possible_base_locations[14]).amount > 0
                            ):
                            self.closestdronee1.move(possible_base_locations[13])
                            #print(self.time_formatted, self.supply_used, "16 hatch drone moving to new alternate expansion location")
                            if self.can_afford(UnitTypeId.HATCHERY):
                                self.closestdronee1.build(UnitTypeId.HATCHERY, possible_base_locations[13])
#17 pool
                if (
                    self.minerals > 150
                    and not self.structures(UnitTypeId.SPAWNINGPOOL)
                    and self.townhalls.amount > 1
                    and not self.already_pending(UnitTypeId.SPAWNINGPOOL)
                    ):
                    if not self.closestdronesptag or not self.closestdronesp:
                        self.closestdronesptag = self.units(UnitTypeId.DRONE).closest_to(self.start_location.position.towards(possible_base_locations[0], -10)).tag
                    if self.closestdronesptag:
                        self.closestdronesp = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronesptag)
                    if self.closestdronesp:
                        if not self.enemy_units.closer_than(4, self.start_location.position.towards(possible_base_locations[0], -10)):
                            self.closestdronesp.move(self.start_location.position.towards(possible_base_locations[0], -10))
                            #print(self.time_formatted, self.supply_used, "17 pool drone moving to pool build location")
                            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                                self.closestdronesp.build(UnitTypeId.SPAWNINGPOOL, self.start_location.position.towards(possible_base_locations[0], -10))
                        if self.enemy_units.closer_than(4, self.start_location.position.towards(possible_base_locations[0], -10)):
                            self.closestdronesp.move(self.start_location.position.towards(possible_base_locations[14], -10))
                            #print(self.time_formatted, self.supply_used, "17 pool drone moving to alternate pool build location")
                            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                                self.closestdronesp.build(UnitTypeId.SPAWNINGPOOL, self.start_location.position.towards(possible_base_locations[14], -10))
#19 hatch
                if (
                    self.minerals > 100
                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) > 18
                    and not self.townhalls.amount > 2
                    ):
                    if not self.closestdronee2tag or not self.closestdronee2:
                        self.closestdronee2tag = self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[13]).tag
                    if self.closestdronee2tag:
                        self.closestdronee2 = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronee2tag)
                    if self.closestdronee2:
                        if (
                            not self.enemy_units.not_flying.closer_than(5, possible_base_locations[13]).amount > 0
                            and not self.enemy_structures.not_flying.closer_than(5, possible_base_locations[13]).amount > 0
                            and self.closestdronee2
                            ):
                            self.closestdronee2.move(possible_base_locations[13])
                            #print(self.time_formatted, self.supply_used, "19 hatch drone moving to new expansion location")
                            if self.can_afford(UnitTypeId.HATCHERY):
                                self.closestdronee2.build(UnitTypeId.HATCHERY, possible_base_locations[13])
                        if (
                            self.enemy_units.not_flying.closer_than(5, possible_base_locations[13]).amount > 0
                            or self.enemy_structures.not_flying.closer_than(5, possible_base_locations[13]).amount > 0
                            ):
                            self.closestdronee2.move(possible_base_locations[12])
                            #print(self.time_formatted, self.supply_used, "19 hatch drone moving to new alternate expansion location")
                            if self.can_afford(UnitTypeId.HATCHERY):
                                self.closestdronee2.build(UnitTypeId.HATCHERY, possible_base_locations[12])
                    if self.closestdronee2:
                        if (
                            self.supply_left > self.townhalls.amount
                            or self.already_pending(UnitTypeId.OVERLORD) >= 1
                            and not self.supply_left == 0
                            ):
                            if (
                                self.can_afford(UnitTypeId.DRONE)
                                and self.townhalls.amount < 3
                                and self.enemy_structures(UnitTypeId.EXTRACTOR).amount < 1
                                and self.enemy_structures(UnitTypeId.REFINERY).amount < 1
                                and self.enemy_structures(UnitTypeId.ASSIMILATOR).amount < 1
                                and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 20
                                ):
                                larva.train(UnitTypeId.DRONE)
                                #print(self.time_formatted, self.supply_used, "19 hatch up to 20 drones")
#if early aggression

#early aggression back to droning after ling scout if we overbuilt units
            if self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount + 1) * 16 + (enemy_gas_buildings.amount + 2) * 3:
                for hatch in self.townhalls:
                    for gas in self.structures(UnitTypeId.EXTRACTOR):
                        if (
                            self.supply_left > self.townhalls.amount
                            or self.already_pending(UnitTypeId.OVERLORD) >= 1
                            and not self.supply_left == 0
                            ):
                            if (
                                self.can_afford(UnitTypeId.DRONE)
                                and self.time > 134
                                and not enemies_near.amount > 0
                                and self.totalvalue_o > self.totalvalue_e
                                and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 120
                                ):
                                if (
                                    self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount + 1) * 16 + (enemy_gas_buildings.amount + 2) * 3
                                    or hatch.assigned_harvesters + gas.assigned_harvesters + self.already_pending(UnitTypeId.DRONE) < hatch.ideal_harvesters + gas.ideal_harvesters
                                    ):
                                    larva.train(UnitTypeId.DRONE)
                                    #print(self.time_formatted, self.supply_used, "our combat units =", self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).amount)
                                    #print(self.time_formatted, self.supply_used, "enemy combat units =", self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                                    print(self.time_formatted, self.supply_used, "Switching from anti aggression to drones - worker made")
#emergency pool
            if not self.units(UnitTypeId.DRONE):
                return
            if self.enemyworkers < 15:
                if (
                    self.minerals > 150
                    and not self.structures(UnitTypeId.SPAWNINGPOOL)
                    ):
                    if not self.closestdronesptag or not self.closestdronesp:
                        self.closestdronesptag = self.units(UnitTypeId.DRONE).closest_to(self.start_location.position.towards(possible_base_locations[0], -10)).tag
                    if self.closestdronesptag:
                        self.closestdronesp = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronesptag)
                    if self.closestdronesp:
                        if not self.already_pending(UnitTypeId.SPAWNINGPOOL) and not self.enemy_units.closer_than(3, self.start_location.position.towards(possible_base_locations[0], -10)):
                            self.closestdronesp.move(self.start_location.position.towards(possible_base_locations[0], -10))
                            #print(self.time_formatted, self.supply_used, "Emergency pool drone moving to pool build location")
                            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                                self.closestdronesp.build(UnitTypeId.SPAWNINGPOOL, self.start_location.position.towards(possible_base_locations[0], -10))
                                print(self.time_formatted, self.supply_used, "Emergency pool drone building pool at build location")
                        if not self.already_pending(UnitTypeId.SPAWNINGPOOL) and self.enemy_units.closer_than(3, self.start_location.position.towards(possible_base_locations[0], -10)):
                            self.closestdronesp.move(self.start_location.position.towards(possible_base_locations[14], 10))
                            #print(self.time_formatted, self.supply_used, "Emergency pool drone moving to pool build location")
                            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                                self.closestdronesp.build(UnitTypeId.SPAWNINGPOOL, self.start_location.position.towards(possible_base_locations[14], 10))
                                print(self.time_formatted, self.supply_used, "Emergency pool drone building pool at alternate build location")
                if (
                    self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) > 0
                    and self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) < 0.2
                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 17
                    and self.can_afford(UnitTypeId.DRONE)
                    ):
                    larva.train(UnitTypeId.DRONE)
                    #print(self.time_formatted, self.supply_used, "Drone while emergency pool starts")
#emergency roach warren
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
                        if not self.closestdronerwtag or not self.closestdronerw:
                            self.closestdronerwtag = self.units(UnitTypeId.DRONE).closest_to(self.start_location.position.towards(possible_base_locations[1], 7)).tag
                        if self.closestdronerwtag:
                            self.closestdronerw = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronerwtag)
                            if (
                                not self.enemy_units.closer_than(3, self.start_location.position.towards(possible_base_locations[1], 7))
                                and not self.structures(UnitTypeId.SPAWNINGPOOL).closer_than(3, self.start_location.position.towards(possible_base_locations[1], 7))
                                ):
                                self.closestdronerw.move(self.start_location.position.towards(possible_base_locations[1], 7))
                                #print(self.time_formatted, self.supply_used, "Emergency roach warren drone moving to roach warren location")
                                if self.can_afford(UnitTypeId.ROACHWARREN):
                                    self.closestdronerw.build(UnitTypeId.ROACHWARREN, self.start_location.position.towards(possible_base_locations[1], 7))
                            if (
                                self.enemy_units.closer_than(3, self.start_location.position.towards(possible_base_locations[1], 7))
                                or self.structures(UnitTypeId.SPAWNINGPOOL).closer_than(3, self.start_location.position.towards(possible_base_locations[1], 7))
                                ):
                                self.closestdronerw.move(self.start_location.position.towards(possible_base_locations[14], 7))
                                #print(self.time_formatted, self.supply_used, "Emergency roach warren drone moving to alternate roach warren location")
                                if self.can_afford(UnitTypeId.ROACHWARREN):
                                    self.closestdronerw.build(UnitTypeId.ROACHWARREN, self.start_location.position.towards(possible_base_locations[14], 7))
        enemies_near = Units([], self)


    async def build_overlords(self):
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
#overlordscout
        if (
            self.time > 179
            and self.time < 181
            ):
            #print(self.time_formatted, self.supply_used, "overlord scout 3min")
            if enemy_gas_buildings.amount < 1:
                self.overlord1.move(possible_base_locations[0].position.towards(possible_base_locations[1], -4.5))
                self.overlord1.move(possible_base_locations[0].position.towards(possible_base_locations[1], -35), queue = True)
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -4.5))
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -24), queue = True)
                #print(self.time_formatted, self.supply_used, "Overlord scout initiated 3:00")
        if (
            self.time > 164
            and self.time < 166
            ):
            #print(self.time_formatted, self.supply_used, "overlord scout 2:45")
            if enemy_gas_buildings.amount > 0:
                self.overlord1.move(possible_base_locations[0].position.towards(possible_base_locations[1], -4.5))
                self.overlord1.move(possible_base_locations[0].position.towards(possible_base_locations[1], -35), queue = True)
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -4.5))
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -24), queue = True)
                #print(self.time_formatted, self.supply_used, "Overlord scout initiated 2:45")
#position overlords
        if not self.units(UnitTypeId.OVERLORD):
            return

#overlord 1
        if self.overlord1tag:
            self.overlord1 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord1tag)
        if not self.overlord1 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord3:
            self.overlord1tag = self.overlord3tag
            self.overlord1 = self.overlord3
            self.overlord3 = False
        if self.overlord1 and self.time > 210:
            self.overlord1.move(possible_base_locations[0].position.towards(possible_base_locations[1], -35))
            
#overlord 2
        if not self.overlord2 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord3:
            self.overlord2tag = self.overlord3tag
            self.overlord2 = self.overlord3
            self.overlord3 = False
        if self.units(UnitTypeId.OVERLORD).amount == 2:
            self.overlord2tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord2tag:
            self.overlord2 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord2tag)
        if self.overlord2:
            if (
                enemy_townhalls.amount > 1
                and self.time < 150
                ):
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -24))
            if self.time < 60:
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -10))
            if (
                enemy_gas_buildings.amount > 0
                and enemy_townhalls.amount < 2
                ):
                if self.time < 120:
                    self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -10))
            elif (
                enemy_gas_buildings.amount < 1
                and self.time > 210
                or enemy_townhalls.amount > 1
                and self.time > 210
                ):
                self.overlord2.move(possible_base_locations[1].position.towards(possible_base_locations[0], -24))
                
#overlord 3        
        if not self.overlord3 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord4:
            self.overlord3tag = self.overlord4tag
            self.overlord3 = self.overlord4
            self.overlord4 = False
        if self.units(UnitTypeId.OVERLORD).amount == 3:
            self.overlord3tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord3tag:
            self.overlord3 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord3tag)
        if self.overlord3:
            self.overlord3.move(possible_base_locations[1].position.towards(self.start_location, 40))
            
#overlord 4
        if not self.overlord4 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord5:
            self.overlord4tag = self.overlord5tag
            self.overlord4 = self.overlord5
            self.overlord5 = False
        if self.units(UnitTypeId.OVERLORD).amount == 4:
            self.overlord4tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord4tag:
            self.overlord4 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord4tag)
        if self.overlord4 and not enemy_townhalls.closer_than(4, possible_base_locations[2]):
            self.overlord4.move(possible_base_locations[2].position.towards(self.start_location, 10))
        elif self.overlord4 and enemy_townhalls.closer_than(4, possible_base_locations[2]):
            self.overlord4.move(possible_base_locations[15].position.towards(possible_base_locations[14], 10))
            
#overlord 5
        if not self.overlord5 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord6:
            self.overlord5tag = self.overlord6tag
            self.overlord5 = self.overlord6
            self.overlord6 = False
        if self.units(UnitTypeId.OVERLORD).amount == 5:
            self.overlord5tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord5tag:
            self.overlord5 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord5tag)
        if self.overlord5 and not enemy_townhalls.closer_than(4, possible_base_locations[3]):
            self.overlord5.move(possible_base_locations[3].position.towards(self.start_location, 10))
        elif self.overlord5 and enemy_townhalls.closer_than(4, possible_base_locations[3]):
            self.overlord5.move(possible_base_locations[15].position.towards(possible_base_locations[14], 10))
                                
#overlord 7            
        if not self.overlord7 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord8:
            self.overlord7tag = self.overlord8tag
            self.overlord7 = self.overlord8
            self.overlord8 = False
        if self.units(UnitTypeId.OVERLORD).amount == 7:
            self.overlord7tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord7tag:
            self.overlord7 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord7tag)
        if self.overlord7 and not enemy_townhalls.closer_than(4, possible_base_locations[5]):
            self.overlord7.move(possible_base_locations[5].position.towards(self.start_location, 10))
        elif self.overlord7 and enemy_townhalls.closer_than(4, possible_base_locations[5]):
            self.overlord7.move(possible_base_locations[15].position.towards(possible_base_locations[14], 10))

#overlord 8            
        if not self.overlord8 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord9:
            self.overlord8tag = self.overlord9tag
            self.overlord8 = self.overlord9
            self.overlord9 = False
        if self.units(UnitTypeId.OVERLORD).amount == 8:
            self.overlord8tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord8tag:
            self.overlord8 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord8tag)
        if self.overlord8 and not enemy_townhalls.closer_than(4, possible_base_locations[6]):
            self.overlord8.move(possible_base_locations[6].position.towards(self.start_location, 10))
        elif self.overlord8 and enemy_townhalls.closer_than(4, possible_base_locations[6]):
            self.overlord8.move(possible_base_locations[15].position.towards(possible_base_locations[14], 10))

#overlord 9            
        if not self.overlord9 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord10:
            self.overlord9tag = self.overlord10tag
            self.overlord9 = self.overlord10
            self.overlord10 = False
        if self.units(UnitTypeId.OVERLORD).amount == 9:
            self.overlord9tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord9tag:
            self.overlord9 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord9tag)
        if self.overlord9 and not enemy_townhalls.closer_than(4, possible_base_locations[7]):
            self.overlord9.move(possible_base_locations[7].position.towards(self.start_location, 10))
        elif self.overlord9 and enemy_townhalls.closer_than(4, possible_base_locations[7]):
            self.overlord9.move(possible_base_locations[15].position.towards(possible_base_locations[14], 10))

#overlord 10            
        if not self.overlord10 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord11:
            self.overlord10tag = self.overlord11tag
            self.overlord10 = self.overlord11
            self.overlord11 = False
        if self.units(UnitTypeId.OVERLORD).amount == 10:
            self.overlord10tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord10tag:
            self.overlord10 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord10tag)
        if self.overlord10 and not enemy_townhalls.closer_than(4, possible_base_locations[8]):
            self.overlord10.move(possible_base_locations[8].position.towards(self.start_location, 10))
        elif self.overlord10 and enemy_townhalls.closer_than(4, possible_base_locations[8]):
            self.overlord10.move(possible_base_locations[15].position.towards(possible_base_locations[14], 10))

#overlord 11            
        if not self.overlord11 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord12:
            self.overlord11tag = self.overlord12tag
            self.overlord11 = self.overlord12
            self.overlord12 = False
        if self.units(UnitTypeId.OVERLORD).amount == 11:
            self.overlord11tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord11tag:
            self.overlord11 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord11tag)
        if self.overlord11 and not enemy_townhalls.closer_than(4, possible_base_locations[9]):
            self.overlord11.move(possible_base_locations[9].position.towards(self.start_location, 10))
        elif self.overlord11 and enemy_townhalls.closer_than(4, possible_base_locations[9]):
            self.overlord11.move(possible_base_locations[15].position.towards(possible_base_locations[14], 10))

#overlord 12            
        if not self.overlord12 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord13:
            self.overlord12tag = self.overlord13tag
            self.overlord12 = self.overlord13
            self.overlord13 = False
        if self.units(UnitTypeId.OVERLORD).amount == 12:
            self.overlord12tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord12tag:
            self.overlord12 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord12tag)
        if self.overlord12 and not enemy_townhalls.closer_than(4, possible_base_locations[10]):
            self.overlord12.move(possible_base_locations[10].position.towards(self.start_location, 10))
        elif self.overlord12 and enemy_townhalls.closer_than(4, possible_base_locations[10]):
            self.overlord12.move(possible_base_locations[15].position.towards(possible_base_locations[14], 10))

#overlord 13            
        if not self.overlord13 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord14:
            self.overlord13tag = self.overlord14tag
            self.overlord13 = self.overlord14
            self.overlord14 = False
        if self.units(UnitTypeId.OVERLORD).amount == 13:
            self.overlord13tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord13tag:
            self.overlord13 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord13tag)
        if self.overlord13 and not enemy_townhalls.closer_than(4, possible_base_locations[11]):
            self.overlord13.move(possible_base_locations[11].position.towards(self.start_location, 10))
        elif self.overlord13 and enemy_townhalls.closer_than(4, possible_base_locations[11]):
            self.overlord13.move(possible_base_locations[15].position.towards(possible_base_locations[14], 10))

#overlord 14            
        if not self.overlord14 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord15:
            self.overlord14tag = self.overlord15tag
            self.overlord14 = self.overlord15
            self.overlord15 = False
        if self.units(UnitTypeId.OVERLORD).amount == 14:
            self.overlord14tag = self.units(UnitTypeId.OVERLORD).closest_to(self.start_location).tag
        if self.overlord14tag:
            self.overlord14 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord14tag)
        if self.overlord14 and not enemy_townhalls.closer_than(4, possible_base_locations[12]):
            self.overlord14.move(possible_base_locations[12].position.towards(self.start_location, 10))
        elif self.overlord14 and enemy_townhalls.closer_than(4, possible_base_locations[12]):
            self.overlord14.move(possible_base_locations[15].position.towards(possible_base_locations[14], 10))

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
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        larva = self.larva.random
        if self.supply_cap < 200:
            if (
                self.supply_left < self.townhalls.amount + 1
                and self.already_pending(UnitTypeId.OVERLORD) < self.townhalls.ready.amount
                and self.can_afford(UnitTypeId.OVERLORD)
                and self.time < 60
                ):
                larva.train(UnitTypeId.OVERLORD)
                print(self.time_formatted, self.supply_used, "First overlord")
            if self.enemyworkers > 14:
                if (
                    self.townhalls.amount > 1
                    and self.supply_used == 19
                    and self.already_pending(UnitTypeId.OVERLORD) < 1
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    if self.townhalls.amount > 2 or self.time > 114 and self.can_afford(UnitTypeId.OVERLORD):
                        larva.train(UnitTypeId.OVERLORD)
                        print(self.time_formatted, self.supply_used, "Second overlord")               
                if (
                    self.townhalls.amount > 1
                    and self.supply_used == 36
                    and self.already_pending(UnitTypeId.OVERLORD) < 1
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                    print(self.time_formatted, self.supply_used, "Third overlord")               
                if (
                    self.townhalls.amount > 2
                    and self.supply_used == 39
                    and self.already_pending(UnitTypeId.OVERLORD) < 1
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    if self.townhalls.ready.amount > 2 and self.supply_used == 39 or self.townhalls.amount > 2 and self.supply_used == 39 and self.time > 180:
                        larva.train(UnitTypeId.OVERLORD)
                        print(self.time_formatted, self.supply_used, "Fourth overlord")
                if (
                    self.townhalls.ready.amount > 2
                    and self.supply_used == 49
                    and self.already_pending(UnitTypeId.OVERLORD) < self.townhalls.ready.amount
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                    print(self.time_formatted, self.supply_used, "Fifth overlord")
                if (
                    self.townhalls.ready.amount > 2
                    and self.supply_used > 50
                    and self.supply_left <= self.townhalls.ready.amount + self.units(UnitTypeId.QUEEN).amount * 2
                    and self.already_pending(UnitTypeId.OVERLORD) < self.townhalls.ready.amount
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                    print(self.time_formatted, self.supply_used, "Sixth overlord and beyond")
                if (
                    self.townhalls.ready.amount > 2
                    and self.supply_used > 50
                    and self.structure_type_build_progress(UnitTypeId.ROACHWARREN) > 0
                    and self.supply_left <= self.townhalls.ready.amount + self.units(UnitTypeId.QUEEN).amount * 3
                    and self.already_pending(UnitTypeId.OVERLORD) < self.townhalls.ready.amount
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                    print(self.time_formatted, self.supply_used, "Sixth overlord and beyond")
            if self.enemyworkers < 15:
                if (
                    self.already_pending(UnitTypeId.ROACHWARREN)
                    or self.structures(UnitTypeId.ROACHWARREN).ready
                    ):
                    if (
                        self.supply_left <= self.townhalls.ready.amount + self.units(UnitTypeId.QUEEN).amount * 3
                        and self.already_pending(UnitTypeId.OVERLORD) < self.townhalls.ready.amount
                        and self.can_afford(UnitTypeId.OVERLORD)
                        ):
                        larva.train(UnitTypeId.OVERLORD)
                        print(self.time_formatted, self.supply_used, "Second overlord after roach warren")
                if (
                    self.time < 80
                    and self.can_afford(UnitTypeId.OVERLORD)
                    and self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) > 0
                    and self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) < 0.5
                    and not self.already_pending(UnitTypeId.OVERLORD)
                    and enemy_townhalls.amount < 2
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                    print(self.time_formatted, self.supply_used, "Emergency defense preparation overlord")
                
            
    async def expand(self):
        if not self.units(UnitTypeId.DRONE):
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
#if early gas aggression, don't expand until they do, if non gas aggression, expand
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
                and self.enemyworkers > 14
                ):
                await self.expand_now()
        if (
            self.time > 45
            and self.time < 120
            ):
            if (
                self.enemy_structures(UnitTypeId.EXTRACTOR).amount > 0
                or self.enemy_structures(UnitTypeId.REFINERY).amount > 0
                or self.enemy_structures(UnitTypeId.ASSIMILATOR).amount > 0
                ):
                if (
                    self.supply_used > 15
                    and self.can_afford(UnitTypeId.HATCHERY)
                    ):
                    if self.townhalls.amount < enemy_townhalls.amount:
                        await self.expand_now()
#stay 1 base ahead of them
        if (
            self.can_afford(UnitTypeId.HATCHERY)
            and enemy_gas_buildings.amount > 0
            ):
            if (
                self.townhalls.amount <= enemy_townhalls.amount
                or self.supply_cap > 199
                ):
                if self.enemy_units.not_flying.closer_than(30, self.start_location).amount < 1:
                    if self.townhalls.closer_than(3, possible_base_locations[15]) and self.time > 105:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[14]).build(UnitTypeId.HATCHERY, possible_base_locations[14])
                    if self.townhalls.closer_than(3, possible_base_locations[14]) and self.townhalls.amount < 3:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[13]).build(UnitTypeId.HATCHERY, possible_base_locations[13])
                    if self.townhalls.closer_than(3, possible_base_locations[13]) and self.townhalls.amount < 4:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[12]).build(UnitTypeId.HATCHERY, possible_base_locations[12])
                    if self.townhalls.closer_than(3, possible_base_locations[12]) and self.townhalls.amount < 5:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[11]).build(UnitTypeId.HATCHERY, possible_base_locations[11])
                    if self.townhalls.closer_than(3, possible_base_locations[11]) and self.townhalls.amount < 6:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[10]).build(UnitTypeId.HATCHERY, possible_base_locations[10])
                    if self.townhalls.closer_than(3, possible_base_locations[10]) and self.townhalls.amount < 7:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[9]).build(UnitTypeId.HATCHERY, possible_base_locations[9])
                    if self.townhalls.closer_than(3, possible_base_locations[9]) and self.townhalls.amount < 8:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[8]).build(UnitTypeId.HATCHERY, possible_base_locations[8])
                    if self.townhalls.closer_than(3, possible_base_locations[8]) and self.townhalls.amount < 9:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[7]).build(UnitTypeId.HATCHERY, possible_base_locations[7])
                    if self.townhalls.closer_than(3, possible_base_locations[7]) and self.townhalls.amount < 10:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[6]).build(UnitTypeId.HATCHERY, possible_base_locations[6])
                    if self.townhalls.closer_than(3, possible_base_locations[6]) and self.townhalls.amount < 11:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[5]).build(UnitTypeId.HATCHERY, possible_base_locations[5])
                    if self.townhalls.closer_than(3, possible_base_locations[5]) and self.townhalls.amount < 12:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[4]).build(UnitTypeId.HATCHERY, possible_base_locations[4])
        if (
            self.can_afford(UnitTypeId.HATCHERY)
            and enemy_gas_buildings.amount < 1
            ):
            if (
                self.townhalls.amount <= enemy_townhalls.amount
                or self.supply_cap > 199
                ):
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(30, self.start_location).amount < 1:
                    if self.townhalls.closer_than(3, possible_base_locations[15]):
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[14]).build(UnitTypeId.HATCHERY, possible_base_locations[14])
                    if self.townhalls.closer_than(3, possible_base_locations[14]) and self.townhalls.amount < 3 and self.time > 105:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[13]).build(UnitTypeId.HATCHERY, possible_base_locations[13])
                    if self.townhalls.closer_than(3, possible_base_locations[13]) and self.townhalls.amount < 4 and self.time > 170:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[12]).build(UnitTypeId.HATCHERY, possible_base_locations[12])
                    if self.townhalls.closer_than(3, possible_base_locations[12]) and self.townhalls.amount < 5 and self.time > 200:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[11]).build(UnitTypeId.HATCHERY, possible_base_locations[11])
                    if self.townhalls.closer_than(3, possible_base_locations[11]) and self.townhalls.amount < 6 and self.time > 230:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[10]).build(UnitTypeId.HATCHERY, possible_base_locations[10])
                    if self.townhalls.closer_than(3, possible_base_locations[10]) and self.townhalls.amount < 7:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[9]).build(UnitTypeId.HATCHERY, possible_base_locations[9])
                    if self.townhalls.closer_than(3, possible_base_locations[9]) and self.townhalls.amount < 8:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[8]).build(UnitTypeId.HATCHERY, possible_base_locations[8])
                    if self.townhalls.closer_than(3, possible_base_locations[8]) and self.townhalls.amount < 9:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[7]).build(UnitTypeId.HATCHERY, possible_base_locations[7])
                    if self.townhalls.closer_than(3, possible_base_locations[7]) and self.townhalls.amount < 10:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[6]).build(UnitTypeId.HATCHERY, possible_base_locations[6])
                    if self.townhalls.closer_than(3, possible_base_locations[6]) and self.townhalls.amount < 11:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[5]).build(UnitTypeId.HATCHERY, possible_base_locations[5])
                    if self.townhalls.closer_than(3, possible_base_locations[5]) and self.townhalls.amount < 12:
                        self.units(UnitTypeId.DRONE).closest_to(possible_base_locations[4]).build(UnitTypeId.HATCHERY, possible_base_locations[4])
        else:
            print("cant expand", self.can_afford(UnitTypeId.HATCHERY), enemy_gas_buildings.amount < 0, self.townhalls.amount <= enemy_townhalls.amount, )
        
    async def build_gas(self):
        if not self.units(UnitTypeId.DRONE):
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        for hatch in self.townhalls.ready:
            geysernear = self.vespene_geyser.closer_than(15, hatch).closest_to(hatch)
            geyserfar = self.vespene_geyser.closer_than(15, hatch).furthest_to(hatch)
            local_minerals_tags = {mineral.tag for mineral in self.mineral_field if mineral.distance_to(hatch) <= 8}
            local_mineral_workers = self.workers.filter(lambda unit: unit.order_target in local_minerals_tags or (unit.is_carrying_minerals and unit.order_target == hatch.tag))
            if (
                self.can_afford(UnitTypeId.EXTRACTOR)
                and self.structures(UnitTypeId.EXTRACTOR).amount + self.already_pending(UnitTypeId.EXTRACTOR) < self.townhalls.amount * 2
                and self.structure_type_build_progress(UnitTypeId.ROACHWARREN) > 0
                ):
                if (
                    self.structures(UnitTypeId.EXTRACTOR).amount + self.already_pending(UnitTypeId.EXTRACTOR) < enemy_gas_buildings.amount
                    or self.structures(UnitTypeId.EXTRACTOR).amount + self.already_pending(UnitTypeId.EXTRACTOR) < 1
                    or self.supply_workers + self.already_pending(UnitTypeId.DRONE) >= (enemy_townhalls.amount + 1) * 16 + (enemy_gas_buildings.amount + 2) * 3 and self.vespene < 100
                    or self.gas_buildings.amount + self.already_pending(UnitTypeId.EXTRACTOR) < self.townhalls.amount and self.time > 300
                    ):
                    if (
                        not self.gas_buildings.closer_than(1, geysernear)
                        and self.vespene < self.minerals
                        ):
                        await self.build(UnitTypeId.EXTRACTOR, geysernear)
                        #print(self.time_formatted, self.supply_used, "Building Gas")
                    elif (
                        not self.gas_buildings.closer_than(1, geyserfar)
                        and self.vespene < self.minerals
                        ):
                        await self.build(UnitTypeId.EXTRACTOR, geyserfar)
                        #print(self.time_formatted, self.supply_used, "Building Gas")
                elif self.supply_workers + self.already_pending(UnitTypeId.DRONE) >= (self.townhalls.amount * 16) + (self.structures(UnitTypeId.EXTRACTOR).amount * 3) and self.minerals > 500:
                    if (
                        not self.gas_buildings.closer_than(1, geysernear)
                        and self.vespene < self.minerals
                        ):
                        await self.build(UnitTypeId.EXTRACTOR, geysernear)
                        #print(self.time_formatted, self.supply_used, "Building Gas")
                    elif (
                        not self.gas_buildings.closer_than(1, geyserfar)
                        and self.vespene < self.minerals
                        ):
                        await self.build(UnitTypeId.EXTRACTOR, geyserfar)
                        #print(self.time_formatted, self.supply_used, "Building Gas")
                    #print(self.time_formatted, self.supply_used, self.already_pending(UnitTypeId.EXTRACTOR))
                    #print(self.time_formatted, self.supply_used, "They got more gas than us, that's not allowed!")
                        
    async def units_value_check(self):
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        ou = self.units.filter(lambda ou: not ou.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN))
#enemy workers
        if not self.enemyworkerstags:
            self.enemyworkerstags = self.enemy_units(scouts).tags
        if self.enemyworkerstags:
            #print(self.time_formatted, self.supply_used, "enemy workers tags = ", self.enemyworkerstags)
            #print(self.time_formatted, self.supply_used, "real enemy workers tags = ", self.enemy_units(scouts).tags)
            #print(self.time_formatted, self.supply_used, "Do we have less?", len(self.enemy_units(scouts).tags) > len(self.enemyworkerstags))
            if len(self.enemy_units(scouts).tags) > len(self.enemyworkerstags):
                self.enemyworkerstags = self.enemy_units(scouts).tags
                #print(self.time_formatted, self.supply_used, "new enemy workers tags = ", self.enemyworkerstags)
                enemyworkers = 0
                for tag in self.enemyworkerstags:
                    #print(self.time_formatted, self.supply_used, "tag = ", tag)
                    enemyworker = self.enemy_units.find_by_tag(tag)
                    #print(self.time_formatted, self.supply_used, "enemy worker from tag = ", enemyworker)
                    enemyworkers = enemyworkers + 1
                    #print(self.time_formatted, self.supply_used, "enemy worker count at = ", enemyworkers)
                else:
                    self.enemyworkers = enemyworkers
                    #print(self.time_formatted, self.supply_used, "enemy workers = ", self.enemyworkers)
            if self.state.dead_units:
                self.enemyworkerstags = (set(self.enemyworkerstags) - set(self.state.dead_units))

#enemy units on map            
        if not self.latest_enemy_units:
            if self.time < 300:
                self.latest_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).tags
            if self.structure_type_build_progress(UnitTypeId.ROACHWARREN) >= 1 and self.time > 299:
                self.latest_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).tags
                print(self.structure_type_build_progress(UnitTypeId.ROACHWARREN), "queens now included in threat eval")
        if self.latest_enemy_units:
            if self.time < 300:
                if len(self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).tags) > len(self.latest_enemy_units):
                    self.latest_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).tags
                    for unit in self.latest_enemy_units:
                        enemyunit = self.enemy_units.find_by_tag(unit)
                        enemyunittypeid = enemyunit.type_id
                        combinedvalue = self.calculate_unit_value(enemyunittypeid).minerals + self.calculate_unit_value(enemyunittypeid).vespene
                        self.totalvalue = self.totalvalue + combinedvalue
                    else:
                        self.totalvalue_e = self.totalvalue
                        self.totalvalue = 0
            if self.structure_type_build_progress(UnitTypeId.ROACHWARREN) >= 1 and self.time > 299:
                if len(self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).tags) > len(self.latest_enemy_units):
                    self.latest_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).tags
                    for unit in self.latest_enemy_units:
                        enemyunit = self.enemy_units.find_by_tag(unit)
                        enemyunittypeid = enemyunit.type_id
                        combinedvalue = self.calculate_unit_value(enemyunittypeid).minerals + self.calculate_unit_value(enemyunittypeid).vespene
                        self.totalvalue = self.totalvalue + combinedvalue
                    else:
                        self.totalvalue_e = self.totalvalue
                        self.totalvalue = 0
            if self.state.dead_units:
                self.latest_enemy_units = (set(self.latest_enemy_units) - set(self.state.dead_units))
#our units
        if self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)):
            for unit in self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)):
                unittypeid = unit.type_id
                combinedvalue = self.calculate_unit_value(unittypeid).minerals + self.calculate_unit_value(unittypeid).vespene
                self.totalvalue = self.totalvalue + combinedvalue
            else:
                self.totalvalue_o = self.totalvalue
                self.totalvalue = 0
    
    async def build_zerglings(self):
        if not self.larva:
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        larva = self.larva.random
        enemies_near = Units([], self)
                    
        for hatch in self.townhalls:
            if not enemies_near:
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                    enemies_near.extend(
                        self.enemy_units.filter(
                            lambda u: not u.is_flying
                            and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)
                            and u.distance_to(hatch) < 40
                        )
                    )
        if (
            self.supply_left > self.townhalls.amount
            or self.already_pending(UnitTypeId.OVERLORD) >= 1
            and not self.supply_left == 0
            or self.supply_cap > 199
            ):
#emergency lings:
            if (
                self.time > 45
                and self.enemyworkers < 15
                and enemy_townhalls.amount < 2
                ):
                if (
                    self.can_afford(UnitTypeId.ZERGLING)
                    and self.structures(UnitTypeId.SPAWNINGPOOL).ready
                    and not self.structures(UnitTypeId.ROACHWARREN).ready
                    ):
                    if (
                        self.time < 120
                        or enemies_near.amount > 0
                        ):
                        larva.train(UnitTypeId.ZERGLING)
                        print(self.time_formatted, self.supply_used, "emergency lings")
#defensive lings:
            if (
                enemies_near.amount > 1
                and self.can_afford(UnitTypeId.ZERGLING)
                and self.structures(UnitTypeId.SPAWNINGPOOL).ready
                and self.vespene < 25
                and self.time > 149
                ):
                larva.train(UnitTypeId.ZERGLING)
                print(self.time_formatted, self.supply_used, "defensive lings")
#macro lings:
            for hatch in self.townhalls:
                if self.structures(UnitTypeId.EXTRACTOR):
                    for gas in self.structures(UnitTypeId.EXTRACTOR):
                        if (
                            self.structures(UnitTypeId.SPAWNINGPOOL).ready
                            and self.can_afford(UnitTypeId.ZERGLING)
                            and self.vespene < 25
                            and self.townhalls.amount >= enemy_townhalls.amount
                            ):
                            if (
                                hatch.assigned_harvesters + gas.assigned_harvesters + self.already_pending(UnitTypeId.DRONE) >= hatch.ideal_harvesters + gas.ideal_harvesters
                                and self.supply_workers + self.already_pending(UnitTypeId.DRONE) >= (enemy_townhalls.amount + 1) * 16
                                ):
                                larva.train(UnitTypeId.ZERGLING)
                                print(self.time_formatted, self.supply_used, "macro lings")
                else:
                    if (
                        self.structures(UnitTypeId.SPAWNINGPOOL).ready
                        and self.can_afford(UnitTypeId.ZERGLING)
                        and self.townhalls.amount >= enemy_townhalls.amount
                        ):
                        if (
                            hatch.assigned_harvesters + self.already_pending(UnitTypeId.DRONE) >= hatch.ideal_harvesters
                            and self.supply_workers + self.already_pending(UnitTypeId.DRONE) >= (enemy_townhalls.amount + 1) * 16
                            ):
                            larva.train(UnitTypeId.ZERGLING)
                            print(self.time_formatted, self.supply_used, "macro lings")
                    
#scout lings:
            if (
                self.structures(UnitTypeId.SPAWNINGPOOL).ready
                and self.can_afford(UnitTypeId.ZERGLING)
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) < 1
                ):
                if self.enemyworkers > 14:
                    if (
                        self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) > 1
                        ):
                        larva.train(UnitTypeId.ZERGLING)
                        print(self.time_formatted, self.supply_used, "scout ling created")
                elif self.enemyworkers < 15:
                    larva.train(UnitTypeId.ZERGLING)
                    print(self.time_formatted, self.supply_used, "scout ling created")
#lings to match enemy lings if they are building up army
            if (
                self.can_afford(UnitTypeId.ZERGLING)
                and self.time > 90
                and self.vespene < 25
                and self.totalvalue_o < self.totalvalue_e
                and self.already_pending(UnitTypeId.ZERGLING) * 50 < self.totalvalue_e
                ):
                larva.train(UnitTypeId.ZERGLING)
                #print(self.time_formatted, self.supply_used, "our combat units =", self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).amount)
                #print(self.time_formatted, self.supply_used, "enemy combat units =", self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                print(self.time_formatted, self.supply_used, "Switching from drones to defensive lings")
                
                print(self.time_formatted, self.supply_used, "Enemyunits", self.totalvalue_e)

        enemies_near = Units([], self)

    async def attack(self):
        roaches = self.units(UnitTypeId.ROACH).ready
        roachcount = self.units(UnitTypeId.ROACH).amount
        lingcount = self.units(UnitTypeId.ZERGLING).amount
        lings = self.units(UnitTypeId.ZERGLING)
        airunits = {UnitTypeId.OVERLORD, UnitTypeId.OVERSEER, UnitTypeId.MUTALISK, UnitTypeId.CORRUPTOR, UnitTypeId.BROODLORD, UnitTypeId.MEDIVAC}
        scouts = {UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}
        queens = self.units(UnitTypeId.QUEEN).ready
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        enemies_near = Units([], self)
        enemies_structures_near = Units([], self)
        enemies_aggressive_structures = self.structures.filter(lambda sa: sa.can_attack)

#hatchery zonal defense system
        for hatch in self.townhalls:
            if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                enemies_near.extend(
                    self.enemy_units.filter(
                        lambda u: not u.is_flying
                        and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)
                        and u.distance_to(hatch) < 40
                    )
                )
            print(self.time_formatted, self.supply_used, "enemies near =", enemies_near)
            if self.enemy_structures.not_flying.closer_than(40, hatch):
                enemies_structures_near.extend(
                    self.enemy_structures.filter(
                        lambda s: not s.is_flying
                        and s.distance_to(hatch) < 40
                    )
                )
            print(self.time_formatted, self.supply_used, "enemies structures near =", enemies_structures_near)
        print(self.time_formatted, self.supply_used, "enemies near total =", enemies_near.amount)
        print(self.time_formatted, self.supply_used, "enemies structures total =", enemies_structures_near.amount)
#defend against the worker rush!
        if self.enemyworkers:
            print("enemy worker")
            naw = self.units.filter(lambda naw: naw.type_id == (UnitTypeId.DRONE) and not naw.is_attacking)
            if self.enemy_units({UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}).closer_than(8, self.start_location):
                for eworker in self.enemy_units({UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}).closer_than(8, self.start_location):
                        print("enemy worker nearby")
                        print("our non attacking workers =", naw)
                        for drone in naw:
                            print("naw = ", naw)
                            print("eworker pos =", eworker.position)
                            print("our worker pos =", drone.position)
                            if drone.position.is_closer_than(3, eworker):
                                drone.attack(eworker)
                                print("worker attacking enemy worker")
        for drone in self.units(UnitTypeId.DRONE):
            if self.time < 30 and self.enemy_units.not_flying.closer_than(10, drone).amount > 2:
                self.units(UnitTypeId.DRONE).furthest_to(self.start_location).gather(self.mineral_field.closest_to(self.townhalls.closest_to(self.start_location)))
            if self.time > 40 and self.time < 50 and self.alert(Alert.UnitUnderAttack):
                self.units(UnitTypeId.DRONE).furthest_to(self.start_location).move(possible_base_locations[0].position.towards(possible_base_locations[1], -2.8))
                self.units(UnitTypeId.DRONE).furthest_to(self.start_location).gather(self.mineral_field.closest_to(self.townhalls.closest_to(self.start_location)), queue = True)
            if not self.structures(UnitTypeId.SPAWNINGPOOL):
                if self.enemy_units.not_flying.closer_than(10, self.start_location).amount > 1:
                    drone.attack(self.enemy_units.not_flying.closer_than(10, self.start_location).closest_to(drone))
                elif self.enemy_structures.not_flying.exclude_type((UnitTypeId.ASSIMILATOR, UnitTypeId.REFINERY, UnitTypeId.EXTRACTOR, UnitTypeId.ENGINEERINGBAY, UnitTypeId.EVOLUTIONCHAMBER, UnitTypeId.FORGE)).closer_than(10, self.start_location).amount > 0:
                    drone.attack(self.enemy_structures.not_flying.closer_than(10, self.start_location).closest_to(drone))
            if (
                self.alert(Alert.UnitUnderAttack)
                and self.enemy_units.not_flying.closer_than(10, self.start_location).amount > 0
                and not self.structures(UnitTypeId.SPAWNINGPOOL).ready
                ):
                drone.attack(self.enemy_units.not_flying.closer_than(10, self.start_location).closest_to(drone))
            if drone.is_attacking:
                if self.enemy_units.not_flying.closer_than(9, self.start_location).amount < 1 and self.enemy_structures.not_flying.closer_than(10, self.start_location).amount < 1:
                    drone.gather(self.mineral_field.closest_to(self.townhalls.closest_to(self.start_location)))

#queens have an attack too
        for queen in queens:
                if (
                    self.enemy_units.not_flying.closer_than(5, queen).amount > 0
                    or self.enemy_units.flying.closer_than(7, queen).amount > 0
                    ):
                    print("qwc =", queen.weapon_cooldown)
                    if (
                        queen.weapon_cooldown == 0
                        ):
                        queen.attack(self.enemy_units.closest_to(queen))
                        queen.move(self.townhalls.closest_to(queen), queue = True)
                        print(self.time_formatted, self.supply_used, "queen unit defense")
                    else:
                        if queen.target_in_range(self.enemy_units.closest_to(queen)):
                            if self.enemy_units.closest_to(queen).ground_range < 5:
                                queen.move(self.enemy_units.closest_to(queen).position.towards(queen, 5))
                                queen.move(self.townhalls.closest_to(queen), queue = True)
                            else:
                                queen.move(self.enemy_units.closest_to(queen).position)
                                queen.move(self.townhalls.closest_to(queen), queue = True)
                                
                                
                
###check enemy units if enemies nearby
##                if not self.nearby_enemy_units:
##                    if self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)):
##                        self.nearby_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])).tags
##                if self.nearby_enemy_units:
##                    if len(self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])).tags) > len(self.nearby_enemy_units):
##                        self.nearby_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])).tags
##                    if len(self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])).tags) < len(self.nearby_enemy_units):
##                        self.nearby_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])).tags
##                    for unit in self.nearby_enemy_units:
##                        enemyunit = self.enemy_units.find_by_tag(unit)
##                        enemyunittypeid = enemyunit.type_id
##                        combinedvalue = self.calculate_unit_value(enemyunittypeid).minerals + self.calculate_unit_value(enemyunittypeid).vespene
##                        self.totalvalue = self.totalvalue + combinedvalue
##                    else:
##                        self.totalvalue_en = self.totalvalue
##                        self.totalvalue = 0
##                        self.nearby_enemy_units = False
##                        print(self.time_formatted, self.supply_used, "self.totalvalue_en =", self.totalvalue_en)
###check our units including itself if enemy units nearby
##                    if not self.nearby_friendly_units:
##                        self.nearby_friendly_units = self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])).tags
##                    if len(self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])).tags) > len(self.nearby_friendly_units):
##                        self.nearby_friendly_units = self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])).tags
##                    if len(self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])).tags) < len(self.nearby_friendly_units):
##                        self.nearby_friendly_units = self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])).tags
##                    for unit in self.nearby_friendly_units:
##                        ourunit = self.units.find_by_tag(unit)
##                        ourunittypeid = ourunit.type_id
##                        combinedvalue = self.calculate_unit_value(ourunittypeid).minerals + self.calculate_unit_value(ourunittypeid).vespene
##                        self.totalvalue = self.totalvalue + combinedvalue
##                    else:
##                        self.totalvalue_on = self.totalvalue
##                        self.totalvalue = 0
##                        self.nearby_friendly_units = False
##                        print(self.time_formatted, self.supply_used, "self.totalvalue_on =", self.totalvalue_on)

#lingu
                    
#lingscoutfront
        if not self.closestling or not self.closestlingtag:
            if lings:
                if self.closestling2 in lings:
                    lings.remove(self.closestling2)
                    if lings:
                        self.closestlingtag = lings.closest_to(possible_base_locations[0]).tag
                        self.closestling = lings.find_by_tag(self.closestlingtag)
                if not self.closestling2:
                    self.closestlingtag = lings.closest_to(possible_base_locations[0]).tag
                    self.closestling = lings.find_by_tag(self.closestlingtag)
        if self.closestling:
            print(self.time_formatted, self.supply_used, "closestling =", self.closestling)                    
            print(self.time_formatted, self.supply_used, "new closest ling selected =", self.closestling)
            print(self.time_formatted, self.supply_used, "entire ling list1 =", lings)
            print(self.time_formatted, self.supply_used, "old ling list =", lings)
            print(self.time_formatted, self.supply_used, "new ling list =", lings)
            print(self.time_formatted, self.supply_used, "closestling =", self.closestling)                    
            if (
                not enemies_near.amount > 0
                and self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling).amount < 3
                and self.closestling.is_idle
                ):
                self.closestling.move(possible_base_locations[1].position.towards(possible_base_locations[0], 2.8))
                self.closestling.move(possible_base_locations[0], queue = True)
                print(self.time_formatted, self.supply_used, "closest ling scouting")
            if (
                self.enemy_units.not_flying.closer_than(10, self.closestling).amount > 2
                and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(4, self.townhalls.closest_to(possible_base_locations[0]))
                and enemies_near.amount > 0
                ):
                self.closestling.move(self.townhalls.ready.closest_to(possible_base_locations[0]).position)
                lings.append(self.closestling)
                self.closestling = False
                print(self.time_formatted, self.supply_used, "closest ling retreating")
                
##        lings = self.units(UnitTypeId.ZERGLING)
##        if self.closestling in lings:
##            lings.remove(self.closestling)
                    
        if not self.closestling2 or not self.closestlingtag2:
            if lings:
                self.closestlingtag2 = lings.closest_to(possible_base_locations[0]).tag
                self.closestling2 = lings.find_by_tag(self.closestlingtag2)
        if self.closestling2:
            if not self.closestlingtag2:
                if lings:
                    self.closestlingtag2 = lings.closest_to(possible_base_locations[0]).tag
                    self.closestling2 = lings.find_by_tag(self.closestlingtag2)
            if self.closestling2:
                print(self.time_formatted, self.supply_used, "closestling 2 =", self.closestling2)                    
                print(self.time_formatted, self.supply_used, "entire ling list1 =", lings)
                print(self.time_formatted, self.supply_used, "old ling list =", lings)
                print(self.time_formatted, self.supply_used, "new ling list =", lings)
                print(self.time_formatted, self.supply_used, "closestling 2 =", self.closestling2)                    
                if (
                    not enemies_near.amount > 0
                    and self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling2).amount < 3
                    and len(self.closestling2.orders) < 1
                    ):
                    if enemy_gas_buildings.amount < 1:
                        if not enemy_townhalls.closer_than(4, possible_base_locations[2]):
                            self.closestling2.move(possible_base_locations[2])
                            self.closestling2.move(possible_base_locations[3], queue = True)
                        elif not enemy_townhalls.closer_than(4, possible_base_locations[3]):
                            self.closestling2.move(possible_base_locations[3])
                            self.closestling2.move(possible_base_locations[4], queue = True)
                        elif not enemy_townhalls.closer_than(4, possible_base_locations[4]):
                            self.closestling2.move(possible_base_locations[4])
                            self.closestling2.move(possible_base_locations[5], queue = True)
                        elif not enemy_townhalls.closer_than(4, possible_base_locations[5]):
                            self.closestling2.move(possible_base_locations[5])
                            self.closestling2.move(possible_base_locations[6], queue = True)
                        elif not enemy_townhalls.closer_than(4, possible_base_locations[6]):
                            self.closestling2.move(possible_base_locations[6])
                            self.closestling2.move(possible_base_locations[7], queue = True)
                    else:
                        self.closestling2.move(possible_base_locations[12])
                        self.closestling2.move(possible_base_locations[11], queue = True)
                        if not enemy_townhalls.closer_than(5, possible_base_locations[10]):
                            self.closestling2.move(possible_base_locations[10], queue = True)
                            if not enemy_townhalls.closer_than(5, possible_base_locations[9]):
                                self.closestling2.move(possible_base_locations[9], queue = True)
                                if not enemy_townhalls.closer_than(5, possible_base_locations[8]):
                                    self.closestling2.move(possible_base_locations[8], queue = True)
                                    if not enemy_townhalls.closer_than(5, possible_base_locations[7]):
                                        self.closestling2.move(possible_base_locations[7], queue = True)
                                        if not enemy_townhalls.closer_than(5, possible_base_locations[6]):
                                            self.closestling2.move(possible_base_locations[6], queue = True)
                                            if not enemy_townhalls.closer_than(5, possible_base_locations[5]):
                                                self.closestling2.move(possible_base_locations[5], queue = True)
                                                if not enemy_townhalls.closer_than(5, possible_base_locations[4]):
                                                    self.closestling2.move(possible_base_locations[4], queue = True)
                                                    if not enemy_townhalls.closer_than(5, possible_base_locations[3]):
                                                        self.closestling2.move(possible_base_locations[3], queue = True)
                                                        if not enemy_townhalls.closer_than(5, possible_base_locations[2]):
                                                            self.closestling2.move(possible_base_locations[2], queue = True)
                        print(self.time_formatted, self.supply_used, "closest ling 2 scouting")
                if (
                    self.enemy_units.not_flying.closer_than(10, self.closestling2).amount > 2
                    and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(4, self.townhalls.closest_to(possible_base_locations[0]))
                    and enemies_near.amount > 0
                    ):
                    self.closestling2.move(self.townhalls.ready.closest_to(possible_base_locations[0]).position)
                    lings.append(self.closestling2)
                    self.closestling2 = False
                    print(self.time_formatted, self.supply_used, "closest ling 2 retreating")
        if self.closestling2 in lings:
            lings.remove(self.closestling2)
                            
        if self.townhalls:
            if (
                not self.totalvalue_on > self.totalvalue_en and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(4, self.townhalls.closest_to(possible_base_locations[0]))
                or self.time < 180 and not self.enemy_units.not_flying.exclude_type(scouts).closer_than(4, self.townhalls.closest_to(possible_base_locations[0]))
                ):
                if lings:
                    if lings.closer_than(5, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0]).position):
                        for ling in lings.closer_than(5, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])):
                            ling.move(self.townhalls.ready.closest_to(possible_base_locations[0]).position)
                if roaches:
                    if roaches.closer_than(5, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0]).position):
                        for roachn in roaches.closer_than(10, self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).closest_to(possible_base_locations[0])):
                            roachn.move(self.townhalls.ready.closest_to(possible_base_locations[0]).position)
                    
        if lings:
            print(self.time_formatted, self.supply_used, "main ling list =", lings)
            for ling in lings:

#defend
#check enemy units if enemies nearby
                if self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)):
                    neu = self.enemy_units.filter(lambda neu: not neu.is_flying and not neu.type_id == (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and neu.position.is_closer_than(10, ling))
                    if neu:
                        if len(self.enemy_units.filter(lambda neu: not neu.is_flying and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and neu.position.is_closer_than(10, ling)).tags) > len(neu.tags):
                            neu = self.enemy_units.filter(lambda neu: not neu.is_flying and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and neu.position.is_closer_than(10, ling))
                        if len(self.enemy_units.filter(lambda neu: not neu.is_flying and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and neu.position.is_closer_than(10, ling)).tags) < len(neu.tags):
                            neu = self.enemy_units.filter(lambda neu: not neu.is_flying and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and neu.position.is_closer_than(10, ling))
                        for eunit in neu:
                            combinedvalue = self.calculate_unit_value(eunit.type_id).minerals + self.calculate_unit_value(eunit.type_id).vespene
                            self.totalvalue = self.totalvalue + combinedvalue
                        else:
                            self.totalvalue_en = self.totalvalue
                            self.totalvalue = 0
                            print(self.time_formatted, self.supply_used, "ling at position =", ling.position, "self.totalvalue_en =", self.totalvalue_en)
#check our units including itself if enemy units nearby
                        onu = self.units.filter(lambda onu: not onu.is_flying and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA] and onu.position.is_closer_than(10, ling))
                        print("our lambda units are =", onu)
                        if len(self.units.filter(lambda onu: not onu.is_flying and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA] and onu.position.is_closer_than(10, ling)).tags) > len(onu.tags):
                            onu = self.units.filter(lambda onu: not onu.is_flying and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA] and onu.position.is_closer_than(10, ling))
                        if len(self.units.filter(lambda onu: not onu.is_flying and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA] and onu.position.is_closer_than(10, ling)).tags) < len(onu.tags):
                            onu = self.units.filter(lambda onu: not onu.is_flying and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA] and onu.position.is_closer_than(10, ling))
                        for ounit in onu:
                            combinedvalue = self.calculate_unit_value(ounit.type_id).minerals + self.calculate_unit_value(ounit.type_id).vespene
                            self.totalvalue = self.totalvalue + combinedvalue
                        else:
                            self.totalvalue_on = self.totalvalue
                            self.totalvalue = 0
                            print(self.time_formatted, self.supply_used, "self.totalvalue_on =", self.totalvalue_on)
                                
                if (
                    enemies_near.amount > 0 and self.totalvalue_on > self.totalvalue_en
                    or self.supply_used > 190
                    and enemies_near.amount > 0
                    or self.time < 180 and self.enemy_units.not_flying.exclude_type(scouts).closer_than(4, self.townhalls.closest_to(possible_base_locations[0]))
                    ):
                    ling.attack(enemies_near.closest_to(ling))
                    print(self.time_formatted, self.supply_used, "unit defending, our nearby units =", self.totalvalue_on)
                    print(self.time_formatted, self.supply_used, "unit defending, enemy nearby units =", self.totalvalue_en)
                    
                if (
                    enemies_structures_near
                    and not enemies_near.amount > 0
                    and self.totalvalue_on > self.totalvalue_en
                    or self.supply_used > 190
                    and enemies_structures_near
                    and not enemies_near.amount > 0
                    ):
                    ling.attack(enemies_structures_near.closest_to(ling))
                    print(self.time_formatted, self.supply_used, "structure defense, our nearby units =", self.totalvalue_on)
                    #print(self.time_formatted, self.supply_used, "structure defense, enemy nearby units =", self.totalvalue_en)
#group
                if (
                    self.totalvalue_o > 0
                    and not enemies_structures_near
                    and not enemies_near.amount > 0
                    and self.supply_used < 180
                    ):
                    if not self.townhalls.amount == enemy_townhalls.amount and not ling.position.is_closer_than(5, self.townhalls.ready.closest_to(self.enemy_start_locations[0]).position.towards(self.enemy_start_locations[0], 7)):
                        ling.move(self.townhalls.ready.closest_to(self.enemy_start_locations[0]).position.towards(self.enemy_start_locations[0], 4))
                    if self.townhalls.amount == enemy_townhalls.amount and not ling.position.is_closer_than(5, self.townhalls.ready.closest_to(self.enemy_start_locations[0]).position.towards(self.enemy_start_locations[0], 7)):
                        ling.move(self.townhalls.closest_to(self.enemy_start_locations[0]).position.towards(self.enemy_start_locations[0], 4))
                    print(self.time_formatted, self.supply_used, "unit group, our units total =", self.totalvalue_o)
                    #print(self.time_formatted, self.supply_used, "unit group, enemy units total =", self.totalvalue_e)
#attack
                if (
                    self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).amount > 0
                    and not enemies_structures_near
                    and not enemies_near.amount > 0
                    and self.supply_used > 190
                    ):
                    ling.attack(self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).closest_to(ling))
                    print(self.time_formatted, self.supply_used, "unit attack, our nearby units =", self.totalvalue_on)
                    #print(self.time_formatted, self.supply_used, "unit attack, enemy nearby units =", self.totalvalue_en)
                    
                if (
                    self.enemy_structures.not_flying.amount > 0
                    and not self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).amount > 0
                    and not enemies_structures_near
                    and not enemies_near.amount > 0
                    and self.supply_used > 190
                    ):
                    ling.attack(self.enemy_structures.not_flying.closest_to(ling))
                    print(self.time_formatted, self.supply_used, "structure attack, our nearby units =", self.totalvalue_on)
                    #print(self.time_formatted, self.supply_used, "structure attack, enemy nearby units =", self.totalvalue_en)
                    
                if (
                    not self.enemy_structures.not_flying.amount > 0
                    and not self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).amount > 0
                    and not enemies_structures_near
                    and not enemies_near.amount > 0
                    and len(ling.orders) < 5
                    and self.supply_used > 190
                    ):
                    ling.attack(possible_base_locations[1])
                    ling.attack(possible_base_locations[0], queue = True)
                    ling.attack(possible_base_locations[2], queue = True)
                    ling.attack(possible_base_locations[3], queue = True)
                    #print(self.time_formatted, self.supply_used, "hunt attack, our nearby units =", self.totalvalue_on)
                    #print(self.time_formatted, self.supply_used, "hunt attack, enemy nearby units =", self.totalvalue_en)
    
            
        for roach in roaches:

            
#defend
#check enemy units if enemies nearby
            if self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)):
                neu = self.enemy_units.filter(lambda neu: not neu.is_flying and not neu.type_id == (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and neu.position.is_closer_than(10, roach))
                print("neu =", neu)
                if neu:
                    if len(self.enemy_units.filter(lambda neu: not neu.is_flying and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and neu.position.is_closer_than(10, roach)).tags) > len(neu.tags):
                        neu = self.enemy_units.filter(lambda neu: not neu.is_flying and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and neu.position.is_closer_than(10, roach))
                    if len(self.enemy_units.filter(lambda neu: not neu.is_flying and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and neu.position.is_closer_than(10, roach)).tags) < len(neu.tags):
                        neu = self.enemy_units.filter(lambda neu: not neu.is_flying and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and neu.position.is_closer_than(10, roach))
                    for eunit in neu:
                        combinedvalue = self.calculate_unit_value(eunit.type_id).minerals + self.calculate_unit_value(eunit.type_id).vespene
                        self.totalvalue = self.totalvalue + combinedvalue
                    else:
                        self.totalvalue_en = self.totalvalue
                        self.totalvalue = 0
                        print(self.time_formatted, self.supply_used, "roach at position =", roach.position, "self.totalvalue_en =", self.totalvalue_en)
#check our units including itself if enemy units nearby
            onu = self.units.filter(lambda onu: not onu.is_flying and not onu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and onu.position.is_closer_than(10, roach))
            if len(self.units.filter(lambda onu: not onu.is_flying and not onu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and onu.position.is_closer_than(10, roach)).tags) > len(onu.tags):
                onu = self.units.filter(lambda onu: not onu.is_flying and not onu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and onu.position.is_closer_than(10, roach))
            if len(self.units.filter(lambda onu: not onu.is_flying and not onu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and onu.position.is_closer_than(10, roach)).tags) < len(onu.tags):
                onu = self.units.filter(lambda onu: not onu.is_flying and not onu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA) and onu.position.is_closer_than(10, roach))
            for ounit in onu:
                combinedvalue = self.calculate_unit_value(ounit.type_id).minerals + self.calculate_unit_value(ounit.type_id).vespene
                self.totalvalue = self.totalvalue + combinedvalue
            else:
                self.totalvalue_on = self.totalvalue
                self.totalvalue = 0
                print(self.time_formatted, self.supply_used, "self.totalvalue_on =", self.totalvalue_on)
            if (
                enemies_near.amount > 0
                and self.totalvalue_on > self.totalvalue_en
                or self.supply_used > 190
                and enemies_near.amount > 0
                ):
                if (
                    roach.weapon_cooldown == 0
                    ):
                    roach.attack(enemies_near.closest_to(roach))
                    print(self.time_formatted, self.supply_used, "roach unit defense, our nearby units =", self.totalvalue_on)
                    print(self.time_formatted, self.supply_used, "roach unit defense, enemy nearby units =", self.totalvalue_en)
                else:
                    if (
                        roach.target_in_range(enemies_near.closest_to(roach))
                        and enemies_near.closest_to(roach).ground_range < 4
                        ):
                        roach.move(enemies_near.closest_to(roach).position.towards(roach, 4))
                    else:
                        roach.move(enemies_near.closest_to(roach).position)
            if (
                enemies_structures_near
                and not enemies_near.amount > 0
                and self.totalvalue_on > self.totalvalue_en
                or self.supply_used > 190
                and enemies_structures_near
                and not enemies_near.amount > 0
                ):
                if (
                    roach.weapon_cooldown == 0
                    ):
                    roach.attack(enemies_structures_near.closest_to(roach))
                else:
                    roach.move(enemies_structures_near.closest_to(roach).position)
            print(self.time_formatted, self.supply_used, "roach structure defense, our nearby units =", self.totalvalue_on, enemies_structures_near.amount > 0, enemies_near.amount > 0, self.totalvalue_on > self.totalvalue_en)
            print(self.time_formatted, self.supply_used, "roach structure defense, enemy nearby units =", self.totalvalue_en)
#group
            if (
                self.totalvalue_o > 0
                and not enemies_structures_near
                and not enemies_near.amount > 0
                and self.supply_used < 180
                ):
                print(self.time_formatted, self.supply_used, "our units =", self.totalvalue_o)
                #print(self.time_formatted, self.supply_used, "enemy units =", self.totalvalue_e)
                if self.townhalls.amount > enemy_townhalls.amount and not roach.position.is_closer_than(5, self.townhalls.ready.closest_to(self.enemy_start_locations[0]).position.towards(self.enemy_start_locations[0], 7)):
                    roach.move(self.townhalls.ready.closest_to(self.enemy_start_locations[0]).position.towards(self.enemy_start_locations[0], 7))
                if self.townhalls.amount <= enemy_townhalls.amount and not roach.position.is_closer_than(5, self.townhalls.ready.closest_to(self.enemy_start_locations[0]).position.towards(self.enemy_start_locations[0], 7)):
                    roach.move(self.townhalls.closest_to(self.enemy_start_locations[0]).position.towards(self.enemy_start_locations[0], 7))
#attack units first
            if (
                self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).amount > 0
                and not enemies_structures_near
                and not enemies_near.amount > 0
                and self.supply_used > 190
                ):
                if (
                    roach.weapon_cooldown == 0
                    ):
                    roach.attack(self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).closest_to(roach))
                    print(self.time_formatted, self.supply_used, "roach unit attack, our nearby units =", self.totalvalue_on)
                    #print(self.time_formatted, self.supply_used, "roach unit attack, enemy nearby units =", self.totalvalue_en)
                else:
                    if (
                        roach.target_in_range(self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).closest_to(roach))
                        and self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).closest_to(roach).ground_range < 4
                        ):
                        roach.move(self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).closest_to(roach).position.towards(roach, 4))
                    else:
                        roach.move(self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).closest_to(roach).position)
#attack structures second
            if (
                self.enemy_structures.not_flying.amount > 0
                and not self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).amount > 0
                and not enemies_structures_near
                and not enemies_near.amount > 0
                and self.supply_used > 190
                ):
                if (
                    roach.weapon_cooldown == 0
                    ):
                    roach.attack(self.enemy_structures.not_flying.closest_to(roach))
                    print(self.time_formatted, self.supply_used, "roach structure attack, our nearby units =", self.totalvalue_on)
                    #print(self.time_formatted, self.supply_used, "roach structure attack, enemy nearby units =", self.totalvalue_en)
                else:
                    roach.move(self.enemy_structures.not_flying.closest_to(roach).position)
#attack locations last
            if (
                not self.enemy_structures.not_flying.amount > 0
                and len(roach.orders) < 1
                and not self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)).amount > 0
                and not enemies_structures_near
                and not enemies_near.amount > 0
                and self.supply_used > 190
                ):
                roach.attack(possible_base_locations[1])
                roach.attack(possible_base_locations[0], queue = True)
                roach.attack(possible_base_locations[2], queue = True)
                roach.attack(possible_base_locations[3], queue = True)

        enemies_near = Units([], self)
        enemies_structures_near = Units([], self)
    async def build_roachwarren(self):
        if not self.units(UnitTypeId.DRONE):
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        roachwarren = self.structures(UnitTypeId.ROACHWARREN)
        if (
            self.can_afford(UnitTypeId.ROACHWARREN)
            and not roachwarren
            and not self.already_pending(UnitTypeId.ROACHWARREN)
            and self.time > 150
            ):
            if (
                self.enemy_structures(UnitTypeId.ROACHWARREN)
                or self.enemy_structures(UnitTypeId.EXTRACTOR)
                or self.enemy_structures(UnitTypeId.REFINERY)
                or self.enemy_structures(UnitTypeId.ASSIMILATOR)
                or self.enemy_structures(UnitTypeId.BANELINGNEST)
                or self.enemy_units(UnitTypeId.BANELING)
                or self.enemy_units(UnitTypeId.ROACH)
                or self.enemy_units(UnitTypeId.HYDRALISK)
                or self.time > 300
                ):
                await self.build(UnitTypeId.ROACHWARREN, near = possible_base_locations[14].position.towards(self.enemy_start_locations[0], 10))

    async def build_roaches(self):
        if not self.larva:
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        larva = self.larva.random
        enemies_near = Units([], self)
                    
        for hatch in self.townhalls:
            if not enemies_near:
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                    enemies_near.extend(
                        self.enemy_units.filter(
                            lambda u: not u.is_flying
                            and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)
                            and u.distance_to(hatch) < 40
                        )
                    )
        if (
            self.supply_left > self.townhalls.ready.amount * 5
            or self.already_pending(UnitTypeId.OVERLORD) >= 1
            and not self.supply_left == 0
            or self.supply_cap > 199
            ):
            if (
                self.can_afford(UnitTypeId.ROACH)
                and self.structures(UnitTypeId.ROACHWARREN).ready
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                and enemies_near.amount > 0
                and self.townhalls.amount + self.already_pending(UnitTypeId.HATCHERY) >= enemy_townhalls.amount
                ):
                larva.train(UnitTypeId.ROACH)
                print(self.time_formatted, self.supply_used, "emergency roaches on the way")
            if (
                self.can_afford(UnitTypeId.ROACH)
                and self.structures(UnitTypeId.ROACHWARREN).ready
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                and self.totalvalue_o < self.totalvalue_e
                ):
                larva.train(UnitTypeId.ROACH)
                #print(self.time_formatted, self.supply_used, "our combat units =", self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).amount)
                #print(self.time_formatted, self.supply_used, "enemy combat units =", self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                print(self.time_formatted, self.supply_used, "too many enemies, making roaches")
            for hatch in self.townhalls:
                for gas in self.structures(UnitTypeId.EXTRACTOR):
                    if (
                        hatch.assigned_harvesters + gas.assigned_harvesters + self.already_pending(UnitTypeId.DRONE) >= hatch.ideal_harvesters + gas.ideal_harvesters
                        and self.townhalls.amount + self.already_pending(UnitTypeId.HATCHERY) > enemy_townhalls.amount
                        and self.can_afford(UnitTypeId.ROACH)
                        and self.structures(UnitTypeId.ROACHWARREN).ready
                        and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                        ):
                        larva.train(UnitTypeId.ROACH)
                        print(self.time_formatted, self.supply_used, "too many drones, making roaches")
                

    async def build_queens(self):
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        if (
            self.structures(UnitTypeId.SPAWNINGPOOL).ready
            and self.can_afford(UnitTypeId.QUEEN)
            and self.townhalls.ready.idle
            and self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) < self.townhalls.amount
            ):
            self.train(UnitTypeId.QUEEN, 1)
            
    async def split_queens(self):
        if not self.units(UnitTypeId.QUEEN):
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        for hatchery in self.townhalls.ready:
                if (
                    self.units(UnitTypeId.QUEEN).closer_than(5, hatchery).amount == 1
                    and hatchery.is_using_ability(AbilityId.TRAINQUEEN_QUEEN)
                    and hatchery.has_buff(BuffId.QUEENSPAWNLARVATIMER)
                    ):
                    #print(self.time_formatted, self.supply_used, "too many queens including trainees")                   
                    sparequeen = self.units(UnitTypeId.QUEEN).closer_than(6, hatchery).furthest_to(hatchery)
                    if sparequeen:
                            #print(self.time_formatted, self.supply_used, "there is a spare queen now because another is training")
                            for hatch in self.townhalls:
                                if (
                                    self.units(UnitTypeId.QUEEN).closer_than(5, hatch).amount < 1
                                    and self.townhalls.ready
                                    and not hatch.is_using_ability(AbilityId.TRAINQUEEN_QUEEN)
                                    ):
                                    sparequeen.move(hatch)
                                    #print(self.time_formatted, self.supply_used, "spare queen because another is training moving to lonely hatchery")
                                    break
                                elif(
                                    self.units(UnitTypeId.QUEEN).closer_than(5, hatch).amount < 1
                                    and self.townhalls.not_ready
                                    ):
                                    sparequeen.move(hatch)
                                    #print(self.time_formatted, self.supply_used, "spare queen because another is training moving to building hatchery")
                                    break
                elif (
                    self.units(UnitTypeId.QUEEN).closer_than(5, hatchery).amount > 1
                    ):
                    sparequeen = self.units(UnitTypeId.QUEEN).closer_than(5, hatchery).furthest_to(hatchery)
                    #print(self.time_formatted, self.supply_used, "too many queens")                   
                    if sparequeen:
                            for hatch in self.townhalls:
                                if (
                                    self.units(UnitTypeId.QUEEN).closer_than(5, hatch).amount < 1
                                    ):
                                    sparequeen.move(hatch)
                                    #print(self.time_formatted, self.supply_used, "spare queen out of 2 moving to lonely hatchery")
                                    break

                if self.minerals > 1000 and self.supply_used > 198:
                    await self.build(UnitTypeId.SPINECRAWLER, near = hatchery.position.towards(possible_base_locations[0], 10))
                    

    async def queen_inject(self):
        if not self.units(UnitTypeId.QUEEN):
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        for queen in self.units(UnitTypeId.QUEEN):
            if self.townhalls.ready:
                hatch = self.townhalls.ready.closest_to(queen)
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
