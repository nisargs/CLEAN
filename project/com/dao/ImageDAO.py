from sqlalchemy import func

from project import db
from project.com.vo.ImageVO import ImageVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.WardVO import WardVO
from project.com.vo.ZoneVO import ZoneVO


class ImageDAO:

    def insertImage(self, imageVO):
        db.session.add(imageVO)
        db.session.commit()

    def viewImage(self, imageVO):
        imageList = db.session.query(ImageVO, WardVO, ZoneVO) \
            .join(WardVO, ImageVO.image_WardId == WardVO.wardId) \
            .join(ZoneVO, ImageVO.image_ZoneId == ZoneVO.zoneId) \
            .filter(ImageVO.image_LoginId == imageVO.image_LoginId).all()

        return imageList

    def adminViewImage(self):
        imageList = db.session.query(ImageVO, WardVO, ZoneVO, LoginVO) \
            .join(WardVO, ImageVO.image_WardId == WardVO.wardId) \
            .join(ZoneVO, ImageVO.image_ZoneId == ZoneVO.zoneId) \
            .join(LoginVO, ImageVO.image_LoginId == LoginVO.loginId) \
            .all()

        return imageList

    def deleteImage(self, imageVO):
        imageList = ImageVO.query.get(imageVO.userfileId)

        db.session.delete(imageList)

        db.session.commit()
        return imageList

    def totalImage(self):
        imageList = ImageVO.query.all()
        return imageList

    def getUniqueUsers(self):
        userList = db.session.query(ImageVO.image_LoginId, RegisterVO.registerFirstName) \
            .distinct(ImageVO.image_LoginId) \
            .join(RegisterVO, ImageVO.image_LoginId == RegisterVO.register_LoginId).all()
        return userList

    def getDateList(self, imageVO):
        userList = db.session.query(ImageVO.imageUploadDate) \
            .distinct(ImageVO.imageUploadDate) \
            .filter(ImageVO.image_LoginId == imageVO.image_LoginId).all()
        return userList

    def ajaxGetGraphData(self, imageVO):
        userList = db.session.query(ImageVO.imageLabel, func.count(ImageVO.imageLabel)) \
            .filter(ImageVO.image_LoginId == imageVO.image_LoginId) \
            .filter(ImageVO.imageUploadDate == imageVO.imageUploadDate) \
            .group_by(ImageVO.imageLabel).all()
        return userList
