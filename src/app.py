# import logging

# from flask import Flask
# from flask import render_template
# from flask import request
# from flask import redirect
# from flask_wtf import CSRFProtect
# from flask_csp.csp import csp_header

# from sqldb import SqlDb
# # OR
# # from ormdb import OrmDb

# log = logging.getLogger(__name__)
# logging.basicConfig(
#     filename="../runtime/log/app.log",
#     encoding="utf-8",
#     level=logging.DEBUG,
#     format=" %(asctime)s %(message)s",
# )

# sql_db = SqlDb("../runtime/db/sql.db")
# # OR
# # orm_db = OrmDb("../runtime/db/orm.db")

# app = Flask(__name__)
# app.secret_key = b"G6z115u8WnfQ0UIJ"  # To get a unique basic 16 key: https://acte.ltd/utils/randomkeygen

# csrf = CSRFProtect(app)

# # Redirect index.html to domain root for consistent UX
# @app.route("/index", methods=["GET"])
# @app.route("/index.htm", methods=["GET"])
# @app.route("/index.asp", methods=["GET"])
# @app.route("/index.php", methods=["GET"])
# @app.route("/index.html", methods=["GET"])
# def root():
#     return redirect("/", 302)

# @app.route("/", methods=["POST", "GET"])
# @csp_header(
#     {
#         # Server Side CSP is consistent with meta CSP in layout.html
#         "base-uri": "'self'",
#         "default-src": "'self'",
#         "style-src": "'self'",
#         "script-src": "'self'",
#         "img-src": "'self' data:",
#         "media-src": "'self'",
#         "font-src": "'self'",
#         "object-src": "'self'",
#         "child-src": "'self'",
#         "connect-src": "'self'",
#         "worker-src": "'self'",
#         "report-uri": "/csp_report",
#         "frame-ancestors": "'none'",
#         "form-action": "'self'",
#         "frame-src": "'none'",
#     }
# )
# def index():
#     return render_template("/index.html")

# @app.route("/privacy.html", methods=["GET"])
# def privacy():
#     return render_template("/privacy.html")

# @app.route("/form_copy.html", methods=["POST", "GET"])
# def form():
#     if request.method == "POST":
#         email = request.form["email"]
#         text = request.form["text"]
#         print(f"<From(email={email}, text='{text}')>")
#         return render_template("/form_copy.html")
#     else:
#         return render_template("/form_copy.html")

# # Endpoint for logging CSP violations
# @app.route("/csp_report", methods=["POST"])
# @csrf.exempt
# def csp_report():
#     app.logger.critical(request.data)
#     return "done"

# if __name__ == "__main__":
#     # app.logger.debug("Started")
#     app.run(debug=True, host="0.0.0.0", port=5000)

import logging
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_wtf import CSRFProtect  
from flask_csp.csp import csp_header

from database import db #connect to database

csrf = CSRFProtect()

def create_app(): #place factory 
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'sleeptracker-2026'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleep.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) 
    csrf.init_app(app) 

    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from routes.sleep import sleep_bp
    app.register_blueprint(sleep_bp)

    with app.app_context():
        from models import User 
        from models import SleepEntry, SleepGoal
        db.create_all()
    
    return app

app = create_app()

@app.route("/", methods=["POST", "GET"])
@csp_header(
    {
        # Server Side CSP is consistent with meta CSP in layout.html
        "base-uri": "'self'",
        "default-src": "'self'",
        "style-src": "'self'",
        "script-src": "'self'",
        "img-src": "'self' data:",
        "media-src": "'self'",
        "font-src": "'self'",
        "object-src": "'self'",
        "child-src": "'self'",
        "connect-src": "'self'",
        "worker-src": "'self'",
        "report-uri": "/csp_report",
        "frame-ancestors": "'none'",
        "form-action": "'self'",
        "frame-src": "'none'",
    }
)
def index():
    return render_template("/index.html")

app.run()