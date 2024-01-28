import touchpi.common.shared
from touchpi.common.config import log


class SimulateApp():
    def __init__(self, testname):
        log.info("SimulateApp.__Init__ in test " + testname)

    @staticmethod
    def insert_test_data(key, value):
        touchpi.common.shared.data.set("_core_", key, value)

    @staticmethod
    def delete_test_data(key):
        touchpi.common.shared.data.delete("_core_", key)

    @staticmethod
    def get_test_data(key):
        return touchpi.common.shared.data.get("_core_", key)