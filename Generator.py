import sys
import math as m
import argparse

class Pump(object):
    def __init__(self, base=25000, level=0):
        self.Water_pump_base = base
        self.pump_level = level
    
    def setPumpLevel(self,pump_level):
        self.pump_level = pump_level
        self.water_pump = self.Water_pump_base*1.5**self.pump_level

    def getPumpWater(self):
        return self.water_pump
    
    def getPumpWaterLevel(self):
        return self.pump_level

class GroundWaterPump(Pump):
    def __init__(self, base=67500, level = 0):
        self.Water_pump_base = base
        self.pump_level = level

class Generator:
    Gen_base = 3
    Gen_water_base = 0
    Gen_max_heat = 900

    def __init__(self,Gen_level=0, Gen_water_level=0):
        self.Gen_level = Gen_level
        self.Gen_water_level = Gen_water_level
        self.Gen = self.Gen_base*1.25**Gen_level
        self.Gen_water = self.Gen_water_base*1.25**Gen_water_level

    def setWaterLevel(self,water_level):
        self.Gen_water_level = water_level
        self.Gen_water = self.Gen_water_base*1.25**self.Gen_water_level

    def setGeneratorLevel(self,gen_level):
        self.Gen_level = gen_level
        self.Gen = self.Gen_base*1.25**self.Gen_level

    def getAttributes(self):
        for func in dir(Generator):
            print("Generator.%-20s = %r" % (func, getattr(Generator, func)))
            #print(func)

    def getGeneratorCapacity(self):
        return self.Gen

    def getWater(self):
        return self.Gen_water

class Generator2(Generator):
    Gen_base = 9
    Gen_water_base = 5000
    Gen_max_heat = 150
    def __init__(self,Gen_level=0, Gen_water_level=0):
        super.__init__(Gen_level,Gen_water_level)

class Generator3(Generator):
    Gen_base = 32
    Gen_water_base = 8000
    Gen_max_heat = 900
    def __init__(self,Gen_level=0, Gen_water_level=0):
        super.Gen_base = 32
        super.Gen_water_base = 8000
        super.Gen_max_heat = 900
        super.__init__(Gen_level,Gen_water_level)
        
class Reactor:
    def __init__(self, reactor_base_pwr=3, reactor_level=0, isolation = None,isolation_number=0):
        self.reactor_base_pwr = reactor_base_pwr
        self.reactor_level    = reactor_level
        self.isolation_number = isolation_number
        if isinstance(isolation,Isolation):
            self.isolation = isolation
        self.setReactorLevel(reactor_level=reactor_level, isolation=isolation,isolation_number=isolation_number)
            
    def setReactorLevel(self, reactor_level=0, isolation = 0,isolation_number=0):
        self.reactor_level = reactor_level
        self.isolation = isolation
        if self.isolation is not None:
            self.reactor_pwr = self.reactor_base_pwr * (1.25**reactor_level) * (1+self.isolation.getIsolation()*isolation_number)
        else:
            self.reactor_pwr = self.reactor_base_pwr*(1.25**reactor_level)
        

    def getReactorPWR(self):
        return self.reactor_pwr
    
class Isolation:
    def __init__(self, base_isolation=0.05, level=0):
        self.base_isolation = base_isolation
        self.isolation = self.base_isolation
        self.level = level

    def setIsolation(self, level = 0):
        self.level = level
        self.isolation = self.base_isolation + (0.05 * level)
    
    def getIsolation(self):
        return self.isolation
    
    def getIsolationLevel(self):
        return self.level

