class process(object):
	def __init__(self, P_ID, arrive_time, service_time):
		self.P_ID = {P_ID:P_ID}
		self.arrive_time = {P_ID:arrive_time}
		self.service_time = {P_ID:service_time}
		self.finish_time = {P_ID:0}  
		self.remain_time =  {P_ID:service_time}

	def processcoming(self, P_ID, arrive_time, service_time):
		self.P_ID[P_ID] = P_ID
		self.arrive_time[P_ID] = arrive_time
		self.service_time[P_ID] = service_time
		self.finish_time[P_ID] = 0
		self.remain_time[P_ID] = service_time

	def pop(self, P_ID):
		self.P_ID.pop(P_ID)
		self.arrive_time.pop(P_ID)
		self.service_time.pop(P_ID)
		self.finish_time.pop(P_ID)
		self.remain_time.pop(P_ID)


class processor(object):
	def __init__(self):
		self.current_time = 0
		self.process = process('A', 0, 3)
		self.process.processcoming('B', 2, 6)
		self.process.processcoming('C', 4, 4)
		self.process.processcoming('D', 6, 5)
		self.process.processcoming('E', 8, 2)

	def create(self, P_ID, arrive_time, service_time):
		self.process.processcoming(P_ID, arrive_time, service_time)

	def run_process(self, P_ID, time, current_time):
		if self.process.remain_time[P_ID] <=  time:
			self.process.finish_time[P_ID] = current_time + self.process.remain_time[P_ID]
			self.current_time += 1
			return self.process.finish_time[P_ID]
		else:
			self.process.remain_time[P_ID] = self.process.remain_time[P_ID] - time
			self.current_time += 1
			return 0

	def fcfs(self):
		while len(self.process.P_ID):
			pid = 'E'
			for p in self.process.P_ID:
				if self.process.arrive_time[p] < self.process.arrive_time[pid]:
					pid = p
			process_finish_time = self.run_process(pid, 1, self.current_time)
			if process_finish_time !=  0:
				print('Process', pid, 'finished at', process_finish_time,
					  "run time", process_finish_time - self.process.arrive_time[pid],
					  "weighted time",
					  float(process_finish_time - self.process.arrive_time[pid])/float(self.process.service_time[pid]))
				self.process.pop(pid)

	def rr(self):
		while len(self.process.P_ID):
			pop_list = []
			for p in self.process.P_ID:
				if self.process.arrive_time[p] <= self.current_time:
					process_finish_time = self.run_process(p, 1, self.current_time)
					if process_finish_time != 0:
						print('Process', p, 'finished at', process_finish_time,
							  "run time", process_finish_time - self.process.arrive_time[p],
							  "weighted time",
								  float(process_finish_time -
										self.process.arrive_time[p])/float(self.process.service_time[p])
							  )
						pop_list.append(p)
			for q in pop_list:
				self.process.pop(q)

	def sjf(self):
		while len(self.process.P_ID):
			pid = 'B'
			for p in self.process.P_ID:
				if self.process.arrive_time[p] <= self.current_time:
					if self.process.remain_time[p] <= self.process.remain_time[pid]:
						pid = p
			process_finish_time = self.run_process(pid, 1, self.current_time)
			if process_finish_time !=  0:
				print('Process', pid, 'finished at', process_finish_time,
					  "run time", process_finish_time - self.process.arrive_time[pid],
					  "weighted time", (float(process_finish_time -
											  self.process.arrive_time[pid]))/float(self.process.service_time[pid])
					  )
				self.process.pop(pid)

	def hrn(self):
		while len(self.process.P_ID):
			identifier = "P_ID"
			rr = 0
			for p in self.process.P_ID:
				if ((self.current_time - self.process.arrive_time[p] + self.process.remain_time[p]) / self.process.service_time[p]) > rr:
					identifier = p
					rr = (self.process.arrive_time[p] - self.current_time + self.process.remain_time[p]) / self.process.service_time[p]
			process_finish_time = self.run_process(identifier, 1, self.current_time)
			if process_finish_time != 0:
				print('Process', identifier, 'finished at',
					  process_finish_time, "run time", process_finish_time - self.process.arrive_time[identifier],
					  "weighted time", float(process_finish_time -
							 self.process.arrive_time[identifier])/float(self.process.service_time[identifier])
					  )
				self.sjf.pop(identifier)
				
if __name__  ==  '__main__':
	processor = processor()
	# processor.create()
	processor.fcfs()



