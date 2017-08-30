import time
from fixture.actions import ActionsHelper
from model.project import Project
from generator.project import generate_str

class ProjectHelper(ActionsHelper):
    def __init__(self, app):
        self.app = app
        self.wd = self.app.wd
        ActionsHelper.__init__(self,app)

    def open_projects_page(self):
        self.link_click("Manage")
        time.sleep(5)
        self.link_click("Manage Projects")
        self.wait_button_clickable("Create New Project")

    def create_random_project(self):
        proj = Project(name = generate_str(prefix = "Proj_"))
        self.create_new_project(proj)
        return proj

    def create_new_project(self, project_instance):
        self.open_projects_page()
        self.click_create_new()
        self.input_data(project_instance)
        self.input_click("Add Project")
        self.wait_button_clickable("Create New Project")
        self.projects_cache=None

    def click_create_new(self):
        self.input_click("Create New Project")
        self.wait_button_clickable("Add Project")

    def input_data(self, project_instance):
        self.text_input_by_id("project-name", project_instance.name)

    def delete_project(self, project_instance):
        self.open_projects_page()
        self.wd.find_element_by_xpath("//div[@class ='row']//a[.='%s']" % project_instance.name).click()
        #self.link_click(project_instance.name)
        self.wait_button_clickable("Delete Project")
        self.input_click("Delete Project")
        time.sleep(3)
        self.wait_button_clickable("Delete Project")
        self.input_click("Delete Project")
        self.wait_manage_projects_page()
        self.projects_cache = None

    def wait_manage_projects_page(self):
        self.wait_button_clickable("Create New Project")




    @property
    def count(self):
        return len(self.wd.find_elements_by_xpath(".//div[@class='table-responsive']/table/tbody/tr"))

    projects_cache = None

    def get_projects_list(self):
        if self.projects_cache is None:
            self.projects_cache = []
            self.open_projects_page()
            for row in self.wd.find_elements_by_xpath(".//div[@class='table-responsive']/table/tbody/tr"):
                columns = row.find_elements_by_xpath("./td")
                if len(columns) != 5:
                    break
                name = columns[0].find_element_by_xpath("./a").text
                self.projects_cache.append(Project(name = name))
        return self.projects_cache




