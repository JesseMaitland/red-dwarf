from pathlib import Path
from typing import List, Dict
import yaml
from typing import NamedTuple


class RedDwarfConfig(NamedTuple):
    path: Path
    schema: str
    table: str
    timestamp_column: str
    days_to_keep: int
    partition_by: str
    s3_bucket: str
    s3_key: str
    delete_after: bool
    vacuum_after: bool
    analyse_after: bool
    iam_role: str


class ProjectContext:

    def __init__(self):
        root = Path.cwd().absolute() / "red_dwarf"
        history = 'history'
        configs = 'configs'

        self._paths = {
            'root': root,
            history: root / history,
            configs: root / configs,
        }

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

    def create_history_file(self, file_name: str) -> None:
        history_dir = self.get_dir('history')
        file_path = history_dir / f"{file_name}.log"

        if file_path.exists():
            raise FileExistsError("history file names must be unique")
        else:
            file_path.touch(exist_ok=True)

    def create_config(self, name: str) -> None:
        template = Path(Path(__file__).parent.absolute() / "config_template.yml").read_text()
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

    def get_configs(self) -> Dict[str, RedDwarfConfig]:
        return {p.name.split('.')[0]: self.parse_config(p) for p in self.get_dir('configs').glob('**/*.yml')}

    def get_config(self, name: str) -> RedDwarfConfig:
        return self.get_configs()[name]

    @staticmethod
    def parse_config(config_path: Path) -> RedDwarfConfig:
        config = yaml.safe_load(config_path.open())['red_dwarf_unload_config']
        config['path'] = config_path
        return RedDwarfConfig(**config)


def provide_project_context(func):
    def wrapper(*args, **kwargs):
        pc = ProjectContext()
        return func(project_context=pc, *args, **kwargs)
    return wrapper