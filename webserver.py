import copy
import datetime
from flask import Flask, redirect, url_for, render_template, session, request
import uuid
import sys

import ration
import settings

PORT = 50100
app = Flask('Rationify')
app.secret_key = uuid.uuid1().bytes
s = None

def run_server(debug=False):
    global s
    s = settings.Settings()
    app.run(port=PORT, debug=debug)

class S:
    profile = 'profile'
    overview_ww = 'overview_ww'
    target_ww = 'target_ww'

    _ww_fmt = '%Y-W%W'

    @staticmethod
    def current_ww_str():
        return datetime.date.today().strftime(S._ww_fmt)

    @staticmethod
    def ww_str(year, ww):
        return f'{year}-W{ww}'


### Main pages
@app.route("/index", methods=["GET"])
def route_index():
    """Login page"""
    profile = _param(session, S.profile)
    profiles = s.get_profiles()
    return render_template('index.html', profiles=profiles, profile=profile)

@app.route("/", methods=["GET"])
def route_root():
    return redirect(url_for("route_index"))

@app.route("/overview", methods=["GET"])
def route_overview():
    profile = _param(session, S.profile)
    current_ww = S.current_ww_str()
    target_ww = _param(session, S.overview_ww, default=current_ww)
    rations = s.get_ration(profile)
    target_ration = rations.get(target_ww, [])
    return render_template('overview.html',
                           profile=profile,
                           ration=target_ration,
                           target_ww=target_ww,
                           current_ww=current_ww)

@app.route("/profile", methods=["GET"])
def route_profile():
    profile = _param(session, S.profile)
    return render_template('profile.html', profile=profile)

@app.route("/ration", methods=["GET"])
def route_ration():
    profile = _param(session, S.profile)
    rations = s.get_ration(profile)[S.current_ww_str()]
    return render_template('ration.html',
                           profile=profile,
                           ration=rations,
                           period=ration.Periods.Week)

@app.route("/history", methods=["GET"])
def route_history():
    profile = _param(session, S.profile)
    return render_template('history.html', profile=profile)

### API
def _last_ww(wws, fmt):
    def d(ww):
        return datetime.datetime.strptime(ww, fmt)
    if wws:
        return max(d(w) for w in wws).strftime(fmt)
    return None

def update_todays_ration(profile):
    cur_ww = S.current_ww_str()
    rations = s.get_ration(profile)
    if not cur_ww in rations:
        if last_ww := _last_ww(rations.keys(), S._ww_fmt):
            rations[cur_ww] = copy.deepcopy(rations[last_ww])
        else:
            rations[cur_ww] = []
    s.store_ration(profile, rations)

def choose_profile(profile):
    session[S.profile] = profile
    update_todays_ration(profile)

@app.route('/create_profile', methods=['POST'])
def route_create_profile():
    profile = _param(request.form, S.profile)
    if profile:
        s.store_profile(profile)
        choose_profile(profile)
        return redirect(url_for('route_overview'))
    return redirect(url_for('route_index'))

@app.route('/choose_profile', methods=['POST'])
def route_set_profile():
    profile = _param(request.form, S.profile)
    if profile:
        choose_profile(profile)
        return redirect(url_for('route_overview'))
    return redirect(url_for('route_index'))

def _param(session, param, default=None):
    if param in session:
        return session[param]
    return default

def _is_item_duplicated(item, items_lst):
    for it in items_lst:
        if it['item'] == item:
            return True
    return False

def save_ration(profile, field, ww):
    ration_json = s.get_ration(profile)  # {'date': {...},}
    if not _is_item_duplicated(field['item'], ration_json[ww]):
        ration_json[ww].append(field)
        s.store_ration(profile, ration_json)

def add_ration(profile, form):
    item = form['new_item']
    quantity = form['new_quantity']
    period = form['new_period']
    if all([item, quantity, period]):
        field = ration.field(item, quantity, period)
        ww = S.current_ww_str()
        save_ration(profile, field, ww)

@app.route('/add_ration', methods=['POST'])
def route_add_ration():
    profile = _param(session, S.profile)
    if profile:
        add_ration(profile, request.form)
        return redirect(url_for('route_ration'))
    return redirect(url_for('route_index'))

def save_intake(profile, form):
    intakes = form.to_dict()
    ww = intakes.pop(S.target_ww)
    if not intakes:
        return
    rations = s.get_ration(profile)
    if ww in rations:
        for d in rations[ww]:
            if d['item'] in intakes:
                d['intake'] = intakes[d['item']]
        s.store_ration(profile, rations)

@app.route('/save_intake', methods=['POST'])
def route_save_intake():
    profile = _param(session, S.profile)
    save_intake(profile, request.form)
    return redirect(url_for('route_overview'))

def overview_choose_date(form):
    session[S.overview_ww] = form['work_week']

@app.route('/overview_choose_date', methods=['POST'])
def route_overview_choose_date():
    overview_choose_date(request.form)
    return redirect(url_for('route_overview'))

if __name__ == "__main__":
    debug = True if 'debug' in sys.argv else False
    run_server(debug)