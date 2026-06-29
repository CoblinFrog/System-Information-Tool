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

    def get_storage_info(self) -> dict:
        raise NotImplementedError

    def get_os_info(self) -> dict:
        raise NotImplementedError

    def get_model_info(self) -> dict:
        raise NotImplementedError
