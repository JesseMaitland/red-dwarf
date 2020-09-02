from pathlib import Path
from jinja2 import Template, FileSystemLoader, Environment, PackageLoader
from rsterm import EntryPoint
from red_dwarf.project import ProjectContext, provide_project_context, RedDwarfConfig


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

    @staticmethod
    def render_unload_template(unload_type: str, config: RedDwarfConfig) -> str:
        allowed_unload_types = ['ONCE', 'INCREMENTAL']

        if unload_type:

            if unload_type not in allowed_unload_types:
                raise ValueError("allowed values for unload types are ONCE, or INCREMENTAL")

            else:
                template_loader = PackageLoader(package_name='red_dwarf')
                template_env = Environment(loader=template_loader, trim_blocks=True, lstrip_blocks=True)
                template = template_env.get_template(f'unload_{unload_type.lower()}.sql')
                return template.render(config=config)


class NewConfig(BaseConfigEntry):

    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        self.validate_config_name()
        project_context.create_config(self.cmd_args.config_name)


class ShowConfig(BaseConfigEntry):
    """
    TODO: remove this before deployment. Serves as a test entrypoint
    """
    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        self.validate_config_name()
        cfg_name = self.cmd_args.config_name

        raw_cfg = project_context.get_config(cfg_name)
        config: RedDwarfConfig = project_context.parse_config(raw_cfg).get(cfg_name)

        templates = {
            config.execution.once: self.render_unload_template(config.execution.once, config),
            config.execution.incremental: self.render_unload_template(config.execution.incremental, config)
        }

        for k, v in templates.items():
            print(v)


