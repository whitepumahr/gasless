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
    closestling = False
    closestlingtag = False
    closestling2 = False
    closestling2tag = False
    mylings = False
    wallqueen = False
    wallqueentag = False
    
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

    overseer1 = False
    overseer2 = False
    overseer3 = False
    overseer4 = False
    overseer5 = False
    overseer6 = False
    overseer1tag = False
    overseer2tag = False
    overseer3tag = False
    overseer4tag = False
    overseer5tag = False
    overseer6tag = False
    
    async def on_start(self):
        print("Game started")
        self.client.game_step = 2
        global possible_base_locations
        possible_base_locations = sorted(self.expansion_locations_list, key=lambda p: p.distance_to(self.start_location), reverse=True)
        print("player 1 or 2", self.player_id)
        print(self.game_info.map_name)
        print(self.expansion_locations_list)
        global o1p
        o1p = False
        global o2p
        o2p = False
        global o3p
        o3p = False
        global ourmain
        global ournat
        global our3rd
        global wql
        global our4th
        global our5th
        global our6th
        global our7th
        global our8th
        global our9th
        wql = False
        our9th = False
        global enemymain
        global enemynat
        global enemy3rd
        global enemy4th
        global enemy5th
        global enemy6th
        global enemy7th
        global enemy8th
        global enemy9th
        global roachwarrenwall
        global evowall1
        global evowall2
        enemy9th = False
        roachwarrenwall = False
        evowall1 = False
        evowall2 = False
        if self.game_info.map_name == "Berlingrad AIE":
            print(self.game_info.map_name)
            ourmain = possible_base_locations[-1]
            ournat = possible_base_locations[-2]
            our3rd = possible_base_locations[-3]
            our4th = possible_base_locations[-5]
            our5th = possible_base_locations[-4]
            our6th = possible_base_locations[-6]
            our7th = possible_base_locations[-7]
            our8th = possible_base_locations[-8]
            enemymain = possible_base_locations[0]
            enemynat = possible_base_locations[1]
            enemy3rd = possible_base_locations[5]
            enemy4th = possible_base_locations[4]
            enemy5th = possible_base_locations[2]
            enemy6th = possible_base_locations[6]
            enemy7th = possible_base_locations[3]
            enemy8th = possible_base_locations[8]
            print(ourmain)
            if ourmain == (120.5, 24.5):
                roachwarrenwall = (116.5, 53.5)
                evowall1 = (113.5, 51.5)
                evowall2 = (118.5, 57.5)
                wql = (117.8, 55.5)
                o1p = (58, 150)
                o2p = (12, 94)
                o3p = (56, 94)
            else:
                roachwarrenwall = (35.5, 102.5)
                evowall1 = (38.5, 104.5)
                evowall2 = (33.5, 98.5)
                wql = (34.2, 100.5)
                o1p = (95, 9)
                o2p = (62, 139)
                o3p = (96, 62)
                
        if self.game_info.map_name == "Hardwire AIE":
            print(self.game_info.map_name)
            ourmain = possible_base_locations[-1]
            ournat = possible_base_locations[-2]
            our3rd = possible_base_locations[-5]
            our4th = possible_base_locations[-3]
            our5th = possible_base_locations[-6]
            our6th = possible_base_locations[-4]
            our7th = possible_base_locations[-8]
            our8th = possible_base_locations[6]
            enemymain = possible_base_locations[0]
            enemynat = possible_base_locations[1]
            enemy3rd = possible_base_locations[2]
            enemy4th = possible_base_locations[3]
            enemy5th = possible_base_locations[7]
            enemy6th = possible_base_locations[4]
            enemy7th = possible_base_locations[5]
            enemy8th = possible_base_locations[-7]
            print(ourmain)
            if ourmain == (157.5, 157.5):
                roachwarrenwall = (125.5, 164.5)
                evowall1 = (128.5, 162.5)
                evowall2 = (130.5, 158.5)
                wql = (129.8, 160.5)
                o1p = (44, 80)
                o2p = (95, 38)
                o3p = (96, 76)
            else:
                roachwarrenwall = (90.5, 51.5)
                evowall1 = (87.5, 53.5)
                evowall2 = (85.5, 57.5)
                wql = (86.2, 55.5)
                o1p = (170, 140)
                o2p = (119, 185)
                o3p = (120, 140)
                
        if self.game_info.map_name == "Inside and OutAIE":
            print(self.game_info.map_name)
            ourmain = possible_base_locations[-1]
            ournat = possible_base_locations[-2]
            our3rd = possible_base_locations[-3]
            our4th = possible_base_locations[-5]
            our5th = possible_base_locations[-4]
            our6th = possible_base_locations[-6]
            our7th = possible_base_locations[-7]
            our8th = possible_base_locations[-8]
            enemymain = possible_base_locations[0]
            enemynat = possible_base_locations[1]
            enemy3rd = possible_base_locations[3]
            enemy4th = possible_base_locations[2]
            enemy5th = possible_base_locations[4]
            enemy6th = possible_base_locations[5]
            enemy7th = possible_base_locations[6]
            enemy8th = possible_base_locations[7]
            print(ourmain)
            if ourmain == (126.5, 129.5):
                roachwarrenwall = (94.5, 125.5)
                evowall1 = (97.5, 123.5)
                evowall2 = (101.5, 122.5)
                wql = (99.5, 123.8)
                o1p = (18, 54)
                o2p = (75, 13)
                o3p = (62, 60)
            else:
                roachwarrenwall = (65.5, 34.5)
                evowall1 = (62.5, 36.5)
                evowall2 = (58.5, 37.5)
                wql = (60.5, 36.2)
                o1p = (142, 107)
                o2p = (84, 150)
                o3p = (98, 100)
            
        if self.game_info.map_name == "MoondanceAIE":
            print(self.game_info.map_name)
            ourmain = possible_base_locations[-1]
            ournat = possible_base_locations[-3]
            our3rd = possible_base_locations[-4]
            our4th = possible_base_locations[-2]
            our5th = possible_base_locations[-6]
            our6th = possible_base_locations[-5]
            our7th = possible_base_locations[-8]
            our8th = possible_base_locations[-10]
            our9th = possible_base_locations[-7]
            enemymain = possible_base_locations[1]
            enemynat = possible_base_locations[4]
            enemy3rd = possible_base_locations[0]
            enemy4th = possible_base_locations[5]
            enemy5th = possible_base_locations[6]
            enemy6th = possible_base_locations[3]
            enemy7th = possible_base_locations[2]
            enemy8th = possible_base_locations[7]
            enemy9th = possible_base_locations[9]
            print(ourmain)
            if ourmain == (119.5, 43.5):
                roachwarrenwall = (130.5, 72.5)
                evowall1 = (131.5, 75.5)
                evowall2 = (126.5, 71.5)
                wql = (128.5, 71.2)
                o1p = (96, 177)
                o2p = (39, 139)
                o3p = (68, 112)
            else:
                roachwarrenwall = (60.5, 128.5)
                evowall1 = (65.5, 132.5)
                evowall2 = (61.5, 131.5)
                wql = (63.5, 132.8)
                o1p = (97, 30)
                o2p = (154, 84)
                o3p = (124, 92)
            
        if self.game_info.map_name == "StargazersAIE":
            print(self.game_info.map_name)
            ourmain = possible_base_locations[-1]
            ournat = possible_base_locations[-2]
            our3rd = possible_base_locations[-4]
            our4th = possible_base_locations[-5]
            our5th = possible_base_locations[-3]
            our6th = possible_base_locations[-6]
            our7th = possible_base_locations[-9]
            our8th = possible_base_locations[-13]
            enemymain = possible_base_locations[3]
            enemynat = possible_base_locations[2]
            enemy3rd = possible_base_locations[6]
            enemy4th = possible_base_locations[1]
            enemy5th = possible_base_locations[5]
            enemy6th = possible_base_locations[0]
            enemy7th = possible_base_locations[4]
            enemy8th = possible_base_locations[7]
            print(ourmain)
            if ourmain == (39.5, 123.5):
                roachwarrenwall = (46.5, 94.5)
                evowall1 = (49.5, 96.5)
                evowall2 = (47.5, 90.5)
                wql = (47.2, 92.5)
                o1p = (136, 145)
                o2p = (172, 82)
                o3p = (124, 106)
            else:
                roachwarrenwall = (153.5, 94.5)
                evowall1 = (150.5, 96.5)
                evowall2 = (152.5, 90.5)
                wql = (153.8, 92.5)
                o1p = (62, 145)
                o2p = (27, 83)
                o3p = (76, 106)
            
        if self.game_info.map_name == "WaterfallAIE":
            print(self.game_info.map_name)
            ourmain = possible_base_locations[-1]
            ournat = possible_base_locations[-2]
            our3rd = possible_base_locations[-3]
            our4th = possible_base_locations[-5]
            our5th = possible_base_locations[-4]
            our6th = possible_base_locations[-8]
            our7th = possible_base_locations[-7]
            our8th = possible_base_locations[-6]
            enemymain = possible_base_locations[0]
            enemynat = possible_base_locations[1]
            enemy3rd = possible_base_locations[4]
            enemy4th = possible_base_locations[2]
            enemy5th = possible_base_locations[3]
            enemy6th = possible_base_locations[5]
            enemy7th = possible_base_locations[8]
            enemy8th = possible_base_locations[7]
            print(ourmain)
            if ourmain == (113.5, 127.5):
                roachwarrenwall = (82.5, 125.5)
                evowall1 = (85.5, 124.5)
                evowall2 = (87.5, 121.5)
                wql = (86.5, 119.5)
                o1p = (17, 47)
                o2p = (69, 14)
                o3p = (62.5, 59.5)
            else:
                roachwarrenwall = (61.5, 30.5)
                evowall1 = (58.5, 31.5)
                evowall2 = (56.5, 34.5)
                wql = (57.5, 36.5)
                o1p = (126, 111)
                o2p = (74, 144)
                o3p = (81.5, 97.5)
            
        print("possible base locations for this map =", possible_base_locations)
        global scouts
        scouts = {UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}
        global scouted
        scouted = False
        
        self.larva.random.train(UnitTypeId.DRONE)
        self.units(UnitTypeId.DRONE).closest_to(enemymain).move(enemymain.position.towards(ourmain, 2.8))
        self.units(UnitTypeId.DRONE).closest_to(enemymain).move(enemymain.position.towards(enemynat, -2.8), queue = True)
        self.units(UnitTypeId.DRONE).closest_to(enemymain).move(enemymain.position.towards(ourmain, 2.8), queue = True)
        self.units(UnitTypeId.DRONE).closest_to(enemymain).move(enemymain.position.towards(enemynat, -2.8), queue = True)
        self.units(UnitTypeId.DRONE).closest_to(enemymain).move(enemymain.position.towards(ourmain, 2.8), queue = True)
        self.units(UnitTypeId.OVERLORD).closest_to(enemymain).move(Point2(o1p))
        self.structures(UnitTypeId.HATCHERY).closest_to(ourmain).smart(self.structures(UnitTypeId.HATCHERY).closest_to(ourmain))

        self.overlord1tag = self.units(UnitTypeId.OVERLORD).closest_to(enemymain).tag
        self.overlord1 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord1tag)

        await self.chat_send("You can thank Ratosh and the rest of the very helpful sc2 botting community for what's about to happen to you, GLHF!")


    async def on_step(self, iteration: int):
        await self.build_tech()
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
        await self.build_wall()
        await self.build_hydras()

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
        need_drones = False
        local_mineral_workers = Units([], self)
        spare_mineral_workers = Units([], self)

        if (
            self.game_info.map_name == "StargazersAIE"
            and self.supply_workers > 16
            and self.mineral_field.closer_than(3, our3rd)
            and self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) > 0
            ):
            for drone in self.workers.closest_n_units(our3rd, 4):
                if not drone.is_carrying_minerals and not drone.orders == self.mineral_field.closer_than(3, our3rd).closest_to(ourmain):
                    drone.gather(self.mineral_field.closer_than(3, our3rd).closest_to(ourmain))
                    drone.gather(self.mineral_field.closer_than(3, our3rd).furthest_to(ourmain), queue = True)
                if drone.is_returning:
                    drone.gather(self.mineral_field.closest_to(ourmain), queue = True)
            

        for base in bases:
            local_minerals_tags = {mineral.tag for mineral in self.mineral_field if mineral.distance_to(base) <= 8}
            local_mineral_workers.extend(self.workers.filter(lambda unit: unit.order_target in local_minerals_tags or (unit.is_carrying_minerals and unit.order_target == base.tag)))
            if base.surplus_harvesters < 0:
                need_drones = True
            if base.surplus_harvesters > 0:
                del local_mineral_workers[:base.ideal_harvesters]
                spare_mineral_workers.extend(local_mineral_workers)
                

        for base in bases:
#worker balance
            if base.surplus_harvesters < 0 and spare_mineral_workers:
                for worker in spare_mineral_workers.take(abs(base.surplus_harvesters)):
                    if self.townhalls.ready.filter(lambda t: t.surplus_harvesters < 0):
                        worker.gather(self.mineral_field.closest_to(self.townhalls.ready.filter(lambda t: t.surplus_harvesters < 0).closest_to(worker)))
                    elif need_drones == False:
                        worker.gather(self.mineral_field.closest_to(base))
#idle worker                    
            for worker in self.workers.idle:
                if self.townhalls.ready.filter(lambda t: t.surplus_harvesters < 0):
                    worker.gather(self.mineral_field.closest_to(self.townhalls.ready.filter(lambda t: t.surplus_harvesters < 0).closest_to(worker)))
                elif need_drones == False:
                    worker.gather(self.mineral_field.closest_to(base))
#fill gas first
            for gas in gas_buildings:
                local_gas_workers = self.workers.filter(lambda unit:  unit.order_target == gas.tag or (unit.is_carrying_vespene and unit.order_target == gas.tag))
                if gas.surplus_harvesters < 0:
                    if self.minerals > self.vespene * 2:
                        print(self.time_formatted, self.supply_used, "need more workers")
                        for worker in local_mineral_workers.take(abs(gas.surplus_harvesters)):
                            print(self.time_formatted, self.supply_used, gas.surplus_harvesters)
                            print(self.time_formatted, self.supply_used, worker)
                            worker.gather(gas)
                            print(self.time_formatted, self.supply_used, gas.surplus_harvesters)
                            print(self.time_formatted, self.supply_used, "gathering gas")
                if gas.surplus_harvesters > 0:
                    for worker in local_gas_workers.take(abs(gas.surplus_harvesters)):
                        print(self.time_formatted, self.supply_used, gas.surplus_harvesters)
                        print(self.time_formatted, self.supply_used, worker)
                        worker.gather(self.mineral_field.closest_to(base))
                    print(self.time_formatted, self.supply_used, "Too many gas workers here")
                if self.vespene > self.minerals * 2 and self.vespene > 200 or self.workers.amount < 9:
                    for worker in local_gas_workers:
                        if self.townhalls.ready.filter(lambda t: t.surplus_harvesters < 0):
                            worker.gather(self.mineral_field.closest_to(self.townhalls.ready.filter(lambda t: t.surplus_harvesters < 0).closest_to(worker)))
                        elif need_drones == False:
                            worker.gather(self.mineral_field.closest_to(base))
                    
                        
                    
                

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
        stillaggression = False
        print(self.time_formatted, self.supply_used, "worker cap =", (enemy_townhalls.amount * 16) + (enemy_townhalls.amount * 4) + (enemy_gas_buildings.amount * 3))
                    
        for hatch in self.townhalls:
            if not enemies_near:
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                    enemies_near.extend(
                        self.enemy_units.filter(
                            lambda u: not u.is_flying
                            and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                            and u.distance_to(hatch) < 40
                        )
                    )
        if self.can_afford(UnitTypeId.DRONE) and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < self.townhalls.amount * 8:
            larva.train(UnitTypeId.DRONE)

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
        if self.time > 180:
            if enemy_townhalls.amount < 2:
                stillaggression = True
        if self.time > 46:
            print(self.time_formatted, self.supply_used, "enemy workers = ", self.enemyworkers)
#if macro
            if self.enemyworkers > 14 and not stillaggression:
                print(self.time_formatted, self.supply_used, "Enemy is playing macro")
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
                if self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount * 16) + (enemy_townhalls.amount * 4) + (enemy_gas_buildings.amount * 3):
                    if not self.structures(UnitTypeId.EXTRACTOR):
                        if (
                            self.can_afford(UnitTypeId.DRONE)
                            and self.townhalls.amount > 1
                            and not enemies_near.amount > 0
                            and self.totalvalue_o >= self.totalvalue_e
                            and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 120
                            ):
                            if (
                                self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) >= self.townhalls.amount
                                or self.already_pending(UnitTypeId.QUEEN) == self.townhalls.ready.amount
                                ):
                                for hatch in self.townhalls:
                                    if (
                                        hatch.assigned_harvesters + self.already_pending(UnitTypeId.DRONE) < hatch.ideal_harvesters
                                        and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount * 16) + (enemy_townhalls.amount * 4) + (enemy_gas_buildings.amount * 3)
                                        ):
                                        if (
                                            self.already_pending(UnitTypeId.ZERGLING) + self.units(UnitTypeId.ZERGLING).amount >= 2
                                            or self.units(UnitTypeId.ZERGLING).amount >= 2
                                            or self.already_pending(UnitTypeId.ZERGLING) > 0
                                            ):
                                            if (
                                                self.townhalls.amount > enemy_townhalls.amount
                                                or self.townhalls.ready.amount + self.already_pending(UnitTypeId.HATCHERY) > enemy_townhalls.amount
                                                ):
                                                if self.supply_used > 22 and self.supply_used < 36:
                                                    if (
                                                        self.already_pending(UnitTypeId.OVERLORD) + self.units(UnitTypeId.OVERLORD).amount >= 3
                                                        and not self.supply_left == 0
                                                        ):
                                                        larva.train(UnitTypeId.DRONE)
                                                        print(self.time_formatted, self.supply_used, "macro droning before third overlord")
                                            if (
                                                self.townhalls.amount > enemy_townhalls.amount
                                                or self.townhalls.ready.amount + self.already_pending(UnitTypeId.HATCHERY) > enemy_townhalls.amount
                                                ):
                                                if (
                                                    self.supply_used > 35 and self.supply_used < 39 and self.already_pending(UnitTypeId.OVERLORD) + self.units(UnitTypeId.OVERLORD).amount >= 6
                                                    and not self.supply_left == 0
                                                    ):
                                                    larva.train(UnitTypeId.DRONE)
                                                    print(self.time_formatted, self.supply_used, "macro droning before fourth overlord")
                                            if (
                                                self.townhalls.amount > enemy_townhalls.amount
                                                or self.townhalls.ready.amount + self.already_pending(UnitTypeId.HATCHERY) > enemy_townhalls.amount
                                                ):
                                                if (
                                                    self.supply_used > 38 and self.supply_used < 49 and self.already_pending(UnitTypeId.OVERLORD) + self.units(UnitTypeId.OVERLORD).amount >= 6
                                                    and not self.supply_left == 0
                                                    ):
                                                    larva.train(UnitTypeId.DRONE)
                                                    print(self.time_formatted, self.supply_used, "macro droning before fifth overlord")
                                            if (
                                                self.townhalls.amount > enemy_townhalls.amount
                                                or self.townhalls.ready.amount + self.already_pending(UnitTypeId.HATCHERY) > enemy_townhalls.amount
                                                ):
                                                if self.structure_type_build_progress(UnitTypeId.ROACHWARREN) == 0:
                                                    if (
                                                        self.supply_left > self.townhalls.ready.amount * 4
                                                        or self.already_pending(UnitTypeId.OVERLORD) >= self.townhalls.ready.amount
                                                        and not self.supply_left == 0
                                                        ):
                                                        larva.train(UnitTypeId.DRONE)
                                                        print(self.time_formatted, self.supply_used, "macro droning after fifth overlord")
                                            if (
                                                self.townhalls.amount > enemy_townhalls.amount
                                                or self.townhalls.ready.amount + self.already_pending(UnitTypeId.HATCHERY) > enemy_townhalls.amount
                                                ):
                                                if (
                                                    self.structure_type_build_progress(UnitTypeId.ROACHWARREN) > 0
                                                    ):
                                                    if (
                                                        self.supply_left > self.townhalls.ready.amount * 6
                                                        or self.already_pending(UnitTypeId.OVERLORD) >= self.townhalls.amount
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
                        if self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource):
                            self.closestdronee1tag = self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource).closest_to(ournat).tag
                    if self.closestdronee1tag:
                        self.closestdronee1 = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronee1tag)
                    if self.closestdronee1:
                        if (
                            not self.enemy_units.not_flying.closer_than(5, ournat).amount > 0
                            and not self.enemy_structures.not_flying.closer_than(5, ournat).amount > 0
                            and self.closestdronee1
                            ):
                            self.closestdronee1.move(ournat)
                            print(self.time_formatted, self.supply_used, "16 hatch drone moving to new expansion location")
                            if self.can_afford(UnitTypeId.HATCHERY):
                                self.closestdronee1.build(UnitTypeId.HATCHERY, ournat)
                        if (
                            self.enemy_units.not_flying.closer_than(5, ournat).amount > 0
                            or self.enemy_structures.not_flying.closer_than(5, ournat).amount > 0
                            ):
                            self.closestdronee1.move(our3rd)
                            print(self.time_formatted, self.supply_used, "16 hatch drone moving to new alternate expansion location")
                            if self.can_afford(UnitTypeId.HATCHERY) and not self.mineral_field.closer_than(3, our3rd):
                                self.closestdronee1.build(UnitTypeId.HATCHERY, our3rd)
                        if (
                            self.enemy_units.not_flying.closer_than(5, ournat).amount > 0
                            or self.enemy_structures.not_flying.closer_than(5, ournat).amount > 0
                            ):
                            if self.mineral_field.closer_than(3, our3rd):
                                self.closestdronee1.move(our4th)
                                if self.can_afford(UnitTypeId.HATCHERY):
                                    self.closestdronee1.build(UnitTypeId.HATCHERY, our4th)
                            
