from project import db
from project.com.vo.UserFileVO import UserFileVO


class UserFileDAO:

    def insertUserFile(self, userfileVO):
        db.session.add(userfileVO)
        db.session.commit()

    def viewUserFile(self):
        userfileList = UserFileVO.query.all()

        return userfileList

    def deleteUserFile(self, userfileVO):
        userfileList = UserFileVO.query.get(userfileVO.userfileId)

        db.session.delete(userfileList)

        db.session.commit()
        return userfileList
