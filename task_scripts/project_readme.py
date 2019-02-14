import sys
from project_manager import ProjectManager

# First argument is the project
# Second argument is the title/description

pm = ProjectManager()

project = sys.argv[1]

pm.project_readme(
    project,
)

