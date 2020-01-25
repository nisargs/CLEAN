from project import db


class DatasetVO(db.Model):
    __tablename__ = 'datasetmaster'
    datasetId = db.Column('datasetId', db.Integer, primary_key=True, autoincrement=True)
    datasetFilename = db.Column('datasetFilename', db.String(100))
    datasetFilepath = db.Column('datasetFilepath', db.String(100))
    datasetUploaddate = db.Column('datasetUploaddate', db.String(100))
    datasetUploadtime = db.Column('datasetUploadtime', db.String(100))

    def as_dict(self):
        return {
            'datasetId': self.datasetId,
            'datasetFilename': self.datasetFilename,
            'datasetFilepath': self.datasetFilepath,
            'datasetUploaddate': self.datasetUploaddate,
            'datasetUploadtime': self.datasetUploadtime
        }


db.create_all()
