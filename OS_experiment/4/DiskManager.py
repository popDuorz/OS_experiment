import matplotlib.pyplot as plt 
class Disk(object):
    def __init__(self):
        self.list = [98,183,37,122,14,124,65,69]
        self.position = 100
        self.move = 0
        self.x = [100]
        self.y = range(9)

    def sstf(self):
        pos = -1
        while len(self.list) != 0:
            for i in range(len(self.list)):
                a = 100000
                if abs(self.list[i] - self.position) < a:
                    a = abs(self.list[i] - self.position)
                    pos = i
            self.move = self.move + abs(self.list[pos] - self.position)
            print(self.list[pos],"move length:",self.move)
            self.x.append(self.list[pos])
            self.position = self.list[pos]
            self.list.pop(pos)

    def scan(self, cur_dir):
        direction = cur_dir
        while len(self.list) != 0:
            if direction == 0:
                a = 10000000
                pos = -1
                for i in range(len(self.list)):
                    if (self.list[i] - self.position) < 0 and abs(self.list[i] - self.position) < a:
                        a = abs(self.list[i] - self.position)
                        pos = i
                if pos != -1:
                    self.move = self.move + abs(self.list[pos] - self.position)
                    print(self.list[pos],"move length",self.move)
                    self.position = self.list[pos]
                    self.x.append(self.list[pos])
                    self.list.pop(pos)
                else:
                    direction = 1
            else:
                a = 10000000
                pos = -1
                for i in range(len(self.list)):
                    if (self.list[i] - self.position) > 0 and abs(self.list[i] - self.position) < a:
                        a = abs(self.list[i] - self.position)
                        pos = i
                if pos != -1:
                    self.move = self.move + abs(self.list[pos] - self.position)
                    print(self.list[pos],"move length",self.move)
                    self.position = self.list[pos]
                    self.x.append(self.list[pos])
                    self.list.pop(pos)
                else:
                    direction = 0

if __name__ == '__main__':
    disk = Disk()
    print("initial position",disk.position)
    disk.scan(1)
    plt.figure(figsize = (10,8))
    ax = plt.axes()
    plt.plot(disk.x, disk.y, label='path', linewidth=0, color='white', marker='o', markerfacecolor='red',markersize='5')
    for i in range(0,len(disk.x) - 1):
        ax.annotate("", xy=(disk.x[i+1], disk.y[i+1]), xytext=(disk.x[i], disk.y[i]), arrowprops=dict(arrowstyle="->"))
    # plt.plot(disk.x,disk.y,label='path',linewidth=3,color='black', marker='o', markerfacecolor='red',markersize=12)
    plt.xlabel('position')
    plt.ylabel('No.')
    plt.legend()
    plt.show()




        
