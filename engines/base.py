class BaseEngine:
    """The mandatory blueprint all OS engines must implement."""

    def get_cpu_info(self) -> dict:
        raise NotImplementedError

    def get_gpu_info(self) -> dict:
        raise NotImplementedError

    def get_memory_info(self) -> dict:
        raise NotImplementedError