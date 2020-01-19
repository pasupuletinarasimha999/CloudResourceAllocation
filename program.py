from collections import defaultdict, OrderedDict
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class ResourceAllocator(object):
	HOURS = 1
	def __init__(self):

		self.cpuWithQuantity = []
		self.TotalCPUCost = 0
		self.PreResult = {}
		self.finalResult = []
		self.server = server
		self.maxCycleChecked = True

	def get_costs(self, zones, cpus, price,hours = HOURS):
		
		self.zones = zones
		self.hours = hours
		self.cpus = cpus
		self.price = float(price)
		self.cpuQty = 0
		for region , v in self.zones.items():
			self.PreResult["region"] 		= region
			self.PreResult["servers"]		= self.getServers(region,v)
			self.PreResult["total_cost"] 	= locale.currency(self.TotalCPUCost)
			self.finalResult.append(self.PreResult)
		return self.finalResult

	def getServers(self, region, v):
		self.cpuQty = 0
		self.cpuWithQuantity = []
		while self.cpuQty < self.cpus:
			for serverType, CpuQty in reversed(self.server):
				self.getTotalCPUQuantity(serverType, CpuQty, region)
		if (self.price and not self.cpus):
			self.getCpuForGivenPrice(region)
		return self.getlistofservers()	

	def getTotalCPUQuantity(self, serverType, CpuQty, region):
		if (self.cpus):
			try:
				if (serverType in self.zones[region]):
					curcpuQty = self.cpuQty + CpuQty
					if (curcpuQty <= self.cpus):
						self.cpuQty = curcpuQty						
						serverCost = self.zones[region][serverType]
						self.cpuWithQuantity.append((str(serverType), (CpuQty, serverCost)))
			except Exception as error:
				print(error)	
	

	def getlistofservers(self):
		self.TotalCPUCost = 0
		TotalCPUQuantity = defaultdict(int)
		for k, i in self.cpuWithQuantity:
			if (self.price != 0):
				if (self.TotalCPUCost < self.price):
					self.TotalCPUCost += self.hours * i[1]
					TotalCPUQuantity[k] += 1
					if (self.TotalCPUCost > self.price):
						self.TotalCPUCost -=self.hours * i[1]
						TotalCPUQuantity[k] -= i[0]
						self.maxCycleChecked = False
			else:
				self.TotalCPUCost += i[1]
				TotalCPUQuantity[k] += i[0]
		return TotalCPUQuantity.items()
		
		
	def getCpuForGivenPrice(self, region):
		self.maxCycleChecked = True
		while self.TotalCPUCost <= self.price and self.maxCycleChecked:
			count = 0
			updatedCost = self.TotalCPUCost
			for serverType, CpuQty in reversed(self.server):
				try:
					if (serverType in self.zones[region]):
						curcpuQty = self.cpuQty + CpuQty
						if (self.TotalCPUCost <= self.price):
							self.cpuQty = curcpuQty						
							serverCost = self.zones[region][serverType]
							self.cpuWithQuantity.append((str(serverType), (CpuQty, serverCost)))
							count += 1
				except Exception as error:
					print(error)
			
			self.getAggregateCpuQty()
			if (count == 0 or self.TotalCPUCost == updatedCost):
				self.maxCycleChecked= False

if __name__ == '__main__':
	zones = {
		"us-east": {
			"large": 0.12,
			"xlarge": 0.23,
			"2xlarge": 0.45,
			"4xlarge": 0.774,
			"8xlarge": 1.4,
			"10xlarge": 2.82
		},
		"us-west": {
			"large": 0.14,
			"2xlarge": 0.413,
			"4xlarge": 0.89,
			"8xlarge": 1.3,
			"10xlarge": 2.97
		},
	}
	server = [("large", 1), 
		  ("xlarge", 2), 
		  ("2xlarge", 4), 
		  ("4xlarge", 8), 
		  ("8xlarge", 16), 
		  ("10xlarge", 32)
		 ]
	hours=int(input("Enter the Number of Hours:\t"))
	cpus=int(input("Enter the Number of CPU's Required:\t"))
	price=float(input("Enter the Amount which you can afford:\t"))
	obj1 =  ResourceAllocator()
	print("\n===============================\n")
	print(obj1.get_costs(zones, cpus, price,hours), "\n"*2)
	print("\n===============================\n")
