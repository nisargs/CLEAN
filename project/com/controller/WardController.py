from flask import request, render_template, redirect, url_for
from project import app
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.dao.WardDAO import WardDAO
from project.com.vo.WardVO import WardVO


@app.route('/admin/loadWard', methods=['GET'])
def adminLoadWard():

    try:
        zoneDAO = ZoneDAO()
        zoneVOList = zoneDAO.viewZone()
        return render_template('admin/addWard.html', zoneVOList=zoneVOList)

    except Exception as ex:
        print(ex)


@app.route('/admin/insertWard', methods=['POST'])
def adminInsertWard():
    try:

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

    except Exception as ex:
        print(ex)


@app.route('/admin/searchWard', methods=['GET'])
def adminViewWard():

    try:
        wardDAO = WardDAO()
        wardVOList = wardDAO.viewWard()
        return render_template('admin/viewWard.html', wardVOList=wardVOList)

    except Exception as ex:
        print(ex)

@app.route('/admin/deleteWard', methods=['GET'])
def adminDeleteWard():
    try:
        wardVO=WardVO()
        wardDAO = WardDAO()

        wardId = request.args.get('wardId')

        wardVO.wardId = wardId

        wardDAO.deleteWard(wardVO)

        return redirect(url_for('adminViewWard'))
    except Exception as ex:
        print(ex)

@app.route('/admin/editWard', methods=['GET'])

def adminEditWard():

    try:
        wardVO = WardVO()

        wardDAO = WardDAO()

        zoneDAO = ZoneDAO()

        wardId = request.args.get('wardId')

        wardVO.wardId = wardId

        wardVOList = wardDAO.editWard(wardVO)

        zoneVOList = zoneDAO.viewZone()

        return render_template('admin/editWard.html', zoneVOList=zoneVOList, wardVOList=wardVOList)
    except Exception as ex:
        print(ex)

@app.route('/admin/updateWard', methods=['POST'])
def adminUpdateWard():
    try:
        wardId = request.form['wardId']
        wardName = request.form['wardName']
        wardDescription = request.form['wardDescription']
        ward_ZoneId = request.form['ward_ZoneId']
        print(ward_ZoneId,'......')
        wardVO = WardVO()
        wardDAO = WardDAO()

        wardVO.wardId = wardId
        wardVO.wardName = wardName
        wardVO.wardDescription = wardDescription
        wardVO.ward_ZoneId = ward_ZoneId

        wardDAO.updateWard(wardVO)

        return redirect(url_for('adminViewWard'))
    except Exception as ex:
        print(ex)