#17 pool
                if (
                    self.minerals > 150
                    and not self.structures(UnitTypeId.SPAWNINGPOOL)
                    and self.townhalls.amount > 1
                    and not self.already_pending(UnitTypeId.SPAWNINGPOOL)
                    ):
                    if not self.closestdronesptag or not self.closestdronesp:
                        if self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource):
                            self.closestdronesptag = self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource).closest_to(ourmain.position.towards(enemymain, -10)).tag
                    if self.closestdronesptag:
                        self.closestdronesp = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronesptag)
                    if self.closestdronesp:
                        if not self.enemy_units.closer_than(4, ourmain.position.towards(enemymain, -10)):
                            self.closestdronesp.move(ourmain.position.towards(enemymain, -10))
                            print(self.time_formatted, self.supply_used, "17 pool drone moving to pool build location")
                            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                                if not self.game_info.map_name == "MoondanceAIE":
                                    self.closestdronesp.build(UnitTypeId.SPAWNINGPOOL, ourmain.position.towards(enemymain, -10))
                                    print(self.time_formatted, self.supply_used, "Emergency pool drone building pool at build location")
                                elif self.game_info.map_name == "MoondanceAIE":
                                    self.closestdronesp.build(UnitTypeId.SPAWNINGPOOL, ourmain.position.towards(enemymain, -9))
                                    print(self.time_formatted, self.supply_used, "Emergency pool drone building pool at moondance build location")
                        if self.enemy_units.closer_than(4, ourmain.position.towards(enemymain, -10)):
                            self.closestdronesp.move(ourmain.position.towards(ournat, -10))
                            print(self.time_formatted, self.supply_used, "17 pool drone moving to alternate pool build location")
                            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                                self.closestdronesp.build(UnitTypeId.SPAWNINGPOOL, ourmain.position.towards(ournat, -10))
#19 hatch
                if (
                    self.minerals > 100
                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) > 18
                    and not self.townhalls.amount > 2
                    ):
                    if not self.closestdronee2tag or not self.closestdronee2:
                        if self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource):
                            self.closestdronee2tag = self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource).closest_to(our3rd).tag
                    if self.closestdronee2tag:
                        self.closestdronee2 = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronee2tag)
                    if self.closestdronee2:
                        if (
                            not self.enemy_units.not_flying.closer_than(5, our3rd).amount > 0
                            and not self.enemy_structures.not_flying.closer_than(5, our3rd).amount > 0
                            and self.closestdronee2
                            ):
                            if self.game_info.map_name == "StargazersAIE" and not self.mineral_field.closer_than(3, our3rd):
                                self.closestdronee2.move(our3rd)
                                print(self.time_formatted, self.supply_used, "19 hatch drone moving to new expansion location")
                                if self.can_afford(UnitTypeId.HATCHERY):
                                    self.closestdronee2.build(UnitTypeId.HATCHERY, our3rd)
                            elif not self.game_info.map_name == "StargazersAIE":
                                self.closestdronee2.move(our3rd)
                                print(self.time_formatted, self.supply_used, "19 hatch drone moving to new expansion location")
                                if self.can_afford(UnitTypeId.HATCHERY):
                                    self.closestdronee2.build(UnitTypeId.HATCHERY, our3rd)
                        if (
                            self.enemy_units.not_flying.closer_than(5, our3rd).amount > 0
                            or self.enemy_structures.not_flying.closer_than(5, our3rd).amount > 0
                            ):
                            self.closestdronee2.move(our6th)
                            print(self.time_formatted, self.supply_used, "19 hatch drone moving to new alternate expansion location")
                            if self.can_afford(UnitTypeId.HATCHERY):
                                self.closestdronee2.build(UnitTypeId.HATCHERY, our6th)
                    if self.closestdronee2:
                        if (
                            self.supply_left > self.townhalls.amount
                            or self.already_pending(UnitTypeId.OVERLORD) >= 1
                            and not self.supply_left == 0
                            ):
                            if (
                                self.can_afford(UnitTypeId.DRONE)
                                and self.townhalls.amount < 3
                                and enemy_gas_buildings.amount < 1
                                and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 20
                                ):
                                larva.train(UnitTypeId.DRONE)
                                print(self.time_formatted, self.supply_used, "19 hatch up to 20 drones")
#if early aggression

#early aggression back to droning after ling scout if we overbuilt units
            if self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount * 16) + (enemy_townhalls.amount * 4) + (enemy_gas_buildings.amount * 3):
                for hatch in self.townhalls:
                    for gas in self.structures(UnitTypeId.EXTRACTOR):
                        if (
                            self.supply_left > self.townhalls.amount + self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) * 3
                            or self.already_pending(UnitTypeId.OVERLORD) >= 2
                            and not self.supply_left == 0
                            ):
                            if (
                                self.already_pending(UnitTypeId.ZERGLING) + self.units(UnitTypeId.ZERGLING).amount >= 2
                                or self.units(UnitTypeId.ZERGLING).amount >= 2
                                or self.already_pending(UnitTypeId.ZERGLING) > 0
                                ):
                                if (
                                    self.can_afford(UnitTypeId.DRONE)
                                    and self.time > 134
                                    and not enemies_near.amount > 0
                                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 120
                                    ):
                                    if self.totalvalue_o >= self.totalvalue_e or self.units(UnitTypeId.ZERGLING).amount * 25 + self.already_pending(UnitTypeId.ZERGLING) * 50 + self.units(UnitTypeId.ROACH).amount * 100 + self.already_pending(UnitTypeId.ROACH) * 100  >= self.totalvalue_e:
                                        if hatch.assigned_harvesters + gas.assigned_harvesters + self.already_pending(UnitTypeId.DRONE) < hatch.ideal_harvesters + gas.ideal_harvesters:
                                            larva.train(UnitTypeId.DRONE)
                                            print(self.time_formatted, self.supply_used, "our combat units =", self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).amount)
                                            print(self.time_formatted, self.supply_used, "enemy combat units =", self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
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
                        if self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource):
                            self.closestdronesptag = self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource).closest_to(ourmain.position.towards(enemymain, -10)).tag
                    if self.closestdronesptag:
                        self.closestdronesp = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronesptag)
                    if self.closestdronesp:
                        if not self.already_pending(UnitTypeId.SPAWNINGPOOL) and not self.enemy_units.closer_than(3, ourmain.position.towards(enemymain, -10)):
                            self.closestdronesp.move(ourmain.position.towards(enemymain, -10))
                            print(self.time_formatted, self.supply_used, "Emergency pool drone moving to pool build location")
                            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                                if not self.game_info.map_name == "MoondanceAIE":
                                    self.closestdronesp.build(UnitTypeId.SPAWNINGPOOL, ourmain.position.towards(enemymain, -10))
                                    print(self.time_formatted, self.supply_used, "Emergency pool drone building pool at build location")
                                elif self.game_info.map_name == "MoondanceAIE":
                                    self.closestdronesp.build(UnitTypeId.SPAWNINGPOOL, ourmain.position.towards(enemymain, -9))
                                    print(self.time_formatted, self.supply_used, "Emergency pool drone building pool at moondance build location")
                        if not self.already_pending(UnitTypeId.SPAWNINGPOOL) and self.enemy_units.closer_than(3, ourmain.position.towards(enemymain, -10)):
                            self.closestdronesp.move(ourmain.position.towards(ournat, 10))
                            print(self.time_formatted, self.supply_used, "Emergency pool drone moving to pool build location")
                            if self.can_afford(UnitTypeId.SPAWNINGPOOL):
                                self.closestdronesp.build(UnitTypeId.SPAWNINGPOOL, ourmain.position.towards(ournat, 10))
                                print(self.time_formatted, self.supply_used, "Emergency pool drone building pool at alternate build location")
                if (
                    self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) > 0
                    and self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) < 0.2
                    and self.supply_workers + self.already_pending(UnitTypeId.DRONE) < 17
                    and self.can_afford(UnitTypeId.DRONE)
                    ):
                    larva.train(UnitTypeId.DRONE)
                    print(self.time_formatted, self.supply_used, "Drone while emergency pool starts")
#emergency roach warren
                if (
                    self.minerals > 100
                    and self.structure_type_build_progress(UnitTypeId.SPAWNINGPOOL) > 0.95
                    and not self.structures(UnitTypeId.ROACHWARREN)
                    and not self.already_pending(UnitTypeId.ROACHWARREN)
                    and self.time < 120
                    ):
                    if enemy_gas_buildings.amount > 0:
                        if not self.closestdronerwtag or not self.closestdronerw:
                            if self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource):
                                self.closestdronerwtag = self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource).closest_to(ourmain.position.towards(enemynat, 7)).tag
                        if self.closestdronerwtag:
                            self.closestdronerw = self.units(UnitTypeId.DRONE).find_by_tag(self.closestdronerwtag)
                            if (
                                not self.enemy_units.closer_than(3, ourmain.position.towards(enemynat, 7))
                                and not self.structures(UnitTypeId.SPAWNINGPOOL).closer_than(3, ourmain.position.towards(enemynat, 7))
                                ):
                                self.closestdronerw.move(ourmain.position.towards(enemynat, 7))
                                print(self.time_formatted, self.supply_used, "Emergency roach warren drone moving to roach warren location")
                                if self.can_afford(UnitTypeId.ROACHWARREN):
                                    self.closestdronerw.build(UnitTypeId.ROACHWARREN, ourmain.position.towards(enemynat, 7))
                            elif (
                                self.enemy_units.closer_than(3, ourmain.position.towards(enemynat, 7))
                                or self.structures(UnitTypeId.SPAWNINGPOOL).closer_than(3, ourmain.position.towards(enemynat, 7))
                                ):
                                self.closestdronerw.move(ourmain.position.towards(ournat, 7))
                                print(self.time_formatted, self.supply_used, "Emergency roach warren drone moving to alternate roach warren location")
                                if self.can_afford(UnitTypeId.ROACHWARREN):
                                    self.closestdronerw.build(UnitTypeId.ROACHWARREN, ourmain.position.towards(ournat, 7))
                                    
            if self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount * 16) + (enemy_townhalls.amount * 4) + (enemy_gas_buildings.amount * 3):
                if self.time > 240 and not enemies_near and self.can_afford(UnitTypeId.DRONE):
                    if (
                        self.supply_left > self.townhalls.ready.amount * 4
                        or self.already_pending(UnitTypeId.OVERLORD) >= 1
                        and not self.supply_left == 0
                        ):
                        if self.structures(UnitTypeId.ROACHWARREN) or self.time < 300:
                            if self.supply_left > self.townhalls.ready.amount * 6:
                                larva.train(UnitTypeId.DRONE)
                                print("worker made")


    async def build_overlords(self):
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        enemies_near = Units([], self)
        enemies_structures_near = Units([], self)
        changeling = self.units.filter(lambda c: c.type_id in (UnitTypeId.CHANGELING, UnitTypeId.CHANGELINGZEALOT, UnitTypeId.CHANGELINGMARINESHIELD, UnitTypeId.CHANGELINGMARINE, UnitTypeId.CHANGELINGZERGLINGWINGS, UnitTypeId.CHANGELINGZERGLING))
        
#hatchery zonal defense system
#enemy units near hatcheries
        for hatch in self.townhalls:
            if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                enemies_near.extend(
                    self.enemy_units.filter(
                        lambda u: not u.is_flying
                        and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                        and u.distance_to(hatch) < 40
                    )
                )
                
#enemy structures near hatcheries
            if self.enemy_structures.not_flying.closer_than(40, hatch):
                enemies_structures_near.extend(
                    self.enemy_structures.filter(
                        lambda s: not s.is_flying
                        and s.distance_to(hatch) < 40
                    )
                )
        
#position overlords
        if not self.units(UnitTypeId.OVERLORD):
            return

#overlord 1
        if not self.overlord1 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord3:
            self.overlord1tag = self.overlord3tag
            self.overlord1 = self.overlord3
            self.overlord3 = False
        if self.overlord1tag:
            self.overlord1 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord1tag)
        if self.overlord1 and self.time > 210:
            self.overlord1.move(Point2(o1p))
            
        if self.overlord1 and self.can_afford(UnitTypeId.OVERSEER) and self.units(UnitTypeId.OVERSEER).amount + self.already_pending(UnitTypeId.OVERSEER) < 1 and self.structures(UnitTypeId.LAIR).ready:
            self.overlord1.build(UnitTypeId.OVERSEER)
            
#overlord 2
        if not self.overlord2 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord3:
            self.overlord2tag = self.overlord3tag
            self.overlord2 = self.overlord3
            self.overlord3 = False
        if self.units(UnitTypeId.OVERLORD).amount == 2:
            self.overlord2tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord2tag:
            self.overlord2 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord2tag)
        if self.overlord2:
            if (
                enemy_townhalls.amount > 1
                and self.time < 150
                ):
                self.overlord2.move(Point2(o2p))
            if self.time < 60:
                self.overlord2.move(enemynat.position.towards(enemymain, -10))
            if (
                enemy_gas_buildings.amount > 0
                and enemy_townhalls.amount < 2
                ):
                if self.time < 120:
                    self.overlord2.move(enemynat.position.towards(enemymain, -10))
            elif (
                enemy_gas_buildings.amount < 1
                and self.time > 210
                or enemy_townhalls.amount > 1
                and self.time > 210
                ):
                self.overlord2.move(Point2(o2p))

        if self.overlord2 and self.can_afford(UnitTypeId.OVERSEER) and self.units(UnitTypeId.OVERSEER).amount + self.already_pending(UnitTypeId.OVERSEER) < 2 and self.structures(UnitTypeId.LAIR).ready:
            self.overlord2.build(UnitTypeId.OVERSEER)

#overlordscout
        if (
            self.time > 179
            and self.time < 181
            ):
            print(self.time_formatted, self.supply_used, "overlord scout 3min")
            if enemy_gas_buildings.amount < 1 or scouted == False:
                if self.overlord1:
                    self.overlord1.move(enemymain.position.towards(enemynat, -4.5))
                    self.overlord1.move(enemymain.position.towards(enemynat, -35), queue = True)
                    scouted == True
                if self.overlord2:
                    self.overlord2.move(enemynat.position.towards(enemymain, -4.5))
                    self.overlord2.move(enemynat.position.towards(enemymain, -24), queue = True)
                    scouted == True
                print(self.time_formatted, self.supply_used, "Overlord scout initiated 3:00")
        if (
            self.time > 164
            and self.time < 166
            ):
            print(self.time_formatted, self.supply_used, "overlord scout 2:45")
            if enemy_gas_buildings.amount > 0:
                if self.overlord1:
                    self.overlord1.move(enemymain.position.towards(enemynat, -4.5))
                    self.overlord1.move(enemymain.position.towards(enemynat, -35), queue = True)
                    scouted == True
                if self.overlord2:
                    self.overlord2.move(enemynat.position.towards(enemymain, -4.5))
                    self.overlord2.move(enemynat.position.towards(enemymain, -24), queue = True)
                    scouted == True
                    print(self.time_formatted, self.supply_used, "Overlord scout initiated 2:45")

            
#overlord 3        
        if not self.overlord3 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord4:
            self.overlord3tag = self.overlord4tag
            self.overlord3 = self.overlord4
            self.overlord4 = False
        if self.units(UnitTypeId.OVERLORD).amount == 3:
            self.overlord3tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord3tag:
            self.overlord3 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord3tag)
        if self.overlord3:
            self.overlord3.move(Point2(o3p))
            
        if self.overlord3 and self.can_afford(UnitTypeId.OVERSEER) and self.units(UnitTypeId.OVERSEER).amount + self.already_pending(UnitTypeId.OVERSEER) < 3 and self.structures(UnitTypeId.LAIR).ready:
            self.overlord3.build(UnitTypeId.OVERSEER)
            
#overlord 4
        if not self.overlord4 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord5:
            self.overlord4tag = self.overlord5tag
            self.overlord4 = self.overlord5
            self.overlord5 = False
        if self.units(UnitTypeId.OVERLORD).amount == 4:
            self.overlord4tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord4tag:
            self.overlord4 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord4tag)
        if self.overlord4 and not enemy_townhalls.closer_than(4, enemy3rd):
            self.overlord4.move(enemy3rd.position.towards(ournat, 15))
        elif self.overlord4 and enemy_townhalls.closer_than(4, enemy3rd):
            self.overlord4.move(enemy4th.position.towards(ournat, 15))
        elif self.overlord4 and enemy_townhalls.closer_than(4, enemy4th):
            self.overlord4.move(enemy5th.position.towards(ournat, 15))
        elif self.overlord4 and enemy_townhalls.closer_than(4, enemy5th):
            self.overlord4.move(enemy6th.position.towards(ournat, 15))
        elif self.overlord4 and enemy_townhalls.closer_than(4, enemy6th):
            self.overlord4.move(enemy7th.position.towards(ournat, 15))
        elif self.overlord4 and enemy_townhalls.closer_than(4, enemy7th):
            self.overlord4.move(enemy8th.position.towards(ournat, 15))
        elif self.overlord4 and enemy_townhalls.closer_than(4, enemy8th):
            self.overlord4.move(our8th.position.towards(ournat, 15))
        elif self.overlord4 and enemy_townhalls.closer_than(4, our8th):
            self.overlord4.move(our7th.position.towards(ournat, 15))
        elif self.overlord4 and enemy_townhalls.closer_than(4, our7th):
            self.overlord4.move(our6th.position.towards(ournat, 15))
            
        if self.overlord4 and self.can_afford(UnitTypeId.OVERSEER) and self.units(UnitTypeId.OVERSEER).amount + self.already_pending(UnitTypeId.OVERSEER) < 4 and self.structures(UnitTypeId.LAIR).ready:
            self.overlord4.build(UnitTypeId.OVERSEER)
            
#overlord 5
        if not self.overlord5 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord6:
            self.overlord5tag = self.overlord6tag
            self.overlord5 = self.overlord6
            self.overlord6 = False
        if self.units(UnitTypeId.OVERLORD).amount == 5:
            self.overlord5tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord5tag:
            self.overlord5 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord5tag)
        if self.overlord5 and not enemy_townhalls.closer_than(4, enemy4th):
            self.overlord5.move(enemy4th.position.towards(ournat, 10))
        elif self.overlord5 and enemy_townhalls.closer_than(4, enemy4th):
            self.overlord5.move(enemy5th.position.towards(ournat, 10))
        elif self.overlord5 and enemy_townhalls.closer_than(4, enemy5th):
            self.overlord5.move(enemy6th.position.towards(ournat, 10))
        elif self.overlord5 and enemy_townhalls.closer_than(4, enemy6th):
            self.overlord5.move(enemy7th.position.towards(ournat, 10))
        elif self.overlord5 and enemy_townhalls.closer_than(4, enemy7th):
            self.overlord5.move(enemy8th.position.towards(ournat, 10))
        elif self.overlord5 and enemy_townhalls.closer_than(4, enemy8th):
            self.overlord5.move(our8th.position.towards(ournat, 10))
        elif self.overlord5 and enemy_townhalls.closer_than(4, our8th):
            self.overlord5.move(our7th.position.towards(ournat, 10))
        elif self.overlord5 and enemy_townhalls.closer_than(4, our7th):
            self.overlord5.move(our6th.position.towards(ournat, 10))
            
        if self.overlord5 and self.can_afford(UnitTypeId.OVERSEER) and self.units(UnitTypeId.OVERSEER).amount + self.already_pending(UnitTypeId.OVERSEER) < 5 and self.structures(UnitTypeId.LAIR).ready:
            self.overlord5.build(UnitTypeId.OVERSEER)
                                
#overlord 6
        if not self.overlord6 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord7:
            self.overlord6tag = self.overlord7tag
            self.overlord6 = self.overlord7
            self.overlord7 = False
        if self.units(UnitTypeId.OVERLORD).amount == 6:
            self.overlord6tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord6tag:
            self.overlord6 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord6tag)
        if self.overlord6 and not enemy_townhalls.closer_than(4, enemy5th):
            self.overlord6.move(enemy5th.position.towards(ournat, 10))
        elif self.overlord6 and enemy_townhalls.closer_than(4, enemy5th):
            self.overlord6.move(enemy6th.position.towards(ournat, 10))
        elif self.overlord6 and enemy_townhalls.closer_than(4, enemy6th):
            self.overlord6.move(enemy7th.position.towards(ournat, 10))
        elif self.overlord6 and enemy_townhalls.closer_than(4, enemy7th):
            self.overlord6.move(enemy8th.position.towards(ournat, 10))
        elif self.overlord6 and enemy_townhalls.closer_than(4, enemy8th):
            self.overlord6.move(our8th.position.towards(ournat, 10))
        elif self.overlord6 and enemy_townhalls.closer_than(4, our8th):
            self.overlord6.move(our7th.position.towards(ournat, 10))
        elif self.overlord6 and enemy_townhalls.closer_than(4, our7th):
            self.overlord6.move(our6th.position.towards(ournat, 10))
            
#overlord 7            
        if not self.overlord7 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord8:
            self.overlord7tag = self.overlord8tag
            self.overlord7 = self.overlord8
            self.overlord8 = False
        if self.units(UnitTypeId.OVERLORD).amount == 7:
            self.overlord7tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord7tag:
            self.overlord7 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord7tag)
        if self.overlord7 and not enemy_townhalls.closer_than(4, enemy6th):
            self.overlord7.move(enemy6th.position.towards(ournat, 10))
        elif self.overlord7 and enemy_townhalls.closer_than(4, enemy6th):
            self.overlord7.move(enemy7th.position.towards(ournat, 10))
        elif self.overlord7 and enemy_townhalls.closer_than(4, enemy7th):
            self.overlord7.move(enemy8th.position.towards(ournat, 10))
        elif self.overlord7 and enemy_townhalls.closer_than(4, enemy8th):
            self.overlord7.move(our8th.position.towards(ournat, 10))
        elif self.overlord7 and enemy_townhalls.closer_than(4, our8th):
            self.overlord7.move(our7th.position.towards(ournat, 10))
        elif self.overlord7 and enemy_townhalls.closer_than(4, our7th):
            self.overlord7.move(our6th.position.towards(ournat, 10))

#overlord 8            
        if not self.overlord8 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord9:
            self.overlord8tag = self.overlord9tag
            self.overlord8 = self.overlord9
            self.overlord9 = False
        if self.units(UnitTypeId.OVERLORD).amount == 8:
            self.overlord8tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord8tag:
            self.overlord8 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord8tag)
        if self.overlord8 and not enemy_townhalls.closer_than(4, enemy7th):
            self.overlord8.move(enemy7th.position.towards(ournat, 10))
        elif self.overlord8 and enemy_townhalls.closer_than(4, enemy7th):
            self.overlord8.move(enemy8th.position.towards(ournat, 10))
        elif self.overlord8 and enemy_townhalls.closer_than(4, enemy8th):
            self.overlord8.move(our8th.position.towards(ournat, 10))
        elif self.overlord8 and enemy_townhalls.closer_than(4, our8th):
            self.overlord8.move(our7th.position.towards(ournat, 10))
        elif self.overlord8 and enemy_townhalls.closer_than(4, our7th):
            self.overlord8.move(our6th.position.towards(enemynat, 10))

#overlord 9            
        if not self.overlord9 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord10:
            self.overlord9tag = self.overlord10tag
            self.overlord9 = self.overlord10
            self.overlord10 = False
        if self.units(UnitTypeId.OVERLORD).amount == 9:
            self.overlord9tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord9tag:
            self.overlord9 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord9tag)
        if self.overlord9 and not enemy_townhalls.closer_than(4, enemy8th):
            self.overlord9.move(enemy8th.position.towards(ourmain, 10))
        elif self.overlord9 and enemy_townhalls.closer_than(4, enemy8th):
            self.overlord9.move(our8th.position.towards(our6th, 10))
        elif self.overlord9 and enemy_townhalls.closer_than(4, our8th):
            self.overlord9.move(our7th.position.towards(our3rd, 10))
        elif self.overlord9 and enemy_townhalls.closer_than(4, our7th):
            self.overlord9.move(our6th.position.towards(ournat, 10))

