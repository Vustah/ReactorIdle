import sys
import math as m
class Generator:
	reactor_pwr = 0
	pump_level = 0
	Gen_base = 9
	Gen_water_base = 5000

	def __init__(self,Gen_level=0, Gen_water_level=0):
		#self.self_defaults()
		self.Gen_level = Gen_level
		self.Gen_water_level = Gen_water_level
		self.Gen = self.Gen_base*1.25**Gen_level
		self.Gen_water = self.Gen_water_base*1.25**Gen_water_level
		

#	def self_defaults(self):
#		self.reactor_pwr = 0
#		self.pump_level = 0
#		self.Gen_base = 9
#		self.Gen_water_base = 5000

	def calcGenerator(self, reactor_pwr=0):
		self.reactor_pwr = reactor_pwr
		return reactor_pwr/(self.Gen+self.Gen_water*100)

	def setWaterLevel(self,water_level):
		self.Gen_water_level = water_level
		self.Gen_water = self.Gen_water_base*1.25**self.Gen_water_level

	def setReactorLevel(self, reactor_base, reactor_level=0):
		self.reactor_base = reactor_base
		self.reactor_level = reactor_level
		self.reactor_pwr = reactor_base*1.25**reactor_level	
	
	def setGeneratorLevel(self,gen_level):
		self.Gen_level = gen_level
		self.Gen = self.Gen_base*1.25**self.Gen_level
		

	def setPumpLevel(self,pump_level):
		self.pump_level = pump_level
		self.Water_pump_base = 25000
		self.water_pump = self.Water_pump_base*1.5**self.pump_level
		

	def calcPumpCapacity(self,pump_level=0):
		generator_per_reactor = m.ceil(self.calcGenerator(self.reactor_pwr))
		heat_disipated_per_generator = self.reactor_pwr/generator_per_reactor
		water_used_per_generator = (heat_disipated_per_generator-self.Gen)/100
		self.setPumpLevel(pump_level)
		generator_per_pump = self.water_pump/water_used_per_generator
		return generator_per_pump

	def getGeneratorStats(self):
		print("Generator level:          %d" %self.Gen_level)
		print("Generator water level:    %d" %self.Gen_water_level)
		print("Generator per reactor:    %d (%.2f)" %(m.ceil(self.calcGenerator(self.reactor_pwr)),self.calcGenerator(self.reactor_pwr)))
		print("Pump Capacity level:      %d" %self.pump_level)
		print("Generator per water pump: %d (%.2f)" %(m.floor(self.calcPumpCapacity(self.pump_level)),self.calcPumpCapacity(self.pump_level)))

	def getAttributes(self):
		for func in dir(Generator):
			print("Generator.%-20s = %r" % (func, getattr(Generator, func)))
			#print(func)

def parseInputs(arguments):
	arg_list = ["-rp", "-rl", "-gl", "-gwl", "-pl"]
	arg_values = [0,0,0,0,0]
	
	for i in range(len(arg_list)):
		if arg_list[i] in arguments:
			arg_values[i] = float(arguments[arguments.index(arg_list[i])+1])
	
	reactor_pwr = arg_values[0] 
	reactor_lvl = arg_values[1]
	gen_lvl = arg_values[2]
	gen_water_lvl = arg_values[3]
	pump_lvl = arg_values[4]
	
	return reactor_pwr,reactor_lvl,gen_lvl,gen_water_lvl,pump_lvl

def help():
	help_statement= """
	-rp : Reactor Power
	-rl : Reactor level
	-gl : Generator Level
	-gwl: Generator Water Level
	-pl : Pump Level
	"""
	print(help_statement)

if __name__ == "__main__":
	try:
		if sys.argv[1] == "-h" or sys.argv[1] == "-help":
			help()
			exit(0)
	except IndexError as e:
		exit(1)		
	try:
		reactor_pwr,reactor_lvl,gen_lvl,gen_water_lvl,pump_lvl = parseInputs(sys.argv[1:])
		Gen = Generator()
		Gen.setWaterLevel(gen_water_lvl)
		Gen.setGeneratorLevel(gen_lvl)
		Gen.setPumpLevel(pump_lvl)
		Gen.setReactorLevel(reactor_pwr,reactor_lvl)
		Gen.getGeneratorStats()

	except IndexError as e:
		exit(1)
	except ZeroDivisionError as e:
		exit(1)

