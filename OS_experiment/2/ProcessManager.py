from progressive.bar import Bar
from progressive.tree import ProgressTree, Value, BarDescriptor
from time import sleep
from blessings import Terminal


class Process(object):
    def __init__(self, _p_id, _arrive_time, _service_time):
        self.p_id = {_p_id: _p_id}
        self.arrive_time = {_p_id: _arrive_time}
        self.service_time = {_p_id: _service_time}
        self.finish_time = {_p_id: 0}
        self.remain_time = {_p_id: _service_time}

    def process_run_info(self, p, process_finish_time, result):
        print('Process \033[;32;0m{0}\033[0m, '
              'finished at \033[;32;0m{1}\033[0m, '
              'run time \033[;32;0m{2}\033[0m, '
              'weighted time \033[;32;0m{3:4.2f}\033[0m'
              .format(self.p_id[p],
                      process_finish_time,
                      process_finish_time - self.arrive_time[p],
                      float(process_finish_time - self.arrive_time[p])/float(self.service_time[p])))

        result.append(Result(p,
                             process_finish_time,
                             process_finish_time - self.arrive_time[p],
                             float(process_finish_time - self.arrive_time[p])/float(self.service_time[p])))

    def add_process(self, _p_id, _arrive_time, _service_time):
        self.p_id[_p_id] = _p_id
        self.arrive_time[_p_id] = _arrive_time
        self.service_time[_p_id] = _service_time
        self.finish_time[_p_id] = 0
        self.remain_time[_p_id] = _service_time

    def process_exit(self, _p_id):
        self.p_id.pop(_p_id)
        self.arrive_time.pop(_p_id)
        self.service_time.pop(_p_id)
        self.finish_time.pop(_p_id)
        self.remain_time.pop(_p_id)


t = Terminal()
n = ProgressTree(term=t)


