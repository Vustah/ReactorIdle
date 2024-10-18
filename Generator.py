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
	Gen_base = 9
	Gen_water_base = 5000

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

	def getGeneratorLevel(self):
		return self.Gen

	def getWaterLevel(self):
		return self.Gen_water

class Reactor:
	def __init__(self, reactor_base_pwr=3, reactor_level=0):
		self.reactor_base_pwr = reactor_base_pwr
		self.reactor_level = reactor_level
		self.setReactorLevel(reactor_level=reactor_level)

	def setReactorLevel(self, reactor_level=0):
		self.reactor_level = reactor_level
		self.reactor_pwr = self.reactor_base_pwr*1.25**reactor_level	

	def getReactorPWR(self):
		return self.reactor_pwr
	

class PowerPlant:
	def __init__(self, generator, pump, groundWaterPump, reactor):
		self.generator = generator
		self.pump = pump
		self.groundWaterPump = groundWaterPump
		self.reactor = reactor

	def calcGenerator(self, reactor_pwr=0):
		self.reactor_pwr = reactor_pwr
		return reactor_pwr/(self.generator.getGeneratorLevel()+self.generator.getWaterLevel()*100)
	
	def calcPumpCapacity(self,pump_level=0):
		generator_per_reactor = m.ceil(self.calcGenerator(self.reactor_pwr))
		heat_disipated_per_generator = self.reactor_pwr/generator_per_reactor
		water_used_per_generator = (heat_disipated_per_generator-self.generator.getGeneratorLevel())/100.0
		self.pump.setPumpLevel(pump_level)
		generator_per_pump = self.pump.getPumpWater()/water_used_per_generator
		return generator_per_pump

	def calcGroundPumpCapacity(self,pump_level=0):
		generator_per_reactor = m.ceil(self.calcGenerator(self.reactor_pwr))
		heat_disipated_per_generator = self.reactor_pwr/generator_per_reactor
		water_used_per_generator = (heat_disipated_per_generator-self.generator.getGeneratorLevel())/100.0
		self.groundWaterPump.setPumpLevel(pump_level)
		generator_per_pump = self.groundWaterPump.getPumpWater()/water_used_per_generator
		return generator_per_pump

	def getGeneratorStats(self):
		pump_level = self.pump.getPumpWaterLevel()
		ground_pump_level = self.groundWaterPump.getPumpWaterLevel()
		print("Generator level:                  %d" %self.generator.Gen_level)
		print("Generator water level:            %d" %self.generator.Gen_water_level)
		print("Generator per reactor:            %d (%.2f)" %(m.ceil(self.calcGenerator(self.reactor.getReactorPWR())),self.calcGenerator(self.reactor.getReactorPWR())))
		print("Pump Capacity level:              %d" %pump_level)
		print("Generator per water pump:         %d (%.2f)" %(m.floor(self.calcPumpCapacity(pump_level)),self.calcPumpCapacity(pump_level)))
		print("Ground Water Pump Capacity level: %d" %ground_pump_level)
		print("Generator per ground water pump:  %d (%.2f)" %(m.floor(self.calcGroundPumpCapacity(ground_pump_level)),self.calcGroundPumpCapacity(ground_pump_level)))

def parseInputs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-rp",    help="Reactor Power",           type=float, default=0, dest="reactor_pwr")
    parser.add_argument("-rl",    help="Reactor level",           type=float, default=0, dest="reactor_lvl")
    parser.add_argument("-gl",    help="Generator Level",         type=float, default=0, dest="gen_lvl")
    parser.add_argument("-gwl",   help="Generator Water Level",   type=float, default=0, dest="gen_water_lvl")
    parser.add_argument("-pl",    help="Pump Level",              type=float, default=0, dest="pump_lvl")
    parser.add_argument("-gpl",   help="Ground Pump Level",       type=float, default=0, dest="ground_pump_lvl" )
    args = parser.parse_args()
    

    return args.reactor_pwr, args.reactor_lvl, args.gen_lvl, args.gen_water_lvl, args.pump_lvl, args.ground_pump_lvl


if __name__ == "__main__":
	try:
		reactor_pwr, reactor_lvl, gen_lvl, gen_water_lvl, pump_lvl, ground_pump_lvl = parseInputs()
		generator = Generator()

		generator.setWaterLevel(gen_water_lvl)
		generator.setGeneratorLevel(gen_lvl)
		
		reactor = Reactor(reactor_pwr)
		reactor.setReactorLevel(reactor_lvl)
		
		pump = Pump()
		pump.setPumpLevel(pump_lvl)

		groundWaterPump = GroundWaterPump()
		groundWaterPump.setPumpLevel(ground_pump_lvl)

		powerPlant = PowerPlant(generator, pump, groundWaterPump, reactor)
		powerPlant.getGeneratorStats()

	except IndexError as e:
		print("INDEX_ERROR")
		exit(1)
	except ZeroDivisionError as e:
		print("ZERO_DIVISION_ERROR")
		exit(1)

	except ValueError as e:
		print("Could not convert argument to float.")
		exit(1)