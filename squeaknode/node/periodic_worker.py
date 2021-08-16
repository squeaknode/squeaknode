import logging
import threading
from abc import ABC
from abc import abstractmethod

logger = logging.getLogger(__name__)


class Worker(ABC):

    @abstractmethod
    def start(self) -> None:
        pass


class PeriodicWorker(Worker):
    """Access a bitcoin daemon using RPC."""

    @abstractmethod
    def work_fn(self) -> None:
        pass

    @abstractmethod
    def get_interval_s(self) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def do_work(self):
        if self.get_interval_s():
            timer = threading.Timer(
                self.get_interval_s(),
                self.do_work,
            )
            timer.daemon = True
            timer.name = "{}_thread".format(self.get_name())
            timer.start()
            self.work_fn()

    def start(self) -> None:
        thread = threading.Thread(
            target=self.do_work,
            args=(),
        )
        thread.start()