#overlord 10            
        if not self.overlord10 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord11:
            self.overlord10tag = self.overlord11tag
            self.overlord10 = self.overlord11
            self.overlord11 = False
        if self.units(UnitTypeId.OVERLORD).amount == 10:
            self.overlord10tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord10tag:
            self.overlord10 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord10tag)
        if self.overlord10 and not enemy_townhalls.closer_than(4, our7th):
            self.overlord10.move(our7th.position.towards(ourmain, 10))
        elif self.overlord10 and enemy_townhalls.closer_than(4, our7th):
            self.overlord10.move(ournat.position.towards(our6th, 10))
        elif self.overlord10 and enemy_townhalls.closer_than(4, enemy8th):
            self.overlord10.move(ourmain.position.towards(our6th, 10))

#overlord 11            
        if not self.overlord11 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord12:
            self.overlord11tag = self.overlord12tag
            self.overlord11 = self.overlord12
            self.overlord12 = False
        if self.units(UnitTypeId.OVERLORD).amount == 11:
            self.overlord11tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord11tag:
            self.overlord11 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord11tag)
        if self.overlord11 and not enemy_townhalls.closer_than(4, enemy8th):
            self.overlord11.move(enemy8th.position.towards(ourmain, 10))
        elif self.overlord11 and enemy_townhalls.closer_than(4, enemy8th):
            self.overlord11.move(ourmain.position.towards(our6th, 25))

#overlord 12            
        if not self.overlord12 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord13:
            self.overlord12tag = self.overlord13tag
            self.overlord12 = self.overlord13
            self.overlord13 = False
        if self.units(UnitTypeId.OVERLORD).amount == 12:
            self.overlord12tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord12tag:
            self.overlord12 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord12tag)
        if self.overlord12 and not enemy_townhalls.closer_than(4, our5th):
            self.overlord12.move(ourmain.position.towards(our6th, 20))

#overlord 13            
        if not self.overlord13 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord14:
            self.overlord13tag = self.overlord14tag
            self.overlord13 = self.overlord14
            self.overlord14 = False
        if self.units(UnitTypeId.OVERLORD).amount == 13:
            self.overlord13tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord13tag:
            self.overlord13 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord13tag)
        if self.overlord13 and not enemy_townhalls.closer_than(4, our4th):
            self.overlord13.move(ourmain.position.towards(our6th, 10))

#overlord 14            
        if not self.overlord14 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord15:
            self.overlord14tag = self.overlord15tag
            self.overlord14 = self.overlord15
            self.overlord15 = False
        if self.units(UnitTypeId.OVERLORD).amount == 14:
            self.overlord14tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord14tag:
            self.overlord14 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord14tag)
        if self.overlord14 and not enemy_townhalls.closer_than(4, our6th):
            self.overlord14.move(ourmain.position.towards(our6th, 10))

#overlord 15            
        if not self.overlord15 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord16:
            self.overlord15tag = self.overlord16tag
            self.overlord15 = self.overlord16
            self.overlord16 = False
        if self.units(UnitTypeId.OVERLORD).amount == 15:
            self.overlord15tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord15tag:
            self.overlord15 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord15tag)
        if self.overlord15:
            self.overlord15.move(ourmain.position.towards(our6th, 10))

#overlord 16            
        if not self.overlord16 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord17:
            self.overlord16tag = self.overlord17tag
            self.overlord16 = self.overlord17
            self.overlord17 = False
        if self.units(UnitTypeId.OVERLORD).amount == 16:
            self.overlord16tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord16tag:
            self.overlord16 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord16tag)
        if self.overlord16:
            self.overlord16.move(ourmain.position.towards(our6th, 10))

#overlord 17            
        if not self.overlord17 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord18:
            self.overlord17tag = self.overlord18tag
            self.overlord17 = self.overlord18
            self.overlord18 = False
        if self.units(UnitTypeId.OVERLORD).amount == 17:
            self.overlord17tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord17tag:
            self.overlord17 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord17tag)
        if self.overlord17:
            self.overlord17.move(ourmain.position.towards(our6th, 10))
            
#overlord 18            
        if not self.overlord18 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord19:
            self.overlord18tag = self.overlord19tag
            self.overlord18 = self.overlord19
            self.overlord19 = False
        if self.units(UnitTypeId.OVERLORD).amount == 18:
            self.overlord18tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord18tag:
            self.overlord18 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord18tag)
        if self.overlord18:
            self.overlord18.move(ourmain.position.towards(our6th, 10))
            
#overlord 19            
        if not self.overlord19 and self.units(UnitTypeId.OVERLORD).amount > 1 and self.overlord20:
            self.overlord19tag = self.overlord20tag
            self.overlord19 = self.overlord20
            self.overlord20 = False
        if self.units(UnitTypeId.OVERLORD).amount == 19:
            self.overlord19tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord19tag:
            self.overlord19 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord19tag)
        if self.overlord19:
            self.overlord19.move(ourmain.position.towards(our6th, 10))
            
#overlord 20            
        if self.units(UnitTypeId.OVERLORD).amount >= 20:
            self.overlord20tag = self.units(UnitTypeId.OVERLORD).closest_to(ourmain).tag
        if self.overlord20tag:
            self.overlord20 = self.units(UnitTypeId.OVERLORD).find_by_tag(self.overlord20tag)
        if self.overlord20:
            self.overlord20.move(ourmain.position.towards(our6th, 10))

#changeling
        if changeling:
            if len(changeling.closest_to(enemymain).orders) < 1:
                changeling.closest_to(enemymain).move(enemymain.position.towards(ourmain, 2.8))
                changeling.closest_to(enemymain).move(enemynat.position.towards(ourmain, 2.8), queue = True)
                changeling.closest_to(enemymain).move(enemy3rd.position.towards(ourmain, 2.8), queue = True)
                changeling.closest_to(enemymain).move(enemy4th.position.towards(ourmain, 2.8), queue = True)
                changeling.closest_to(enemymain).move(enemy5th.position.towards(ourmain, 2.8), queue = True)

#overseer1
        if self.units(UnitTypeId.OVERSEER).amount == 1:
            self.overseer1tag = self.units(UnitTypeId.OVERSEER).closest_to(enemymain).tag
        if not self.overseer1 and self.units(UnitTypeId.OVERSEER).amount > 1 and self.overseer3:
            self.overseer1tag = self.overseer3tag
            self.overseer1 = self.overseer3
            self.overseer3 = False
        if self.overseer1tag:
            self.overseer1 = self.units(UnitTypeId.OVERSEER).find_by_tag(self.overseer1tag)
        if self.overseer1 and self.time > 300 and len(self.overseer1.orders) < 1:
            self.overseer1.move(enemymain.position.towards(enemynat, -35))
        if self.overseer1 and self.overseer1.energy >= 50:
            self.overseer1.move(enemymain.position.towards(enemynat, -10))
            self.overseer1(AbilityId.SPAWNCHANGELING_SPAWNCHANGELING, queue = True)
            

        if self.units(UnitTypeId.OVERSEER).amount == 2:
            self.overseer2tag = self.units(UnitTypeId.OVERSEER).closest_to(enemynat).tag
        if not self.overseer2 and self.units(UnitTypeId.OVERSEER).amount > 1 and self.overseer3:
            self.overseer2tag = self.overseer3tag
            self.overseer2 = self.overseer3
            self.overseer3 = False
        if self.overseer2tag:
            self.overseer2 = self.units(UnitTypeId.OVERSEER).find_by_tag(self.overseer2tag)
        if self.overseer2 and self.time > 300 and len(self.overseer2.orders) < 1:
            self.overseer2.move(enemynat.position.towards(enemymain, -24))
        if self.overseer2 and self.overseer2.energy >= 50:
            self.overseer2.move(enemynat.position.towards(enemymain, -10))
            self.overseer2(AbilityId.SPAWNCHANGELING_SPAWNCHANGELING, queue = True)

        if self.units(UnitTypeId.OVERSEER).amount == 3:
            self.overseer3tag = self.units(UnitTypeId.OVERSEER).closest_to(enemynat.position.towards(ournat, 40)).tag
        if not self.overseer3 and self.units(UnitTypeId.OVERSEER).amount > 1 and self.overseer4:
            self.overseer3tag = self.overseer4tag
            self.overseer3 = self.overseer4
            self.overseer4 = False
        if self.overseer3tag:
            self.overseer3 = self.units(UnitTypeId.OVERSEER).find_by_tag(self.overseer3tag)
        if self.overseer3 and self.time > 300 and len(self.overseer3.orders) < 1:
            self.overseer3.move(enemynat.position.towards(ournat, 40))
        if self.overseer3 and self.overseer3.energy >= 50:
            self.overseer3.move(enemynat.position.towards(ournat, 40))
            self.overseer3(AbilityId.SPAWNCHANGELING_SPAWNCHANGELING, queue = True)

        if self.units(UnitTypeId.OVERSEER).amount == 4:
            self.overseer4tag = self.units(UnitTypeId.OVERSEER).closest_to(enemy3rd.position.towards(ournat, 15)).tag
        if not self.overseer4 and self.units(UnitTypeId.OVERSEER).amount > 1 and self.overseer5:
            self.overseer4tag = self.overseer5tag
            self.overseer4 = self.overseer5
            self.overseer5 = False
        if self.overseer4tag:
            self.overseer4 = self.units(UnitTypeId.OVERSEER).find_by_tag(self.overseer4tag)
        if self.overseer4 and self.time > 300 and len(self.overseer4.orders) < 1:
            if self.units(UnitTypeId.ROACH):
                if enemies_near:
                    self.overseer4.move(self.units(UnitTypeId.ROACH).in_closest_distance_to_group(enemies_near))
                else:
                    self.overseer4.move(self.units(UnitTypeId.ROACH).closest_to(enemymain))
        if self.overseer4 and self.overseer4.energy >= 50:
            self.overseer4(AbilityId.SPAWNCHANGELING_SPAWNCHANGELING)

        if self.units(UnitTypeId.OVERSEER).amount == 5:
            self.overseer5tag = self.units(UnitTypeId.OVERSEER).closest_to(enemy4th.position.towards(ournat, 15)).tag
        if not self.overseer5 and self.units(UnitTypeId.OVERSEER).amount > 1 and self.overseer6:
            self.overseer5tag = self.overseer6tag
            self.overseer5 = self.overseer6
            self.overseer6 = False
        if self.overseer5tag:
            self.overseer5 = self.units(UnitTypeId.OVERSEER).find_by_tag(self.overseer5tag)
        if self.overseer5 and self.time > 300 and len(self.overseer5.orders) < 1:
            if self.units(UnitTypeId.ROACH):
                if enemies_near:
                    if enemies_near.in_closest_distance_to_group(self.units(UnitTypeId.ROACH)).is_burrowed:
                        self.overseer5.move(enemies_near.in_closest_distance_to_group(self.units(UnitTypeId.ROACH)))
                    elif enemies_near.in_closest_distance_to_group(self.units(UnitTypeId.ROACH)).is_cloaked:
                        self.overseer5.move(enemies_near.in_closest_distance_to_group(self.units(UnitTypeId.ROACH)))
                else:
                    self.overseer5.move(self.units(UnitTypeId.ROACH).closest_to(enemymain))
        if self.overseer5 and self.overseer5.energy >= 50:
            self.overseer5(AbilityId.SPAWNCHANGELING_SPAWNCHANGELING)

                
#spawn more overlords
        if not self.larva:
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        larva = self.larva.random
        if self.supply_cap < 200:
            if self.supply_left <= 0 and self.already_pending(UnitTypeId.OVERLORD) < self.townhalls.ready.amount and self.time > 120:
                larva.train(UnitTypeId.OVERLORD)
                print(self.time_formatted, self.supply_used, "Emergency overlords")
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
                    and self.supply_used > 30 and self.supply_used < 40
                    and self.units(UnitTypeId.OVERLORD).amount + self.already_pending(UnitTypeId.OVERLORD) < 6
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                    print(self.time_formatted, self.supply_used, "Third overlord")               
                if (
                    self.townhalls.amount > 2
                    and self.supply_used > 39 and self.supply_used < 49
                    and self.already_pending(UnitTypeId.OVERLORD) < 1
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                    print(self.time_formatted, self.supply_used, "Fourth overlord")
                if (
                    self.townhalls.ready.amount > 2
                    and self.supply_used > 48 and self.supply_used < 50
                    and self.already_pending(UnitTypeId.OVERLORD) < self.townhalls.ready.amount
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                    print(self.time_formatted, self.supply_used, "Fifth overlord")
                if (
                    self.townhalls.ready.amount > 2
                    and self.supply_used > 49
                    and self.supply_left <= self.townhalls.ready.amount + self.units(UnitTypeId.QUEEN).amount * 2
                    and self.already_pending(UnitTypeId.OVERLORD) < self.townhalls.ready.amount
                    and self.can_afford(UnitTypeId.OVERLORD)
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                    print(self.time_formatted, self.supply_used, "Sixth overlord and beyond")
                if (
                    self.structure_type_build_progress(UnitTypeId.ROACHWARREN) > 0
                    and self.supply_left <= self.townhalls.ready.amount * 6
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
                        self.supply_left <= self.townhalls.ready.amount * 6
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

                if (
                    self.time > 80
                    and self.can_afford(UnitTypeId.OVERLORD)
                    and self.supply_left <= self.townhalls.ready.amount * 4
                    and not self.already_pending(UnitTypeId.OVERLORD) >= self.townhalls.ready.amount
                    and enemy_townhalls.amount < 2
                    ):
                    larva.train(UnitTypeId.OVERLORD)
                    print(self.time_formatted, self.supply_used, "Emergency defense preparation overlord")

                
                
            
    async def expand(self):
        if not self.units(UnitTypeId.DRONE):
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        basecount = self.townhalls.amount
#if early gas aggression, don't expand until they do, if non gas aggression, expand
        if (
            self.time > 45
            and self.time < 120
            and enemy_gas_buildings.amount < 1
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
            if enemy_gas_buildings.amount > 0:
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
                basecount <= enemy_townhalls.amount
                or self.supply_cap > 199
                and self.minerals > 1000
                ):
                if self.enemy_units.not_flying.closer_than(30, ourmain).amount < 1:
                    if self.townhalls.closer_than(3, ourmain) and self.time > 105:
                        self.units(UnitTypeId.DRONE).closest_to(ournat).build(UnitTypeId.HATCHERY, ournat)
                    if self.townhalls.closer_than(3, ournat) and self.townhalls.amount < 3 and not enemy_townhalls.closer_than(3, our3rd):
                        self.units(UnitTypeId.DRONE).closest_to(our3rd).build(UnitTypeId.HATCHERY, our3rd)
                    if self.townhalls.closer_than(3, our3rd) and self.townhalls.amount < 4 and not enemy_townhalls.closer_than(3, our4th):
                        self.units(UnitTypeId.DRONE).closest_to(our4th).build(UnitTypeId.HATCHERY, our4th)
                    if self.townhalls.closer_than(3, our4th) and self.townhalls.amount < 5 and not enemy_townhalls.closer_than(3, our5th):
                        self.units(UnitTypeId.DRONE).closest_to(our5th).build(UnitTypeId.HATCHERY, our5th)
                    if self.townhalls.closer_than(3, our5th) and self.townhalls.amount < 6 and not enemy_townhalls.closer_than(3, our6th):
                        self.units(UnitTypeId.DRONE).closest_to(our6th).build(UnitTypeId.HATCHERY, our6th)
                    if self.townhalls.closer_than(3, our6th) and self.townhalls.amount < 7 and not enemy_townhalls.closer_than(3, our7th):
                        self.units(UnitTypeId.DRONE).closest_to(our7th).build(UnitTypeId.HATCHERY, our7th)
                    if self.townhalls.closer_than(3, our7th) and self.townhalls.amount < 8 and not enemy_townhalls.closer_than(3, our8th):
                        self.units(UnitTypeId.DRONE).closest_to(our8th).build(UnitTypeId.HATCHERY, our8th)
                    if self.game_info.map_name == "MoondanceAIE":
                        if self.townhalls.closer_than(3, our8th) and self.townhalls.amount < 9 and not enemy_townhalls.closer_than(3, our9th):
                            self.units(UnitTypeId.DRONE).closest_to(our9th).build(UnitTypeId.HATCHERY, our9th)
                    if self.game_info.map_name == "MoondanceAIE":
                        if self.townhalls.closer_than(3, our9th) and self.townhalls.amount < 10 and not enemy_townhalls.closer_than(3, enemy9th):
                            self.units(UnitTypeId.DRONE).closest_to(enemy9th).build(UnitTypeId.HATCHERY, enemy9th)
                    if self.game_info.map_name == "MoondanceAIE":
                        if self.townhalls.closer_than(3, enemy9th) and self.townhalls.amount < 11 and not enemy_townhalls.closer_than(3, enemy8th):
                            self.units(UnitTypeId.DRONE).closest_to(enemy8th).build(UnitTypeId.HATCHERY, enemy8th)
                    if self.townhalls.closer_than(3, our8th) and self.townhalls.amount < 12 and not self.townhalls.closer_than(3, enemy8th) and not enemy_townhalls.closer_than(3, enemy8th):
                        self.units(UnitTypeId.DRONE).closest_to(enemy8th).build(UnitTypeId.HATCHERY, enemy8th)
                    if self.townhalls.closer_than(3, enemy8th) and self.townhalls.amount < 13 and not self.townhalls.closer_than(3, enemy7th) and not enemy_townhalls.closer_than(3, enemy7th):
                        self.units(UnitTypeId.DRONE).closest_to(enemy7th).build(UnitTypeId.HATCHERY, enemy7th)
                    if self.townhalls.closer_than(3, enemy7th) and self.townhalls.amount < 14 and not self.townhalls.closer_than(3, enemy6th) and not enemy_townhalls.closer_than(3, enemy6th):
                        self.units(UnitTypeId.DRONE).closest_to(enemy6th).build(UnitTypeId.HATCHERY, enemy6th)
                    if self.townhalls.closer_than(3, enemy6th) and self.townhalls.amount < 15 and not self.townhalls.closer_than(3, enemy5th) and not enemy_townhalls.closer_than(3, enemy5th):
                        self.units(UnitTypeId.DRONE).closest_to(enemy5th).build(UnitTypeId.HATCHERY, enemy5th)
        if (
            self.can_afford(UnitTypeId.HATCHERY)
            and enemy_gas_buildings.amount < 1
            ):
            for hatch in self.townhalls:
                if self.mineral_field.closer_than(10, hatch).amount < 5:
                    basecount = basecount - 1
            if (
                basecount <= enemy_townhalls.amount
                or self.supply_cap > 199
                and self.minerals > 1000
                ):
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(30, ourmain).amount < 1:
                    if self.townhalls.closer_than(3, ourmain):
                        self.units(UnitTypeId.DRONE).closest_to(ournat).build(UnitTypeId.HATCHERY, ournat)
                    if self.townhalls.closer_than(3, ournat) and self.townhalls.amount < 3 and self.time > 105 and not enemy_townhalls.closer_than(3, our3rd):
                        self.units(UnitTypeId.DRONE).closest_to(our3rd).build(UnitTypeId.HATCHERY, our3rd)
                    if self.townhalls.closer_than(3, our3rd) and self.townhalls.amount < 4 and self.time > 170 and not enemy_townhalls.closer_than(3, our4th):
                        self.units(UnitTypeId.DRONE).closest_to(our4th).build(UnitTypeId.HATCHERY, our4th)
                    if self.townhalls.closer_than(3, our4th) and self.townhalls.amount < 5 and self.time > 200 and not enemy_townhalls.closer_than(3, our5th):
                        self.units(UnitTypeId.DRONE).closest_to(our5th).build(UnitTypeId.HATCHERY, our5th)
                    if self.townhalls.closer_than(3, our5th) and self.townhalls.amount < 6 and self.time > 230 and not enemy_townhalls.closer_than(3, our6th):
                        self.units(UnitTypeId.DRONE).closest_to(our6th).build(UnitTypeId.HATCHERY, our6th)
                    if self.townhalls.closer_than(3, our6th) and self.townhalls.amount < 7 and not enemy_townhalls.closer_than(3, our7th):
                        self.units(UnitTypeId.DRONE).closest_to(our7th).build(UnitTypeId.HATCHERY, our7th)
                    if self.townhalls.closer_than(3, our7th) and self.townhalls.amount < 8 and not enemy_townhalls.closer_than(3, our8th):
                        self.units(UnitTypeId.DRONE).closest_to(our8th).build(UnitTypeId.HATCHERY, our8th)
                    if self.game_info.map_name == "MoondanceAIE":
                        if self.townhalls.closer_than(3, our8th) and self.townhalls.amount < 9 and not enemy_townhalls.closer_than(3, our9th):
                            self.units(UnitTypeId.DRONE).closest_to(our9th).build(UnitTypeId.HATCHERY, our9th)
                    if self.game_info.map_name == "MoondanceAIE":
                        if self.townhalls.closer_than(3, our9th) and self.townhalls.amount < 10 and not enemy_townhalls.closer_than(3, enemy9th):
                            self.units(UnitTypeId.DRONE).closest_to(enemy9th).build(UnitTypeId.HATCHERY, enemy9th)
                    if self.game_info.map_name == "MoondanceAIE":
                        if self.townhalls.closer_than(3, enemy9th) and self.townhalls.amount < 11 and not enemy_townhalls.closer_than(3, enemy8th):
                            self.units(UnitTypeId.DRONE).closest_to(enemy8th).build(UnitTypeId.HATCHERY, enemy8th)
                    if self.townhalls.closer_than(3, our8th) and self.townhalls.amount < 12 and not self.townhalls.closer_than(3, enemy8th) and not enemy_townhalls.closer_than(3, enemy8th):
                        self.units(UnitTypeId.DRONE).closest_to(enemy8th).build(UnitTypeId.HATCHERY, enemy8th)
                    if self.townhalls.closer_than(3, enemy8th) and self.townhalls.amount < 13 and not self.townhalls.closer_than(3, enemy7th) and not enemy_townhalls.closer_than(3, enemy7th):
                        self.units(UnitTypeId.DRONE).closest_to(enemy7th).build(UnitTypeId.HATCHERY, enemy7th)
                    if self.townhalls.closer_than(3, enemy7th) and self.townhalls.amount < 14 and not self.townhalls.closer_than(3, enemy6th) and not enemy_townhalls.closer_than(3, enemy6th):
                        self.units(UnitTypeId.DRONE).closest_to(enemy6th).build(UnitTypeId.HATCHERY, enemy6th)
                    if self.townhalls.closer_than(3, enemy6th) and self.townhalls.amount < 15 and not self.townhalls.closer_than(3, enemy5th) and not enemy_townhalls.closer_than(3, enemy5th):
                        self.units(UnitTypeId.DRONE).closest_to(enemy5th).build(UnitTypeId.HATCHERY, enemy5th)
            for hatch in self.townhalls:
                if self.mineral_field.closer_than(10, hatch).amount < 5:
                    basecount = basecount + 1
        else:
            print("cant expand", self.can_afford(UnitTypeId.HATCHERY), enemy_gas_buildings.amount < 0, self.townhalls.amount <= enemy_townhalls.amount, )
            pass
        
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
            print("workers for gas", (self.supply_workers + self.already_pending(UnitTypeId.DRONE)) / 11 - 1)
            if (
                self.can_afford(UnitTypeId.EXTRACTOR)
                and self.structures(UnitTypeId.EXTRACTOR).amount + self.already_pending(UnitTypeId.EXTRACTOR) < self.townhalls.amount * 2
                and self.structure_type_build_progress(UnitTypeId.ROACHWARREN) > 0
                and (self.supply_workers + self.already_pending(UnitTypeId.DRONE)) / 11 - 1 > self.structures(UnitTypeId.EXTRACTOR).amount + self.already_pending(UnitTypeId.EXTRACTOR)
                ):
                if (
                    self.structures(UnitTypeId.EXTRACTOR).amount + self.already_pending(UnitTypeId.EXTRACTOR) < enemy_gas_buildings.amount
                    or self.structures(UnitTypeId.EXTRACTOR).amount + self.already_pending(UnitTypeId.EXTRACTOR) < 1
                    or self.supply_workers + self.already_pending(UnitTypeId.DRONE) >= (enemy_townhalls.amount * 16) + (enemy_townhalls.amount * 4) + (enemy_gas_buildings.amount * 3) and self.vespene < 100
                    or self.gas_buildings.amount + self.already_pending(UnitTypeId.EXTRACTOR) < self.townhalls.amount and self.time > 300
                    ):
                    if (
                        not self.gas_buildings.closer_than(1, geysernear)
                        and self.vespene < self.minerals
                        ):
                        await self.build(UnitTypeId.EXTRACTOR, geysernear)
                        print(self.time_formatted, self.supply_used, "Building Gas1")
                        break
                    if (
                        not self.gas_buildings.closer_than(1, geyserfar)
                        and self.vespene < self.minerals
                        ):
                        await self.build(UnitTypeId.EXTRACTOR, geyserfar)
                        print(self.time_formatted, self.supply_used, "Building Gas2")
                        break
                elif self.supply_workers + self.already_pending(UnitTypeId.DRONE) >= (self.townhalls.amount * 16) + (self.structures(UnitTypeId.EXTRACTOR).amount * 3) and self.minerals > 500:
                    if (
                        not self.gas_buildings.closer_than(1, geysernear)
                        and self.vespene < self.minerals
                        ):
                        await self.build(UnitTypeId.EXTRACTOR, geysernear)
                        print(self.time_formatted, self.supply_used, "Building Gas3")
                        break
                    if (
                        not self.gas_buildings.closer_than(1, geyserfar)
                        and self.vespene < self.minerals
                        ):
                        await self.build(UnitTypeId.EXTRACTOR, geyserfar)
                        print(self.time_formatted, self.supply_used, "Building Gas4")
                        break
                    print(self.time_formatted, self.supply_used, self.already_pending(UnitTypeId.EXTRACTOR))
                    print(self.time_formatted, self.supply_used, "They got more gas than us, that's not allowed!")
                        
    async def units_value_check(self):
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        ou = self.units.filter(lambda ou: not ou.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE))
#enemy workers
        if not self.enemyworkerstags:
            self.enemyworkerstags = self.enemy_units(scouts).tags
        if self.enemyworkerstags:
            print(self.time_formatted, self.supply_used, "enemy workers tags = ", self.enemyworkerstags)
            print(self.time_formatted, self.supply_used, "real enemy workers tags = ", self.enemy_units(scouts).tags)
            print(self.time_formatted, self.supply_used, "Do we have less?", len(self.enemy_units(scouts).tags) > len(self.enemyworkerstags))
            if len(self.enemy_units(scouts).tags) > len(self.enemyworkerstags):
                self.enemyworkerstags = self.enemy_units(scouts).tags
                print(self.time_formatted, self.supply_used, "new enemy workers tags = ", self.enemyworkerstags)
                enemyworkers = 0
                for tag in self.enemyworkerstags:
                    print(self.time_formatted, self.supply_used, "tag = ", tag)
                    enemyworker = self.enemy_units.find_by_tag(tag)
                    print(self.time_formatted, self.supply_used, "enemy worker from tag = ", enemyworker)
                    enemyworkers = enemyworkers + 1
                    print(self.time_formatted, self.supply_used, "enemy worker count at = ", enemyworkers)
                else:
                    self.enemyworkers = enemyworkers
                    print(self.time_formatted, self.supply_used, "enemy workers = ", self.enemyworkers)
            if self.state.dead_units:
                self.enemyworkerstags = (set(self.enemyworkerstags) - set(self.state.dead_units))

#enemy units on map            
        if not self.latest_enemy_units:
            if self.time < 360:
                self.latest_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)).tags
            if self.structure_type_build_progress(UnitTypeId.ROACHWARREN) >= 1 and self.time > 359:
                self.latest_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)).tags
                print(self.structure_type_build_progress(UnitTypeId.ROACHWARREN), "queens now included in threat eval")
        if self.latest_enemy_units:
            if self.time < 360:
                if len(self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)).tags) > len(self.latest_enemy_units):
                    self.latest_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)).tags
                    for unit in self.latest_enemy_units:
                        enemyunit = self.enemy_units.find_by_tag(unit)
                        enemyunittypeid = enemyunit.type_id
                        combinedvalue = self.calculate_unit_value(enemyunittypeid).minerals + self.calculate_unit_value(enemyunittypeid).vespene
                        self.totalvalue = self.totalvalue + combinedvalue
                    else:
                        self.totalvalue_e = self.totalvalue
                        self.totalvalue = 0
            if self.structure_type_build_progress(UnitTypeId.ROACHWARREN) >= 1 and self.time > 359:
                if len(self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)).tags) > len(self.latest_enemy_units):
                    self.latest_enemy_units = self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)).tags
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
        if self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)):
            for unit in self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)):
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
        supplyrequirement = False
        makelings = True
                    
        for hatch in self.townhalls:
            if not enemies_near:
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                    enemies_near.extend(
                        self.enemy_units.filter(
                            lambda u: not u.is_flying
                            and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                            and u.distance_to(hatch) < 40
                        )
                    )
        if self.structure_type_build_progress(UnitTypeId.ROACHWARREN) > 0:
            if self.supply_left > self.townhalls.ready.amount * 6:
                supplyrequirement = True
        elif self.supply_left > self.townhalls.ready.amount * 4 or self.already_pending(UnitTypeId.OVERLORD) >= self.townhalls.ready.amount:
            supplyrequirement = True
        print("supply yes?", supplyrequirement)
        print(self.supply_left > self.townhalls.amount * 4)
        print(self.structure_type_build_progress(UnitTypeId.ROACHWARREN) > 0)
        print(self.supply_left > self.townhalls.ready.amount * 6)
        if (
            supplyrequirement
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
                    if self.time < 300:
                        larva.train(UnitTypeId.ZERGLING)
                        print(self.time_formatted, self.supply_used, "emergency lings")
                    elif self.totalvalue_o < self.totalvalue_e:
                        larva.train(UnitTypeId.ZERGLING)
                        print(self.time_formatted, self.supply_used, "one base gasless defensive lings")
#defensive lings:
            print("lack of vespene for defensive lings", self.vespene)
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
            if self.structures(UnitTypeId.EXTRACTOR):
                for gas in self.structures(UnitTypeId.EXTRACTOR):
                    if (
                        self.structures(UnitTypeId.SPAWNINGPOOL).ready
                        and self.can_afford(UnitTypeId.ZERGLING)
                        and self.vespene < 25
                        and self.townhalls.amount >= enemy_townhalls.amount
                        ):
                        for hatch in self.townhalls:
                            if self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount * 16) + (enemy_townhalls.amount * 4) + (enemy_gas_buildings.amount * 3):
                                makelings == False
                        if makelings == True:
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
                        and self.supply_workers + self.already_pending(UnitTypeId.DRONE) >= (enemy_townhalls.amount * 16) + (enemy_townhalls.amount * 4) + (enemy_gas_buildings.amount * 3)
                        ):
                        larva.train(UnitTypeId.ZERGLING)
                        print(self.time_formatted, self.supply_used, "macro lings")
                
