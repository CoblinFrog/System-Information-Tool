from engines.base import BaseEngine

class Windows(BaseEngine):
    def get_cpu_info(self) -> dict:
        return{"cpu": "cpu"}