class Processor(object):
    def __init__(self, _p_id, _arrive_time, _service_time):
        self.current_time = 0
        self.result = []
        self.process = Process(p_id, _arrive_time, _service_time)
        # self.process.add_process('B', 2, 6)
        # self.process.add_process('C', 4, 4)
        # self.process.add_process('D', 6, 5)
        # self.process.add_process('E', 8, 2)

    def all_process_done(self):
        for p in self.process.p_id:
            if self.process.remain_time[p] != 0:
                return False
        return True

    def create(self, _p_id, _arrive_time, _service_time):
        self.process.add_process(_p_id, _arrive_time, _service_time)

    def init_progressive(self, leaf_values, bd_defaults, test_d):
        for p in self.process.p_id:
            leaf_value = self.process.service_time[p] - self.process.remain_time[p]
            leaf_values[p] = (Value(leaf_value))
        for p in self.process.p_id:
            bd_defaults[p] = dict(type=Bar, kwargs=dict(max_value=self.process.service_time[p]))
            test_d[p] = BarDescriptor(value=leaf_values[p], **bd_defaults[p])

    def update_leaf_values(self, leaf_values):
        for p in self.process.p_id:
            leaf_values[p].value = self.process.service_time[p] - self.process.remain_time[p]

    def run_process(self, _p_id, time, current_time, leaf_values):
        if self.process.remain_time[_p_id] <= time:
            self.process.finish_time[_p_id] = current_time + self.process.remain_time[_p_id]
            self.process.remain_time[_p_id] = self.process.remain_time[_p_id] - time
            self.current_time += 1
            self.update_leaf_values(leaf_values)
            return self.process.finish_time[_p_id]
        else:
            self.process.remain_time[_p_id] = self.process.remain_time[_p_id] - time
            self.current_time += 1
            self.update_leaf_values(leaf_values)
            return 0

    def fcfs(self):

        leaf_values = {}
        bd_defaults = {}
        test_d = {}
        self.init_progressive(leaf_values, bd_defaults, test_d)
        n.make_room(test_d)
        latest_p = 'A'
        n.draw(test_d, BarDescriptor(bd_defaults[latest_p]))
        for p in self.process.p_id:
            if self.process.arrive_time[p] >= self.process.arrive_time[latest_p]:
                latest_p = p

        while len(self.process.p_id):
            pid = latest_p
            for p in self.process.p_id:
                if self.process.arrive_time[p] < self.process.arrive_time[pid]:
                    pid = p
            if self.current_time < self.process.arrive_time[pid]:
                sleep(1)
                self.current_time += 1
                print('\r current time: %d' % self.current_time, end='')
                continue
            process_finish_time = self.run_process(pid, 1, self.current_time, leaf_values)
            sleep(1)
            n.cursor.restore()
            n.draw(test_d, BarDescriptor(bd_defaults[pid]))
            print('\r current time: %d' % self.current_time)

            if process_finish_time != 0:
                self.process.process_run_info(pid, process_finish_time, self.result)
                self.process.process_exit(pid)

    def rr(self):

        leaf_values = {}
        bd_defaults = {}
        test_d = {}
        self.init_progressive(leaf_values, bd_defaults, test_d)
        n.make_room(test_d)
        n.draw(test_d, BarDescriptor(bd_defaults['A']))

        while len(self.process.p_id):
            pop_list = []
            need_sleep = True
            for p in self.process.p_id:
                if self.process.arrive_time[p] <= self.current_time:
                    need_sleep = False
                    n.cursor.restore()
                    process_finish_time = self.run_process(p, 1, self.current_time, leaf_values)
                    sleep(1)
                    n.draw(test_d, BarDescriptor(bd_defaults[p]))
                    print('\r current time: %d' % self.current_time)
                    if process_finish_time != 0:
                        self.process.process_run_info(p, process_finish_time, self.result)
                        pop_list.append(p)

            if need_sleep:
                sleep(1)
                self.current_time += 1
                print('\r current time: %d' % self.current_time, end='')
            for q in pop_list:
                self.process.process_exit(q)

    def sjf(self):

        leaf_values = {}
        bd_defaults = {}
        test_d = {}
        self.init_progressive(leaf_values, bd_defaults, test_d)
        longest_p = 'A'
        n.make_room(test_d)
        n.draw(test_d, BarDescriptor(bd_defaults['A']))
        for p in self.process.p_id:
            if self.process.service_time[p] > self.process.service_time[longest_p]:
                longest_p = p

        while len(self.process.p_id):
            pid = longest_p
            for p in self.process.p_id:
                if self.process.arrive_time[p] <= self.current_time:
                    if self.process.service_time[p] < self.process.service_time[pid]:
                        pid = p

            if self.current_time < self.process.arrive_time[pid]:
                sleep(1)
                self.current_time += 1
                print('\r current time: %d' % self.current_time, end='')
                continue
            process_finish_time = self.run_process(pid, 1, self.current_time, leaf_values)
            sleep(1)
            n.cursor.restore()
            n.draw(test_d, BarDescriptor(bd_defaults[pid]))
            print('\r current time: %d' % self.current_time)

            if process_finish_time != 0:
                self.process.process_run_info(pid, process_finish_time, self.result)
                self.process.process_exit(pid)

    def hrn(self):

        leaf_values = {}
        bd_defaults = {}
        test_d = {}
        self.init_progressive(leaf_values, bd_defaults, test_d)
        n.make_room(test_d)
        n.draw(test_d, BarDescriptor(bd_defaults['A']))

        while len(self.process.p_id):
            identifier = "p_id"
            rr = 0
            for p in self.process.p_id:
                p_rr = (self.current_time - self.process.arrive_time[p] + self.process.remain_time[p]) /\
                       self.process.service_time[p]
                if p_rr > rr:
                    identifier = p
                    rr = p_rr

            if self.current_time < self.process.arrive_time[identifier]:
                sleep(1)
                self.current_time += 1
                print('\r current time: %d' % self.current_time, end='')
                continue

            process_finish_time = self.run_process(identifier, 1, self.current_time, leaf_values)
            sleep(1)
            n.cursor.restore()
            n.draw(test_d, BarDescriptor(bd_defaults[identifier]))
            print('\r current time: %d' % self.current_time)

            if process_finish_time != 0:
                self.process.process_run_info(identifier, process_finish_time, self.result)
                self.process.process_exit(identifier)

    def print_results(self):
        for r in self.result:
            r.print_result_info()


class Result:
    def __init__(self, _p_id, _finish_time=0, _run_time=0, _weight_time=0.0):
        self.p_id = _p_id
        self.finish_time = _finish_time
        self.run_time = _run_time
        self.weight_time = _weight_time

    def print_result_info(self):
        print('Process \033[;32;0m{0}\033[0m, '
              'finished at \033[;32;0m{1}\033[0m, '
              'run time \033[;32;0m{2}\033[0m, '
              'weighted time \033[;32;0m{3:4.2f}\033[0m'
              .format(self.p_id,
                      self.finish_time,
                      self.run_time,
                      self.weight_time))


if __name__ == '__main__':
    p_num = input('Please enter the number of process:')
    print('Please enter the arrive time and the service time of processes:')
    p_id, arrive_time, service_time = input().split()
    processor = Processor(p_id, int(arrive_time), int(service_time))
    for i in range(0, int(p_num) - 1):
        p_id, arrive_time, service_time = input().split()
        processor.process.add_process(p_id, int(arrive_time), int(service_time))

    print('Choose a approach to run processes:')
    print('1.fcfs')
    print('2.rr')
    print('3.sjf')
    print('4.hrn')
    choice = input()

    if choice == '1':
        processor.fcfs()
    elif choice == '2':
        processor.rr()
    elif choice == '3':
        processor.sjf()
    elif choice == '4':
        processor.hrn()

    print()
    print('The running result are:')
    processor.print_results()
    print()
