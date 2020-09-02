import os
import yaml
from pathlib import Path
from typing import List, Dict, Callable
from jinja2 import Template


class ProjectContext:
    _template_path = Path(__file__).absolute().parent.parent / "templates"

    def __init__(self):
        root = Path.cwd().absolute() / "red-dwarf"
        configs = 'configs'
        rendered = 'rendered'

        self._paths = {
            'root': root,
            configs: root / configs,
            rendered: root / rendered
        }

        self.parse_config: Callable = None

    @property
    def template_path(self) -> Path:
        return self._template_path

    @property
    def unload_template_path(self) -> Path:
        return self._template_path / "unload.sql"

    def set_config_parser(self, config_parser: Callable) -> None:
        self.parse_config = config_parser

    def get_dir(self, name: str) -> Path:
        return self._paths[name]

    def init_project(self):
        self.create_project_dirs()

    def create_project_dirs(self):

        if self.get_dir('root').exists():
            raise FileExistsError("Red Dwarf project already exists!")
        else:
            for name, path in self._paths.items():
                path.mkdir(parents=True, exist_ok=True)

    def create_config(self, name: str) -> None:
        template = Path(self._template_path / "config_template.yml").read_text()
        config_path = self.get_dir('configs')
        config_file = config_path / f"{name}.yml"

        if config_file.exists():
            raise FileExistsError("config file names must be unique.")
        else:
            config_file.touch(exist_ok=True)
            config_file.write_text(template)

    def list_configs(self) -> List[str]:
        return [f.name for f in self.get_dir('configs').glob('**/*.yml')]

    def list_config_paths(self) -> List[Path]:
        return [f for f in self.get_dir('configs').glob('**/*.yml')]

    def get_configs(self) -> Dict[str, Path]:
        return {p.name.split('.')[0]: p for p in self.get_dir('configs').glob('**/*.yml')}

    def get_config(self, name: str) -> Dict[str, Path]:
        config = self.get_configs()[name]
        return {name: config}

    def render_query(self, config_name: str, query_type: str, iam_role: str = None) -> str:
        valid_query_types = ['unload', 'table_meta']

        if query_type not in valid_query_types:
            raise ValueError(f"{query_type} is not a valid query type. Valid types are {valid_query_types}")

        if query_type == 'unload' and iam_role is None:
            raise ValueError("for query type unload, an AWS IAM-ROLE must be provided")

        template_path = self._template_path / f"{query_type}.sql"

        config = self.get_config(config_name)
        config['iam-role'] = iam_role

        template = Template(template_path.read_text())
        return template.render(config=config)
