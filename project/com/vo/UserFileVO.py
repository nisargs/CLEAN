from project import db


class UserFileVO(db.Model):
    __tablename__ = 'userfilemaster'
    userfileId = db.Column('userfileId', db.Integer, primary_key=True, autoincrement=True)
    userfilename = db.Column('userfilename', db.String(100))
    userfilepath = db.Column('userfilepath', db.String(100))
    userfileUploaddate = db.Column('userfileUploaddate', db.String(100))
    userfileUploadtime = db.Column('userfileUploadtime', db.String(100))

    def as_dict(self):
        return {
            'userfileId': self.userfileId,
            'userfilename': self.userfilename,
            'userfilepath': self.userfilepath,
            'userfileUploaddate': self.userfileUploaddate,
            'userfileUploadtime': self.userfileUploadtime
        }


db.create_all()
