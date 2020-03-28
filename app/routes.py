from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import CommercialForm, LoginForm
from app.models import User
# used to be: from .modules.commercial_assessment_app.main import CommercialApp, form_data_parser
from app.modules.commercial_assessment_app.main import CommercialApp, form_data_parser

@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")

@app.route("/commercial_assessment", methods=["GET", "POST"])
@login_required
def commercial_assessment():
    form = CommercialForm()
    commercial_results = None
    if form.validate_on_submit():
        form_data = request.form
        commercial_app_form_data = form_data_parser(form_data)
        commercial_results = CommercialApp(commercial_app_form_data).run()
        flash("Results available below.")
    return render_template("commercial_assessment.html", title="Commercial Assessment", form=form, results=commercial_results)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("sign_in.html", title="Sign In", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))