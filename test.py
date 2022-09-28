import os
import pytest
import shutil

from flask.testing import FlaskClient

import ration
import settings
import webserver

### Scenario tests
@pytest.fixture()
def client():
    test_settings_dir = 'test_settings'
    if os.path.exists(test_settings_dir):
        shutil.rmtree(test_settings_dir)  # start with clean ration/profiles
    webserver.app.testing = True
    webserver.s = settings.Settings(root_path=test_settings_dir)
    with webserver.app.test_client() as client:
        yield client


profile_Garderobis = 'Garderobis'
ration_data = {
    'new_item': 'Milk',
    'new_quantity': '1 cup',
    'new_period': ration.Periods.Week
}

def create_profile(client, profile):
    return client.post('/create_profile',
        data={'profile': profile}, follow_redirects=True)

def test_create_profile(client: FlaskClient):
    resp = create_profile(client, profile_Garderobis)
    assert profile_Garderobis in resp.data.decode()
    for page in ['/overview', '/index', '/ration']:
        resp_data = client.get(page, follow_redirects=True).data.decode()
        assert f'nav_profile_name">{profile_Garderobis}' in resp_data
    
def test_choose_profile(client: FlaskClient):
    create_profile(client, profile_Garderobis)
    resp_data= client.post('/choose_profile',
        data={'profile': profile_Garderobis},
        follow_redirects=True).data.decode()
    assert f'nav_profile_name">{profile_Garderobis}' in resp_data

def add_ration(client, data):
    return client.post('/add_ration',
                       data=data,
                       follow_redirects=True).data.decode()

def test_add_ration_check_overview(client: FlaskClient):
    create_profile(client, profile_Garderobis)
    resp_data = add_ration(client, ration_data)
    for i in ration_data.values():  # 'Milk', '1 cup', 'Week'
        assert i in resp_data
    resp_data = client.get('/overview').data.decode()
    for i in ration_data.values():
        assert i in resp_data

def test_save_intake(client):
    create_profile(client, profile_Garderobis)
    add_ration(client, ration_data)
    resp = client.get('/overview').data.decode()
    assert 'value="0" name="Milk"' in resp
    resp = client.post('/save_intake',
                       data={'Milk': 73, 
                             'target_ww': webserver.S.current_ww_str()},
                       follow_redirects=True).data.decode()
    assert 'value="73" name="Milk"' in resp

def test_overview_choose_date(client):
    resp = client.get('/overview').data.decode()
    assert f'name="work_week" value="{webserver.S.current_ww_str()}"' in resp
    new_ww = webserver.S.ww_str(2022,5)
    resp = client.post('/overview_choose_date',
                       data={'work_week': new_ww},
                       follow_redirects=True).data.decode()
    assert f'name="work_week" value="{new_ww}"' in resp

###
def test_param():
    a = {'a': 1}
    assert webserver._param(a, 'a') == 1
    assert webserver._param(a, 'y') == None
    assert webserver._param(a, 'y', 4) == 4

def test_last_ww():
    fmt = webserver.S._ww_fmt
    assert webserver._last_ww([], fmt) == None
