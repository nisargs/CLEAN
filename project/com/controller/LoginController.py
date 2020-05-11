import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.dao.ImageDAO import ImageDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.LoginVO import LoginVO


@app.route('/')
def adminLoadLogin():
    try:
        print("in login")
        session.clear()
        return render_template('admin/login.html')
    except Exception as ex:
        print(ex)


@app.route("/admin/validateLogin", methods=['POST'])
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginStatus = "active"

        loginVOList = loginDAO.validateLogin(loginVO)

        loginDictList = [i.as_dict() for i in loginVOList]

        print(loginDictList)

        lenLoginDictList = len(loginDictList)

        if lenLoginDictList == 0:

            msg = 'Username Or Password is Incorrect !'

            return render_template('admin/login.html', msg=msg)

        elif loginDictList[0]['loginStatus'] == 'inactive':
            msg = 'You are temporarily blocked by admin!'
            return render_template('admin/login.html', msg=msg)

        else:

            for row1 in loginDictList:

                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                loginRole = row1['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect(url_for('adminLoadDashboard'))
                elif loginRole == 'user':
                    return redirect(url_for('userLoadDashboard'))

    except Exception as ex:
        print(ex)


@app.route('/admin/loadDashboard', methods=['GET'])
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            userList = registerDAO.totalUser()
            totalUser = len(userList)
            print(totalUser)

            complainDAO = ComplainDAO()
            complainList = complainDAO.totalComplain()
            totalComplain = len(complainList)
            print(totalComplain)

            complainVO = ComplainVO()
            complainVO.complainStatus = 'Pending'
            pendingList = complainDAO.adminViewComplain(complainVO)
            totalPending = len(pendingList)
            print(totalPending)

            feedbackDAO = FeedbackDAO()
            feedbackList = feedbackDAO.totalFeedback()
            totalFeedback = len(feedbackList)
            print(totalFeedback)

            imageDAO = ImageDAO()
            imageList = imageDAO.totalImage()
            totalImage = len(imageList)
            print(totalImage)
            registerVOList = registerDAO.searchUser()

            imageDAO = ImageDAO()
            userList = imageDAO.getUniqueUsers()
            print("userList >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ", userList)

            return render_template('admin/index.html', registerVOList=registerVOList, totalComplain=totalComplain,
                                   totalFeedback=totalFeedback, totalUser=totalUser, totalImage=totalImage,
                                   userList=userList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/loadDashboard')
def userLoadDashboard():
    try:
        return render_template("user/index.html")
    except Exception as ex:
        print(ex)


@app.route("/admin/loadForgotPassword")
def adminForgotPassword():
    try:
        return render_template("user/forgotPassword.html")
    except Exception as ex:
        print(ex)


@app.route("/admin/generateOTP", methods=["post"])
def adminGenerateOTP():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()

        loginUsername = request.form['loginUsername']

        loginVO.loginUsername = loginUsername
        loginVO.loginRole = "user"

        loginVOList = loginDAO.validateLoginUsername(loginVO)
        print("loginVOList >>>>>>>>>>>>>>>>>>> ", loginVOList)

        loginDictList = [i.as_dict() for i in loginVOList]
        lenLoginDictList = len(loginDictList)

        session["session_loginUsername"] = loginDictList[0]['loginUsername']
        session["session_loginId"] = loginDictList[0]['loginId']

        if lenLoginDictList == 0:
            msg = "Please enter valid email address !"
            return render_template("user/forgotPassword.html", msg=msg)

        else:
            otp = ''.join((random.choice(string.digits)) for x in range(4))
            session["session_otp"] = otp

            sender = "cleanyourstreet@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "Reset Password"

            msg.attach(MIMEText(otp, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "CLEAN12345")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)

            server.quit()

            return render_template("user/addOTP.html")

    except Exception as ex:
        print(ex)


@app.route("/admin/validateOTP", methods=['post'])
def adminValidateOtp():
    try:
        loginOtp = request.form["loginOTP"]

        loginUsername = session['session_loginUsername']
        if session["session_otp"] == loginOtp:
            loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            print("loginPassword=" + loginPassword)

            sender = "cleanyourstreet@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['Subject'] = "NEW PASSWORD"

            msg.attach(MIMEText(loginPassword, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login(sender, "CLEAN12345")

            text = msg.as_string()

            server.sendmail(sender, receiver, text)
            server.quit()

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginId = session['session_loginId']
            loginVO.loginPassword = loginPassword
            loginDAO.loginUpdateUser(loginVO)

            return render_template("admin/login.html")
        else:
            msg = "Please enter correct OTP sent to you!"
            return render_template("user/addOTP.html", error=msg)
    except Exception as ex:
        print(ex)


@app.route('/admin/loginSession')
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:
            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")
            if session['session_loginRole'] == 'admin':

                return 'admin'

            elif session['session_loginRole'] == 'user':

                return 'user'

            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")

        else:

            print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")

            return False
    except Exception as ex:
        print(ex)


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    try:
        session.clear()
        return redirect(url_for('adminLoadLogin'))

    except Exception as ex:
        print(ex)


@app.route("/admin/userBlock", methods=['GET'])
def adminUserBlock():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()

        loginId = request.args.get('loginId')
        loginVO.loginId = loginId

        loginVO.loginStatus = 'inactive'
        loginDAO.userBlock(loginVO)

        return redirect(url_for('adminSearchUser'))
    except Exception as ex:
        print(ex)


@app.route("/admin/userUnblock", methods=['GET'])
def adminUserUnblock():
    try:

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginId = request.args.get('loginId')
        loginVO.loginId = loginId

        loginVO.loginStatus = 'active'
        loginDAO.userBlock(loginVO)

        return redirect(url_for('adminSearchUser'))
    except Exception as ex:
        print(ex)
