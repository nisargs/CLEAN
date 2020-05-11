import os
from datetime import date, datetime

from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.UserFileDAO import UserFileDAO
from project.com.vo.UserFileVO import UserFileVO

UPLOAD_FOLDER = 'project/static/adminResource/userfile/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/user/loadUserFile', methods=['GET'])
def userLoadUserFile():
    try:
        if adminLoginSession() == 'user':
            return render_template('user/addUserFile.html')
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/insertUserFile', methods=['POST'])
def userInsertUserFile():
    try:
        if adminLoginSession() == 'user':
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            userfileVO = UserFileVO()
            userfileDAO = UserFileDAO()

            file = request.files['userfilename']
            print(file)

            userfilename = secure_filename(file.filename)
            print(userfilename)

            userfilepath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(userfilepath)

            file.save(os.path.join(userfilepath, userfilename))

            userfileUploaddate = date.today()
            print(userfileUploaddate)

            userfileUploadtime = datetime.now().strftime("%H:%M:%S")
            print(userfileUploadtime)

            userfileVO.userfilename = userfilename
            userfileVO.userfilepath = userfilepath.replace('project', '..')
            userfileVO.userfileUploaddate = userfileUploaddate
            userfileVO.userfileUploadtime = userfileUploadtime

            userfileDAO.insertUserFile(userfileVO)

            return redirect(url_for('userSearchUserFile'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/searchUserFile', methods=['GET'])
def userSearchUserFile():
    try:
        if adminLoginSession() == 'user':
            userfileDAO = UserFileDAO()
            userfileVOList = userfileDAO.viewUserFile()
            return render_template('user/viewUserFile.html', userfileVOList=userfileVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/deleteUserFile', methods=['GET'])
def userDeleteUserFile():
    try:
        if adminLoginSession() == 'user':
            userfileVO = UserFileVO()
            userfileDAO = UserFileDAO()

            userfileId = request.args.get('userfileId')

            userfileVO.userfileId = userfileId

            userfileVOList = userfileDAO.deleteUserFile(userfileVO)

            userfilename = userfileVOList.userfilename
            userfilepath = userfileVOList.userfilepath

            userfileFullPath = userfilepath.replace('..', 'project') + userfilename
            os.remove(userfileFullPath)
            return redirect(url_for('userSearchUserFile'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)
