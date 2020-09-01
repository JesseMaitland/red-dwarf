from rsterm import EntryPoint
from red_dwarf.project import provide_project_context, ProjectContext


class InitProject(EntryPoint):

    @provide_project_context
    def run(self, project_context: ProjectContext) -> None:
        project_context.init_project()

