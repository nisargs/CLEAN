from project import db


class ZoneVO(db.Model):
    __tablename__ = 'zonemaster'
    zoneId = db.Column('zoneId', db.Integer, primary_key=True, autoincrement=True)
    zoneName = db.Column('zoneName', db.String(100))
    zoneDescription = db.Column('zoneDescription', db.String(100))

    def as_dict(self):
        return {
            'zoneId': self.zoneId,
            'zoneName': self.zoneName,
            'zoneDescription': self.zoneDescription
        }


db.create_all()


