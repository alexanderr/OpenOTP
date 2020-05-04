from otp.util import getPuppetChannel, getAccountChannel


from . import AIRepository

from .AIZoneData import AIZoneData


class DistributedObjectAI:
    QUIET_ZONE = 1
    do_id = None

    def __init__(self, air: AIRepository.AIRepository):
        self.air = air
        self.dclass = air.dcFile.namespace[self.__class__.__name__[:-2]]
        self.zoneId = 0
        self.parentId = 0

        self._zoneData = None

        self.lastLogicalZoneId = 0

    def generateWithRequired(self, zone_id):
        self.zoneId = zone_id
        self.air.generateWithRequired(self, self.air.district.do_id, zone_id)

    def sendUpdate(self, field_name, args):
        dg = self.dclass.ai_format_update(field_name, self.do_id, self.do_id, self.air.ourChannel, args)
        self.air.send(dg)

    def sendUpdateToChannel(self, channel, field_name, args):
        dg = self.dclass.ai_format_update(field_name, self.do_id, channel, self.air.ourChannel, args)
        self.air.send(dg)

    def sendUpdateToSender(self, field_name, args):
        self.sendUpdateToChannel(self.air.currentSender, field_name, args)

    def sendUpdateToAvatar(self, av_id, field_name, args):
        self.sendUpdateToChannel(getPuppetChannel(av_id), field_name, args)

    def sendUpdateToAccount(self, disl_id, field_name, args):
        self.sendUpdateToChannel(getAccountChannel(disl_id), field_name, args)

    @property
    def location(self):
        return self.parentId, self.zoneId

    @location.setter
    def location(self, location):
        if location == self.location:
            return
        parentId, zoneId = location
        oldParentId, oldZoneId = self.location
        self.parentId = parentId
        self.zoneId = zoneId

        self.air.storeLocation(self.do_id, oldParentId, oldZoneId, parentId, zoneId)

        self.handleZoneChange(oldZoneId, zoneId)

        if zoneId != DistributedObjectAI.QUIET_ZONE:
            self.handleLogicalZoneChange(oldZoneId, zoneId)
            self.lastLogicalZoneId = zoneId

    @property
    def zoneData(self) -> AIZoneData:
        if self._zoneData is None:
            self._zoneData = AIZoneData(self.air, self.parentId, self.zoneId)
        return self._zoneData

    @property
    def render(self):
        return self.zoneData.render

    @property
    def nonCollidableParent(self):
        return self.zoneData.nonCollidableParent

    @property
    def parentMgr(self):
        return self.zoneData.parentMgr

    def releaseZoneData(self):
        if self._zoneData is not None:
            self._zoneData.destroy()
            self._zoneData = None

    def handleLogicalZoneChange(self, old_zone: int, new_zone: int):
        pass

    def generate(self):
        pass

    def announceGenerate(self):
        pass

    def delete(self):
        if self.air:
            self.releaseZoneData()
            self.air = None
            self.zoneId = 0
            self.parentId = 0
            self.do_id = None

    @property
    def deleted(self):
        return self.air is None

    @property
    def generated(self):
        return self.do_id is not None

    def requestDelete(self):
        if not self.do_id:
            print(f'Tried deleting {self.__class__.__name__} more than once!')
            return

        self.air.requestDelete(self)

    def uniqueName(self, name):
        return f'{name}={self.do_id}'

    def handleChildArrive(self, obj, zoneId):
        pass

    def handleChildArriveZone(self, obj, zoneId):
        pass

    def handleChildLeave(self, obj, zoneId):
        pass

    def handleChildLeaveZone(self, obj, zoneId):
        pass

    def handleZoneChange(self, oldZoneId, zoneId):
        pass
