from project import db
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.LoginVO import LoginVO


class ComplainDAO:
    def insertComplain(self, complainVO):
        db.session.add(complainVO)
        db.session.commit()

    def viewComplain(self):
        complainList = db.session.query(ComplainVO, LoginVO).join(LoginVO,
                                                                  ComplainVO.complainFrom_loginId == LoginVO.loginId).all()
        return complainList

    def userDeleteComplain(self, complainVO):
        complainList = ComplainVO.query.get(complainVO.complainId)
        db.session.delete(complainList)
        db.session.commit()
        return complainList

    def adminInsertComplainReply(self, complainVO):
        db.session.merge(complainVO)
        db.session.commit()

    def userViewComplain(self, complainVO):
        complainList = ComplainVO.query.filter_by(complainFrom_loginId=complainVO.complainFrom_loginId).all()
        return complainList

    def adminViewComplain(self, complainVO):
        complainList = db.session.query(ComplainVO, LoginVO).join(LoginVO,
                                                                  ComplainVO.complainFrom_loginId == LoginVO.loginId).filter(
            ComplainVO.complainStatus == complainVO.complainStatus).all()
        return complainList

    def userViewComplainReply(self, complainVO):
        complainList = ComplainVO.query.filter_by(complainId=complainVO.complainId)
        return complainList

    def totalComplain(self):
        complainList=ComplainVO.query.all()
        return complainList