#scout lings:
            if (
                self.structures(UnitTypeId.SPAWNINGPOOL).ready
                and self.can_afford(UnitTypeId.ZERGLING)
                ):
                if (
                    self.units(UnitTypeId.ZERGLING).amount < 2
                    and self.already_pending(UnitTypeId.ZERGLING) < 1
                    ):
                    if self.enemyworkers > 14:
                        if (
                            self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) > 1
                            ):
                            larva.train(UnitTypeId.ZERGLING)
                            print(self.time_formatted, self.supply_used, "scout ling created", self.units(UnitTypeId.ZERGLING).amount, self.already_pending(UnitTypeId.ZERGLING))
                    elif self.enemyworkers < 15:
                        larva.train(UnitTypeId.ZERGLING)
                        print(self.time_formatted, self.supply_used, "scout ling created", self.units(UnitTypeId.ZERGLING).amount, self.already_pending(UnitTypeId.ZERGLING))
#lings to match enemy lings if they are building up army
                if (
                    self.can_afford(UnitTypeId.ZERGLING)
                    and self.time > 90
                    and self.vespene < 25
                    and self.totalvalue_o < self.totalvalue_e
                    and self.already_pending(UnitTypeId.ZERGLING) * 50 < self.totalvalue_e
                    ):
                    larva.train(UnitTypeId.ZERGLING)
                    print(self.time_formatted, self.supply_used, "our combat units =", self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).amount)
                    print(self.time_formatted, self.supply_used, "enemy combat units =", self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                    print(self.time_formatted, self.supply_used, "Switching from drones to defensive lings")
                    print(self.vespene)
                    
                    print(self.time_formatted, self.supply_used, "Enemyunits", self.totalvalue_e)

        enemies_near = Units([], self)

    async def attack(self):
        roaches = self.units(UnitTypeId.ROACH)
        lingcount = self.units(UnitTypeId.ZERGLING).amount
        lings = self.units(UnitTypeId.ZERGLING)
        airunits = {UnitTypeId.OVERLORD, UnitTypeId.OVERSEER, UnitTypeId.MUTALISK, UnitTypeId.CORRUPTOR, UnitTypeId.BROODLORD, UnitTypeId.MEDIVAC}
        scouts = {UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}
        queens = self.units(UnitTypeId.QUEEN)
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        enemies_near = Units([], self)
        enemies_structures_near = Units([], self)
        enemies_aggressive_structures = self.structures.filter(lambda sa: sa.can_attack)
        allenemies = self.enemy_units.filter(lambda ae:
                                             not ae.is_flying
                                             and not ae.type_id in (UnitTypeId.EGG, UnitTypeId.LARVA))
        hydras = self.units(UnitTypeId.HYDRALISK)
        stillattacking = False
        
#hatchery zonal defense system
#enemy units near hatcheries
        for hatch in self.townhalls:
            if self.time < 120:
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                    enemies_near.extend(
                        self.enemy_units.filter(
                            lambda u: not u.is_flying
                            and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                            and u.distance_to(hatch) < 40
                        )
                    )
            else:
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                    enemies_near.extend(
                        self.enemy_units.filter(
                            lambda u: not u.is_flying
                            and u.type_id not in (UnitTypeId.EGG, UnitTypeId.LARVA)
                            and u.distance_to(hatch) < 40
                        )
                    )
                
#enemy structures near hatcheries
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
        if self.enemyworkers and self.time > 60:
            print("enemy worker")
            aw = self.units.filter(lambda aw: aw.type_id == (UnitTypeId.DRONE) and aw.is_attacking)
            for drone in aw:
                if drone.health_percentage < 0.5:
                    if self.mineral_field.closer_than(10, ourmain):
                        drone.gather(self.mineral_field.closer_than(10, ourmain).furthest_to(drone))
            naw = self.units.filter(lambda naw: naw.type_id == (UnitTypeId.DRONE) and not naw.is_attacking)
            if self.enemy_units({UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}).closer_than(8, ourmain):
                    print("enemy worker nearby")
                    print("our non attacking workers =", naw)
                    for drone in naw:
                        print("naw = ", naw)
                        print("our worker pos =", drone.position)
                        if drone.position.is_closer_than(3, self.enemy_units({UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}).closer_than(8, ourmain).closest_to(drone)):
                            if drone.health_percentage >= 0.5:
                                if not drone.order_target == self.enemy_units({UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}).closer_than(8, ourmain).closest_to(drone).tag:
                                    drone.attack(self.enemy_units({UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}).closer_than(8, ourmain).closest_to(drone))
                                print("worker attacking enemy worker")
                            elif drone.health_percentage < 0.5:
                                if self.mineral_field.closer_than(10, ourmain):
                                    if not drone.order_target == self.mineral_field.closer_than(10, ourmain).furthest_to(self.enemy_units(scouts).closest_to(drone)).tag:
                                        drone.gather(self.mineral_field.closer_than(10, ourmain).furthest_to(self.enemy_units(scouts).closest_to(drone)))
                                
        for drone in self.units(UnitTypeId.DRONE):
            if self.time < 30 and self.enemy_units.not_flying.closer_than(10, drone).amount > 2:
                self.units(UnitTypeId.DRONE).furthest_to(ourmain).gather(self.mineral_field.closest_to(self.townhalls.closest_to(ourmain)))
            if self.time > 40 and self.time < 50 and self.alert(Alert.UnitUnderAttack):
                self.units(UnitTypeId.DRONE).furthest_to(ourmain).move(enemymain.position.towards(enemynat, -2.8))
                self.units(UnitTypeId.DRONE).furthest_to(ourmain).gather(self.mineral_field.closest_to(self.townhalls.closest_to(ourmain)), queue = True)
            if not self.structures(UnitTypeId.SPAWNINGPOOL):
                if self.enemy_units({UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE}).closer_than(8, ourmain).amount > 1:
                    if not drone.order_target == self.enemy_units.not_flying.closer_than(10, ourmain).closest_to(drone).tag:
                        drone.attack(self.enemy_units.not_flying.closer_than(10, ourmain).closest_to(drone))
                elif self.enemy_structures({UnitTypeId.BUNKER, UnitTypeId.PYLON, UnitTypeId.PHOTONCANNON, UnitTypeId.SPINECRAWLER}).closer_than(15, ourmain).amount > 0:
                    if not drone.order_target == self.enemy_structures.not_flying.closer_than(10, ourmain).closest_to(drone).tag:
                        drone.attack(self.enemy_structures.not_flying.closer_than(10, ourmain).closest_to(drone))
            if (
                self.alert(Alert.UnitUnderAttack)
                and self.enemy_units.not_flying.closer_than(10, ourmain).amount > 3
                and not self.structures(UnitTypeId.SPAWNINGPOOL).ready
                ):
                if not drone.order_target == self.enemy_units.not_flying.closer_than(10, ourmain).closest_to(drone).tag:
                    drone.attack(self.enemy_units.not_flying.closer_than(10, ourmain).closest_to(drone))
            if drone.is_attacking:
                if self.enemy_units.not_flying.closer_than(9, ourmain).amount < 1 and self.enemy_structures.not_flying.closer_than(10, ourmain).amount < 1:
                    drone.gather(self.mineral_field.closest_to(self.townhalls.closest_to(ourmain)))

#queens have an attack too
##        if enemies_near and queens:
##            if queens.in_closest_distance_to_group(enemies_near).is_attacking:
##                stillattacking = True
##                print("queen is attacking1")
                    
        for queen in queens:
            if enemies_near:
                neu = self.enemy_units.filter(lambda neu:
                                              not neu.is_flying
                                              and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                              and neu.position.is_closer_than(10, enemies_near.closest_to(queen)))
                if len(self.enemy_units.filter(lambda neu:
                                               not neu.is_flying
                                               and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                               and neu.position.is_closer_than(10, enemies_near.closest_to(queen))).tags) > len(neu.tags):
                    neu = self.enemy_units.filter(lambda neu:
                                                  not neu.is_flying
                                                  and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                  and neu.position.is_closer_than(10, enemies_near.closest_to(queen)))
                if len(self.enemy_units.filter(lambda neu:
                                               not neu.is_flying
                                               and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                               and neu.position.is_closer_than(10, enemies_near.closest_to(queen))).tags) < len(neu.tags):
                    neu = self.enemy_units.filter(lambda neu:
                                                  not neu.is_flying
                                                  and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                  and neu.position.is_closer_than(10, enemies_near.closest_to(queen)))
                for eunit in neu:
                    combinedvalue = self.calculate_unit_value(eunit.type_id).minerals + self.calculate_unit_value(eunit.type_id).vespene
                    self.totalvalue = self.totalvalue + combinedvalue
                else:
                    self.totalvalue_en = self.totalvalue
                    self.totalvalue = 0
                    print("enemy value near queen =", self.totalvalue_en)
                for queen in queens.closer_than(10, enemies_near.in_closest_distance_to_group(queens)):
                    onu = self.units.filter(lambda onu:
                                            not onu.is_flying
                                            and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                            and onu.position.is_closer_than(10, enemies_near.closest_to(queen)))
                    print("our lambda units are =", onu)
                    if len(self.units.filter(lambda onu:
                                             not onu.is_flying
                                             and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                             and onu.position.is_closer_than(10, enemies_near.closest_to(queen))).tags) > len(onu.tags):
                        onu = self.units.filter(lambda onu:
                                                not onu.is_flying
                                                and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                and onu.position.is_closer_than(10, enemies_near.closest_to(queen)))
                    if len(self.units.filter(lambda onu:
                                             not onu.is_flying
                                             and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                             and onu.position.is_closer_than(10, enemies_near.closest_to(queen))).tags) < len(onu.tags):
                        onu = self.units.filter(lambda onu:
                                                not onu.is_flying
                                                and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                and onu.position.is_closer_than(10, enemies_near.closest_to(queen)))
                    for ounit in onu:
                        combinedvalue = self.calculate_unit_value(ounit.type_id).minerals + self.calculate_unit_value(ounit.type_id).vespene
                        self.totalvalue = self.totalvalue + combinedvalue
                    else:
                        self.totalvalue_on = self.totalvalue
                        self.totalvalue = 0
                        print(self.time_formatted, self.supply_used, "self.totalvalue_on =", self.totalvalue_on)
                if queen.is_idle:
                    print("queens gotta move away")
                    queen.move(self.townhalls.closest_to(enemies_near.closest_to(queen)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(queen))).furthest_to(enemynat), 3))
                    queen.move(self.townhalls.closest_to(enemies_near.closest_to(queen)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(queen))).furthest_to(enemynat), 3), queue = True)

                if lings:
                    if enemies_near.closer_than(10, self.townhalls.ready.in_closest_distance_to_group(enemies_near).position) or lings.in_closest_distance_to_group(enemies_near).position.is_closer_than(1, enemies_near.in_closest_distance_to_group(lings)):
                        print("queen time to attack", stillattacking)
                        print("queen attack?", self.totalvalue_on > self.totalvalue_en)
                        print("enemy distance for queen to attack", enemies_near.closest_to(queen).distance_to(self.townhalls.closest_to(queen)), enemies_near.closest_to(queen))
                        if (
                            queen.weapon_cooldown == 0
                            or queen.weapon_cooldown > 10
                            ):
                            if not queen.order_target == enemies_near.closest_to(queen).tag:
                                queen.attack(enemies_near.closest_to(queen))
                                queen.attack(enemies_near.closest_to(queen), queue = True)
                                print("we have more queen attack")
                                stillattacking = True
                        else:
                            if enemies_near.closest_to(queen).ground_range < 5:
                                if not queen.is_moving:
                                    queen.move(enemies_near.closest_to(queen).position.towards(queen, 5))
                                    queen.move(enemies_near.closest_to(queen).position.towards(queen, 5), queue = True)
                                    stillattacking = True
                            if queen.is_attacking:
                                if enemies_near.closest_to(queen).position.is_further_than(17, self.townhalls.closest_to(enemies_near.closest_to(queen))) or queen.position.is_further_than(12, self.townhalls.closest_to(enemies_near.closest_to(queen))):
                                    queen.move(self.townhalls.closest_to(enemies_near.closest_to(queen)))
                                    queen.move(self.townhalls.closest_to(enemies_near.closest_to(queen)), queue = True)
                                    print("queen or enemy is too far away")
                        print(self.time_formatted, self.supply_used, "queen unit defense")
                else:
                    if enemies_near.closer_than(10, self.townhalls.ready.in_closest_distance_to_group(enemies_near).position):
                        print("queen time to attack", stillattacking)
                        print("queen attack?", self.totalvalue_on > self.totalvalue_en)
                        print("enemy distance for queen to attack", enemies_near.closest_to(queen).distance_to(self.townhalls.closest_to(queen)), enemies_near.closest_to(queen))
                        if (
                            queen.weapon_cooldown == 0
                            or queen.weapon_cooldown > 10
                            ):
                            if not queen.order_target == enemies_near.closest_to(queen).tag:
                                queen.attack(enemies_near.closest_to(queen))
                                queen.attack(enemies_near.closest_to(queen), queue = True)
                                print("we have more queen attack")
                                stillattacking = True
                        else:
                            if enemies_near.closest_to(queen).ground_range < 5:
                                if not queen.is_moving:
                                    queen.move(enemies_near.closest_to(queen).position.towards(queen, 5))
                                    queen.move(enemies_near.closest_to(queen).position.towards(queen, 5), queue = True)
                                    stillattacking = True
                            if queen.is_attacking:
                                if enemies_near.closest_to(queen).position.is_further_than(17, self.townhalls.closest_to(enemies_near.closest_to(queen))) or queen.position.is_further_than(12, self.townhalls.closest_to(enemies_near.closest_to(queen))):
                                    queen.move(self.townhalls.closest_to(enemies_near.closest_to(queen)))
                                    queen.move(self.townhalls.closest_to(enemies_near.closest_to(queen)), queue = True)
                                    print("queen or enemy is too far away")
                        print(self.time_formatted, self.supply_used, "queen unit defense")
                if not self.has_creep(queen.position):
                    if self.townhalls:
                        if not queen.is_moving:
                            print("queens gotta move away")
                            queen.move(self.townhalls.closest_to(enemies_near.closest_to(queen)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(queen))).furthest_to(enemynat), 3))
                            queen.move(self.townhalls.closest_to(enemies_near.closest_to(queen)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(queen))).furthest_to(enemynat), 3), queue = True)

            if not enemies_near:
                if queen.is_idle:
                    queen.move(self.townhalls.closest_to(queen).position.towards(self.mineral_field.closest_to(self.townhalls.closest_to(queen)), 3))
                

