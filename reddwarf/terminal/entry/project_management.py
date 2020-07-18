from rsterm import EntryPoint
from reddwarf.environment import provide_project_context, ProjectContext


class NewProject(EntryPoint):

    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        project_context.init_project()
