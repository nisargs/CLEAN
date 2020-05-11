import os
from datetime import date, datetime
from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO


@app.route('/user/loadComplain')
def userLoadComplain():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainFrom_loginId = session['session_loginId']
            complainVO.complainFrom_loginId = complainFrom_loginId
            complainVOList = complainDAO.userViewComplain(complainVO)
            print("__________________", complainVOList)
            return render_template('user/addComplain.html', complainVOList=complainVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession() == 'user':
            UPLOAD_FOLDER = 'project/static/adminResource/complainAttachment/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainSubject = request.form['complainSubject']
            complainDescription = request.form['complainDescription']
            print("desc: ", complainDescription)

            complainStatus = 'Pending'

            file = request.files['complainFilename']
            complainFilename = secure_filename(file.filename)
            print("complain file name:", complainFilename)

            complainFilepath = os.path.join(app.config['UPLOAD_FOLDER'])
            print("complain file path:", complainFilepath)

            file.save(os.path.join(complainFilepath, complainFilename))

            complainDate = date.today()
            print(complainDate)
            complainTime = datetime.now().strftime("%H:%M:%S")
            print(complainTime)

            complainFrom_loginId = session['session_loginId']

            complainVO.complainSubject = complainSubject
            complainVO.complainDescription = complainDescription
            complainVO.complainDate = complainDate
            complainVO.complainTime = complainTime
            complainVO.complainStatus = complainStatus
            complainVO.complainFilename = complainFilename
            complainVO.complainFilepath = complainFilepath.replace('project', '..')
            complainVO.complainFrom_loginId = complainFrom_loginId
            complainDAO.insertComplain(complainVO)

            return redirect(url_for('userLoadComplain'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            complainVOList = complainDAO.userDeleteComplain(complainVO)

            complainFilename = complainVOList.complainFilename
            complainFilepath = complainVOList.complainFilepath
            complainStatus = complainVOList.complainStatus

            complainFullPath = complainFilepath.replace('..', 'project') + complainFilename
            os.remove(complainFullPath)

            if complainStatus == 'Replied':
                replyFilename = complainVOList.replyFilename
                replyFilepath = complainVOList.replyFilepath

                replyFullPath = replyFilepath.replace('..', 'project') + replyFilename
                os.remove(replyFullPath)

            else:
                print("Your complain status is still pending")

            return redirect(url_for('userLoadComplain'))
        else:
            return redirect(url_for('adminLogoutSession'))

    except Exception as ex:
        print(ex)


@app.route('/admin/searchComplain', methods=['GET'])
def adminViewComplain():
    try:
        if adminLoginSession() == 'admin':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainVO.complainStatus = 'Pending'
            complainVOList = complainDAO.adminViewComplain(complainVO)
            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply', methods=['GET'])
def adminLoadComplainReply():
    try:
        if adminLoginSession() == 'admin':
            complainId = request.args.get('complainId')
            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplainReply():
    try:
        if adminLoginSession() == 'admin':
            UPLOAD_FOLDER = 'project/static/adminResource/replyAttachment/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']
            complainStatus = 'Replied'

            complainFilepath = os.path.join(app.config['UPLOAD_FOLDER'])
            print("complain file path:", complainFilepath)

            file = request.files['replyFilename']
            replyFilename = secure_filename(file.filename)
            replyFilepath = os.path.join(app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(replyFilepath, replyFilename))

            replyDate = date.today()
            replyTime = datetime.now().strftime("%H:%M:%S")

            complainTo_loginId = session['session_loginId']

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFilename = replyFilename
            complainVO.replyFilepath = replyFilepath.replace('project', '..')
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainStatus = complainStatus
            complainVO.complainTo_loginId = complainTo_loginId

            complainDAO.adminInsertComplainReply(complainVO)

            return redirect(url_for('adminViewComplain'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route("/user/viewComplainReply", methods=['GET'])
def userViewComplainReplay():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainId = request.args.get('complainId')
            complainVO.complainId = complainId
            complainVOList = complainDAO.userViewComplainReply(complainVO)
            return render_template("user/viewComplainReply.html", complainVOList=complainVOList)
        else:
            return redirect(url_for('adminLogoutSession'))

    except Exception as ex:
        print(ex)
