import psutil
import struct
import typing

from Type import Type
from Value import Value


def _get_pid(name: str) -> int:
    """
    Tries to find a process by a given name
    :param name: name of the process
    :return: pid of the process or None if not found
    """
    for proc in psutil.process_iter():
        if name in proc.name():
            return proc.pid


class Memory:
    """
    This class is for reading/writing to another process, optimally you'd probably map the pages you wanted to
    read/write to the current process but we'll see, initially I'll use /proc/{pid}/maps

    It's quite unlikely that this class will receive unit tests since it's very easy to manually test this but quite hard
    to make automatic tests for it.
    """

    def __init__(self):
        """
        NOTE: if you give the name it tries to find a process by that name but it may get it wrong

        :param pid: pid or name of process
        """
        self.pid: int = 0
        self.memory: typing.BinaryIO = None
        self.process: psutil.Process = None
        self.entries: list[Value] = None

    def attach(self, pid: int):
        self.memory = open(f"/proc/{pid}/mem", "r+b")
        self.process = psutil.Process(pid)

    def detach(self):
        """
        detaches itself from an attached process
        """
        if self.memory is not None:
            self.memory.close()
        self.memory = None
        self.process = None

    def read(self, address: int, type_: Type) -> typing.Any:
        """
        read size bytes from the processes memory
        :param address: address to read from
        :param size: bytes to read
        :return: the bytes
        """
        self.memory.seek(int(address))
        buf = self.memory.read(type_.size())
        return struct.unpack(type_.get_format(), buf)[0]

    def write(self, address: int, data: typing.Any) -> None:
        """
        tries to write to a given memory address

        :param address: address of to write to
        :param data: data to write
        :return:
        """
        self.memory.seek(int(address))
        self.memory.write(data)

    def progress(self):
        """
        this will be for the eventual progress bar
        :return:
        """
        raise NotImplementedError("progress not implemented")

    def reset_scan(self):
        self.entries = None

    def scan(self, value: typing.Any, value_type: Type = Type.UINT32, aligned: bool = True):
        """
        scans the memory for a given number
        TODO: add more configuration of what to search, e.g. only look in stack, non executables etc


        NOTE: this could probably read a page at a time, I'll have to do performance tests though
        this should also be optimized a lot more, wastes quite a lot of memory currently as it creates a new
        list each time it filters the results though on "new" computers it would probably not be an issue
        :param value: value to compare to
        :param value_type: type of the value
        :param aligned: whether or not the search should be aligned or not, ignored if not initial scan
        :return:
        """
        if isinstance(value, str):
            value = value_type.parse_value(value)

        if self.entries is None:
            return self._scan_initial(value, value_type, aligned)
        else:
            return self._scan_cull(value, value_type)

    def _scan_initial(self, value: typing.Any, value_type: Type, aligned: bool = True):
        """
        initial scanning, creates the first list which then will be culled down
        :param value: value to look for
        :param value_type: the type of the value
        :param aligned: whether or not the search will be aligned or not
        :return: a list of entries found
        """
        offset = value_type.size() if aligned else 1
        self.entries = []

        for mem_map in self.process.memory_maps(grouped=False):
            if mem_map.path in ("[vvar]", "[vsyscall]") or "r" not in mem_map.perms:
                continue  # There seems to be some bug that you cannot read from vvar from an outside process

            print("scanning range:", mem_map.addr)
            addr = int(mem_map.addr.split("-")[0], 16)
            map_size = int(mem_map.size)

            for i in range(0, map_size, offset):
                read_value = self.read(addr+i, value_type)

                if read_value == value:
                    self.entries.append(Value(addr + i, value_type, read_value))

        return self.entries

    def _scan_cull(self, value: typing.Any, value_type: Type):
        if self.entries is None:
            return
        new_list: list = []

        for e in self.entries:
            new_value = self.read(e.address, e.type)

            if new_value == value:
                new_list.append(e)

        self.entries = new_list
        return self.entries
