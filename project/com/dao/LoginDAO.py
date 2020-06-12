from project import db
from project.com.vo.LoginVO import LoginVO


class LoginDAO:
    def insertLogin(self, loginVO):
        db.session.add(loginVO)
        db.session.commit()

    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername, loginPassword=loginVO.loginPassword)
        return loginList

    def userBlock(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def validateLoginUsername(self, loginVO):
        loginList = LoginVO.query \
            .filter_by(loginUsername=loginVO.loginUsername, loginRole=loginVO.loginRole).all()

        return loginList

    def loginUpdateUser(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()