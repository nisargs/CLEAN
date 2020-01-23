from project import db
from project.com.vo.ZoneVO import ZoneVO


class WardVO(db.Model):
    __tablename__ = 'wardmaster'
    wardId = db.Column('wardId', db.Integer, primary_key=True, autoincrement=True)
    wardName = db.Column('wardName', db.String(100), nullable=False)
    wardDescription = db.Column('wardDescription', db.String(100), nullable=False)
    ward_ZoneId = db.Column('ward_ZoneId', db.Integer, db.ForeignKey(ZoneVO.zoneId))

    def as_dict(self):
        return {
            'wardId': self.wardId,
            'wardName': self.wardName,
            'wardDescription': self.wardDescription,
            'ward_ZoneId': self.ward_ZoneId
        }


db.create_all()