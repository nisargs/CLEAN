import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, jsonify

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.dao.WardDAO import WardDAO
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.WardVO import WardVO


@app.route('/user/loadRegister', methods=['GET'])
def userLoadRegister():
    try:
        zoneDAO = ZoneDAO()
        zoneVOList = zoneDAO.viewZone()
        wardDAO = WardDAO()
        wardVOList = wardDAO.viewWard()
        return render_template("user/register.html", zoneVOList=zoneVOList, wardVOList=wardVOList)
    except Exception as ex:
        print(ex)


@app.route('/user/insertRegister', methods=['POST'])
def userInsertRegister():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        registerVO = RegisterVO()
        registerDAO = RegisterDAO()

        loginUsername = request.form['loginUsername']
        registerFirstName = request.form['registerFirstName']
        registerLastName = request.form['registerLastName']
        registerGender = request.form['registerGender']
        register_ZoneId = request.form['register_ZoneId']
        register_WardId = request.form['register_WardId']
        registerAddress = request.form['registerAddress']
        registerContact = request.form['registerContact']

        loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

        print("loginPassword=" + loginPassword)

        sender = "cleanyourstreet@gmail.com"

        receiver = loginUsername

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "CLEAN LOGIN PASSWORD"

        email_template = """\
        <html>
        <body style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; line-height: 1.6em; margin: 0;" bgcolor="#f7f0f0">

<table class="body-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; width: 100%;  margin: 0;">
	<tbody>
		<tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; margin: 0;">
			<td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
			<td class="container" width="600" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; vertical-align: top; display: block !important; max-width: 600px !important; clear: both !important; margin: 0 auto;" valign="top">
				<div class="content" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; max-width: 600px; display: block; margin: 0 auto; padding: 20px;">
					<table class="main" width="100%" cellpadding="0" cellspacing="0" itemprop="action" itemscope="" itemtype="http://schema.org/ConfirmAction" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px;  margin: 0; border: none;">
						<tbody><tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; margin: 0;">
							<td class="content-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; vertical-align: top; margin: 0;padding: 30px;border: 3px solid #4c7ff0; background-color: #fff;" valign="top">
								<meta itemprop="name" content="Confirm Email" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; margin: 0;">
										<img src="https://drive.google.com/uc?export=view&id=1cAsLtAM79VetlH565wgp-fNPk5z9q9Mh" style="width: 31%;position: relative; left: 165px;"><br>
										<hr>
								<table width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; margin: 0;">
									<tbody>
										<tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; margin: 0;">
											<td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
												Hi <b>{registerFirstName}</b><br>
												Thanks for registering on CLEAN!<br>
												The below is your password to login to your CLEAN Account.
											</td>
										</tr>
										<tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; margin: 0;">
											<td>Password: <b>{loginPassword}</b>
                                            </td>
										</tr>
										<tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; margin: 0;">
											<td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
												Link to our website https://github.com/nisargs/CLEAN<br>
												Thanks!
											</td>
										</tr>
										<tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; margin: 0;">
											<td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
												<b>CLEAN</b>
											</td>
										</tr>
									</tbody>
								</table>
							</td>
						</tr>
					</tbody></table>

				</div>
			</td>
			<td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
		</tr>
	</tbody>
</table>


</body>
        </html>
        """.format(loginPassword=loginPassword, registerFirstName=registerFirstName)

        # password_send = loginPassword

        # part1= MIMEText(password_send, "plain")
        part2 = MIMEText(email_template, "html")
        # msg.attach(part1)
        msg.attach(part2)
        # msg.attach(MIMEText(loginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(sender, "CLEAN12345")

        text = msg.as_string()

        server.sendmail(sender, receiver, text)

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "user"
        loginVO.loginStatus = "active"

        loginDAO.insertLogin(loginVO)

        registerVO.registerFirstName = registerFirstName
        registerVO.registerLastName = registerLastName
        registerVO.registerGender = registerGender
        registerVO.register_ZoneId = register_ZoneId
        registerVO.register_WardId = register_WardId
        registerVO.registerAddress = registerAddress
        registerVO.registerContact = registerContact
        registerVO.register_LoginId = loginVO.loginId

        registerDAO.insertRegister(registerVO)

        server.quit()

        return render_template("admin/login.html")
    except Exception as ex:
        print(ex)


@app.route('/admin/searchUser', methods=['GET'])
def adminSearchUser():
    try:

        if adminLoginSession() == 'admin':

            registerDAO = RegisterDAO()
            registerVOList = registerDAO.searchUser()
            print("__________________", registerVOList)
            return render_template('admin/viewUser.html', registerVOList=registerVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxLoadWard', methods=['GET'])
def adminAjaxLoadWard():
    try:
        register_ZoneId = request.args.get('register_ZoneId')

        wardVO = WardVO()
        wardDAO = WardDAO()
        wardVO.ward_ZoneId = register_ZoneId
        wardList = wardDAO.getWardList(wardVO)

        print("wardList >>>>>>>>>>>>>>>>>> ", wardList)

        wardDictList = [i.as_dict() for i in wardList]

        return jsonify(wardDictList)

    except Exception as ex:
        print(ex)
