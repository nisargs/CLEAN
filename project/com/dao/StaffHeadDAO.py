from project import db
from project.com.vo.StaffHeadVO import StaffHeadVO
from project.com.vo.ZoneVO import ZoneVO
from project.com.vo.WardVO import WardVO


class StaffHeadDAO:

    def insertStaffHead(self, staffheadVO):
        db.session.add(staffheadVO)

        db.session.commit()

    def viewStaffHead(self):

        staffheadList = db.session.query(StaffHeadVO, WardVO, ZoneVO).join(ZoneVO, StaffHeadVO.staffhead_ZoneId == ZoneVO.zoneId).join(WardVO, StaffHeadVO.staffhead_WardId == WardVO.wardId).all()

        return staffheadList

    def deleteStaffHead(self, staffheadVO):
        staffheadList = StaffHeadVO.query.get(staffheadVO.staffheadId)

        print(staffheadList)

        db.session.delete(staffheadList)

        db.session.commit()

    def editStaffHead(self, staffheadVO):
        # staffheadList = StaffHeadVO.query.get(staffheadVO.staffheadId)

        # staffheadList = StaffHeadVO.query.filter_by(staffheadId=staffheadVO.staffheadId)

        staffheadList = StaffHeadVO.query.filter_by(staffheadId=staffheadVO.staffheadId).all()

        return staffheadList

    def updateStaffHead(self, staffheadVO):

        db.session.merge(staffheadVO)

        db.session.commit()

    # def ajaxStaffHeadProduct(self, staffheadVO):
    #
    #     ajaxProductStaffHeadList = staffheadVO.query.filter_by(staffhead_ZoneId=staffheadVO.staffhead_ZoneId).all()
    #
    #     return ajaxProductStaffHeadList
