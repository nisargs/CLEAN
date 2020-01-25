from project import db
from project.com.vo.DatasetVO import DatasetVO


class DatasetDAO:

    def insertDataset(self, datasetVO):
        db.session.add(datasetVO)
        db.session.commit()

    def viewDataset(self):
        datasetList=DatasetVO.query.all()

        return datasetList

    def deleteDataset(self,datasetVO):

        datasetList = DatasetVO.query.get(datasetVO.datasetId)

        db.session.delete(datasetList)

        db.session.commit()

    # def editDataset(self,datasetVO):
    #
    #     # datasetList = DatasetVO.query.get(datasetVO.datasetId)
    #
    #     # datasetList = DatasetVO.query.filter_by(datasetId=datasetVO.datasetId)
    #
    #     datasetList = DatasetVO.query.filter_by(datasetId=datasetVO.datasetId).all()
    #
    #     return datasetList

    # def updateDataset(self,datasetVO):
    #
    #     db.session.merge(datasetVO)
    #
    #     db.session.commit()