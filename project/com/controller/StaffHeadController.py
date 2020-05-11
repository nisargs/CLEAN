from flask import request, render_template, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.StaffHeadDAO import StaffHeadDAO
from project.com.dao.WardDAO import WardDAO
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.vo.StaffHeadVO import StaffHeadVO


@app.route('/admin/loadStaffHead', methods=['GET'])
def adminStaffHead():
    try:
        if adminLoginSession() == 'admin':
            zoneDAO = ZoneDAO()
            zoneVOList = zoneDAO.viewZone()
            wardDAO = WardDAO()
            wardVOList = wardDAO.viewWard()
            return render_template('admin/addStaffHead.html', zoneVOList=zoneVOList, wardVOList=wardVOList)
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/insertStaffHead', methods=['POST'])
def adminInsertStaffHead():
    try:
        if adminLoginSession() == 'admin':
            staffheadName = request.form['staffheadName']
            staffheadContact = request.form['staffheadContact']
            staffheadEmail = request.form['staffheadEmail']
            staffhead_ZoneId = request.form['staffhead_ZoneId']
            staffhead_WardId = request.form['staffhead_WardId']

            staffheadVO = StaffHeadVO()
            staffheadDAO = StaffHeadDAO()

            staffheadVO.staffheadName = staffheadName
            staffheadVO.staffheadContact = staffheadContact
            staffheadVO.staffheadEmail = staffheadEmail
            staffheadVO.staffhead_ZoneId = staffhead_ZoneId
            staffheadVO.staffhead_WardId = staffhead_WardId

            staffheadDAO.insertStaffHead(staffheadVO)

            return redirect(url_for('adminViewStaffHead'))
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/searchStaffHead', methods=['GET'])
def adminViewStaffHead():
    try:
        if adminLoginSession() == 'admin':
            staffheadDAO = StaffHeadDAO()
            staffheadVOList = staffheadDAO.viewStaffHead()
            return render_template('admin/viewStaffHead.html', staffheadVOList=staffheadVOList)
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteStaffHead', methods=['GET'])
def adminDeleteStaffHead():
    try:
        if adminLoginSession() == 'admin':
            staffheadVO = StaffHeadVO()
            staffheadDAO = StaffHeadDAO()

            staffheadId = request.args.get('staffheadId')

            staffheadVO.staffheadId = staffheadId

            staffheadDAO.deleteStaffHead(staffheadVO)

            return redirect(url_for('adminViewStaffHead'))
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/editStaffHead', methods=['GET'])
def adminEditStaffHead():
    try:
        if adminLoginSession() == 'admin':
            staffheadVO = StaffHeadVO()
            staffheadDAO = StaffHeadDAO()
            wardDAO = WardDAO()
            zoneDAO = ZoneDAO()

            staffheadId = request.args.get('staffheadId')
            staffheadVO.staffheadId = staffheadId

            staffheadVOList = staffheadDAO.editStaffHead(staffheadVO)
            zoneVOList = zoneDAO.viewZone()
            wardVOList = wardDAO.viewWard()

            return render_template('admin/editStaffHead.html', zoneVOList=zoneVOList, wardVOList=wardVOList,
                                   staffheadVOList=staffheadVOList)
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)


@app.route('/admin/updateStaffHead', methods=['POST'])
def adminUpdateStaffHead():
    try:
        if adminLoginSession() == 'admin':
            staffheadId = request.form['staffheadId']
            staffheadName = request.form['staffheadName']
            staffheadContact = request.form['staffheadContact']
            staffheadEmail = request.form['staffheadEmail']
            staffhead_ZoneId = request.form['staffhead_ZoneId']
            staffhead_WardId = request.form['staffhead_WardId']

            staffheadVO = StaffHeadVO()
            staffheadDAO = StaffHeadDAO()

            staffheadVO.staffheadId = staffheadId
            staffheadVO.staffheadName = staffheadName
            staffheadVO.staffheadContact = staffheadContact
            staffheadVO.staffheadEmail = staffheadEmail
            staffheadVO.staffhead_ZoneId = staffhead_ZoneId
            staffheadVO.staffhead_WardId = staffhead_WardId

            staffheadDAO.updateStaffHead(staffheadVO)

            return redirect(url_for('adminViewStaffHead'))
        else:
            return redirect(url_for('adminLoadDashboard'))
    except Exception as ex:
        print(ex)