#lingu
                    
#lingscoutfront
        if self.closestling:
            self.closestling = self.units(UnitTypeId.ZERGLING).find_by_tag(self.closestlingtag)
        if self.closestling:
            if (
                not self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling).amount > 1
                and not enemies_near
                ):
                if self.closestling in lings:
                    lings.remove(self.closestling)
                print(self.time_formatted, self.supply_used, "new closest ling selected =", self.closestling)
                print(self.time_formatted, self.supply_used, "entire ling list1 =", lings)
                print(self.time_formatted, self.supply_used, "old ling list =", lings)
                print(self.time_formatted, self.supply_used, "new ling list =", lings)
                print(self.time_formatted, self.supply_used, "self.closestling =", self.closestling)                    
                if (
                    not enemies_near.amount > 0
                    and self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling).amount < 2
                    and len(self.closestling.orders) < 2
                    ):
                    self.closestling.move(enemynat.position.towards(enemymain, 2.8))
                    self.closestling.move(enemymain.position.towards(enemynat, 2.8), queue = True)
                    self.closestling.move(enemynat.position.towards(enemymain, 2.8), queue = True)
                    print(self.time_formatted, self.supply_used, "closest ling scouting")
            
        if not self.closestling:
            if self.closestling2:
                if self.closestling2 in lings:
                    lings.remove(self.closestling2)
                if lings:
                    self.closestlingtag = lings.closest_to(enemymain).tag
                    self.closestling = lings.find_by_tag(self.closestlingtag)
                    if (
                        not self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling).amount > 1
                        and not enemies_near
                        ):
                        lings.remove(self.closestling)
                        if self.closestling:
                            print(self.time_formatted, self.supply_used, "new closest ling selected =", self.closestling)
                            print(self.time_formatted, self.supply_used, "entire ling list1 =", lings)
                            print(self.time_formatted, self.supply_used, "old ling list =", lings)
                            print(self.time_formatted, self.supply_used, "new ling list =", lings)
                            print(self.time_formatted, self.supply_used, "self.closestling =", self.closestling)                    
                            if (
                                not enemies_near.amount > 0
                                and self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling).amount < 2
                                and len(self.closestling.orders) < 2
                                ):
                                self.closestling.move(enemynat.position.towards(enemymain, 2.8))
                                self.closestling.move(enemymain.position.towards(enemynat, 2.8), queue = True)
                                self.closestling.move(enemynat.position.towards(enemymain, 2.8), queue = True)
                                print(self.time_formatted, self.supply_used, "closest ling scouting")

            if not self.closestling2:
                if lings:
                    self.closestlingtag = lings.closest_to(enemymain).tag
                    self.closestling = lings.find_by_tag(self.closestlingtag)
                    if (
                        not self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling).amount > 1
                        and not enemies_near
                        ):
                        lings.remove(self.closestling)
                        if self.closestling:
                            print(self.time_formatted, self.supply_used, "new closest ling selected =", self.closestling)
                            print(self.time_formatted, self.supply_used, "entire ling list1 =", lings)
                            print(self.time_formatted, self.supply_used, "old ling list =", lings)
                            print(self.time_formatted, self.supply_used, "new ling list =", lings)
                            print(self.time_formatted, self.supply_used, "self.closestling =", self.closestling)                    
                            if (
                                not enemies_near
                                and self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling).amount < 2
                                and len(self.closestling.orders) < 2
                                ):
                                self.closestling.move(enemynat.position.towards(enemymain, 2.8))
                                self.closestling.move(enemymain.position.towards(enemynat, 2.8), queue = True)
                                self.closestling.move(enemynat.position.towards(enemymain, 2.8), queue = True)
                                print(self.time_formatted, self.supply_used, "closest ling scouting")
                    
        if self.closestling2:
            self.closestling2 = self.units(UnitTypeId.ZERGLING).find_by_tag(self.closestlingtag2)
        if self.closestling2:
            if (
                not self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling2).amount > 1
                and not enemies_near
                ):
                if self.closestling2 in lings:
                    lings.remove(self.closestling2)
                if self.closestling2:
                    print(self.time_formatted, self.supply_used, "entire ling list1 =", lings)
                    print(self.time_formatted, self.supply_used, "old ling list =", lings)
                    print(self.time_formatted, self.supply_used, "new ling list =", lings)
                    print(self.time_formatted, self.supply_used, "self.closestling 2 =", self.closestling2)                    
                    if (
                        not enemies_near.amount > 0
                        and self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling2).amount < 2
                        and len(self.closestling2.orders) < 1
                        ):
                        if enemy_gas_buildings.amount < 1:
                            if not enemy_townhalls.closer_than(4, enemy3rd):
                                self.closestling2.move(enemy3rd)
                                self.closestling2.move(enemy4th, queue = True)
                            elif not enemy_townhalls.closer_than(4, enemy4th):
                                self.closestling2.move(enemy4th)
                                self.closestling2.move(enemy5th, queue = True)
                            elif not enemy_townhalls.closer_than(4, enemy5th):
                                self.closestling2.move(enemy5th)
                                self.closestling2.move(enemy6th, queue = True)
                            elif not enemy_townhalls.closer_than(4, enemy6th):
                                self.closestling2.move(enemy6th)
                                self.closestling2.move(enemy7th, queue = True)
                            elif not enemy_townhalls.closer_than(4, enemy7th):
                                self.closestling2.move(enemy7th)
                                self.closestling2.move(enemy8th, queue = True)
                        else:
                            if not enemy_townhalls.closer_than(5, enemy3rd):
                                self.closestling2.move(enemy3rd)
                            elif not enemy_townhalls.closer_than(5, enemy4th):
                                self.closestling2.move(enemy4th, queue = True)
                            elif not enemy_townhalls.closer_than(5, enemy5th):
                                self.closestling2.move(enemy5th, queue = True)
                            elif not enemy_townhalls.closer_than(5, enemy6th):
                                self.closestling2.move(enemy6th, queue = True)
                            elif not enemy_townhalls.closer_than(5, enemy7th):
                                self.closestling2.move(enemy7th, queue = True)
                            elif not enemy_townhalls.closer_than(5, enemy8th):
                                self.closestling2.move(enemy8th, queue = True)
                            elif not enemy_townhalls.closer_than(5, our8th):
                                self.closestling2.move(our8th, queue = True)
                            elif not enemy_townhalls.closer_than(5, our7th):
                                self.closestling2.move(our7th, queue = True)
                            elif not enemy_townhalls.closer_than(5, our6th):
                                self.closestling2.move(our6th, queue = True)
                            elif not enemy_townhalls.closer_than(5, our5th):
                                self.closestling2.move(our5th, queue = True)
                            elif not enemy_townhalls.closer_than(5, our4th):
                                self.closestling2.move(our4th, queue = True)
                            print(self.time_formatted, self.supply_used, "closest ling 2 scouting")
            
        if not self.closestling2:
            if lings:
                self.closestlingtag2 = lings.closest_to(enemymain).tag
                self.closestling2 = lings.find_by_tag(self.closestlingtag2)
            if self.closestling2:
                if (
                    not self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling2).amount > 1
                    and not enemies_near
                    ):
                    lings.remove(self.closestling2)
                    if self.closestling2:
                        print(self.time_formatted, self.supply_used, "entire ling list1 =", lings)
                        print(self.time_formatted, self.supply_used, "old ling list =", lings)
                        print(self.time_formatted, self.supply_used, "new ling list =", lings)
                        print(self.time_formatted, self.supply_used, "self.closestling 2 =", self.closestling2)                    
                        if (
                            not enemies_near.amount > 0
                            and self.enemy_units.not_flying.exclude_type(scouts).closer_than(10, self.closestling2).amount < 2
                            and len(self.closestling2.orders) < 1
                            ):
                            if enemy_gas_buildings.amount < 1:
                                if not enemy_townhalls.closer_than(4, enemy3rd):
                                    self.closestling2.move(enemy3rd)
                                    self.closestling2.move(enemy4th, queue = True)
                                elif not enemy_townhalls.closer_than(4, enemy4th):
                                    self.closestling2.move(enemy4th)
                                    self.closestling2.move(enemy5th, queue = True)
                                elif not enemy_townhalls.closer_than(4, enemy5th):
                                    self.closestling2.move(enemy5th)
                                    self.closestling2.move(enemy6th, queue = True)
                                elif not enemy_townhalls.closer_than(4, enemy6th):
                                    self.closestling2.move(enemy6th)
                                    self.closestling2.move(enemy7th, queue = True)
                                elif not enemy_townhalls.closer_than(4, enemy7th):
                                    self.closestling2.move(enemy7th)
                                    self.closestling2.move(enemy8th, queue = True)
                            else:
                                if not enemy_townhalls.closer_than(5, enemy3rd):
                                    self.closestling2.move(enemy3rd)
                                elif not enemy_townhalls.closer_than(5, enemy4th):
                                    self.closestling2.move(enemy4th, queue = True)
                                elif not enemy_townhalls.closer_than(5, enemy5th):
                                    self.closestling2.move(enemy5th, queue = True)
                                elif not enemy_townhalls.closer_than(5, enemy6th):
                                    self.closestling2.move(enemy6th, queue = True)
                                elif not enemy_townhalls.closer_than(5, enemy7th):
                                    self.closestling2.move(enemy7th, queue = True)
                                elif not enemy_townhalls.closer_than(5, enemy8th):
                                    self.closestling2.move(enemy8th, queue = True)
                                elif not enemy_townhalls.closer_than(5, our8th):
                                    self.closestling2.move(our8th, queue = True)
                                elif not enemy_townhalls.closer_than(5, our7th):
                                    self.closestling2.move(our7th, queue = True)
                                elif not enemy_townhalls.closer_than(5, our6th):
                                    self.closestling2.move(our6th, queue = True)
                                elif not enemy_townhalls.closer_than(5, our5th):
                                    self.closestling2.move(our5th, queue = True)
                                elif not enemy_townhalls.closer_than(5, our4th):
                                    self.closestling2.move(our4th, queue = True)
                                print(self.time_formatted, self.supply_used, "closest ling 2 scouting")


#################################
#enemy unit zone logic
        if lings:
            if enemies_near:
#compare unit value
                neu = self.enemy_units.filter(lambda neu:
                                              not neu.is_flying
                                              and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                              and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(lings)))
                if len(self.enemy_units.filter(lambda neu:
                                               not neu.is_flying
                                               and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                               and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(lings))).tags) > len(neu.tags):
                    neu = self.enemy_units.filter(lambda neu:
                                                  not neu.is_flying
                                                  and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                  and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(lings)))
                if len(self.enemy_units.filter(lambda neu:
                                               not neu.is_flying
                                               and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                               and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(lings))).tags) < len(neu.tags):
                    neu = self.enemy_units.filter(lambda neu:
                                                  not neu.is_flying
                                                  and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                  and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(lings)))
                for eunit in neu:
                    combinedvalue = self.calculate_unit_value(eunit.type_id).minerals + self.calculate_unit_value(eunit.type_id).vespene
                    self.totalvalue = self.totalvalue + combinedvalue
                else:
                    self.totalvalue_en = self.totalvalue
                    self.totalvalue = 0
                    print("enemy value near ling =", self.totalvalue_en)
                if lings.closer_than(10, enemies_near.in_closest_distance_to_group(lings)):
                    onu = self.units.filter(lambda onu:
                                            not onu.is_flying
                                            and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                            and onu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(lings)))
                    print("our lambda units are =", onu)
                    if len(self.units.filter(lambda onu:
                                             not onu.is_flying
                                             and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                             and onu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(lings))).tags) > len(onu.tags):
                        onu = self.units.filter(lambda onu:
                                                not onu.is_flying
                                                and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                and onu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(lings)))
                    if len(self.units.filter(lambda onu:
                                             not onu.is_flying
                                             and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                             and onu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(lings))).tags) < len(onu.tags):
                        onu = self.units.filter(lambda onu:
                                                not onu.is_flying
                                                and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                and onu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(lings)))
                    for ounit in onu:
                        combinedvalue = self.calculate_unit_value(ounit.type_id).minerals + self.calculate_unit_value(ounit.type_id).vespene
                        self.totalvalue = self.totalvalue + combinedvalue
                    else:
                        self.totalvalue_on = self.totalvalue
                        self.totalvalue = 0
                        print(self.time_formatted, self.supply_used, "self.totalvalue_on =", self.totalvalue_on)

#if further away then go to attack formation                            
                for ling in lings:
                    if ling.position.is_further_than(10, enemies_near.closest_to(ling)):
                        if queens and not self.units(UnitTypeId.ROACH):
                            if queens.closest_to(enemies_near.closest_to(ling)).is_attacking or stillattacking == True:
                                if not ling.order_target == enemies_near.closest_to(ling).tag:
                                    ling.attack(enemies_near.closest_to(ling))
                                    ling.attack(enemies_near.closest_to(ling), queue = True)
                                    print("queen and no roach stillattacking?", stillattacking)
                            else:
                                if not ling.order_target == self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3).position:
                                    print("queens not attacking and stillattacking is not true")
                                    ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3))
                                    ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3), queue = True)
                        elif self.units(UnitTypeId.ROACH) and queens:
                            if self.units(UnitTypeId.ROACH).closest_to(enemies_near.closest_to(ling)).is_attacking or queens.closest_to(enemies_near.closest_to(ling)).is_attacking or stillattacking == True:
                                if not ling.order_target == enemies_near.closest_to(ling).tag:
                                    ling.attack(enemies_near.closest_to(ling))
                                    ling.attack(enemies_near.closest_to(ling), queue = True)
                                    print(ling.orders)
                            else:
                                if self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))):
                                    if not ling.position.is_closer_than(5, self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3)):
                                        ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3))
                                        ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3), queue = True)
                        else:
                            if not ling.order_target == enemies_near.closest_to(ling).tag:
                                ling.attack(enemies_near.closest_to(ling))
                                ling.attack(enemies_near.closest_to(ling), queue = True)
                            
#if our army value is better then attack else run
                for ling in lings:
                    if ling.position.is_closer_than(10, enemies_near.closest_to(ling)):
                        print(ling)
                        if self.townhalls:
                            if (
                                self.totalvalue_en >= self.totalvalue_on and not enemies_near.closer_than(6, self.townhalls.closest_to(enemies_near.closest_to(ling))) and not self.units(UnitTypeId.QUEEN)
                                or self.totalvalue_en > self.totalvalue_on and self.units(UnitTypeId.QUEEN) and not enemies_near.closer_than(6, self.townhalls.closest_to(enemies_near.closest_to(ling)))
                                ):
                                print("Enemy has more than lings")
                                if ling.position.is_closer_than(enemies_near.closest_to(ling).ground_range, enemies_near.closest_to(ling)):
                                    self.totalvalue_en = self.totalvalue_en * 0.5
                                if (
                                    self.totalvalue_en >= self.totalvalue_on and not enemies_near.closer_than(4, self.townhalls.closest_to(enemies_near.closest_to(ling))) and not self.units(UnitTypeId.QUEEN)
                                    or self.totalvalue_en > self.totalvalue_on and self.units(UnitTypeId.QUEEN)
                                    ):
                                    print("Enemy still has more than lings")
                                    if self.units(UnitTypeId.QUEEN):
                                        ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3))
                                        ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3), queue = True)
                                        print("ling to queen1")
                                    elif lings.further_than(10, enemies_near.closest_to(ling)):
                                        ling.move(lings.further_than(10, enemies_near.closest_to(ling)).closest_to(ling))
                                        ling.move(lings.further_than(10, enemies_near.closest_to(ling)).closest_to(ling), queue = True)
                                    else:
                                        if not self.townhalls.amount == enemy_townhalls.amount:
                                            if not ling.position.is_closer_than(5, self.townhalls.ready.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3)):
                                                ling.move(self.townhalls.ready.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3))
                                                ling.move(self.townhalls.ready.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3), queue = True)
                                        if self.townhalls.amount == enemy_townhalls.amount:
                                            if not ling.position.is_closer_than(5, self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3)):
                                                ling.move(self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3))
                                                ling.move(self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3), queue = True)
                                if ling.position.is_closer_than(enemies_near.closest_to(ling).ground_range, enemies_near.closest_to(ling)):
                                    self.totalvalue_en = self.totalvalue_en * 2

                            elif (
                                self.totalvalue_on > self.totalvalue_en and not queens
                                or self.totalvalue_on >= self.totalvalue_en and queens or queens and stillattacking == True
                                or enemies_near.closer_than(4, self.townhalls.closest_to(enemies_near.closest_to(ling)))
                                ):
                                print("ours is more", stillattacking)
                                if ling.position.is_closer_than(enemies_near.closest_to(ling).ground_range, enemies_near.closest_to(ling)):
                                    self.totalvalue_en = self.totalvalue_en * 0.5
                                if not self.units(UnitTypeId.QUEEN):
                                    print("but no queen")
                                    if ling.weapon_cooldown == 0:
                                        if not ling.order_target == enemies_near.closest_to(ling).tag:
                                            ling.attack(enemies_near.closest_to(ling))
                                            ling.attack(enemies_near.closest_to(ling), queue = True)
                                            print("lwc", ling.weapon_cooldown)
                                    else:
                                        if not ling.is_moving:
                                            print("lwc and ling surrounding", ling.weapon_cooldown)
                                            ling.move(enemies_near.furthest_to(lings.closest_to(self.townhalls.in_closest_distance_to_group(enemies_near))))
                                            ling.move(enemies_near.furthest_to(lings.closest_to(self.townhalls.in_closest_distance_to_group(enemies_near))), queue = True)
                                elif self.units(UnitTypeId.QUEEN) and not roaches:
                                    print("queen and no roach stillattacking?", stillattacking)
                                    if not self.units(UnitTypeId.QUEEN).closest_to(enemies_near.closest_to(ling)).is_attacking and stillattacking == False:
                                        if not ling.position.is_closer_than(5, self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3)):
                                            ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3))
                                            ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3), queue = True)
                                            print("queen but not attacking", stillattacking)
                                    elif queens.closest_to(enemies_near.closest_to(ling)).is_attacking or stillattacking == True:
                                        if enemies_near.filter(lambda u: not u.type_id in [UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE]).closer_than(10, self.townhalls.ready.in_closest_distance_to_group(enemies_near).position) and stillattacking == True:
                                            if ling.weapon_cooldown == 0:
                                                if not ling.order_target == enemies_near.closest_to(ling).tag:
                                                    ling.attack(enemies_near.closest_to(ling))
                                                    ling.attack(enemies_near.closest_to(ling), queue = True)
                                                    print("ling attack enemy combat unit with queen and stillattacking")
                                            else:
                                                if not ling.is_moving:
                                                    print("lwc1", ling.weapon_cooldown)
                                                    ling.move(enemies_near.furthest_to(lings.closest_to(self.townhalls.in_closest_distance_to_group(enemies_near))).position.towards(self.townhalls.in_closest_distance_to_group(enemies_near), -1))
                                                    ling.move(enemies_near.furthest_to(lings.closest_to(self.townhalls.in_closest_distance_to_group(enemies_near))).position.towards(self.townhalls.in_closest_distance_to_group(enemies_near), -1), queue = True)
                                        elif enemies_near.filter(lambda u: u.type_id in [UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE]).closer_than(10, self.townhalls.ready.in_closest_distance_to_group(enemies_near).position):
                                                print("lwc2", ling.weapon_cooldown)
                                                ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3))
                                                ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3), queue = True)
                                        elif enemies_near.filter(lambda u: not u.type_id in [UnitTypeId.DRONE, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE]).closer_than(10, self.townhalls.ready.in_closest_distance_to_group(enemies_near).position) or stillattacking == True:
                                            if ling.weapon_cooldown == 0:
                                                if not ling.order_target == enemies_near.closest_to(ling).tag:
                                                    ling.attack(enemies_near.closest_to(ling))
                                                    ling.attack(enemies_near.closest_to(ling), queue = True)
                                                    print("ling attack enemy combat unit with queen or stillattacking")
                                            else:
                                                if not ling.is_moving:
                                                    print("lwc3", ling.weapon_cooldown)
                                                    ling.move(enemies_near.furthest_to(lings.closest_to(self.townhalls.in_closest_distance_to_group(enemies_near))).position.towards(self.townhalls.in_closest_distance_to_group(enemies_near), -1))
                                                    ling.move(enemies_near.furthest_to(lings.closest_to(self.townhalls.in_closest_distance_to_group(enemies_near))).position.towards(self.townhalls.in_closest_distance_to_group(enemies_near), -1), queue = True)
                                            
                                    elif not ling.position.is_closer_than(5, self.townhalls.closest_to(enemies_near.closest_to(queen)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(queen))).furthest_to(enemynat), 3)):
                                        ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3))
                                        ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3), queue = True)
                                        print("ling to queen3", stillattacking)
                                    else:
                                        if not ling.position.is_closer_than(5, self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3)):
                                            ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3))
                                            ling.move(self.townhalls.closest_to(enemies_near.closest_to(ling)).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(ling))).furthest_to(enemynat), 3), queue = True)
                                        print("ling to queen3", stillattacking)
                                elif roaches and queens:
                                    if roaches.closest_to(enemies_near.closest_to(ling)).is_attacking or queens.closest_to(enemies_near.closest_to(ling)).is_attacking or stillattacking == True:
                                        if ling.weapon_cooldown == 0:
                                            if not ling.order_target == enemies_near.closest_to(ling).tag:
                                                ling.attack(enemies_near.closest_to(ling))
                                                ling.attack(enemies_near.closest_to(ling), queue = True)
                                                print("lwc", ling.weapon_cooldown)
                                        else:
                                            if not ling.is_moving:
                                                print("lwc and ling surrounding", ling.weapon_cooldown)
                                                ling.move(enemies_near.furthest_to(lings.closest_to(self.townhalls.in_closest_distance_to_group(enemies_near))).position.towards(self.townhalls.in_closest_distance_to_group(enemies_near), -1))
                                                ling.move(enemies_near.furthest_to(lings.closest_to(self.townhalls.in_closest_distance_to_group(enemies_near))).position.towards(self.townhalls.in_closest_distance_to_group(enemies_near), -1), queue = True)
                                        
                                if ling.position.is_closer_than(enemies_near.closest_to(ling).ground_range, enemies_near.closest_to(ling)):
                                    self.totalvalue_en = self.totalvalue_en * 2


#kill the structures
            if not enemies_near and enemies_structures_near:
                for ling in lings:
                    if not ling.order_target == enemies_structures_near.closest_to(ling).tag:
                        ling.attack(enemies_structures_near.closest_to(ling))
                            
