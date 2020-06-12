from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.WardVO import WardVO
from project.com.vo.ZoneVO import ZoneVO


class RegisterVO(db.Model):
    __tablename__ = 'registermaster'
    registerId = db.Column('registerId', db.Integer, primary_key=True, autoincrement=True)
    registerFirstName = db.Column('registerFirstName', db.String(100), nullable=False)
    registerLastName = db.Column('registerLastName', db.String(100), nullable=False)
    registerGender = db.Column('registerGender', db.String(100), nullable=False)
    register_ZoneId = db.Column('register_ZoneId', db.Integer, db.ForeignKey(ZoneVO.zoneId))
    register_WardId = db.Column('register_WardId', db.Integer, db.ForeignKey(WardVO.wardId))
    registerAddress = db.Column('registerAddress', db.String(100), nullable=False)
    registerContact = db.Column('registerContact', db.String(100), nullable=False)
    register_LoginId = db.Column('register_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'registerId': self.registerId,
            'registerFirstName': self.registerFirstName,
            'registerLastName': self.registerLastName,
            'registerGender': self.registerGender,
            'register_ZoneId': self.register_ZoneId,
            'register_WardId': self.register_WardId,
            'registerAddress': self.registerAddress,
            'registerContact': self.registerContact,
            'register_LoginId': self.register_LoginId
        }


db.create_all()
