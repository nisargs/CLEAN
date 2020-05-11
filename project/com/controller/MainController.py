from flask import render_template, redirect, url_for
from project import app
from project.com.controller.LoginController import adminLoginSession


@app.route('/user/loadFile')
def userLoadFile():
    if adminLoginSession() == "user":
        return render_template("user/addUserFile.html")
    else:
        return redirect(url_for('adminLogoutSession'))


@app.route('/user/searchFile')
def userSearchFile():
    if adminLoginSession() == "user":
        return render_template("user/viewUserFile.html")
    else:
        return redirect(url_for('adminLogoutSession'))

