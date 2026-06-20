class BaseEngine:
    """The mandatory blueprint all OS engines must implement."""

    def get_cpu_info(self) -> dict:
        raise NotImplementedError

    def get_graphics_info(self) -> dict:
        raise NotImplementedError

    def get_memory_info(self) -> dict:
        raise NotImplementedError

    def get_battery_info(self) -> dict:
        raise NotImplementedError

    def get_misc_info(self) -> dict:
        raise NotImplementedError