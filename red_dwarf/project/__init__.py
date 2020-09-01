import yaml
from pathlib import Path
from typing import Dict
from .context import ProjectContext
from .configs import RedDwarfConfig


def parse_configs(config_paths: Dict[str, Path]) -> Dict[str, RedDwarfConfig]:
    parsed_configs = {}
    for name, config_path in config_paths.items():
        parsed_configs[name] = RedDwarfConfig(**yaml.safe_load(config_path.open())['red_dwarf_config'])
    return parsed_configs


def provide_project_context(func):
    def wrapper(*args, **kwargs):
        pc = ProjectContext()
        pc.set_config_parser(parse_configs)
        return func(project_context=pc, *args, **kwargs)

    return wrapper
