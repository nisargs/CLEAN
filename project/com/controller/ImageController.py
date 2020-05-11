import os
import smtplib
from datetime import date, datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import cv2
import imutils
import numpy as np
from flask import request, render_template, redirect, url_for, session, jsonify
from keras.models import load_model
# import the necessary packages
from keras.preprocessing.image import img_to_array
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.ImageDAO import ImageDAO
from project.com.dao.StaffHeadDAO import StaffHeadDAO
from project.com.dao.WardDAO import WardDAO
from project.com.dao.ZoneDAO import ZoneDAO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.StaffHeadVO import StaffHeadVO
from project.com.vo.WardVO import WardVO
from project.com.vo.ZoneVO import ZoneVO

UPLOAD_INPUTFOLDER = 'project/static/adminResource/input/'
app.config['UPLOAD_INPUTFOLDER'] = UPLOAD_INPUTFOLDER

UPLOAD_OUTPUTFOLDER = 'project/static/adminResource/output/'
app.config['UPLOAD_OUTPUTFOLDER'] = UPLOAD_OUTPUTFOLDER


@app.route('/user/loadImage', methods=['GET'])
def userLoadImage():
    try:
        if adminLoginSession() == 'user':
            zoneDAO = ZoneDAO()
            zoneVOList = zoneDAO.viewZone()

            wardDAO = WardDAO()
            wardVOList = wardDAO.viewWard()

            print('zoneVOList>>>>', zoneVOList)
            print('wardVOList>>>>', wardVOList)
            return render_template('user/addImage.html', zoneVOList=zoneVOList, wardVOList=wardVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/insertImage', methods=['POST'])
def userInsertImage():
    try:
        if adminLoginSession() == 'user':
            imageVO = ImageVO()
            imageDAO = ImageDAO()
            wardDAO = WardDAO()
            wardVO = WardVO()
            zoneVO = ZoneVO()
            zoneDAO = ZoneDAO()

            image_ZoneId = request.form['image_ZoneId']
            image_WardId = request.form['image_WardId']
            file = request.files['file']
            print(file)

            zoneName = ''
            wardName = ''

            if image_WardId != 0:
                wardVO.wardId = image_WardId
                wardList = wardDAO.findWardName(wardVO)

                zoneVO.zoneId = image_ZoneId
                zoneList = zoneDAO.getZoneName(zoneVO)

                zoneName = zoneList[0].zoneName
                wardName = wardList[0].wardName

            imageInputFileName = secure_filename(file.filename)
            print(imageInputFileName)

            imageInputFilePath = os.path.join(app.config['UPLOAD_INPUTFOLDER'])
            print(imageInputFilePath)

            currentDate = date.today()
            print(currentDate)

            currentTime = datetime.now().strftime("%H:%M:%S")
            print(currentTime)

            file.save(os.path.join(imageInputFilePath, imageInputFileName))

            # load the image
            inputImage = imageInputFilePath + imageInputFileName

            print("inputImage>>>>>>>", inputImage)

            modelName = r'project/static/adminResource/GarbageModel/Garbage.model'

            imageOutputFileName = imageInputFileName

            imageOutputFilePath = os.path.join(app.config['UPLOAD_OUTPUTFOLDER'])

            image = cv2.imread(inputImage)
            orig = image.copy()

            # pre-process the image for classification
            image = cv2.resize(image, (28, 28))
            image = image.astype("float") / 255.0
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)

            # load the trained  convolutional neural network
            print("[INFO] loading network...")
            model = load_model(modelName)

            # classify the input image
            (notGarbage, garbage) = model.predict(image)[0]

            # build the label
            label = "Garbage" if garbage > notGarbage else "Not Garbage"
            proba = garbage if garbage > notGarbage else notGarbage
            label_proba = "{}: {:.2f}%".format(label, proba * 100)

            staffHeadVO = StaffHeadVO()
            staffHeadDAO = StaffHeadDAO()
            staffHeadVO.staffhead_ZoneId = image_ZoneId
            staffList = staffHeadDAO.getStaffUsername(staffHeadVO)
            print("staffList >>>>>>>>>>>>>>>>>>>>>>>>>>> ", staffList)

            loginUsername = ''
            for i in staffList:
                loginUsername = i.staffheadEmail + ", "

            print("loginUsername >>>>>>>>>>>>>>>>>>>>>>>>>>> ", loginUsername)

            # Email Notification
            # if label == "Garbage":
            #     sender = "cleanyourstreet@gmail.com"
            #
            #     receiver = loginUsername
            #     # elif (zoneName == "East Zone"):
            #     #     receiver = "deepgajjar76@gmail.com"
            #
            #     text_message = "The garbage is detected at {} Ward and {} Zone.".format(wardName, zoneName)
            #
            #     msg = MIMEMultipart()
            #
            #     msg['From'] = sender
            #
            #     msg['To'] = receiver
            #
            #     msg['Subject'] = "Garbage Detected"
            #
            #     filename = imageOutputFilePath + imageOutputFileName
            #     with open(filename, 'rb') as fp:
            #         img = MIMEImage(fp.read())
            #         img.add_header('Content-Disposition', 'attachment', filename=filename)
            #         msg.attach(img)
            #
            #     msg.attach(MIMEText(text_message, 'plain'))
            #
            #     server = smtplib.SMTP('smtp.gmail.com', 587)
            #
            #     server.starttls()
            #
            #     server.login(sender, "CLEAN12345")
            #
            #     text = msg.as_string()
            #
            #     server.sendmail(sender, receiver, text)
            #
            #     server.quit()
            #
            #     print("Mail Sent")
            # draw the label on the image
            output = imutils.resize(orig, width=400)
            cv2.putText(output, label_proba, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)

            outputImage = imageOutputFilePath + imageOutputFileName
            # show the output image
            #cv2.imshow("Output", output)
            cv2.waitKey(0)

            cv2.imwrite(outputImage, output)
            ################### Email Notification ################

            if label == "Garbage":
                sender = "cleanyourstreet@gmail.com"

                receiver = loginUsername

                text_message = "The garbage is detected at {} Ward and {}.".format(wardName, zoneName)

                msg = MIMEMultipart()

                msg['From'] = sender

                msg['To'] = receiver

                msg['Subject'] = "Garbage Detected"

                html_email = """\
                <html>
                    <body style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: none; width: 100% !important; height: 100%; line-height: 1.6em; margin: 0;" bgcolor="#f7f0f0">
            
            <table class="body-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; width: 100%; margin: 0;">
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
                                                            
                                                            The garbage is detected at: <br>
                                                            <b><u>Ward:</u></b> {wardName} <br>
                                                            <b><u>Zone:</u></b> {zoneName}
                                                        </td>
                                                    </tr>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif;  font-size: 14px; margin: 0;">
                                                        <td>Kindly refer to the attached garbage photo.</b>
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
        """.format(wardName=wardName,zoneName=zoneName)

                filename = imageOutputFilePath + imageOutputFileName
                with open(filename, 'rb') as fp:
                    img = MIMEImage(fp.read())
                    img.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(img)

                #msg.attach(MIMEText(text_message, 'plain'))
                msg.attach(MIMEText(html_email, 'html'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "CLEAN12345")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()

                print("Mail Sent")
            imageVO.imageInputFileName = imageInputFileName
            imageVO.imageInputFilePath = imageInputFilePath.replace('project', '..')
            imageVO.imageOutputFileName = imageOutputFileName
            imageVO.imageOutputFilePath = imageOutputFilePath.replace('project', '..')
            imageVO.imageUploadDate = currentDate
            imageVO.imageUploadTime = currentTime
            imageVO.imageLabel = label
            imageVO.image_ZoneId = image_ZoneId
            imageVO.image_WardId = image_WardId
            imageVO.image_LoginId = session['session_loginId']

            imageDAO.insertImage(imageVO)
            return redirect(url_for('userSearchImage'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/searchImage', methods=['GET'])
def userSearchImage():
    try:
        if adminLoginSession() == 'user':
            imageVO = ImageVO()
            imageDAO = ImageDAO()

            imageVO.image_LoginId = session['session_loginId']

            imageVOList = imageDAO.viewImage(imageVO)
            print('imageVOList>>>>>>', imageVOList)

            return render_template('user/viewImage.html', imageVOList=imageVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/searchImage', methods=['GET'])
def adminSearchImage():
    try:
        if adminLoginSession() == 'admin':
            imageDAO = ImageDAO()

            imageVOList = imageDAO.adminViewImage()

            print('imageVOList>>>>>>', imageVOList)
            return render_template('admin/viewImage.html', imageVOList=imageVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/deleteImage', methods=['GET'])
def userDeleteImage():
    try:
        if adminLoginSession() == 'user':
            imageVO = ImageVO()
            imageDAO = ImageDAO()

            userfileId = request.args.get('userfileId')

            imageVO.userfileId = userfileId

            imageVOList = imageDAO.deleteImage(imageVO)

            userfilename = imageVOList.userfilename
            userfilepath = imageVOList.userfilepath

            userfileFullPath = userfilepath.replace('..', 'project') + userfilename
            os.remove(userfileFullPath)
            return redirect(url_for('userSearchImage'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxDateImage', methods=['GET'])
def adminAjaxDateImage():
    try:
        if adminLoginSession() == 'admin':
            image_LoginId = request.args.get('image_LoginId')

            imageVO = ImageVO()
            imageDAO = ImageDAO()
            imageVO.image_LoginId = image_LoginId
            imageDateList = imageDAO.getDateList(imageVO)

            print("imageDateList >>>>>>>>>>>>>>>>>> ", imageDateList)

            ajaxAdminIndexDateList = []
            for i in imageDateList:
                ajaxAdminIndexDateList.append(i[0])

            print("ajaxAdminIndexDateList >>>>>>>>>>>>>>>>>> ", ajaxAdminIndexDateList)
            return jsonify(ajaxAdminIndexDateList)

        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/ajaxGetGraphData')
def adminAjaxGetGraphData():
    image_LoginId = request.args.get('image_LoginId')
    date = request.args.get("date")

    imageVO = ImageVO()
    imageDAO = ImageDAO()

    imageVO.image_LoginId = image_LoginId
    imageVO.imageUploadDate = date

    ajaxGraphDataList = imageDAO.ajaxGetGraphData(imageVO)

    print("ajaxGraphDataList >>>>>>>>>>>>>>>>>> ", ajaxGraphDataList)

    graphDict = {}
    counter = False
    if len(ajaxGraphDataList) != 0:
        counter = True

        dict1 = {}
        for i in ajaxGraphDataList:
            dict1[i[0]] = i[1]

        graphDict.update(dict1)
    print('graphDict>>>', graphDict)
    if counter:
        response = {'responseKey': graphDict}
        print('response>>>>>>>>', response)

    else:
        response = {'responseKey': 'Error'}

    return jsonify(response)
