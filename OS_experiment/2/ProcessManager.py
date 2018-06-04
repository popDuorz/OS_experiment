class process(object):
	def __init__(self, p_id, arrive_time, service_time):
		self.p_id = {p_id:p_id}
		self.arrive_time = {p_id:arrive_time}
		self.service_time = {p_id:service_time}
		self.finish_time = {p_id:0}  
		self.remain_time =  {p_id:service_time}

	def add_process(self, p_id, arrive_time, service_time):
		self.p_id[p_id] = p_id
		self.arrive_time[p_id] = arrive_time
		self.service_time[p_id] = service_time
		self.finish_time[p_id] = 0
		self.remain_time[p_id] = service_time

	def process_exit(self, p_id):
		self.p_id.pop(p_id)
		self.arrive_time.pop(p_id)
		self.service_time.pop(p_id)
		self.finish_time.pop(p_id)
		self.remain_time.pop(p_id)

	def process_run_info(self, p, process_finish_time):
		print('Process \033[;32;0m{0}\033[0m, finished at \033[;32;0m{1}\033[0m, run time \033[;32;0m{2}\033[0m, weighted time \033[;32;0m{3:4.2f}\033[0m'
			.format(self.p_id[p], process_finish_time, 
				process_finish_time - self.arrive_time[p], 
				float(process_finish_time - self.arrive_time[p])/float(self.service_time[p])
			  )
			)
   

class processor(object):
	def __init__(self):
		self.current_time = 0
		self.process = process('A', 0, 3)
		self.process.add_process('B', 2, 6)
		self.process.add_process('C', 4, 4)
		self.process.add_process('D', 6, 5)
		self.process.add_process('E', 8, 2)

	def create(self, p_id, arrive_time, service_time):
		self.process.add_process(p_id, arrive_time, service_time)

	def run_process(self, p_id, time, current_time):
		if self.process.remain_time[p_id] <=  time:
			self.process.finish_time[p_id] = current_time + self.process.remain_time[p_id]
			self.current_time += 1
			return self.process.finish_time[p_id]
		else:
			self.process.remain_time[p_id] = self.process.remain_time[p_id] - time
			self.current_time += 1
			return 0

	def fcfs(self):
		while len(self.process.p_id):
			pid = 'E'
			for p in self.process.p_id:
				if self.process.arrive_time[p] < self.process.arrive_time[pid]:
					pid = p
			process_finish_time = self.run_process(pid, 1, self.current_time)
			if process_finish_time !=  0:
				self.process.process_run_info(pid, process_finish_time)
				self.process.process_exit(pid)

	def rr(self):
		while len(self.process.p_id):
			pop_list = []
			for p in self.process.p_id:
				if self.process.arrive_time[p] <= self.current_time:
					process_finish_time = self.run_process(p, 1, self.current_time)
					if process_finish_time != 0:
						self.process.process_run_info(p, process_finish_time)
						pop_list.append(p)
			for q in pop_list:
				self.process.process_exit(q)

	def sjf(self):
		while len(self.process.p_id):
			pid = 'B'
			for p in self.process.p_id:
				if self.process.arrive_time[p] <= self.current_time:
					if self.process.remain_time[p] <= self.process.remain_time[pid]:
						pid = p
			process_finish_time = self.run_process(pid, 1, self.current_time)
			if process_finish_time !=  0:
				self.process.process_run_info(pid, process_finish_time)
				self.process.process_exit(pid)

	def hrn(self):
		while len(self.process.p_id):
			identifier = "p_id"
			rr = 0
			for p in self.process.p_id:
				if ((self.current_time - self.process.arrive_time[p] + self.process.remain_time[p]) / self.process.service_time[p]) > rr:
					identifier = p
					rr = (self.process.arrive_time[p] - self.current_time + self.process.remain_time[p]) / self.process.service_time[p]
			process_finish_time = self.run_process(identifier, 1, self.current_time)
			if process_finish_time != 0:
				self.process.process_run_info(identifier, process_finish_time)
				self.rr()
				
if __name__  ==  '__main__':
	processor = processor()
	# processor.create()
	processor.sjf()



