import sys
class VirtualStorage(object):
    def __init__(self,num):
        self.page_num = num
        self.lost = 0
        self.hit = 0
        self.page = []
        for i in range(num):
            self.page.append(0)

    def fifo(self,page_id):
        if page_id in self.page:
            self.hit = self.hit + 1
        else:
            for i in range(self.page_num - 1):
                self.page[i] = self.page[i + 1]
            self.page[self.page_num - 1] = page_id
            self.lost = self.lost + 1
            self.print_result()

    def lru(self,page_id):
        if page_id in self.page:
            self.hit = self.hit + 1
            for i in range(self.page.index(page_id), self.page_num - 1):
                self.page[i] = self.page[i + 1]
        else:
            self.lost = self.lost + 1
            for i in range(self.page_num - 1):
                self.page[i] = self.page[i + 1]
        self.page[self.page_num - 1] = page_id
        self.print_result()

    def print_result(self):
        for i in range(self.page_num):
            sys.stdout.write(str(self.page[i]) + '   ')
        sys.stdout.write(str(self.hit) + '   ' + str(self.lost) + '\n')

if __name__ == '__main__':
    # content = [1,2,3,4,2,1,5,6,2,1,2,3,7,6,3,2,1,2,3,6]
    content = [1, 2, 3, 4, 2, 1]
    virtual_storage = VirtualStorage(4)
    print('1   2   3   4  hit lost\n')
    for i in range(len(content)):
        virtual_storage.lru(content[i])
