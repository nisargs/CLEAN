from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.vo.ZoneVO import ZoneVO


@app.route('/admin/loadZone', methods=['GET'])
def adminLoadZone():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addZone.html')
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/insertZone', methods=['POST'])
def adminInsertZone():
    try:
        if adminLoginSession() == 'admin':
            zoneName = request.form['zoneName']
            zoneDescription = request.form['zoneDescription']

            zoneVO = ZoneVO()
            zoneDAO = ZoneDAO()

            zoneVO.zoneName = zoneName
            zoneVO.zoneDescription = zoneDescription

            zoneDAO.insertZone(zoneVO)

            return redirect(url_for('adminSearchZone'))
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/searchZone', methods=['GET'])
def adminSearchZone():
    try:
        if adminLoginSession() == 'admin':
            zoneDAO = ZoneDAO()
            zoneVOList = zoneDAO.viewZone()
            print("__________________", zoneVOList)
            return render_template('admin/viewZone.html', zoneVOList=zoneVOList)
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteZone', methods=['GET'])
def adminDeleteZone():
    try:
        if adminLoginSession() == 'admin':
            zoneVO = ZoneVO()

            zoneDAO = ZoneDAO()

            zoneId = request.args.get('zoneId')

            zoneVO.zoneId = zoneId

            zoneDAO.deleteZone(zoneVO)

            return redirect(url_for('adminSearchZone'))
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/editZone', methods=['GET'])
def adminEditZone():
    try:
        if adminLoginSession() == 'admin':
            zoneVO = ZoneVO()

            zoneDAO = ZoneDAO()

            zoneId = request.args.get('zoneId')

            zoneVO.zoneId = zoneId

            zoneVOList = zoneDAO.editZone(zoneVO)

            print("=======zoneVOList=======", zoneVOList)

            print("=======type of zoneVOList=======", type(zoneVOList))

            return render_template('admin/editZone.html', zoneVOList=zoneVOList)
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/updateZone', methods=['POST'])
def adminUpdateZone():
    try:
        if adminLoginSession() == 'admin':
            zoneId = request.form['zoneId']
            zoneName = request.form['zoneName']
            zoneDescription = request.form['zoneDescription']

            zoneVO = ZoneVO()
            zoneDAO = ZoneDAO()

            zoneVO.zoneId = zoneId
            zoneVO.zoneName = zoneName
            zoneVO.zoneDescription = zoneDescription

            zoneDAO.updateZone(zoneVO)

            return redirect(url_for('adminSearchZone'))
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)