##group
            if not enemies_near and not enemies_structures_near and self.supply_used < 180:
                for ling in lings:
                    if self.townhalls:
                        if self.units(UnitTypeId.ROACH):
                            if not ling.position.is_closer_than(5, self.units(UnitTypeId.ROACH).closest_to(ling)):
                                ling.move(self.units(UnitTypeId.ROACH).closest_to(ling))
                        elif self.units(UnitTypeId.QUEEN):
                            if not self.townhalls.amount == enemy_townhalls.amount:
                                if not ling.position.is_closer_than(5, self.townhalls.ready.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3)):
                                    ling.move(self.townhalls.ready.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3))
                            if self.townhalls.amount == enemy_townhalls.amount:
                                if not ling.position.is_closer_than(5, self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3)):
                                    ling.move(self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3))
                        else:
                            if not self.townhalls.amount == enemy_townhalls.amount:
                                if not ling.position.is_closer_than(5, self.townhalls.ready.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3)):
                                    ling.move(self.townhalls.ready.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3))
                            if self.townhalls.amount == enemy_townhalls.amount:
                                if not ling.position.is_closer_than(5, self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3)):
                                    ling.move(self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3))
                        
##attack
            if (
                allenemies
                and not enemies_structures_near
                and not enemies_near
                and self.supply_used > 190
                ):
                if self.enemy_structures.not_flying:
                    if not self.enemy_structures.not_flying.in_closest_distance_to_group(lings).position.distance_to(self.enemy_structures.not_flying.in_closest_distance_to_group(lings)) < allenemies.in_closest_distance_to_group(lings).position.distance_to(allenemies.in_closest_distance_to_group(lings)):
                        neu = self.enemy_units.filter(lambda neu:
                                                      not neu.is_flying
                                                      and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                      and neu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(lings)))
                        if len(self.enemy_units.filter(lambda neu:
                                                       not neu.is_flying
                                                       and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                       and neu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(lings))).tags) > len(neu.tags):
                            neu = self.enemy_units.filter(lambda neu:
                                                          not neu.is_flying
                                                          and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                          and neu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(lings)))
                        if len(self.enemy_units.filter(lambda neu:
                                                       not neu.is_flying
                                                       and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                       and neu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(lings))).tags) < len(neu.tags):
                            neu = self.enemy_units.filter(lambda neu:
                                                          not neu.is_flying
                                                          and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                          and neu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(lings)))
                        for eunit in neu:
                            combinedvalue = self.calculate_unit_value(eunit.type_id).minerals + self.calculate_unit_value(eunit.type_id).vespene
                            self.totalvalue = self.totalvalue + combinedvalue
                        else:
                            self.totalvalue_en = self.totalvalue
                            self.totalvalue = 0
                        if lings.closer_than(10, allenemies.in_closest_distance_to_group(lings)):
                            onu = self.units.filter(lambda onu:
                                                    not onu.is_flying
                                                    and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                    and onu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(lings)))
                            print("our lambda units are =", onu)
                            if len(self.units.filter(lambda onu:
                                                     not onu.is_flying
                                                     and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                     and onu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(lings))).tags) > len(onu.tags):
                                onu = self.units.filter(lambda onu:
                                                        not onu.is_flying
                                                        and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                        and onu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(lings)))
                            if len(self.units.filter(lambda onu:
                                                     not onu.is_flying
                                                     and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                     and onu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(lings))).tags) < len(onu.tags):
                                onu = self.units.filter(lambda onu:
                                                        not onu.is_flying
                                                        and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                        and onu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(lings)))
                            for ounit in onu:
                                combinedvalue = self.calculate_unit_value(ounit.type_id).minerals + self.calculate_unit_value(ounit.type_id).vespene
                                self.totalvalue = self.totalvalue + combinedvalue
                            else:
                                self.totalvalue_on = self.totalvalue
                                self.totalvalue = 0
                                print(self.time_formatted, self.supply_used, "self.totalvalue_on =", self.totalvalue_on)

#if further away then go to attack formation                            
                        for ling in lings:
                            if not ling.position.is_closer_than(10, allenemies.closest_to(ling)) or ling.is_idle and not enemies_near:
                                if not ling.order_target == allenemies.closest_to(ling).tag:
                                    ling.attack(allenemies.closest_to(ling))

#if our army value is better then attack
                        for ling in lings:
                            if ling.position.is_closer_than(10, allenemies.closest_to(ling)):
                                if self.townhalls:
                                    if (
                                        self.totalvalue_en > self.totalvalue_on
                                        ):
                                        if lings.further_than(10, allenemies.closest_to(ling)):
                                            if not ling.order_target == lings.further_than(10, allenemies.closest_to(ling)).closest_to(ling).tag:
                                                ling.move(lings.further_than(10, allenemies.closest_to(ling)).closest_to(ling))
                                        else:
                                            if not ling.order_target == self.townhalls.closest_to(ling).tag:
                                                ling.move(self.townhalls.closest_to(ling))
                                    elif (
                                        self.totalvalue_on >= self.totalvalue_en
                                        ):
                                        if not ling.order_target == allenemies.closest_to(ling).tag:
                                            ling.attack(allenemies.closest_to(ling))
                    
                    if (
                        self.enemy_structures.not_flying
                        and not enemies_structures_near
                        and not enemies_near
                        and self.supply_used > 190
                        ):
                        if not allenemies or self.enemy_structures.not_flying.in_closest_distance_to_group(lings).position.distance_to(self.enemy_structures.not_flying.in_closest_distance_to_group(lings)) < allenemies.in_closest_distance_to_group(lings).position.distance_to(allenemies.in_closest_distance_to_group(lings)):
                            for ling in lings:
                                if not ling.order_target == self.enemy_structures.not_flying.closest_to(ling).tag:
                                    ling.attack(self.enemy_structures.not_flying.closest_to(ling))
                                    print(self.time_formatted, self.supply_used, "structure attack, our nearby units =", self.totalvalue_on)
                                    print(self.time_formatted, self.supply_used, "structure attack, enemy nearby units =", self.totalvalue_en)
                
                    if (
                        not self.enemy_structures.not_flying
                        and not allenemies
                        and not enemies_structures_near
                        and not enemies_near
                        and self.supply_used > 190
                        ):
                        for ling in lings:
                            if len(ling.orders) < 1:
                                ling.attack(enemynat)
                                ling.attack(enemymain, queue = True)
                                ling.attack(enemy3rd, queue = True)
                                ling.attack(enemy4th, queue = True)
                                print(self.time_formatted, self.supply_used, "hunt attack, our nearby units =", self.totalvalue_on)
                                print(self.time_formatted, self.supply_used, "hunt attack, enemy nearby units =", self.totalvalue_en)        

                                    
##roachies
##defend
        if roaches:
#defend against backdoor first
            if (
                self.enemy_structures(UnitTypeId.NYDUSCANAL).closer_than(50, ourmain)
                ):
                print("nydus?", self.enemy_structures(UnitTypeId.NYDUSCANAL).closer_than(50, ourmain))
                if self.structures(UnitTypeId.SPINECRAWLER).ready:
                    if not self.structures(UnitTypeId.SPINECRAWLER).ready.closest_to(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(ourmain)).target_in_range(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(ourmain)):
                        for roach in roaches.closest_n_units(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(ourmain), 5):
                            print(self.time_formatted, self.supply_used, "roach nydus defense, our nearby units =", self.totalvalue_on)
                            print(self.time_formatted, self.supply_used, "roach nydus defense, enemy nearby units =", self.totalvalue_en)
                            print(self.time_formatted, self.supply_used, "roach nydus defense, enemy nearest to roach =", self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(roach))
                            if not roach.order_target == self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(roach).position:
                                roach.attack(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(roach).position)
                        
                elif not self.structures(UnitTypeId.SPINECRAWLER).ready:
                    for roach in roaches.closest_n_units(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(ourmain), 5):
                        print(self.time_formatted, self.supply_used, "roach nydus defense, our nearby units =", self.totalvalue_on)
                        print(self.time_formatted, self.supply_used, "roach nydus defense, enemy nearby units =", self.totalvalue_en)
                        print(self.time_formatted, self.supply_used, "roach nydus defense, enemy nearest to roach =", self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(roach))
                        if not roach.order_target == self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(roach).position:
                            roach.attack(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(roach).position)
                        
#defend against enemies near
            if enemies_near and not self.enemy_structures(UnitTypeId.NYDUSCANAL).closer_than(50, ourmain):
                print("enemies near?", enemies_near == True, self.enemy_structures(UnitTypeId.NYDUSCANAL).closer_than(50, ourmain) == True)
                neu = self.enemy_units.filter(lambda neu:
                                              not neu.is_flying
                                              and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                              and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(roaches)))
                if len(self.enemy_units.filter(lambda neu:
                                               not neu.is_flying
                                               and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                               and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(roaches))).tags) > len(neu.tags):
                    neu = self.enemy_units.filter(lambda neu:
                                                  not neu.is_flying
                                                  and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                  and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(roaches)))
                if len(self.enemy_units.filter(lambda neu:
                                               not neu.is_flying
                                               and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                               and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(roaches))).tags) < len(neu.tags):
                    neu = self.enemy_units.filter(lambda neu:
                                                  not neu.is_flying
                                                  and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                  and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(roaches)))
                for eunit in neu:
                    combinedvalue = self.calculate_unit_value(eunit.type_id).minerals + self.calculate_unit_value(eunit.type_id).vespene
                    self.totalvalue = self.totalvalue + combinedvalue
                else:
                    self.totalvalue_en = self.totalvalue
                    self.totalvalue = 0
                if roaches.closer_than(10, enemies_near.in_closest_distance_to_group(roaches)):
                    onu = self.units.filter(lambda onu:
                                            not onu.is_flying
                                            and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                            and onu.position.is_closer_than(15, enemies_near.in_closest_distance_to_group(roaches)))
                    print("our lambda units are =", onu)
                    if len(self.units.filter(lambda onu:
                                             not onu.is_flying
                                             and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                             and onu.position.is_closer_than(15, enemies_near.in_closest_distance_to_group(roaches))).tags) > len(onu.tags):
                        onu = self.units.filter(lambda onu:
                                                not onu.is_flying
                                                and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                and onu.position.is_closer_than(15, enemies_near.in_closest_distance_to_group(roaches)))
                    if len(self.units.filter(lambda onu:
                                             not onu.is_flying
                                             and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                             and onu.position.is_closer_than(15, enemies_near.in_closest_distance_to_group(roaches))).tags) < len(onu.tags):
                        onu = self.units.filter(lambda onu:
                                                not onu.is_flying
                                                and not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                and onu.position.is_closer_than(15, enemies_near.in_closest_distance_to_group(roaches)))
                    for ounit in onu:
                        combinedvalue = self.calculate_unit_value(ounit.type_id).minerals + self.calculate_unit_value(ounit.type_id).vespene
                        self.totalvalue = self.totalvalue + combinedvalue
                    else:
                        self.totalvalue_on = self.totalvalue
                        self.totalvalue = 0
                        print(self.time_formatted, self.supply_used, "self.totalvalue_on =", self.totalvalue_on)
                    
#if further away then go to attack formation                                                            
                for roach in roaches:
                    if roach.position.is_further_than(10, enemies_near.closest_to(roach)) or roach.is_idle:
                        if enemy_townhalls.amount < 2 and enemies_near.closer_than(10, self.townhalls.ready.in_closest_distance_to_group(enemies_near).position) or stillattacking == True:
                            if not roach.order_target == enemies_near.closest_to(roach).tag:
                                roach.attack(enemies_near.closest_to(roach))
                        else:
                            if not roach.order_target == enemies_near.closest_to(roach).tag:
                                roach.attack(enemies_near.closest_to(roach))
                        
                        
#if our army value is better then attack
                for roach in roaches:
                    if roach.position.is_closer_than(10, enemies_near.closest_to(roach)):
                        if self.townhalls:
                            if (
                                self.totalvalue_en > self.totalvalue_on and not enemies_near.closer_than(4, self.townhalls.closest_to(enemies_near.closest_to(roach)))
                                ):
                                print("nearby enemy value is higher so we run", self.totalvalue_en > self.totalvalue_on)
                                if roaches.further_than(10, enemies_near.closest_to(roach)):
                                    if enemies_near.closest_to(roach).position.distance_to(roaches.further_than(10, enemies_near.closest_to(roach)).closest_to(roach)) > roach.position.distance_to(roaches.further_than(10, enemies_near.closest_to(roach)).closest_to(roach)):
                                        roach.move(roaches.further_than(10, enemies_near.closest_to(roach)).closest_to(roach))
                                    elif enemies_near.closest_to(roach).position.distance_to(roaches.further_than(10, enemies_near.closest_to(roach)).closest_to(roach)) > roach.position.distance_to(self.townhalls.closest_to(roach)):
                                        roach.move(self.townhalls.closest_to(roach))
                                    else:
                                        roach.move(enemies_near.closest_to(roach).position.towards(roach, 11))
                                elif queens.further_than(10, enemies_near.closest_to(roach)):
                                    if enemies_near.closest_to(roach).position.distance_to(queens.further_than(10, enemies_near.closest_to(roach)).closest_to(roach)) > roach.position.distance_to(queens.further_than(10, enemies_near.closest_to(roach)).closest_to(roach)):
                                        roach.move(queens.further_than(10, enemies_near.closest_to(roach)).closest_to(roach))
                                    elif enemies_near.closest_to(roach).position.distance_to(queens.further_than(10, enemies_near.closest_to(roach)).closest_to(roach)) > roach.position.distance_to(self.townhalls.closest_to(roach)):
                                        roach.move(self.townhalls.closest_to(roach))
                                    else:
                                        roach.move(enemies_near.closest_to(roach).position.towards(roach, 11))
                                else:
                                    roach.move(enemies_near.closest_to(roach).position.towards(roach, 11))
                                
                            elif (
                                enemies_near.closer_than(10, self.townhalls.closest_to(enemies_near.closest_to(roach)))
                                or stillattacking == True
                                ):
                                if self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)):
                                    if (
                                        roach.weapon_cooldown == 0
                                        ):
                                        if not roach.order_target == enemies_near.closest_to(roach).tag:
                                            roach.attack(enemies_near.closest_to(roach))
                                            roach.attack(enemies_near.closest_to(roach), queue = True)
                                            print(self.time_formatted, self.supply_used, "roach unit attack, our nearby units =", self.totalvalue_on)
                                            print(self.time_formatted, self.supply_used, "roach unit attack, enemy nearby units =", self.totalvalue_en)
                                    else:
                                        if (
                                            roach.target_in_range(enemies_near.closest_to(roach))
                                            and enemies_near.closest_to(roach).ground_range < 4
                                            ):
                                            if not roach.is_moving:
                                                roach.move(enemies_near.closest_to(roach).position.towards(roach, 4))
                                        else:
                                            if not roach.is_moving:
                                                roach.move(enemies_near.closest_to(roach).position)
                                

#kill the structures                
            if not enemies_near and enemies_structures_near:
                print("structures?", enemies_structures_near == True, enemies_near == False)
                for roach in roaches:
                    if not roach.order_target == enemies_structures_near.closest_to(roach).tag:
                        roach.attack(enemies_structures_near.closest_to(roach))
##group
            if not enemies_near and not enemies_structures_near and self.supply_used < 180:
                print("group?", enemies_near, enemies_structures_near, self.supply_used < 180)
                for roach in roaches:
                    if self.townhalls:
                        if not self.townhalls.amount == enemy_townhalls.amount and not roach.position.is_closer_than(5, self.townhalls.ready.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3)):
                            if not roach.order_target == self.townhalls.ready.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3).position:
                                roach.move(self.townhalls.ready.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3))
                        if self.townhalls.amount == enemy_townhalls.amount and not roach.position.is_closer_than(5, self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3)):
                            if not roach.order_target == self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3).position:
                                roach.move(self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3))
                    print(self.time_formatted, self.supply_used, "unit group, our units total =", self.totalvalue_o)
                    print(self.time_formatted, self.supply_used, "unit group, enemy units total =", self.totalvalue_e)
##attack
            if (
                allenemies
                and not enemies_structures_near
                and not enemies_near
                ):
                if self.supply_used > 190 or self.structures(UnitTypeId.SPINECRAWLER).amount >= self.townhalls.amount * 5:
                    if self.enemy_structures.not_flying:
                        if not self.enemy_structures.not_flying.in_closest_distance_to_group(roaches).position.distance_to(self.enemy_structures.not_flying.in_closest_distance_to_group(roaches)) < allenemies.in_closest_distance_to_group(roaches).position.distance_to(allenemies.in_closest_distance_to_group(roaches)):
                            print("attack enemies?", allenemies, self.supply_used > 190, enemies_structures_near, enemies_near)
                            for roach in roaches:
                                if (
                                    roach.weapon_cooldown == 0
                                    ):
                                    if not roach.is_attacking:
                                        roach.attack(allenemies.closest_to(roach).position)
                                    print(self.time_formatted, self.supply_used, "roach unit attack, our nearby units =", self.totalvalue_on)
                                    print(self.time_formatted, self.supply_used, "roach unit attack, enemy nearby units =", self.totalvalue_en)
                                else:
                                    if (
                                        roach.target_in_range(allenemies.closest_to(roach))
                                        and allenemies.closest_to(roach).ground_range < 4
                                        ):
                                        roach.move(allenemies.closest_to(roach).position.towards(roach, 4))
                                    else:
                                        roach.move(allenemies.closest_to(roach).position)

            if (
                self.enemy_structures.not_flying
                and not enemies_structures_near
                and not enemies_near
                ):
                if self.supply_used > 190 or self.structures(UnitTypeId.SPINECRAWLER).amount >= self.townhalls.amount * 5:
                    if not allenemies or self.enemy_structures.not_flying.in_closest_distance_to_group(roaches).position.distance_to(self.enemy_structures.not_flying.in_closest_distance_to_group(roaches)) < allenemies.in_closest_distance_to_group(roaches).position.distance_to(allenemies.in_closest_distance_to_group(roaches)):
                        print("attack structures?", self.enemy_structures.not_flying, self.supply_used > 190, allenemies, enemies_structures_near, enemies_near)
                        for roach in roaches:
                            if (
                                roach.weapon_cooldown == 0
                                ):
                                if not roach.order_target == self.enemy_structures.not_flying.closest_to(roach).tag:
                                    roach.attack(self.enemy_structures.not_flying.closest_to(roach))
                                print(self.time_formatted, self.supply_used, "roach structure attack, our nearby units =", self.totalvalue_on)
                                print(self.time_formatted, self.supply_used, "roach structure attack, enemy nearby units =", self.totalvalue_en)
                            else:
                                if not roach.is_moving:
                                    roach.move(self.enemy_structures.not_flying.closest_to(roach))
                        
            if (
                not self.enemy_structures.not_flying
                and not allenemies
                and not enemies_structures_near
                and not enemies_near
                ):
                if self.supply_used > 190 or self.structures(UnitTypeId.SPINECRAWLER).amount >= self.townhalls.amount * 5:
                    for roach in roaches:
                        if len(roach.orders) < 1:
                            roach.attack(enemynat)
                            roach.attack(enemymain, queue = True)
                            roach.attack(enemy3rd, queue = True)
                            roach.attack(enemy4th, queue = True)

        enemies_near = Units([], self)
        enemies_structures_near = Units([], self)

##hydraz
##defend
        
#hatchery zonal defense system
#enemy units near hatcheries
        for hatch in self.townhalls:
            if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                enemies_near.extend(
                    self.enemy_units.filter(
                        lambda u: u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                        and u.distance_to(hatch) < 40
                    )
                )
#enemy structures near hatcheries
            print(self.time_formatted, self.supply_used, "enemies near =", enemies_near)
            if self.enemy_structures.not_flying.closer_than(40, hatch):
                enemies_structures_near.extend(
                    self.enemy_structures.filter(
                        lambda s: s.distance_to(hatch) < 40
                    )
                )
            print(self.time_formatted, self.supply_used, "enemies structures near =", enemies_structures_near)
        print(self.time_formatted, self.supply_used, "enemies near total =", enemies_near.amount)
        print(self.time_formatted, self.supply_used, "enemies structures total =", enemies_structures_near.amount)
        allenemies = self.enemy_units.filter(lambda ae:
                                             not ae.type_id in (UnitTypeId.EGG, UnitTypeId.LARVA))


        if hydras:
#defend against backdoor first
            if (
                self.enemy_structures(UnitTypeId.NYDUSCANAL).closer_than(50, ourmain)
                ):
                print("nydus?", self.enemy_structures(UnitTypeId.NYDUSCANAL).closer_than(50, ourmain))
                if self.structures(UnitTypeId.SPINECRAWLER).ready:
                    if not self.structures(UnitTypeId.SPINECRAWLER).ready.closest_to(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(ourmain)).target_in_range(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(ourmain)):
                        for hydra in hydras.closest_n_units(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(ourmain), 5):
                            print(self.time_formatted, self.supply_used, "hydra nydus defense, our nearby units =", self.totalvalue_on)
                            print(self.time_formatted, self.supply_used, "hydra nydus defense, enemy nearby units =", self.totalvalue_en)
                            print(self.time_formatted, self.supply_used, "hydra nydus defense, enemy nearest to hydra =", self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(hydra))
                            if not hydra.order_target == self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(hydra).tag:
                                hydra.attack(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(hydra))
                        
                elif not self.structures(UnitTypeId.SPINECRAWLER).ready:
                    for hydra in hydras.closest_n_units(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(ourmain), 5):
                        print(self.time_formatted, self.supply_used, "hydra nydus defense, our nearby units =", self.totalvalue_on)
                        print(self.time_formatted, self.supply_used, "hydra nydus defense, enemy nearby units =", self.totalvalue_en)
                        print(self.time_formatted, self.supply_used, "hydra nydus defense, enemy nearest to hydra =", self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(hydra))
                        if not hydra.order_target == self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(hydra).tag:
                            hydra.attack(self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(hydra))
                        
