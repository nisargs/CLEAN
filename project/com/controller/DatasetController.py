from flask import request, render_template, redirect, url_for
from project import app
from werkzeug.utils import secure_filename
import os
from project.com.dao.DatasetDAO import DatasetDAO
from project.com.vo.DatasetVO import DatasetVO
from datetime import date, datetime

UPLOAD_FOLDER = 'project/static/adminResource/dataset/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/admin/loadDataset', methods=['GET'])
def adminLoadDataset():
    try:
        return render_template('admin/addDataset.html')
    except Exception as ex:
        print(ex)


@app.route('/admin/insertDataset', methods=['POST'])
def adminInsertDataset():
    try:
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        datasetVO = DatasetVO()
        datasetDAO = DatasetDAO()

        file = request.files['datasetFileName']
        print(file)

        datasetFilename = secure_filename(file.filename)
        print(datasetFilename)

        datasetFilepath = os.path.join(app.config['UPLOAD_FOLDER'])
        print(datasetFilepath)

        file.save(os.path.join(datasetFilepath, datasetFilename))

        datasetUploaddate = date.today()
        print(datasetUploaddate)

        datasetUploadtime = datetime.now().strftime("%H:%M:%S")
        print(datasetUploadtime)

        datasetVO.datasetFilename = datasetFilename
        datasetVO.datasetFilepath = datasetFilepath.replace('project', '..')
        datasetVO.datasetUploaddate = datasetUploaddate
        datasetVO.datasetUploadtime = datasetUploadtime

        datasetDAO.insertDataset(datasetVO)

        return redirect(url_for('adminSearchDataset'))
    except Exception as ex:
        print(ex)


@app.route('/admin/searchDataset', methods=['GET'])
def adminSearchDataset():
    try:
        datasetDAO = DatasetDAO()
        datasetVOList = datasetDAO.viewDataset()
        return render_template('admin/viewDataset.html', datasetVOList=datasetVOList)
    except Exception as ex:
        print(ex)


@app.route('/admin/deleteDataset', methods=['GET'])
def adminDeleteDataset():
    try:
        datasetVO = DatasetVO()
        datasetDAO = DatasetDAO()

        datasetId = request.args.get('datasetId')

        datasetVO.datasetId = datasetId

        datasetDAO.deleteDataset(datasetVO)

        return redirect(url_for('adminViewDataset'))
    except Exception as ex:
        print(ex)
