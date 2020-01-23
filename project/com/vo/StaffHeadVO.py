from project import db
from project.com.vo.ZoneVO import ZoneVO
from project.com.vo.WardVO import WardVO


class StaffHeadVO(db.Model):
    __tablename__ = 'staffheadmaster'
    staffheadId = db.Column('staffheadId', db.Integer, primary_key=True, autoincrement=True)
    staffheadName = db.Column('staffheadName', db.String(100), nullable=False)
    staffheadContact = db.Column('staffheadContact', db.String(100), nullable=False)
    staffheadEmail = db.Column('staffheadEmail', db.String(100), nullable=False)
    staffhead_ZoneId = db.Column('staffhead_ZoneId', db.Integer, db.ForeignKey(ZoneVO.zoneId))
    staffhead_WardId = db.Column('staffhead_WardId', db.Integer, db.ForeignKey(WardVO.wardId))


    def as_dict(self):
        return {
            'staffheadId': self.staffheadId,
            'staffheadName': self.staffheadName,
            'staffheadContact': self.staffheadContact,
            'staffheadEmail': self.staffheadEmail,
            'staffhead_ZoneId': self.staffhead_ZoneId,
            'staffhead_WardId': self.staffhead_WardId
        }


db.create_all()