#defend against enemies near
            if enemies_near and not self.enemy_structures(UnitTypeId.NYDUSCANAL).closer_than(50, ourmain):
                print("enemies near?", enemies_near == True, self.enemy_structures(UnitTypeId.NYDUSCANAL).closer_than(50, ourmain) == True)
                neu = self.enemy_units.filter(lambda neu:
                                              not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                              and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(hydras)))
                if len(self.enemy_units.filter(lambda neu:
                                               not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                               and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(hydras))).tags) > len(neu.tags):
                    neu = self.enemy_units.filter(lambda neu:
                                                  not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                  and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(hydras)))
                if len(self.enemy_units.filter(lambda neu:
                                               not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                               and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(hydras))).tags) < len(neu.tags):
                    neu = self.enemy_units.filter(lambda neu:
                                                  not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                  and neu.position.is_closer_than(10, enemies_near.in_closest_distance_to_group(hydras)))
                for eunit in neu:
                    combinedvalue = self.calculate_unit_value(eunit.type_id).minerals + self.calculate_unit_value(eunit.type_id).vespene
                    self.totalvalue = self.totalvalue + combinedvalue
                else:
                    self.totalvalue_en = self.totalvalue
                    self.totalvalue = 0
                if hydras.closer_than(10, enemies_near.in_closest_distance_to_group(hydras)):
                    onu = self.units.filter(lambda onu:
                                            not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                            and onu.position.is_closer_than(15, enemies_near.in_closest_distance_to_group(hydras)))
                    print("our lambda units are =", onu)
                    if len(self.units.filter(lambda onu:
                                             not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                             and onu.position.is_closer_than(15, enemies_near.in_closest_distance_to_group(hydras))).tags) > len(onu.tags):
                        onu = self.units.filter(lambda onu:
                                                not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                and onu.position.is_closer_than(15, enemies_near.in_closest_distance_to_group(hydras)))
                    if len(self.units.filter(lambda onu:
                                             not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                             and onu.position.is_closer_than(15, enemies_near.in_closest_distance_to_group(hydras))).tags) < len(onu.tags):
                        onu = self.units.filter(lambda onu:
                                                not onu.type_id in [UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA]
                                                and onu.position.is_closer_than(15, enemies_near.in_closest_distance_to_group(hydras)))
                    for ounit in onu:
                        combinedvalue = self.calculate_unit_value(ounit.type_id).minerals + self.calculate_unit_value(ounit.type_id).vespene
                        self.totalvalue = self.totalvalue + combinedvalue
                    else:
                        self.totalvalue_on = self.totalvalue
                        self.totalvalue = 0
                        print(self.time_formatted, self.supply_used, "self.totalvalue_on =", self.totalvalue_on)
                                
#if further away then go to attack formation                                                            
                for hydra in hydras:
                    if hydra.position.is_further_than(10, enemies_near.closest_to(hydra)) or hydra.is_idle:
                        if not hydra.order_target == enemies_near.closest_to(hydra).tag:
                            hydra.attack(enemies_near.closest_to(hydra))
                        
#if our army value is better then attack
                for hydra in hydras:
                    if hydra.position.is_closer_than(10, enemies_near.closest_to(hydra)):
                        if self.townhalls:
                            if (
                                self.totalvalue_en > self.totalvalue_on and not enemies_near.closer_than(4, self.townhalls.closest_to(enemies_near.closest_to(hydra)))
                                ):
                                print("nearby enemy value is higher so we run", self.totalvalue_en > self.totalvalue_on)
                                if hydras.further_than(10, enemies_near.closest_to(hydra)):
                                    if enemies_near.closest_to(hydra).position.distance_to(hydras.further_than(10, enemies_near.closest_to(hydra)).closest_to(hydra)) > hydra.position.distance_to(hydras.further_than(10, enemies_near.closest_to(hydra)).closest_to(hydra)):
                                        hydra.move(hydras.further_than(10, enemies_near.closest_to(hydra)).closest_to(hydra))
                                    elif enemies_near.closest_to(hydra).position.distance_to(hydras.further_than(10, enemies_near.closest_to(hydra)).closest_to(hydra)) > hydra.position.distance_to(self.townhalls.closest_to(hydra)):
                                        hydra.move(self.townhalls.closest_to(hydra))
                                    else:
                                        hydra.move(enemies_near.closest_to(hydra).position.towards(hydra, 11))
                            elif (
                                self.totalvalue_on >= self.totalvalue_en
                                or enemies_near.closer_than(4, self.townhalls.closest_to(enemies_near.closest_to(hydra)))
                                ):
                                if self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)):
                                    if (
                                        hydra.weapon_cooldown == 0
                                        ):
                                        if not hydra.order_target == enemies_near.closest_to(hydra).tag:
                                            hydra.attack(enemies_near.closest_to(hydra))
                                        print(self.time_formatted, self.supply_used, "hydra unit attack, our nearby units =", self.totalvalue_on)
                                        print(self.time_formatted, self.supply_used, "hydra unit attack, enemy nearby units =", self.totalvalue_en)
                                    else:
                                        if (
                                            hydra.target_in_range(enemies_near.closest_to(hydra))
                                            and enemies_near.closest_to(hydra).ground_range < 5
                                            ):
                                            hydra.move(enemies_near.closest_to(hydra).position.towards(hydra, 5))
                                        else:
                                            hydra.move(enemies_near.closest_to(hydra).position)

#kill the structures                
            if not enemies_near and enemies_structures_near:
                print("structures?", enemies_structures_near == True, enemies_near == False)
                for hydra in hydras:
                    if not hydra.order_target == enemies_structures_near.closest_to(hydra).tag:
                        hydra.attack(enemies_structures_near.closest_to(hydra))
##group
            if not enemies_near and not enemies_structures_near and self.supply_used < 180:
                print("group?", enemies_near, enemies_structures_near, self.supply_used < 180)
                for hydra in hydras:
                    if not self.townhalls.amount == enemy_townhalls.amount and not hydra.position.is_closer_than(5, self.townhalls.ready.closest_to(enemymain).position.towards(enemymain, 7)):
                        if not hydra.order_target == self.townhalls.ready.closest_to(enemymain).position.towards(enemymain, 4).position:
                            hydra.move(self.townhalls.ready.closest_to(enemymain).position.towards(enemymain, 4))
                    if self.townhalls.amount == enemy_townhalls.amount and not hydra.position.is_closer_than(5, self.townhalls.ready.closest_to(enemymain).position.towards(enemymain, 7)):
                        if not hydra.order_target == self.townhalls.closest_to(enemymain).position.towards(enemymain, 4).position:
                            hydra.move(self.townhalls.closest_to(enemymain).position.towards(enemymain, 4))
                    print(self.time_formatted, self.supply_used, "unit group, our units total =", self.totalvalue_o)
                    print(self.time_formatted, self.supply_used, "unit group, enemy units total =", self.totalvalue_e)
##attack
            if (
                allenemies
                and not enemies_structures_near
                and not enemies_near
                ):
                if self.supply_used > 190 or self.structures(UnitTypeId.SPINECRAWLER).amount >= self.townhalls.amount * 5:
                    if self.enemy_structures.not_flying:
                        if not self.enemy_structures.not_flying.in_closest_distance_to_group(hydras).position.distance_to(self.enemy_structures.not_flying.in_closest_distance_to_group(hydras)) < allenemies.in_closest_distance_to_group(hydras).position.distance_to(allenemies.in_closest_distance_to_group(hydras)):
                            print("attack enemies?", allenemies, self.supply_used > 190, enemies_structures_near, enemies_near)
                            neu = self.enemy_units.filter(lambda neu:
                                                          not neu.is_flying
                                                          and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                          and neu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(hydras)))
                            if len(self.enemy_units.filter(lambda neu:
                                                           not neu.is_flying
                                                           and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                           and neu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(hydras))).tags) > len(neu.tags):
                                neu = self.enemy_units.filter(lambda neu:
                                                              not neu.is_flying
                                                              and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                              and neu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(hydras)))
                            if len(self.enemy_units.filter(lambda neu:
                                                           not neu.is_flying
                                                           and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                           and neu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(hydras))).tags) < len(neu.tags):
                                neu = self.enemy_units.filter(lambda neu:
                                                              not neu.is_flying
                                                              and not neu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                                                              and neu.position.is_closer_than(10, allenemies.in_closest_distance_to_group(hydras)))
                            for eunit in neu:
                                combinedvalue = self.calculate_unit_value(eunit.type_id).minerals + self.calculate_unit_value(eunit.type_id).vespene
                                self.totalvalue = self.totalvalue + combinedvalue
                            else:
                                self.totalvalue_en = self.totalvalue
                                self.totalvalue = 0
                            if hydras.closer_than(10, allenemies.in_closest_distance_to_group(hydras)):
                                onu = self.units.filter(lambda onu:
                                                        not onu.is_flying
                                                        and not onu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)
                                                        and onu.position.is_closer_than(15, allenemies.in_closest_distance_to_group(hydras)))
                                if len(self.units.filter(lambda onu:
                                                         not onu.is_flying
                                                         and not onu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)
                                                         and onu.position.is_closer_than(15, allenemies.in_closest_distance_to_group(hydras))).tags) > len(onu.tags):
                                    onu = self.units.filter(lambda onu:
                                                            not onu.is_flying
                                                            and not onu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)
                                                            and onu.position.is_closer_than(15, allenemies.in_closest_distance_to_group(hydras)))
                                if len(self.units.filter(lambda onu:
                                                         not onu.is_flying
                                                         and not onu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)
                                                         and onu.position.is_closer_than(15, allenemies.in_closest_distance_to_group(hydras))).tags) < len(onu.tags):
                                    onu = self.units.filter(lambda onu:
                                                            not onu.is_flying
                                                            and not onu.type_id in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)
                                                            and onu.position.is_closer_than(15, allenemies.in_closest_distance_to_group(hydras)))
                                for ounit in onu:
                                    combinedvalue = self.calculate_unit_value(ounit.type_id).minerals + self.calculate_unit_value(ounit.type_id).vespene
                                    self.totalvalue = self.totalvalue + combinedvalue
                                else:
                                    self.totalvalue_on = self.totalvalue
                                    self.totalvalue = 0
                                    print(self.time_formatted, self.supply_used, "self.totalvalue_on =", self.totalvalue_on)
                                        
#if further away then go to attack formation                                                            
                            for hydra in hydras:
                                if hydra.position.is_further_than(10, allenemies.closest_to(hydra)) or hydra.is_idle:
                                    if not hydra.order_target == allenemies.closest_to(hydra).tag:
                                        hydra.attack(allenemies.closest_to(hydra))
                        
#if our army value is better then attack
                            for hydra in hydras:
                                if (
                                    self.totalvalue_en > self.totalvalue_on
                                    ):
                                    if hydras.further_than(10, allenemies.closest_to(hydra)):
                                        if allenemies.closest_to(hydra).position.distance_to(hydras.further_than(10, allenemies.closest_to(hydra)).closest_to(hydra)) > hydra.position.distance_to(hydras.further_than(10, allenemies.closest_to(hydra)).closest_to(hydra)):
                                            hydra.move(hydras.further_than(10, allenemies.closest_to(hydra)).closest_to(hydra))
                                        elif allenemies.closest_to(hydra).position.distance_to(hydras.further_than(10, allenemies.closest_to(hydra)).closest_to(hydra)) > hydra.position.distance_to(self.townhalls.closest_to(hydra)):
                                            hydra.move(self.townhalls.closest_to(hydra))
                                        else:
                                            hydra.move(allenemies.closest_to(hydra).position.towards(hydra, 11))
                                elif (
                                    self.totalvalue_on >= self.totalvalue_en
                                    ):
                                    if self.enemy_units.not_flying.exclude_type((UnitTypeId.EGG, UnitTypeId.LARVA)):
                                        if (
                                            hydra.weapon_cooldown == 0
                                            ):
                                            if not hydra.order_target == allenemies.closest_to(hydra).tag:
                                                hydra.attack(allenemies.closest_to(hydra))
                                            print(self.time_formatted, self.supply_used, "hydra unit attack, our nearby units =", self.totalvalue_on)
                                            print(self.time_formatted, self.supply_used, "hydra unit attack, enemy nearby units =", self.totalvalue_en)
                                        else:
                                            if (
                                                hydra.target_in_range(allenemies.closest_to(hydra))
                                                and allenemies.closest_to(hydra).ground_range < 5
                                                ):
                                                hydra.move(allenemies.closest_to(hydra).position.towards(hydra, 5))
                                            else:
                                                hydra.move(allenemies.closest_to(hydra).position)

            if (
                self.enemy_structures.not_flying
                and not enemies_structures_near
                and not enemies_near
                ):
                if self.supply_used > 190 or self.structures(UnitTypeId.SPINECRAWLER).amount >= self.townhalls.amount * 5:
                    if not allenemies or self.enemy_structures.not_flying.in_closest_distance_to_group(hydras).position.distance_to(self.enemy_structures.not_flying.in_closest_distance_to_group(hydras)) < allenemies.in_closest_distance_to_group(hydras).position.distance_to(allenemies.in_closest_distance_to_group(hydras)):
                        print("attack structures?", self.enemy_structures.not_flying, self.supply_used > 190, allenemies, enemies_structures_near, enemies_near)
                        for hydra in hydras:
                            if (
                                hydra.weapon_cooldown == 0
                                ):
                                if not hydra.order_target == self.enemy_structures.not_flying.closest_to(hydra).tag:
                                    hydra.attack(self.enemy_structures.not_flying.closest_to(hydra))
                                print(self.time_formatted, self.supply_used, "hydra structure attack, our nearby units =", self.totalvalue_on)
                                print(self.time_formatted, self.supply_used, "hydra structure attack, enemy nearby units =", self.totalvalue_en)
                            else:
                                if not hydra.is_moving:
                                    hydra.move(self.enemy_structures.not_flying.closest_to(hydra).position)
                        
            if (
                not self.enemy_structures.not_flying
                and not allenemies
                and not enemies_structures_near
                and not enemies_near
                ):
                if self.supply_used > 190 or self.structures(UnitTypeId.SPINECRAWLER).amount >= self.townhalls.amount * 5:
                    print("hunt?", self.supply_used > 190, self.enemy_structures.not_flying, allenemies, enemies_structures_near, enemies_near)
                    for hydra in hydras:
                        if len(hydra.orders) < 1:
                            hydra.attack(enemynat)
                            hydra.attack(enemymain, queue = True)
                            hydra.attack(enemy3rd, queue = True)
                            hydra.attack(enemy4th, queue = True)

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
            and self.time > 180
            and self.has_creep(Point2(roachwarrenwall))
            ):
            if (
                self.enemy_structures(UnitTypeId.ROACHWARREN)
                or enemy_gas_buildings
                or self.enemy_structures(UnitTypeId.BANELINGNEST)
                or self.enemy_units(UnitTypeId.BANELING)
                or self.enemy_units(UnitTypeId.ROACH)
                or self.enemy_units(UnitTypeId.HYDRALISK)
                or self.time > 300
                ):
                if self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource):
                    if enemy_townhalls.amount > 1:
                        self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource).closest_to(ournat).build(UnitTypeId.ROACHWARREN, Point2(roachwarrenwall))
                    elif enemy_townhalls.amount < 2:
                        self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource).closest_to(ournat).build(UnitTypeId.ROACHWARREN, ourmain.position.towards(enemy4th, 7))
                
                

    async def build_roaches(self):
        if not self.larva:
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        larva = self.larva.random
        enemies_near = Units([], self)
        makeroaches = True
    
        for hatch in self.townhalls:
            if not enemies_near:
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                    enemies_near.extend(
                        self.enemy_units.filter(
                            lambda u: not u.is_flying
                            and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                            and u.distance_to(hatch) < 40
                        )
                    )
                    
        if self.structures(UnitTypeId.EXTRACTOR):
            for hatch in self.townhalls:
                for gas in self.structures(UnitTypeId.EXTRACTOR):
                    if self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount * 16) + (enemy_townhalls.amount * 4) + (enemy_gas_buildings.amount * 3):
                        makeroaches = False
        print("make roaches1?", makeroaches)
        if enemy_townhalls.amount > 1:
            if self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.idle or self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL1) and self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL1):
                if (
                    not self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL1)
                    or not self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL1)
                    or not self.already_pending(UnitTypeId.LAIR) and not self.structures(UnitTypeId.LAIR).ready
                    ):
                    makeroaches = False
                if self.structures(UnitTypeId.LAIR).ready:
                    if (
                        not self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL2)
                        and not self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL2)
                        ):
                        makeroaches = False
        print("make roaches2?", makeroaches)
        if self.structures(UnitTypeId.ROACHWARREN).ready and self.structures(UnitTypeId.LAIR).ready:
            if not self.already_pending(UpgradeId.GLIALRECONSTITUTION):
                makeroaches = False
        print("make roaches3?", makeroaches)
        if self.structures(UnitTypeId.HYDRALISKDEN).ready:
            if self.units(UnitTypeId.HYDRALISK).amount + self.already_pending(UnitTypeId.HYDRALISK) < self.enemy_units.flying.filter(lambda flyer: not flyer.type_id in (UnitTypeId.OVERLORD, UnitTypeId.OVERSEER, UnitTypeId.OBSERVER)).amount * 2:
                makeroaches = False
        print("make roaches4?", makeroaches)
        
        if (
            self.supply_left > self.townhalls.ready.amount * 6
            or self.already_pending(UnitTypeId.OVERLORD) >= 1
            and not self.supply_left == 0
            or self.supply_cap > 199
            ):
            if (
                self.can_afford(UnitTypeId.ROACH)
                and self.structures(UnitTypeId.ROACHWARREN).ready
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                and enemies_near
                and not self.totalvalue_o > self.totalvalue_e * 3
                or self.supply_cap > 199
                and enemies_near
                ):
                larva.train(UnitTypeId.ROACH)
                print(self.time_formatted, self.supply_used, "emergency roaches on the way")
            if (
                self.can_afford(UnitTypeId.ROACH)
                and self.structures(UnitTypeId.ROACHWARREN).ready
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                and self.totalvalue_o < self.totalvalue_e
                and makeroaches == True
                ):
                larva.train(UnitTypeId.ROACH)
                print(self.time_formatted, self.supply_used, "our combat units =", self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).amount)
                print(self.time_formatted, self.supply_used, "enemy combat units =", self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                print(self.time_formatted, self.supply_used, "too many enemies, making roaches")
            if (
                makeroaches == True
                and self.townhalls.amount + self.already_pending(UnitTypeId.HATCHERY) > enemy_townhalls.amount
                and self.can_afford(UnitTypeId.ROACH)
                and self.structures(UnitTypeId.ROACHWARREN).ready
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                or self.units(UnitTypeId.DRONE).amount > 95
                and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                and self.can_afford(UnitTypeId.ROACH)
                and self.structures(UnitTypeId.ROACHWARREN).ready
                ):
                larva.train(UnitTypeId.ROACH)
                print(self.time_formatted, self.supply_used, "too many drones, making roaches")

    async def build_hydras(self):
        if not self.larva:
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        larva = self.larva.random
        enemies_near = Units([], self)
        makehydras = True
    
        for hatch in self.townhalls:
            if not enemies_near:
                if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                    enemies_near.extend(
                        self.enemy_units.filter(
                            lambda u: not u.is_flying
                            and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                            and u.distance_to(hatch) < 40
                        )
                    )
                    
        if self.structures(UnitTypeId.EXTRACTOR):
            for hatch in self.townhalls:
                for gas in self.structures(UnitTypeId.EXTRACTOR):
                    if self.supply_workers + self.already_pending(UnitTypeId.DRONE) < (enemy_townhalls.amount * 16) + (enemy_townhalls.amount * 4) + (enemy_gas_buildings.amount * 3):
                        makehydras = False
        print("make hydras1?", makehydras)
                        
        if self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.idle or self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL1) and self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL1):
            if (
                not self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL1)
                or not self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL1)
                or not self.already_pending(UnitTypeId.LAIR) and not self.structures(UnitTypeId.LAIR).ready
                ):
                makehydras = False
            if self.structures(UnitTypeId.LAIR).ready:
                if (
                    not self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL2)
                    and not self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL2)
                    ):
                    makehydras = False
        print("make hydras3?", makehydras)
        if self.structures(UnitTypeId.HYDRALISKDEN).ready.idle and self.structures(UnitTypeId.LAIR).ready:
            if not self.already_pending(UpgradeId.EVOLVEMUSCULARAUGMENTS):
                makehydras = False
            if not self.already_pending(UpgradeId.EVOLVEGROOVEDSPINES):
                makehydras = False
        print("make hydras4?", makehydras)
        if self.enemy_units.flying.filter(lambda flyer: not flyer.type_id in (UnitTypeId.OVERLORD, UnitTypeId.OVERSEER, UnitTypeId.OBSERVER)) or self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL3):
            if (
                self.supply_left > self.townhalls.ready.amount * 6
                or self.already_pending(UnitTypeId.OVERLORD) >= 1
                and not self.supply_left == 0
                or self.supply_cap > 199
                ):
                if (
                    self.can_afford(UnitTypeId.HYDRALISK)
                    and self.structures(UnitTypeId.HYDRALISKDEN).ready
                    and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                    and enemies_near
                    and self.townhalls.amount + self.already_pending(UnitTypeId.HATCHERY) >= enemy_townhalls.amount
                    or self.supply_cap > 199
                    and enemies_near
                    ):
                    larva.train(UnitTypeId.HYDRALISK)
                    print(self.time_formatted, self.supply_used, "emergency hydras on the way")
                if (
                    self.can_afford(UnitTypeId.HYDRALISK)
                    and self.structures(UnitTypeId.HYDRALISKDEN).ready
                    and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                    and self.totalvalue_o < self.totalvalue_e
                    and makehydras == True
                    ):
                    larva.train(UnitTypeId.HYDRALISK)
                    print(self.time_formatted, self.supply_used, "our combat units =", self.units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.QUEEN)).amount)
                    print(self.time_formatted, self.supply_used, "enemy combat units =", self.enemy_units.exclude_type((UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA)).amount)
                    print(self.time_formatted, self.supply_used, "too many enemies, making hydras")
                if (
                    makehydras == True
                    and self.townhalls.amount + self.already_pending(UnitTypeId.HATCHERY) > enemy_townhalls.amount
                    and self.can_afford(UnitTypeId.HYDRALISK)
                    and self.structures(UnitTypeId.HYDRALISKDEN).ready
                    and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                    or self.units(UnitTypeId.DRONE).amount > 95
                    and self.units(UnitTypeId.ZERGLING).amount + self.already_pending(UnitTypeId.ZERGLING) > 0
                    and self.can_afford(UnitTypeId.HYDRALISK)
                    and self.structures(UnitTypeId.HYDRALISKDEN).ready
                    ):
                    larva.train(UnitTypeId.HYDRALISK)
                    print(self.time_formatted, self.supply_used, "too many drones, making hydras")
                

    async def build_queens(self):
        if not self.townhalls.ready:
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        if (
            self.can_afford(UnitTypeId.QUEEN)
            and self.townhalls.ready.idle
            and self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) < self.townhalls.amount
            and self.structures(UnitTypeId.SPAWNINGPOOL).ready
            ):
            self.train(UnitTypeId.QUEEN, 1)
        print(self.wallqueen)
        if self.can_afford(UnitTypeId.QUEEN) and self.structures(UnitTypeId.SPAWNINGPOOL).ready and self.units(UnitTypeId.QUEEN).amount + self.already_pending(UnitTypeId.QUEEN) <= self.townhalls.amount and not self.wallqueen:
            if self.already_pending(UnitTypeId.EVOLUTIONCHAMBER) or self.structures(UnitTypeId.EVOLUTIONCHAMBER):
                self.train(UnitTypeId.QUEEN, 1)
                
        if self.enemyworkers < 15 and self.can_afford(UnitTypeId.QUEEN) and self.larva.amount < 1 and self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            self.train(UnitTypeId.QUEEN, 1)
            
    async def split_queens(self):
        if not self.units(UnitTypeId.QUEEN):
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        queens = self.units(UnitTypeId.QUEEN)
        enemies_near = Units([], self)
        enemies_structures_near = Units([], self)
