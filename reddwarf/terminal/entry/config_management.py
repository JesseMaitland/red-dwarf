from rsterm import EntryPoint
from reddwarf.environment import ProjectContext, provide_project_context


def validate_config_name(self):
    invalid_chars = '!"#$%&\'()*+,/:;<=>?@[\\]^`{|}~ '

    try:
        for char in self.cmd_args.config_name:
            if char in invalid_chars:
                raise ValueError(f"{invalid_chars} are not allowed in config names.")

    except ValueError as e:
        print(e.args[0])


common_args = {
    ('config_name',): {
        'help': 'The name of the configuration to create'
    }
}


class NewConfig(EntryPoint):
    entry_point_args = common_args

    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        validate_config_name(self.cmd_args.config_name)
        project_context.create_config(self.cmd_args.config_name)


class RunConfig(EntryPoint):
    entry_point_args = common_args

    @provide_project_context
    def __init__(self, project_context: ProjectContext) -> None:
        self.project_context = project_context
        super().__init__()

    def run(self) -> None:
        validate_config_name(self.cmd_args.config_name)
        db_connection = self.config.get_db_connection('red-dwarf')
        sql_template = self.fetch_and_render_sql_template(self.cmd_args.config_name)
        cursor = db_connection.cursor()

        try:
            cursor.execute(sql_template)
            db_connection.commit()
        except Exception:
            db_connection.rollback()
        finally:
            db_connection.close()

    def fetch_and_render_sql_template(self, config_name: str) -> str:
        return self.project_context.render_config(config_name=config_name)