class PowerPlant:
    def __init__(self, generator, pump, groundWaterPump, reactor,isolation):
        self.generator = generator
        self.pump = pump
        self.groundWaterPump = groundWaterPump
        self.reactor = reactor
        self.isolation = isolation

    def calcGenerator(self, reactor_pwr=0):
        self.reactor_pwr = reactor_pwr
        return reactor_pwr/(self.generator.getGeneratorCapacity()+self.generator.getWater()*100)
    
    def calcPumpCapacity(self,pump_level=0):
        generator_per_reactor = m.ceil(self.calcGenerator(self.reactor_pwr))
        heat_disipated_per_generator = self.reactor_pwr/generator_per_reactor
        water_used_per_generator = (heat_disipated_per_generator-self.generator.getGeneratorCapacity())/100.0
        self.pump.setPumpLevel(pump_level)
        generator_per_pump = self.pump.getPumpWater()/water_used_per_generator
        return generator_per_pump

    def calcGroundPumpCapacity(self,pump_level=0):
        generator_per_reactor = m.ceil(self.calcGenerator(self.reactor_pwr))
        heat_disipated_per_generator = self.reactor_pwr/generator_per_reactor
        water_used_per_generator = (heat_disipated_per_generator-self.generator.getGeneratorCapacity())/100.0
        self.groundWaterPump.setPumpLevel(pump_level)
        generator_per_pump = self.groundWaterPump.getPumpWater()/water_used_per_generator
        return generator_per_pump

    def printGeneratorStats(self):
        pump_level = self.pump.getPumpWaterLevel()
        ground_pump_level = self.groundWaterPump.getPumpWaterLevel()
        local_reactor_pwr = self.reactor.getReactorPWR()
        num_generators = self.calcGenerator(local_reactor_pwr)
        pump_capacity = self.calcPumpCapacity(pump_level)
        ground_pump_capacity = self.calcGroundPumpCapacity(ground_pump_level)
        try:
            isolation_level = int(self.isolation.getIsolationLevel())
        except AttributeError:
            isolation_level = None
        
        # print("Reactor output:                   %f" %local_reactor_pwr)
        print("Reactor output:                   {:>15,}           ".format(int(local_reactor_pwr)))
        print("Generator level:                  {:>15,}           ".format(int(self.generator.Gen_level)))
        print("Generator water level:            {:>15,}           ".format(int(self.generator.Gen_water_level)))
        print("Generator per reactor:            {:>15,} ({:>,.2f})".format(m.ceil(num_generators),num_generators))
        print("Pump Capacity level:              {:>15,}           ".format(int(pump_level)))
        print("Generator per water pump:         {:>15,} ({:>,.2f})".format(m.floor(pump_capacity),pump_capacity))
        print("Ground Water Pump Capacity level: {:>15,}           ".format(int(ground_pump_level)))
        print("Generator per ground water pump:  {:>15,} ({:>,.2f})".format(m.floor(ground_pump_capacity),ground_pump_capacity))
        try:
            print("Isolation level:                  {:>15,}".format(int(isolation_level)))
        except TypeError:
            pass

            



def parseInputs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-rp",    help="Reactor Power",         type=float, default=0, dest="reactor_pwr")
    parser.add_argument("-rl",    help="Reactor level",         type=float, default=0, dest="reactor_lvl")
    parser.add_argument("-gl",    help="Generator Level",       type=float, default=0, dest="gen_lvl")
    parser.add_argument("-gwl",   help="Generator Water Level", type=float, default=0, dest="gen_water_lvl")
    parser.add_argument("-pl",    help="Pump Level",            type=float, default=0, dest="pump_lvl")
    parser.add_argument("-gpl",   help="Ground Pump Level",     type=float, default=0, dest="ground_pump_lvl" )
    parser.add_argument("-iso",   help="Isolation Level",       type=float, default=None, dest="isolation_lvl" )
    parser.add_argument("-iso_no",   help="Isolation number",   type=float, default=0, dest="isolation_no" )
    
    args = parser.parse_args()
    

    return args.reactor_pwr, args.reactor_lvl, args.gen_lvl, args.gen_water_lvl, args.pump_lvl, args.ground_pump_lvl, args.isolation_lvl,args.isolation_no


if __name__ == "__main__":
    try:
        reactor_pwr, reactor_lvl, gen_lvl, gen_water_lvl, pump_lvl, ground_pump_lvl,isolation_lvl,isolation_no = parseInputs()
        generator1 = Generator()

        generator1.setWaterLevel(gen_water_lvl)
        generator1.setGeneratorLevel(gen_lvl)
        
        generator2 = Generator()

        generator2.setWaterLevel(gen_water_lvl)
        generator2.setGeneratorLevel(gen_lvl)
        
        generator3 = Generator()

        generator3.setWaterLevel(gen_water_lvl)
        generator3.setGeneratorLevel(gen_lvl)
        
        
        isolation = None
        if isolation_lvl != None:
            isolation = Isolation()
            isolation.setIsolation(isolation_lvl)
        
        
        reactor = Reactor(reactor_pwr,isolation=isolation,isolation_number=isolation_no)
        reactor.setReactorLevel(reactor_lvl,isolation=isolation,isolation_number=isolation_no)
        
        pump = Pump()
        pump.setPumpLevel(pump_lvl)

        groundWaterPump = GroundWaterPump()
        groundWaterPump.setPumpLevel(ground_pump_lvl)
        
        powerPlant = PowerPlant(generator3, pump, groundWaterPump, reactor,isolation)
        powerPlant.printGeneratorStats()

    except IndexError as e:
        print("INDEX_ERROR")
        exit(1)
    except ZeroDivisionError as e:
        print("ZERO_DIVISION_ERROR")
        exit(1)

    except ValueError as e:
        print("Could not convert argument to float.")
        exit(1)