#hatchery zonal defense system
#enemy units near hatcheries
        for hatch in self.townhalls:
            if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                enemies_near.extend(
                    self.enemy_units.filter(
                        lambda u: not u.is_flying
                        and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                        and u.distance_to(hatch) < 40
                    )
                )
                
#enemy structures near hatcheries
            if self.enemy_structures.not_flying.closer_than(40, hatch):
                enemies_structures_near.extend(
                    self.enemy_structures.filter(
                        lambda s: not s.is_flying
                        and s.distance_to(hatch) < 40
                    )
                )


        if self.wallqueen:
            self.wallqueen = queens.find_by_tag(self.wallqueentag)

        if self.wallqueen:
            self.wallqueen = queens.find_by_tag(self.wallqueentag)
            queens.remove(self.wallqueen)
            print(self.time_formatted, self.supply_used, "wallqueen position", self.wallqueen.position)
            if len(self.wallqueen.orders) < 2 and not self.units.exclude_type((UnitTypeId.OVERLORD, UnitTypeId.QUEEN)).closer_than(2, Point2(wql)):
                if not self.wallqueen.position.is_closer_than(1, Point2(wql)):
                    if not queens.closer_than(2, Point2(wql)):
                        print("wallqueen moving again")
                        self.wallqueen.move(Point2(wql))
                        self.wallqueen.hold_position(queue = True)
                        self.wallqueen.hold_position(queue = True)
        
        if not self.wallqueen:
            if queens.amount > 3:
                if self.structures(UnitTypeId.EVOLUTIONCHAMBER).amount > 1 and self.structures(UnitTypeId.EVOLUTIONCHAMBER):
                    self.wallqueentag = queens.closest_to(Point2(evowall1)).tag
                    self.wallqueen = queens.find_by_tag(self.wallqueentag)
                    queens.remove(self.wallqueen)
                    if not self.wallqueen.position.is_closer_than(1, Point2(wql)):
                        print("wallqueen moving")
                        self.wallqueen.move(Point2(wql))
                        self.wallqueen.hold_position(queue = True)
                        
        if self.wallqueen:
            if self.wallqueen.position.is_closer_than(3, Point2(wql)):
                print("wallqueen is there")
                if self.units.exclude_type((UnitTypeId.OVERLORD, UnitTypeId.QUEEN)).closer_than(2, self.wallqueen) or queens.closer_than(2, self.wallqueen):
                    print("wallqueen has units nearby")
                    print(self.units.exclude_type((UnitTypeId.OVERLORD, UnitTypeId.QUEEN)).closer_than(2, self.wallqueen))
                    print(self.units.exclude_type((UnitTypeId.OVERLORD, UnitTypeId.QUEEN)).closer_than(3, self.wallqueen))
                    if not self.enemy_units.closer_than(10, self.wallqueen):
                        print("wallqueen enemies not nearby")
                        self.wallqueen.stop()
        
        if queens.amount + self.already_pending(UnitTypeId.QUEEN) < self.townhalls.amount and self.can_afford(UnitTypeId.QUEEN) and self.townhalls.ready.idle and self.structures(UnitTypeId.SPAWNINGPOOL).ready:
            self.train(UnitTypeId.QUEEN, 1)
            
        for hatchery in self.townhalls.ready:
            if self.minerals > 100 and self.supply_used > 198:
                if self.enemy_structures(UnitTypeId.NYDUSCANAL) and not self.already_pending(UnitTypeId.SPINECRAWLER) > 1 and not self.structures(UnitTypeId.SPINECRAWLER).ready.closer_than(8, self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(ourmain)).amount > 1:
                    await self.build(UnitTypeId.SPINECRAWLER, near = self.enemy_structures(UnitTypeId.NYDUSCANAL).closest_to(ourmain).position.towards(ourmain, 3))
                elif self.minerals > 500 and not self.structures(UnitTypeId.SPINECRAWLER).ready.closer_than(10, hatchery).amount > 5:
                    if not hatchery.position.is_closer_than(3, ournat):
                        await self.build(UnitTypeId.SPINECRAWLER, near = hatchery.position.towards(enemynat, 10))
                    if hatchery.position.is_closer_than(3, ournat):
                        await self.build(UnitTypeId.SPINECRAWLER, near = Point2(evowall1).towards(ournat, 3))
            if (
                queens.closer_than(5, hatchery).amount == 1
                and hatchery.is_using_ability(AbilityId.TRAINQUEEN_QUEEN)
                and hatchery.has_buff(BuffId.QUEENSPAWNLARVATIMER)
                and queens.amount <= self.townhalls.amount
                and not enemies_near
                ):
                print(self.time_formatted, self.supply_used, "too many queens including trainees")                   
                sparequeen = queens.closer_than(6, hatchery).furthest_to(hatchery)
                if sparequeen:
                    print(self.time_formatted, self.supply_used, "there is a spare queen now because another is training")
                    for hatch in self.townhalls:
                        if (
                            queens.closer_than(5, hatch).amount < 1
                            and self.townhalls.ready
                            and not hatch.is_using_ability(AbilityId.TRAINQUEEN_QUEEN)
                            ):
                            sparequeen.move(hatch)
                            print(self.time_formatted, self.supply_used, "spare queen because another is training moving to lonely hatchery")
                            break
                        elif(
                            queens.closer_than(5, hatch).amount < 1
                            and self.townhalls.not_ready
                            ):
                            sparequeen.move(hatch)
                            print(self.time_formatted, self.supply_used, "spare queen because another is training moving to building hatchery")
                            break
            elif queens.closer_than(5, hatchery).amount > 1:
                sparequeen = self.units(UnitTypeId.QUEEN).closer_than(6, hatchery).furthest_to(hatchery)
                print(self.time_formatted, self.supply_used, "too many queens")
                if queens.amount + self.already_pending(UnitTypeId.QUEEN) > self.townhalls.amount:
                    if sparequeen:
                        for hatch in self.townhalls:
                            if not enemies_near:
                                if self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)):
                                    sparequeen.move(self.townhalls.closest_to(enemynat).position.towards(self.mineral_field.closer_than(10, self.townhalls.closest_to(enemynat)).furthest_to(enemynat), 3))
                                    print(self.time_formatted, self.supply_used, "spare queen out of 2 moving to lonely hatchery")
                                    break
                            if (
                                queens.closer_than(5, hatch).amount < 1
                                and not enemies_near
                                ):
                                sparequeen.move(hatch.position.towards(self.mineral_field.closest_to(hatch), 3))
                                print(self.time_formatted, self.supply_used, "spare queen out of 2 moving to lonely hatchery")
                                break
                else:
                    if sparequeen:
                        for hatch in self.townhalls:
                            if (
                                queens.closer_than(5, hatch).amount < 1
                                ):
                                sparequeen.move(hatch.position.towards(self.mineral_field.closest_to(hatch), 3))
                                print(self.time_formatted, self.supply_used, "spare queen out of 2 moving to lonely hatchery")
                                break
        
                    

    async def queen_inject(self):
        if not self.units(UnitTypeId.QUEEN):
            return
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        queens = self.units(UnitTypeId.QUEEN)
        enemies_near = Units([], self)
        enemies_structures_near = Units([], self)
#hatchery zonal defense system
#enemy units near hatcheries
        for hatch in self.townhalls:
            if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                enemies_near.extend(
                    self.enemy_units.filter(
                        lambda u: not u.is_flying
                        and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                        and u.distance_to(hatch) < 40
                    )
                )
                
#enemy structures near hatcheries
            if self.enemy_structures.not_flying.closer_than(40, hatch):
                enemies_structures_near.extend(
                    self.enemy_structures.filter(
                        lambda s: not s.is_flying
                        and s.distance_to(hatch) < 40
                    )
                )

        if self.wallqueen in queens:
            queens.remove(self.wallqueen)
            
        for queen in queens:
            if self.townhalls.ready:
                hatch = self.townhalls.ready.closest_to(queen)
                if (
                    self.can_cast(UnitTypeId.QUEEN, AbilityId.EFFECT_INJECTLARVA)
                    and not hatch.has_buff(BuffId.QUEENSPAWNLARVATIMER)
                    and not queen.is_using_ability(AbilityId.EFFECT_INJECTLARVA)
                    and not self.already_pending(AbilityId.EFFECT_INJECTLARVA)
                    and not queen.is_attacking
                    and not enemies_near.closer_than(17, queen)
                    ):
                    queen(AbilityId.EFFECT_INJECTLARVA, hatch)
                    
        if queens.filter(lambda q: q.energy > 50):
            if self.units.filter(lambda iu: iu.health_max > 125 and iu.health_percentage < 0.4 and not iu.has_buff(BuffId.TRANSFUSION)):
                if queens.filter(lambda q: q.energy > 50).in_closest_distance_to_group(self.units.filter(lambda iu: iu.health_max > 125 and iu.health_percentage < 0.4 and not iu.has_buff(BuffId.TRANSFUSION))) in self.units.filter(lambda iu: iu.health_max > 125 and iu.health_percentage < 0.4 and not iu.has_buff(BuffId.TRANSFUSION)):
                    print(self.units.filter(lambda iu: iu.health_max > 125 and iu.health_percentage < 0.4), "is injured")
                    print(queens.filter(lambda q: q.energy > 50).closest_n_units(self.units.filter(lambda iu: iu.health_max > 125 and iu.health_percentage < 0.4 and not iu.has_buff(BuffId.TRANSFUSION)).in_closest_distance_to_group(queens.filter(lambda q: q.energy > 50)), 2), "closest 2 queens to nearest injured unit")
                    print(queens.filter(lambda q: q.energy > 50).closest_n_units(self.units.filter(lambda iu: iu.health_max > 125
                                                                                                   and iu.health_percentage < 0.4
                                                                                                   and not iu.has_buff(BuffId.TRANSFUSION))
                                                                                 .in_closest_distance_to_group(queens.filter
                                                                                  (lambda
                                                                                  q: q.energy > 50)), 2).furthest_to(self.units.filter(lambda iu: iu.health_max > 125
                                                                                  and iu.health_percentage < 0.4
                                                                                  and not iu.has_buff(BuffId.TRANSFUSION)).in_closest_distance_to_group(queens.filter(lambda q: q.energy > 50))), "the furthest queen out of the 2")
                                        
                    queens.filter(lambda q: q.energy > 50).closest_n_units(self.units.filter(lambda iu: iu.health_max > 125 and iu.health_percentage < 0.4 and not iu.has_buff(BuffId.TRANSFUSION)).in_closest_distance_to_group(queens.filter(lambda q: q.energy > 50)), 2).furthest_to(self.units.filter(lambda iu: iu.health_max > 125 and iu.health_percentage < 0.4 and not iu.has_buff(BuffId.TRANSFUSION)).in_closest_distance_to_group(queens.filter(lambda q: q.energy > 50)))(AbilityId.TRANSFUSION_TRANSFUSION, self.units.filter(lambda iu: iu.health_max > 125 and iu.health_percentage < 0.4 and not iu.has_buff(BuffId.TRANSFUSION)).in_closest_distance_to_group(queens.filter(lambda q: q.energy > 50)))
                else:
                    queens.filter(lambda q: q.energy > 50).in_closest_distance_to_group(self.units.filter(lambda iu: iu.health_max > 125 and iu.health_percentage < 0.4 and not iu.has_buff(BuffId.TRANSFUSION)))(AbilityId.TRANSFUSION_TRANSFUSION, self.units.filter(lambda iu: iu.health_max > 125 and iu.health_percentage < 0.4 and not iu.has_buff(BuffId.TRANSFUSION)).in_closest_distance_to_group(queens.filter(lambda q: q.energy > 50)))

    async def build_wall(self):
        if not self.units(UnitTypeId.DRONE):
            return
        
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        enemies_near = Units([], self)
        enemies_structures_near = Units([], self)
        roachwarren = self.structures(UnitTypeId.ROACHWARREN)
        
#hatchery zonal defense system
#enemy units near hatcheries
        for hatch in self.townhalls:
            if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                enemies_near.extend(
                    self.enemy_units.filter(
                        lambda u: not u.is_flying
                        and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                        and u.distance_to(hatch) < 40
                    )
                )
                
#enemy structures near hatcheries
            if self.enemy_structures.not_flying.closer_than(40, hatch):
                enemies_structures_near.extend(
                    self.enemy_structures.filter(
                        lambda s: not s.is_flying
                        and s.distance_to(hatch) < 40
                    )
                )
        if (
            self.can_afford(UnitTypeId.ROACHWARREN)
            and not roachwarren
            and not self.already_pending(UnitTypeId.ROACHWARREN)
            and self.time > 180
            and self.has_creep(Point2(roachwarrenwall))
            ):
            if (
                self.enemy_structures(UnitTypeId.ROACHWARREN)
                or enemy_gas_buildings
                or self.enemy_structures(UnitTypeId.BANELINGNEST)
                or self.enemy_units(UnitTypeId.BANELING)
                or self.enemy_units(UnitTypeId.ROACH)
                or self.enemy_units(UnitTypeId.HYDRALISK)
                or self.enemy_units(UnitTypeId.ADEPT)
                or self.enemy_units(UnitTypeId.HELLION)
                or self.enemy_units(UnitTypeId.HELLIONTANK)
                or self.time > 300
                and enemy_townhalls.amount > 1
                ):
                self.units(UnitTypeId.DRONE).filter(lambda drone: drone.is_collecting and not drone.is_carrying_resource).closest_to(Point2(roachwarrenwall)).build(UnitTypeId.ROACHWARREN, Point2(roachwarrenwall))
        print(self.time_formatted, self.supply_used, "our resources for evo", self.minerals, self.vespene)
        if (
            self.can_afford(UnitTypeId.EVOLUTIONCHAMBER)
            and self.time > 180
            and self.has_creep(Point2(evowall1))
            and enemy_townhalls.amount > 1
            and not self.already_pending(UnitTypeId.EVOLUTIONCHAMBER) > 0
            and not self.structures(UnitTypeId.EVOLUTIONCHAMBER)
            and not self.structures(UnitTypeId.EVOLUTIONCHAMBER).closer_than(1, Point2(evowall1))
            ):
            if roachwarren or self.already_pending(UnitTypeId.ROACHWARREN):
                if self.units(UnitTypeId.DRONE).filter(lambda drone: drone.is_collecting and not drone.is_carrying_resource):
                    self.units(UnitTypeId.DRONE).filter(lambda drone: drone.is_collecting and not drone.is_carrying_resource).closest_to(Point2(evowall1)).build(UnitTypeId.EVOLUTIONCHAMBER, Point2(evowall1))
        print(self.time_formatted, self.supply_used, "our resources for evo 2", self.minerals, self.vespene)
        if (
            self.can_afford(UnitTypeId.EVOLUTIONCHAMBER)
            and self.time > 180
            and self.has_creep(Point2(evowall2))
            and enemy_townhalls.amount > 1
            and not self.already_pending(UnitTypeId.EVOLUTIONCHAMBER) > 1
            and not self.structures(UnitTypeId.EVOLUTIONCHAMBER).amount > 1
            and not self.structures(UnitTypeId.EVOLUTIONCHAMBER).closer_than(1, Point2(evowall2))
            ):
            if self.already_pending(UnitTypeId.EVOLUTIONCHAMBER) or self.structures(UnitTypeId.EVOLUTIONCHAMBER):
                if roachwarren or self.already_pending(UnitTypeId.ROACHWARREN):
                    self.units(UnitTypeId.DRONE).filter(lambda drone: drone.is_collecting and not drone.is_carrying_resource).closest_to(Point2(evowall2)).build(UnitTypeId.EVOLUTIONCHAMBER, Point2(evowall2))
                    
        if (
            self.can_afford(UnitTypeId.EVOLUTIONCHAMBER)
            and self.time > 180
            and self.has_creep(Point2(roachwarrenwall))
            and enemy_townhalls.amount > 1
            and not self.already_pending(UnitTypeId.EVOLUTIONCHAMBER) > 2
            and not roachwarren.closer_than(3, roachwarrenwall)
            and not self.already_pending(UnitTypeId.ROACHWARREN)
            ):
            if roachwarren or self.already_pending(UnitTypeId.ROACHWARREN):
                self.units(UnitTypeId.DRONE).filter(lambda drone: drone.is_collecting and not drone.is_carrying_resource).closest_to(Point2(roachwarrenwall)).build(UnitTypeId.EVOLUTIONCHAMBER, Point2(roachwarrenwall))


    async def build_tech(self):
        if not self.units(UnitTypeId.DRONE):
            return
        
        enemy_gas_buildings = self.enemy_structures.same_tech({UnitTypeId.EXTRACTOR, UnitTypeId.REFINERY, UnitTypeId.ASSIMILATOR})
        enemy_townhalls = self.enemy_structures.same_tech({UnitTypeId.COMMANDCENTER, UnitTypeId.HATCHERY, UnitTypeId.NEXUS})
        enemies_near = Units([], self)
        enemies_structures_near = Units([], self)

        
#hatchery zonal defense system
#enemy units near hatcheries
        for hatch in self.townhalls:
            if self.enemy_units.not_flying.exclude_type(scouts).closer_than(40, hatch):
                enemies_near.extend(
                    self.enemy_units.filter(
                        lambda u: not u.is_flying
                        and u.type_id not in (UnitTypeId.EGG, UnitTypeId.DRONE, UnitTypeId.OVERLORD, UnitTypeId.LARVA, UnitTypeId.SCV, UnitTypeId.PROBE, UnitTypeId.MULE)
                        and u.distance_to(hatch) < 40
                    )
                )
                
#enemy structures near hatcheries
            if self.enemy_structures.not_flying.closer_than(40, hatch):
                enemies_structures_near.extend(
                    self.enemy_structures.filter(
                        lambda s: not s.is_flying
                        and s.distance_to(hatch) < 40
                    )
                )
        print(self.time_formatted, self.supply_used, "our resources", self.minerals, self.vespene)
        print(self.time_formatted, self.supply_used, "our lair", self.already_pending(UnitTypeId.LAIR))
        if self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.idle and enemy_townhalls.amount > 1:
            if enemy_gas_buildings.amount > enemy_townhalls.amount and self.structures(UnitTypeId.LAIR) or enemy_gas_buildings.amount <= enemy_townhalls.amount:
                print(self.time_formatted, self.supply_used, "evo ready", self.minerals, self.vespene)
                
                if self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall1)).is_idle and not self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL1):
                    self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall1)).research(UpgradeId.ZERGGROUNDARMORSLEVEL1, can_afford_check = True)
                if self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall1)).is_idle and self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL1) and not self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL2):
                    self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall1)).research(UpgradeId.ZERGGROUNDARMORSLEVEL2, can_afford_check = True)
                if self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall1)).is_idle and self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL2) and not self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL3):
                    self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall1)).research(UpgradeId.ZERGGROUNDARMORSLEVEL3, can_afford_check = True)
                    
                if self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall2)).is_idle and self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL1) and not self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL1):
                    self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall2)).research(UpgradeId.ZERGMISSILEWEAPONSLEVEL1, can_afford_check = True)
                if self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall2)).is_idle and self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL2) and not self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL2):
                    self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall2)).research(UpgradeId.ZERGMISSILEWEAPONSLEVEL2, can_afford_check = True)
                if self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall2)).is_idle and self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL3) and not self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL3):
                    self.structures(UnitTypeId.EVOLUTIONCHAMBER).ready.closest_to(Point2(evowall2)).research(UpgradeId.ZERGMISSILEWEAPONSLEVEL3, can_afford_check = True)

        if not self.already_pending(UpgradeId.GLIALRECONSTITUTION):
            if self.structures(UnitTypeId.ROACHWARREN).ready and self.structures(UnitTypeId.LAIR).ready and self.can_afford(UpgradeId.GLIALRECONSTITUTION):
                self.structures(UnitTypeId.ROACHWARREN).ready.closest_to(ourmain).research(UpgradeId.GLIALRECONSTITUTION)

        if self.can_afford(UnitTypeId.LAIR) and self.townhalls.ready and not self.already_pending(UnitTypeId.LAIR) and not self.structures(UnitTypeId.LAIR):
            if self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL1) and self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL1) or enemy_gas_buildings.amount > enemy_townhalls.amount:
                self.townhalls.closest_to(ourmain).build(UnitTypeId.LAIR)

        if self.can_afford(UnitTypeId.HYDRALISKDEN) and not self.already_pending(UnitTypeId.HYDRALISKDEN):
            if self.enemy_units.flying.filter(lambda flyer: not flyer.type_id in (UnitTypeId.OVERLORD, UnitTypeId.OVERSEER, UnitTypeId.OBSERVER)):
                if self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource):
                    self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource).closest_to(ourmain).build(UnitTypeId.HYDRALISKDEN, ourmain.position.towards(ournat, 7))

        if self.can_afford(UnitTypeId.INFESTATIONPIT) and self.structures(UnitTypeId.LAIR).ready and self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL2) > 0.2:
            if self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource):
                self.units(UnitTypeId.DRONE).filter(lambda drone: not drone.is_carrying_resource).closest_to(ourmain).build(UnitTypeId.INFESTATIONPIT, ourmain.position.towards(enemymain, 7))
        
        if self.can_afford(UnitTypeId.HIVE) and self.townhalls.ready and not self.already_pending(UnitTypeId.HIVE) and not self.structures(UnitTypeId.HIVE) and self.already_pending(UpgradeId.ZERGGROUNDARMORSLEVEL2) and self.already_pending(UpgradeId.ZERGMISSILEWEAPONSLEVEL2):
            self.townhalls.closest_to(ourmain).build(UnitTypeId.HIVE)

        if self.structures(UnitTypeId.HYDRALISKDEN).ready.idle and self.structures(UnitTypeId.LAIR).ready or self.structures(UnitTypeId.HYDRALISKDEN).ready.idle and self.structures(UnitTypeId.HIVE):
            if not self.already_pending(UpgradeId.EVOLVEMUSCULARAUGMENTS) and self.can_afford(UpgradeId.EVOLVEMUSCULARAUGMENTS):
                self.structures(UnitTypeId.HYDRALISKDEN).ready.idle.closest_to(ourmain).research(UpgradeId.EVOLVEMUSCULARAUGMENTS)
            if self.already_pending(UpgradeId.EVOLVEMUSCULARAUGMENTS) > 0.99 and self.can_afford(UpgradeId.EVOLVEGROOVEDSPINES) and not self.already_pending(UpgradeId.EVOLVEGROOVEDSPINES):
                self.structures(UnitTypeId.HYDRALISKDEN).ready.idle.closest_to(ourmain).research(UpgradeId.EVOLVEGROOVEDSPINES)

            
    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")
