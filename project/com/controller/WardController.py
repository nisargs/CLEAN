from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.WardDAO import WardDAO
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.vo.WardVO import WardVO


@app.route('/admin/loadWard', methods=['GET'])
def adminLoadWard():
    try:
        if adminLoginSession() == 'admin':
            zoneDAO = ZoneDAO()
            zoneVOList = zoneDAO.viewZone()
            return render_template('admin/addWard.html', zoneVOList=zoneVOList)
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/insertWard', methods=['POST'])
def adminInsertWard():
    try:
        if adminLoginSession() == 'admin':
            wardName = request.form['wardName']
            wardDescription = request.form['wardDescription']
            ward_ZoneId = request.form['ward_ZoneId']

            wardVO = WardVO()
            wardDAO = WardDAO()

            wardVO.wardName = wardName
            wardVO.wardDescription = wardDescription
            wardVO.ward_ZoneId = ward_ZoneId

            wardDAO.insertWard(wardVO)

            return redirect(url_for('adminViewWard'))
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/searchWard', methods=['GET'])
def adminViewWard():
    try:
        if adminLoginSession() == 'admin':
            wardDAO = WardDAO()
            wardVOList = wardDAO.viewWard()
            return render_template('admin/viewWard.html', wardVOList=wardVOList)
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteWard', methods=['GET'])
def adminDeleteWard():
    try:
        if adminLoginSession() == 'admin':
            wardVO = WardVO()
            wardDAO = WardDAO()

            wardId = request.args.get('wardId')

            wardVO.wardId = wardId

            wardDAO.deleteWard(wardVO)

            return redirect(url_for('adminViewWard'))
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/editWard', methods=['GET'])
def adminEditWard():
    try:
        if adminLoginSession() == 'admin':
            wardVO = WardVO()

            wardDAO = WardDAO()

            zoneDAO = ZoneDAO()

            wardId = request.args.get('wardId')

            wardVO.wardId = wardId

            wardVOList = wardDAO.editWard(wardVO)

            zoneVOList = zoneDAO.viewZone()

            return render_template('admin/editWard.html', zoneVOList=zoneVOList, wardVOList=wardVOList)
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/updateWard', methods=['POST'])
def adminUpdateWard():
    try:
        if adminLoginSession() == 'admin':
            wardId = request.form['wardId']
            wardName = request.form['wardName']
            wardDescription = request.form['wardDescription']
            ward_ZoneId = request.form['ward_ZoneId']
            print(ward_ZoneId, '......')
            wardVO = WardVO()
            wardDAO = WardDAO()

            wardVO.wardId = wardId
            wardVO.wardName = wardName
            wardVO.wardDescription = wardDescription
            wardVO.ward_ZoneId = ward_ZoneId

            wardDAO.updateWard(wardVO)

            return redirect(url_for('adminViewWard'))
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)
