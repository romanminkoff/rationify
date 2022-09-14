from flask import Flask, redirect, url_for, render_template, session, request
import uuid

import settings

PORT = 50100
app = Flask("Rationify")

def main():
    app.secret_key = uuid.uuid1().bytes
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
    return render_template('overview.html', profile=profile)

@app.route("/profile", methods=["GET"])
def route_profile():
    profile = _param(session, 'profile')
    return render_template('profile.html', profile=profile)

@app.route("/ration", methods=["GET"])
def route_ration():
    profile = _param(session, 'profile')
    return render_template('ration.html', profile=profile)

@app.route("/history", methods=["GET"])
def route_history():
    profile = _param(session, 'profile')
    return render_template('history.html', profile=profile)

### API
@app.route('/create_profile', methods=['POST'])
def route_create_profile():
    profile = request.form['profile']
    session['profile'] = profile
    settings.store_profile(profile)
    return redirect(url_for('route_overview'))

@app.route('/choose_profile', methods=['POST'])
def route_set_profile():
    print(request.form)
    profile = request.form['profile_name']
    if profile:
        session['profile'] = profile
        return redirect(url_for('route_overview'))
    return redirect(url_for('route_index'))

def _param(session, param, default=None):
    if param in session:
        return session[param]
    return default

if __name__ == "__main__":
    main()