from dataclasses import dataclass


@dataclass
class PluginConfig:
    keys: list[str]
    dest_dir: str
    dest_file: str
