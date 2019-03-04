import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path
from jsonpath import jsonpath

class ProjectManager:
    def __init__(self):
        #self.directory_check()

        self.EDITOR = os.environ.get('EDITOR', 'vim')
        self.w = TaskWarrior()
        self.tasks = self.w.load_tasks()
        self.home_dir = str(Path.home())
        self.personal_dir = '{}/core/personal'.format(self.home_dir)

    def project_min(self):
        filedir = '{}/project_notes'.format(self.personal_dir)
        filename = 'MINIMUM'

        self.modify_file(
            filename,
            filedir,
        )


    def project_readme(
        self,
        project,
    ):
        filedir = self.get_full_dir_path(project)
        filename = 'README'

        self.modify_file(
            filename,
            filedir,
        )


    def project_note(
        self,
        project,
        description,
    ):
        date = datetime.strftime(
            datetime.now(),
            '%Y-%m-%d',
        )
        task_id = self.get_task_id(project)
        filedir = self.get_full_dir_path(
            project,
            date[:7],
        )
        note_number = 0
        all_notes = os.listdir(filedir)
        for note in all_notes:
            if date == note[:10]:
                note_number += 1

        note_name = '{date}_{num}_{desc}'.format(
            date=date,
            num=note_number,
            desc=description,
        )
        self.create_file(
            note_name,
            filedir,
            description,
        )
        call(['task', str(task_id), 'annotate', note_name])

    def get_task_id(
        self,
        project,
    ):
        project_id = jsonpath(
            self.tasks, 
            "$..[?(@.description=='{project}')].id".format(
                project=project
            )
        )
        return project_id[0]


    def get_full_dir_path(
        self,
        project,
        final_dir=None,
    ):
        if final_dir:
            full_dir_path = '{project}/{final_dir}'.format(
                project=project,
                final_dir=final_dir,
            )
        else:
            full_dir_path = project

        project_id = jsonpath(
            self.tasks,
            "$..[?(@.description=='{project}')].uuid".format(
                project=project
            )
        )
        current_id = jsonpath(
            self.tasks, 
            "$..[?('{}' in @.depends)].uuid".format(
                project_id[0]
            )
        )
        while current_id:
            parent_project = jsonpath(
                self.tasks,
                "$..[?(@.uuid=='{}')].description".format(
                    current_id[0]
                )
            )
            full_dir_path = '{project}/{path}'.format(
                project=parent_project[0],path=full_dir_path
            )
            current_id = jsonpath(
                self.tasks, "$..[?('{}' in @.depends)].uuid".format(
                    current_id[0]
                )
            )

        full_dir_path = '{personal_dir}/project_notes/{path}'.format(
            personal_dir=self.personal_dir,
            path=full_dir_path
        )
        call(['mkdir', '-p', full_dir_path])
        return full_dir_path

    def create_file(
        self,
        filename,
        filedir,
        defaulttext='',
    ):

        filepath = '{0}/{1}'.format(
            filedir,
            filename,
        )
        with open(filepath, 'w') as _in:
            _in.write(defaulttext)
            _in.flush()
            call([self.EDITOR, _in.name])


    def modify_file(
        self,
        filename,
        filedir,
        defaulttext='',
    ):
        filepath = '{0}/{1}'.format(
            filedir,
            filename,
        )
        if filename in os.listdir(filedir):
            with open(filepath, 'r') as _in:
                call([self.EDITOR, _in.name])
        else:
            self.create_file(
                filename,
                filedir,
                defaulttext,
            )


    def directory_check(
        self,
    ):
        current_dir = os.getcwd()
        home_dir = str(Path.home())

        if current_dir != '{}/core'.format(home_dir):
            raise ValueError('Wrong directory; switch to ~/core')
