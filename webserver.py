from flask import Flask, redirect, url_for, render_template

PORT = 50100

app = Flask("Rationify")

def main():
    app.run(port=PORT)

@app.route("/index", methods=["GET"])
def route_index():
    """Login page"""
    return render_template('index.html')

@app.route("/", methods=["GET"])
def route_root():
    return redirect(url_for("route_index"))

@app.route("/overview", methods=["GET"])
def route_overview():
    return render_template('overview.html')

@app.route("/profile", methods=["GET"])
def route_profile():
    return render_template('profile.html')

@app.route("/ration", methods=["GET"])
def route_ration():
    return render_template('ration.html')

@app.route("/history", methods=["GET"])
def route_history():
    return render_template('history.html')

if __name__ == "__main__":
    main()