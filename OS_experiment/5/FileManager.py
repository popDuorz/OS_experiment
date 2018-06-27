import random

class File(object):

    def __init__(self, _name='untitled.txt', _start=0, _block_length=0, _size=0):
        self.name = _name
        self.start = _start
        self.block_length = _block_length
        self.size = _size

    def print_file_info(self):
         print('filename: '       + '\033[;32;0m' + self.name          + '\033[0m' +
              ' file position: ' + '\033[;32;0m' + str(self.start)     + '\033[0m' +
              ' file size: '   + '\033[;32;0m' + str(self.size) + 'kb' + '\033[0m')

    def get_block_length(self):
        return self.block_length

    def get_start(self):
        return self.start

class Disk:

    def __init__(self):
        self.bitmap = [0 for i in range(500)]

    def find_block(self, _length):
        for _start in range(0, 500):
            has_fragment = 0
            for y in range(_start, _start + _length):
                if self.bitmap[y]:
                    has_fragment = 1
                    break
            if has_fragment == 0:
                for z in range(_start, _start + _length):
                    self.bitmap[z] = 1
                return _start

    def show_disk(self):
        for x in range(0,500):
            if self.bitmap[x] == 0:
                print("\033[;42m \033[0m", end='')
            else:
                print("\033[;41m \033[0m", end='')
            if (x+1) % 100 == 0 :
                print("\n", end='')

    def delete_file(self, file):
        for x in range(file.start, file.get_start() + file.get_block_length()):
            self.bitmap[x] = 0


if __name__ == '__main__':
    disk = Disk()
    files = [None] * 55
    disk.show_disk()
    print()

    print("Create new files")
    print("New files' information:")
    for i in range(50):
        size = random.randint(2, 9)
        length = round(size / 2)
        start = disk.find_block(length)
        name = str(i + 1) + '.txt'
        files[i] = File(name, start, length, size)
        files[i].print_file_info()

    print()
    print("Disk status after creating:")
    disk.show_disk()
    print()

    print("Delete odd number files")
    print("Deleted files information:")
    for i in range(0, 50, 2):
        disk.delete_file(files[i])
        files[i].print_file_info()

    print()
    print("Disk status after deleting:")
    disk.show_disk()
    print()

    print("Insert new files")
    print("Inserted files information")
    file_names = ['A.txt','B.txt','C.txt','D.txt','E.txt']
    for index, name in enumerate(file_names):
        size = random.randint(2, 9)
        length = round(size / 2)
        start = disk.find_block(length)
        files[index + 50] = File(name, start, length, size)
        files[index + 50].print_file_info()

    print()
    print("Disk status after inserting:")
    disk.show_disk()
    print()
