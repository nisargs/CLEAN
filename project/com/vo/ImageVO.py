from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.WardVO import WardVO
from project.com.vo.ZoneVO import ZoneVO


class ImageVO(db.Model):
    __tablename__ = 'imagemaster'
    imageId = db.Column('imageId', db.Integer, primary_key=True, autoincrement=True)
    imageInputFileName = db.Column('imageInputFileName', db.String(100))
    imageInputFilePath = db.Column('imageInputFilePath', db.String(100))
    imageOutputFileName = db.Column('imageOutputFileName', db.String(100))
    imageOutputFilePath = db.Column('imageOutputFilePath', db.String(100))
    imageUploadDate = db.Column('imageUploadDate', db.String(100))
    imageUploadTime = db.Column('userfileUploadtime', db.String(100))
    imageLabel = db.Column('imageLabel', db.String(100))
    image_ZoneId = db.Column('image_ZoneId', db.Integer, db.ForeignKey(ZoneVO.zoneId))
    image_WardId = db.Column('image_WardId', db.Integer, db.ForeignKey(WardVO.wardId))
    image_LoginId = db.Column('image_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'imageId': self.imageId,
            'imageInputFileName': self.imageInputFileName,
            'imageInputFilePath': self.imageInputFilePath,
            'imageOutputFileName': self.imageOutputFileName,
            'imageOutputFilePath': self.imageOutputFilePath,
            'imageUploadDate': self.imageUploadDate,
            'imageUploadTime': self.imageUploadTime,
            'imageLabel': self.imageLabel,
            'image_ZoneId': self.image_ZoneId,
            'image_WardId': self.image_WardId,
            'image_LoginId': self.image_LoginId

        }


db.create_all()
