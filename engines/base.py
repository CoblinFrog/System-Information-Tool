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

    def format_size_units(self, value, input_unit: str = "bytes") -> str:
        """
        Dynamically scales and formats any data size (Cache, RAM, Disk)
        into the most readable human format (B, KB, MB, GB, TB).
        """
        try:
            # Strip out any trailing text or units if the raw output included them
            if isinstance(value, str):
                cleaned = "".join(c for c in value if c.isdigit() or c == '.')
                raw_number = float(cleaned) if '.' in cleaned else int(cleaned)
            else:
                raw_number = value
        except (ValueError, TypeError):
            return "Unknown"

        if raw_number <= 0:
            return "Unknown"

        # Definition of scales relative to a single Byte
        scales = {"b": 1, "bytes": 1, "kb": 1024, "mb": 1024 ** 2, "gb": 1024 ** 3, "tb": 1024 ** 4}

        unit_key = input_unit.lower().strip()
        if unit_key not in scales:
            return f"{value} {input_unit}"  # Fallback if an unsupported unit string is passed

        total_bytes = raw_number * scales[unit_key]
        labels = ["B", "KB", "MB", "GB", "TB"]
        current_value = float(total_bytes)
        label_index = 0

        while current_value >= 1024 and label_index < len(labels) - 1:
            current_value /= 1024
            label_index += 1

        if current_value.is_integer():
            return f"{int(current_value)} {labels[label_index]}"

        return f"{round(current_value, 2)} {labels[label_index]}"