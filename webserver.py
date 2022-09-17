from flask import Flask, redirect, url_for, render_template, session, request
import uuid

import ration
import settings

PORT = 50100
app = Flask("Rationify")
app.secret_key = uuid.uuid1().bytes

def main():
    app.run(port=PORT)

### Main pages
@app.route("/index", methods=["GET"])
def route_index():
    """Login page"""
    profile = _param(session, 'profile')
    profiles = settings.get_profiles()
    return render_template('index.html', profiles=profiles, profile=profile)

@app.route("/", methods=["GET"])
def route_root():
    return redirect(url_for("route_index"))

@app.route("/overview", methods=["GET"])
def route_overview():
    profile = _param(session, 'profile')
    rations = settings.get_ration(profile)
    return render_template('overview.html', profile=profile, ration=rations)

@app.route("/profile", methods=["GET"])
def route_profile():
    profile = _param(session, 'profile')
    return render_template('profile.html', profile=profile)

@app.route("/ration", methods=["GET"])
def route_ration():
    profile = _param(session, 'profile')
    rations = settings.get_ration(profile)
    return render_template('ration.html', profile=profile,
                           ration=rations, periods=ration.periods)

@app.route("/history", methods=["GET"])
def route_history():
    profile = _param(session, 'profile')
    return render_template('history.html', profile=profile)

### API
def choose_profile(profile):
    session['profile'] = profile

@app.route('/create_profile', methods=['POST'])
def route_create_profile():
    profile = request.form['profile']
    settings.store_profile(profile)
    choose_profile(profile)
    return redirect(url_for('route_overview'))

@app.route('/choose_profile', methods=['POST'])
def route_set_profile():
    profile = request.form['profile_name']
    if profile:
        choose_profile(profile)
        return redirect(url_for('route_overview'))
    return redirect(url_for('route_index'))

def _param(session, param, default=None):
    if param in session:
        return session[param]
    return default

def save_ration(profile, form):
    item = form['new_item']
    quantity = form['new_quantity']
    period = form['new_period']
    if all([item, quantity, period]):
        ration_json = settings.get_ration(profile)
        field = ration.field(item, quantity, period)
        ration_json.append(field)
        settings.store_ration(profile, ration_json)

@app.route('/save_ration', methods=['POST'])
def route_save_ration():
    profile = _param(session, 'profile')
    if profile:
        save_ration(profile, request.form)
        return redirect(url_for('route_ration'))
    return redirect(url_for('route_index'))

def save_intake(profile, form):
    intakes = form.to_dict()  # TODO: should not include diplicates!
    if not intakes:
        return
    rations = settings.get_ration(profile)
    new_rations = []
    for d in rations:
        _d = d.copy()
        if _d['item'] in intakes:
            _d['intake'] = intakes[_d['item']]
        new_rations.append(_d)
    settings.store_ration(profile, new_rations)

@app.route('/save_intake', methods=['POST'])
def route_save_intake():
    profile = _param(session, 'profile')
    save_intake(profile, request.form)
    return redirect(url_for('route_overview'))

if __name__ == "__main__":
    main()