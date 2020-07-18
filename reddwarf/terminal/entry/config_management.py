from rsterm import EntryPoint
from reddwarf.environment import ProjectContext, provide_project_context


class NewConfig(EntryPoint):

    entry_point_args = {
        ('config_name', ): {
            'help': 'The name of the configuration to create'
        }
    }

    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        self.validate_config_name()

    def validate_config_name(self):
        invalid_chars = '!"#$%&\'()*+,/:;<=>?@[\\]^`{|}~ '

        try:
            for char in self.cmd_args.config_name:
                if char in invalid_chars:
                    raise ValueError(f"{invalid_chars} are not allowed in config names.")

        except ValueError as e:
            print(e.args[0])
