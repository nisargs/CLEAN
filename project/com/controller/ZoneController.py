from flask import request, render_template, redirect, url_for
from project import app
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.vo.ZoneVO import ZoneVO


# @app.route('/')
# def adminLoadDashboard():
#     return render_template('admin/index.html')


@app.route('/admin/loadZone', methods=['GET'])
def adminLoadZone():
    try:
        return render_template('admin/addZone.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertZone', methods=['POST'])
def adminInsertZone():
    try:
        zoneName = request.form['zoneName']
        zoneDescription = request.form['zoneDescription']

        zoneVO = ZoneVO()
        zoneDAO = ZoneDAO()

        zoneVO.zoneName = zoneName
        zoneVO.zoneDescription = zoneDescription

        zoneDAO.insertZone(zoneVO)

        return redirect(url_for('adminSearchZone'))
    except Exception as ex:
        print(ex)


@app.route('/admin/searchZone', methods=['GET'])
def adminSearchZone():
    try:
        zoneDAO = ZoneDAO()
        zoneVOList = zoneDAO.viewZone()
        print("__________________", zoneVOList)
        return render_template('admin/viewZone.html', zoneVOList=zoneVOList)
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteZone', methods=['GET'])
def adminDeleteZone():
    try:
        zoneVO = ZoneVO()

        zoneDAO = ZoneDAO()

        zoneId = request.args.get('zoneId')

        zoneVO.zoneId = zoneId

        zoneDAO.deleteZone(zoneVO)

        return redirect(url_for('adminSearchZone'))
    except Exception as ex:
        print(ex)


@app.route('/admin/editZone', methods=['GET'])
def adminEditZone():
    try:
        zoneVO = ZoneVO()

        zoneDAO = ZoneDAO()

        zoneId = request.args.get('zoneId')

        zoneVO.zoneId = zoneId

        zoneVOList = zoneDAO.editZone(zoneVO)

        print("=======zoneVOList=======", zoneVOList)

        print("=======type of zoneVOList=======", type(zoneVOList))

        return render_template('admin/editZone.html', zoneVOList=zoneVOList)
    except Exception as ex:
        print(ex)


@app.route('/admin/updateZone', methods=['POST'])
def adminUpdateZone():
    try:
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
    except Exception as ex:
        print(ex)