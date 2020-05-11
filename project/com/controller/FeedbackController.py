from datetime import date, datetime

from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO

UPLOAD_FOLDER = 'project/static/adminResource/attachment/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/user/loadFeedback', methods=['GET'])
def userLoadFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()
            feedbackFrom_loginId = session['session_loginId']
            feedbackVO.feedbackFrom_loginId = feedbackFrom_loginId
            feedbackVOList = feedbackDAO.viewFeedback(feedbackVO)
            print("__________________", feedbackVOList)
            return render_template('user/addFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST'])
def userInsertFeedback():
    try:
        if adminLoginSession() == 'user':

            feedbackSubject = request.form['feedbackSubject']
            feedbackDescription = request.form['feedbackDescription']
            feedbackRating = request.form['rate']
            feedbackFrom_loginId = session['session_loginId']

            feedbackDate = date.today()
            print(feedbackDate)
            feedbackTime = datetime.now().strftime("%H:%M:%S")
            print(feedbackTime)

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackSubject = feedbackSubject
            feedbackVO.feedbackDescription = feedbackDescription
            feedbackVO.feedbackRating = feedbackRating
            feedbackVO.feedbackDate = feedbackDate
            feedbackVO.feedbackTime = feedbackTime
            feedbackVO.feedbackFrom_loginId = feedbackFrom_loginId
            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('userLoadFeedback'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/user/deleteFeedback', methods=['GET'])
def userDeleteFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()
            feedbackId = request.args.get('feedbackId')
            feedbackVO.feedbackId = feedbackId
            feedbackDAO.deleteFeedback(feedbackVO)

            return redirect(url_for('userLoadFeedback'))
        else:
            return redirect(url_for('adminLogoutSession'))

    except Exception as ex:
        print(ex)


@app.route('/admin/searchFeedback', methods=['GET'])
def adminViewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVOList = feedbackDAO.searchFeedback()
            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)


@app.route('/admin/reviewFeedback', methods=['GET'])
def adminReviewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackId = request.args.get('feedbackId')
            feedbackTo_loginId = session['session_loginId']

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_loginId = feedbackTo_loginId

            feedbackDAO.reviewFeedback(feedbackVO)
            # if feedbackTo_loginId in session:
            #     return "Reviewed"
            # else:
            return redirect(url_for('adminViewFeedback'))
        else:
            return redirect(url_for('adminLogoutSession'))
    except Exception as ex:
        print(ex)
