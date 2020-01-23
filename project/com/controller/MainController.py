from flask import request, render_template, redirect, url_for
from project import app


@app.route('/')
def adminLoadDashboard():
    return render_template("admin/index.html")


@app.route('/admin/searchUser')
def adminSearchUser():
    return render_template("admin/viewUser.html")


# @app.route('/admin/loadZone')
# def loadZone():
#     return render_template("admin/addZone.html")
#
#
# @app.route('/admin/searchZone')
# def searchZone():
#     return render_template("admin/viewZone.html")


# @app.route('/admin/loadWard')
# def adminLoadWard():
#     return render_template("admin/addWard.html")


# @app.route('/admin/searchWard')
# def adminSearchWard():
#     return render_template("admin/viewWard.html")


# @app.route('/admin/loadStaff')
# def adminLoadStaff():
#     return render_template("admin/addStaffHead.html")
#
#
# @app.route('/admin/searchStaff')
# def adminSearchStaff():
#     return render_template("admin/viewStaffHead.html")


@app.route('/admin/loadDataset')
def adminLoadDataset():
    return render_template("admin/addDataset.html")


@app.route('/admin/searchDataset')
def adminSearchDataset():
    return render_template("admin/viewDataset.html")


# @app.route('/admin/searchImages')
# def searchImages():
#     return render_template("admin/viewDataset.html")


@app.route('/admin/searchComplain')
def adminSearchComplain():
    return render_template("admin/viewComplain.html")


@app.route('/admin/searchFeedback')
def adminSearchFeedback():
    return render_template("admin/viewFeedback.html")