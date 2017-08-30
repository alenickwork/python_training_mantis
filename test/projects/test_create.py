from model.project import Project

def test_create(app, json_projects):
    project = json_projects

    old_list = app.project.get_projects_list()

    app.project.create_new_project(project)

    new_list = app.project.get_projects_list()

    assert len(old_list) + 1 == len(new_list)

    old_list.append(project)

    assert sorted(new_list, key = Project.name_or_null) == sorted(old_list, key = Project.name_or_null)