import datetime
import os
import pytest
import shutil

from flask.testing import FlaskClient

import ration
import db
import webserver

### Scenario tests
@pytest.fixture()
def client():
    test_db_dir = 'test_db'
    if os.path.exists(test_db_dir):
        shutil.rmtree(test_db_dir)  # start with clean ration/profiles
    webserver.app.testing = True
    webserver._db = db.DB(root_path=test_db_dir)
    with webserver.app.test_client() as client:
        yield client


profile_Garderobis = 'Garderobis'
ration_data = {
    'new_item': 'Milk',
    'new_quantity': '1 cup',
    'new_period': ration.Periods.Week
}
ration_data_duplicated = {
    'new_item': 'Milk',
    'new_quantity': '2 cups',
    'new_period': ration.Periods.Week
}
ration_data_delete = {
    'delete_item': 'Milk'
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

def delete_ration(client, data):
    return client.post('/delete_ration',
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

def test_add_ration_diplicated(client: FlaskClient):
    create_profile(client, profile_Garderobis)
    add_ration(client, ration_data)
    resp_data = add_ration(client, ration_data_duplicated)
    assert '2 cups' not in resp_data

def test_delete_ration(client: FlaskClient):
    create_profile(client, profile_Garderobis)
    resp_data = add_ration(client, ration_data)
    assert 'Milk' in resp_data
    resp_data = delete_ration(client, ration_data_delete)
    assert not 'Milk' in resp_data

def test_save_intake(client):
    create_profile(client, profile_Garderobis)
    add_ration(client, ration_data)
    resp = client.get('/overview').data.decode()
    assert 'value="0" name="Milk"' in resp
    resp = client.post('/save_intake',
                       data={'Milk': 73, 
                             'target_ww': webserver.WW.current_str()},
                       follow_redirects=True).data.decode()
    assert 'value="73" name="Milk"' in resp

def test_overview_choose_date(client):
    resp = client.get('/overview').data.decode()
    assert f'name="work_week" value="{webserver.WW.current_str()}"' in resp
    to_str = webserver.WW.to_str
    new_ww = to_str(datetime.date(2022,5,20))
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

def test_WW_last_in():
    last_in = webserver.WW.last_in
    assert last_in([]) == None
    assert last_in(['2022-W20']) == '2022-W20'
    assert last_in(['2022-W18', '2022-W20', '2022-W19']) == '2022-W20'

def test_WW_to_str_to_date():
    to_str = webserver.WW.to_str
    to_date = webserver.WW.to_date
    d = datetime.date(2022,1,20)  # W3
    d_str = to_str(d)
    d_date = to_date(d_str)
    assert to_str(d_date)=='2022-W03'

def test_WW_str_range():
    r = webserver.WW.str_range
    assert r('2022-W0','2022-W0') == ['2022-W00']
    assert r('2022-W0','2022-W1') == ['2022-W00','2022-W01']
    assert r('2022-W9','2022-W11') == ['2022-W09','2022-W10','2022-W11']
    assert r('2021-W51','2022-W1') == ['2021-W51','2022-W00','2022-W01']
    with pytest.raises(webserver.WWException):
        r('2022-W6','2022-W4')
    with pytest.raises(ValueError):
        r('2022-W60', '2022-W60')


# ration
def test_ration_reset_intake():
    r = [
        {"item": "A", "quantity": "5", "period": "Week", "intake": "53"},
        {"item": "B", "quantity": "200 gr.", "period": "Week", "intake": "9"}
    ]
    r_clean_intake = [
        {"item": "A", "quantity": "5", "period": "Week", "intake": "0"},
        {"item": "B", "quantity": "200 gr.", "period": "Week", "intake": "0"}
    ]
    assert ration.reset_intake(r) == r_clean_intake