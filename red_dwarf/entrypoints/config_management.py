from rsterm import EntryPoint
from red_dwarf.project import ProjectContext, provide_project_context, RedDwarfConfig
from redscope.api import introspect_redshift


class BaseConfigEntry(EntryPoint):

    entry_point_args = {
        ('config_name',): {
            'help': 'The name of the configuration in /red-dwarf/configs'
        }
    }

    def run(self) -> None:
        raise NotImplementedError

    def validate_config_name(self):
        invalid_chars = '!"#$%&\'()*+,/:;<=>?@[\\]^`{|}~ '

        try:
            for char in self.cmd_args.config_name:
                if char in invalid_chars:
                    raise ValueError(f"{invalid_chars} are not allowed in config names.")

        except ValueError as e:
            print(e.args[0])


class NewConfig(BaseConfigEntry):

    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        self.validate_config_name()
        project_context.create_config(self.cmd_args.config_name)


class ShowConfig(BaseConfigEntry):

    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        self.validate_config_name()

        config_path = project_context.get_config(self.cmd_args.config_name)
        config: RedDwarfConfig = project_context.parse_config(config_path)
        print(config[self.cmd_args.config_name].table.name)
