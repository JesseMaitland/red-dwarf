from rsterm import EntryPoint
from reddwarf.environment import ProjectContext, provide_project_context


def validate_config_name(config_name):
    invalid_chars = '!"#$%&\'()*+,/:;<=>?@[\\]^`{|}~ '

    try:
        for char in config_name:
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
    def run(self, project_context: ProjectContext) -> None:
        validate_config_name(self.cmd_args.config_name)

        sql_template = self.fetch_and_render_sql_template(self.cmd_args.config_name, project_context)
        print(sql_template)

        # cursor = db_connection.cursor()

        # try:
        #     cursor.execute(sql_template)
        #     db_connection.commit()
        # except Exception:
        #     db_connection.rollback()
        # finally:
        #     db_connection.close()

        db_connection = self.config.get_db_connection('red-dwarf')

    def fetch_and_render_sql_template(self, config_name: str, project_context: ProjectContext) -> str:
        iam_role = self.config.get_iam_role('red-dwarf')
        return project_context.render_config(config_name=config_name, iam_role=iam_role)
