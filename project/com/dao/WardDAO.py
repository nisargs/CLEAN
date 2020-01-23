from project import db
from project.com.vo.WardVO import WardVO
from project.com.vo.ZoneVO import ZoneVO


class WardDAO:

    def insertWard(self, wardVO):
        db.session.add(wardVO)

        db.session.commit()

    def viewWard(self):

        wardList = db.session.query(WardVO, ZoneVO).join(ZoneVO, WardVO.ward_ZoneId == ZoneVO.zoneId).all()

        return wardList

    def deleteWard(self, wardVO):
        wardList = WardVO.query.get(wardVO.wardId)

        print(wardList)

        db.session.delete(wardList)

        db.session.commit()

    def editWard(self, wardVO):
        # wardList = WardVO.query.get(wardVO.wardId)

        # wardList = WardVO.query.filter_by(wardId=wardVO.wardId)

        wardList = WardVO.query.filter_by(wardId=wardVO.wardId)

        return wardList

    def updateWard(self, wardVO):

        db.session.merge(wardVO)

        db.session.commit()

    def ajaxWardProduct(self, wardVO):

        ajaxProductWardList = wardVO.query.filter_by(ward_ZoneId=wardVO.ward_ZoneId).all()

        return ajaxProductWardList
