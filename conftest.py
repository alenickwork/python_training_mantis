import pytest
from fixture.application import Application
from fixture.session import SessionBroken
import json
import jsonpickle
import os
import importlib

fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        file)
        with open(config_file_path) as config_file:
            target = json.load(config_file)
    return target

@pytest.fixture(scope="class")
def app(request):
    global fixture
    global target
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser, web_config['web']["baseUrl"])
        fixture.session.login(username = web_config['webadmin']["username"],
                              password = web_config['webadmin']["password"])
    return fixture

@pytest.fixture(scope="session", autouse = True)
def stop(request):
    def fin():
        try:
            fixture.session.ensure_logout()
            fixture.destroy()
        except SessionBroken:
            pass
    request.addfinalizer(fin)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")

def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_from_json(jfile):
    file_p = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data/%s.json" % jfile)
    with open(file_p) as jfile_cont:
        return jsonpickle.decode(jfile_cont.read())

def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids = [str(x) for x in testdata])

def load_from_json(jfile):
    file_p = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data/%s.json" % jfile)
    with open(file_p) as jfile_cont:
        return jsonpickle.decode(jfile_cont.read())