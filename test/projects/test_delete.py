from model.project import Project


def test_delete(app):
    project = app.project.create_random_project()

    old_list = app.project.get_projects_list()

    app.project.delete_project(project)

    new_list = app.project.get_projects_list()

    assert len(old_list) - 1 == len(new_list)

    old_list.remove(project)

    assert sorted(new_list, key = Project.name_or_null) == sorted(old_list, key = Project.name_or_null)