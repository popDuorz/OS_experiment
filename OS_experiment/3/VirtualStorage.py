import sys
import random
from time import sleep


class VirtualStorage(object):
    def __init__(self, num):
        self.page_num = num
        self.lost = 0
        self.hit = 0
        self.page = []
        for i in range(num):
            self.page.append(0)
        hit = False

    def fifo(self, page_id):
        new = page_id
        old = self.page[0]
        changed_page_num = self.page_num
        if page_id in self.page:
            self.hit = self.hit + 1
            hit = True
            changed_page_num = self.page.index(page_id) + 1
        else:
            hit = False
            for i in range(self.page_num - 1):
                self.page[i] = self.page[i + 1]
            self.page[self.page_num - 1] = page_id
            self.lost = self.lost + 1
        self.print_result(old, new, changed_page_num, hit)

    def lru(self, page_id):
        new = page_id
        old = self.page[0]
        changed_page_num = self.page_num
        if page_id in self.page:
            hit = True
            changed_page_num = self.page.index(page_id) + 1
            self.hit = self.hit + 1
            for i in range(self.page.index(page_id), self.page_num - 1):
                self.page[i] = self.page[i + 1]

        else:
            hit = False
            self.lost = self.lost + 1
            for i in range(self.page_num - 1):
                self.page[i] = self.page[i + 1]
        self.page[self.page_num - 1] = page_id
        self.print_result(old, new, changed_page_num, hit)

    def print_result(self, old, new, changed_page_num, hit):
        if hit:
            action = 'Hit in page ' + str(changed_page_num) + ' and refresh pages'
        elif old == 0:
            action = 'Lost and insert to page ' + str(changed_page_num)
        else:
            action = 'Replace ' + str(old) + ' -> ' + str(new) + ' to ' + 'page ' + str(changed_page_num)
        for i in range(self.page_num):
            sys.stdout.write(str(self.page[i]) + '   ')
        sys.stdout.write(' ' + str(self.hit) + '   ' + str(self.lost) + '    ' + action + '\n')
        sleep(1)


if __name__ == '__main__':
    page_num = input('Input the page number:')
    rw = input('Input the r/w times number:')
    content = []
    for r in range(int(rw)):
        content.append(random.randint(1, int(page_num)+1))
    virtual_storage = VirtualStorage(int(page_num))

    print('Choose a approach:')
    print('1.fifo')
    print('2.lru')
    choice = input()
    print('The access sequence is: ', end='')
    for c in content:
        print(c, end=' ')
    print()

    if choice == '1':
        for i in range(int(page_num)):
            print('\033[1;21;42m'+str(i+1) + '   ' + '\033[0m', end='')
        print('\033[1;21;41mhit lost    action\033[0m')
        for i in range(int(page_num)):
            print('0', end='   ')
        print()
        for i in range(len(content)):
            virtual_storage.fifo(content[i])

    elif choice == '2':
        for i in range(int(page_num)):
            print('\033[1;21;42m'+str(i+1) + '   ' + '\033[0m', end='')
        print('\033[1;21;41mhit lost    action\033[0m')
        for i in range(int(page_num)):
            print('0', end='   ')
        print()
        for i in range(int(content)):
            virtual_storage.lru(content[i])
    hitRatio = float(virtual_storage.hit/int(rw)) * 100
    print('The hit ratio is: %.1f%%' % hitRatio)
    print()

