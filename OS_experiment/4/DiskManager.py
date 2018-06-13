import matplotlib.pyplot as plt 
import random
class Disk(object):
    def __init__(self, _start_position, _movement_num):
        self.list_for_sstf = [] 
        for m in range(_movement_num):
            self.list_for_sstf.append(random.randint(1, 1000) % 500)
        self.list_for_scan = self.list_for_sstf.copy()
        self.position = _start_position
        self.move_for_sstf = 0
        self.move_for_scan = 0
        self.x_for_sstf = [_start_position]
        self.y_for_sstf = range(_movement_num + 1)
        self.x_for_scan = [_start_position]
        self.y_for_scan = range(_movement_num + 1)

    def sstf(self):
        pos = -1
        while len(self.list_for_sstf) != 0:
            for i in range(len(self.list_for_sstf)):
                a = 100000
                if abs(self.list_for_sstf[i] - self.position) < a:
                    a = abs(self.list_for_sstf[i] - self.position)
                    pos = i
            self.move_for_sstf = self.move_for_sstf + abs(self.list_for_sstf[pos] - self.position)
            print(self.list_for_sstf[pos],"sstf move length:",self.move_for_sstf)
            self.x_for_sstf.append(self.list_for_sstf[pos])
            self.position = self.list_for_sstf[pos]
            self.list_for_sstf.pop(pos)

    def scan(self, cur_dir):
        direction = cur_dir
        while len(self.list_for_scan) != 0:
            if direction == 0:
                a = 10000000
                pos = -1
                for i in range(len(self.list_for_scan)):
                    if (self.list_for_scan[i] - self.position) < 0 and abs(self.list_for_scan[i] - self.position) < a:
                        a = abs(self.list_for_scan[i] - self.position)
                        pos = i
                if pos != -1:
                    self.move_for_scan = self.move_for_scan + abs(self.list_for_scan[pos] - self.position)
                    print(self.list_for_scan[pos],"move length",self.move_for_scan)
                    self.position = self.list_for_scan[pos]
                    self.x_for_scan.append(self.list_for_scan[pos])
                    self.list_for_scan.pop(pos)
                else:
                    direction = 1
            else:
                a = 10000000
                pos = -1
                for i in range(len(self.list_for_scan)):
                    if (self.list_for_scan[i] - self.position) > 0 and abs(self.list_for_scan[i] - self.position) < a:
                        a = abs(self.list_for_scan[i] - self.position)
                        pos = i
                if pos != -1:
                    self.move_for_scan = self.move_for_scan + abs(self.list_for_scan[pos] - self.position)
                    print(self.list_for_scan[pos],"move length",self.move_for_scan)
                    self.position = self.list_for_scan[pos]
                    self.x_for_scan.append(self.list_for_scan[pos])
                    self.list_for_scan.pop(pos)
                else:
                    direction = 0

if __name__ == '__main__':
    _start_position = input('Input the start position:')
    _movement_num = input('Input the movement number:')

    disk = Disk(int(_start_position), int(_movement_num))
    print("initial position", disk.position)
    plt.figure(figsize = (10,8))
    ax = plt.axes()

    disk.scan(1)
    plt.plot(disk.x_for_scan, disk.y_for_scan, label='SCAN', linewidth=0, color='white', marker='o', markerfacecolor='red',markersize='10')
    for i in range(0,len(disk.x_for_scan) - 1):
        ax.annotate("", xy=(disk.x_for_scan[i+1], disk.y_for_scan[i+1]), xytext=(disk.x_for_scan[i], disk.y_for_scan[i]), arrowprops=dict(arrowstyle="->", facecolor='red'))

    disk.sstf()
    plt.plot(disk.x_for_sstf, disk.y_for_sstf, label='SSTF', linewidth=0, color='white', marker='v', markerfacecolor='blue',markersize='10')
    for i in range(0,len(disk.x_for_sstf) - 1):
        ax.annotate("", xy=(disk.x_for_sstf[i+1], disk.y_for_sstf[i+1]), xytext=(disk.x_for_sstf[i], disk.y_for_sstf[i]), arrowprops=dict(arrowstyle="->", facecolor='blue'))
    # plt.plot(disk.x,disk.y,label='path',linewidth=3,color='black', marker='o', markerfacecolor='red',markersize=12)
    plt.xlabel('position')
    plt.ylabel('No.')
    plt.legend()
    plt.show()







        
