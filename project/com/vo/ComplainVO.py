from project import db


class ComplainVO(db.Model):
    __tablename__ = 'complainmaster'
    complainId = db.Column('complainId', db.Integer, primary_key=True, autoincrement=True)
    complainSubject = db.Column('complainSubject', db.String(100))
    complainDescription = db.Column('complainDescription', db.String(500))
    complainDate = db.Column('complainDate', db.Date)
    complainTime = db.Column('complainTime', db.Time)
    complainStatus = db.Column('complainStatus', db.String(100))
    complainFilename = db.Column('complainFilename', db.String(100))
    complainFilepath = db.Column('complainFilepath', db.String(100))
    complainTo_loginId = db.Column('complainTo_loginId', db.Integer, nullable=True)
    complainFrom_loginId = db.Column('complainFrom_loginId', db.Integer, nullable=False)
    replySubject = db.Column('replySubject', db.String(100))
    replyMessage = db.Column('replyMessage', db.String(500))
    replyFilename = db.Column('replyFilename', db.String(100))
    replyFilepath = db.Column('replyFilepath', db.String(100))
    replyDate = db.Column('replyDate', db.Date)
    replyTime = db.Column('replyTime', db.Time)

    def as_dict(self):
        return {
            'complainId': self.complainId,
            'complainSubject': self.complainSubject,
            'complainDescription': self.complainDescription,
            'complainDate': self.complainDate,
            'complainTime': self.complainTime,
            'complainStatus': self.complainStatus,
            'complainFilename': self.complainFilename,
            'complainFilepath': self.complainFilepath,
            'complainTo_loginId': self.complainTo_loginId,
            'complainFrom_loginId': self.complainFrom_loginId,
            'replySubject': self.replySubject,
            'replyMessage': self.replyMessage,
            'replyFilename': self.replyFilename,
            'replyFilepath': self.replyFilepath,
            'replyDate': self.replyDate,
            'replyTime': self.replyTime
        }


db.create_all()
