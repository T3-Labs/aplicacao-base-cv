from queue import Queue
from typing import Any, NoReturn

class QMQT():

    def __init__(self, buffer = 100) -> NoReturn:
        self._Q = Queue(buffer)
        self.queue = self._Q.queue

    def collect(self, item)-> NoReturn:
        """
        args: Any value
        --------------
        Put item in Queue.
        """
        self._Q.put(item)

        
    def clear(self)-> NoReturn:
        """
        args: don't have
        --------------
        Clear Queue.
        """
        self._Q.empty()

    def cat(self)-> Any:
        """
        arg: don't have
        --------------
        returns first item from Queue.
        """
        return self._Q.get()

    def get_size(self)-> int:
        """
        arg: don't have
        --------------
        returns Queue size.
        """
        return self._Q.qsize()
