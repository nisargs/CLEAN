from project import db
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO


class FeedbackDAO:
    def insertFeedback(self, feedbackVO):
        db.session.add(feedbackVO)
        db.session.commit()

    def viewFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.filter_by(feedbackFrom_loginId=feedbackVO.feedbackFrom_loginId)
        return feedbackList

    def reviewFeedback(self, feedbackVO):
        db.session.merge(feedbackVO)
        db.session.commit()

    def searchFeedback(self):
        feedbackList = db.session.query(FeedbackVO, LoginVO).join(LoginVO,
                                                                  FeedbackVO.feedbackFrom_loginId == LoginVO.loginId).all()
        return feedbackList

    def deleteFeedback(self, feedbackVO):
        feedbackList = FeedbackVO.query.get(feedbackVO.feedbackId)

        db.session.delete(feedbackList)

        db.session.commit()

    def totalFeedback(self):
        feedbackList = FeedbackVO.query.all()
        return feedbackList
