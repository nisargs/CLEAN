from project import db
#from project.com.controller.LoginController import LoginVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.WardVO import WardVO
from project.com.vo.ZoneVO import ZoneVO


class RegisterDAO:
    def insertRegister(self, registerVO):
        db.session.add(registerVO)
        db.session.commit()

    def searchUser(self):
        userList = db.session.query(RegisterVO, LoginVO, ZoneVO, WardVO).join(LoginVO, RegisterVO.register_LoginId == LoginVO.loginId).join(
            ZoneVO, RegisterVO.register_ZoneId == ZoneVO.zoneId).join(WardVO, RegisterVO.register_WardId == WardVO.wardId)
        return userList

    def totalUser(self):
        userList=RegisterVO.query.all()
        return userList


