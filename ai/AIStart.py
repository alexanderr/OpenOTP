from otp import config

import asyncio

from direct.directnotify import DirectNotify
from direct.showbase import Messenger, BulletinBoard, EventManager, JobManager
from direct.task import Task
from direct.interval.IntervalGlobal import ivalMgr


from panda3d.core import GraphicsEngine, ClockObject, TrueClock, PandaNode
from otp.messagetypes import *
from dc.util import Datagram
from otp.constants import *

import time


from .DistributedObjectAI import DistributedObjectAI

directNotify = DirectNotify.DirectNotify()


OTP_ZONE_ID_OLD_QUIET_ZONE = 1
OTP_ZONE_ID_MANAGEMENT = 2
OTP_ZONE_ID_DISTRICTS = 3
OTP_ZONE_ID_DISTRICTS_STATS = 4
OTP_ZONE_ID_ELEMENTS = 5


OTP_DO_ID_TOONTOWN = 4618


class DistributedDirectoryAI(DistributedObjectAI):
    do_id = OTP_DO_ID_TOONTOWN


class ToontownDistrictAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.name = 'Coontown'
        self.available = True

    def getName(self):
        return self.name

    def getAvailable(self):
        return self.available


class ToontownDistrictStatsAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.district_id = 0
        self.avatar_count = 0
        self.new_avatar_count = 0

    def gettoontownDistrictId(self):
        return self.district_id

    def getAvatarCount(self):
        return self.avatar_count

    def getNewAvatarCount(self):
        return self.new_avatar_count


class DistributedInGameNewsMgrAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.latest_issue = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1379606399))

    def getLatestIssueStr(self):
        return self.latest_issue


class NewsManagerAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

    def getWeeklyCalendarHolidays(self):
        return []

    def getYearlyCalendarHolidays(self):
        return []

    def getOncelyCalendarHolidays(self):
        return []

    def getRelativelyCalendarHolidays(self):
        return []

    def getMultipleStartHolidays(self):
        return []


class AIBase:
    AISleep = 0.04

    def __init__(self):
        self.eventMgr = EventManager.EventManager()
        self.messenger = Messenger.Messenger()
        self.bboard = BulletinBoard.BulletinBoard()
        self.taskMgr = Task.TaskManager()

        self.graphicsEngine = GraphicsEngine()

        globalClock = ClockObject.get_global_clock()
        self.trueClock = TrueClock.get_global_ptr()
        globalClock.set_real_time(self.trueClock.get_short_time())
        globalClock.set_average_frame_rate_interval(30.0)
        globalClock.tick()
        self.taskMgr.globalClock = globalClock

        self._setup()

        self.air = AIRepository()

    def _setup(self):
        self.taskMgr.add(self._reset_prev_transform, 'resetPrevTransform', priority=-51)
        self.taskMgr.add(self._ival_loop, 'ivalLoop', priority=20)
        self.taskMgr.add(self._ig_loop, 'igLoop', priority=50)
        self.eventMgr.restart()

    def _reset_prev_transform(self, state):
        PandaNode.resetAllPrevTransform()
        return Task.cont

    def _ival_loop(self, state):
        ivalMgr.step()
        return Task.cont

    def _ig_loop(self, state):
        self.graphicsEngine.renderFrame()
        return Task.cont

    def run(self):
        self.air.run()
        self.start_read_poll_task()
        self.taskMgr.run()

    def start_read_poll_task(self):
        self.taskMgr.add(self.air.read_until_empty, 'readPoll', priority=-30)


from otp.networking import ToontownProtocol


class AIProtocol(ToontownProtocol):
    def connection_made(self, transport):
        print('connection made')
        ToontownProtocol.connection_made(self, transport)

    def connection_lost(self, exc):
        raise Exception('AI CONNECTION LOST', exc)

    async def receive_datagram(self, dg):
        print('ai protocol got dg:')
        self.service.queue.put_nowait(dg)

    def data_received(self, data: bytes):
        print('got data...')
        ToontownProtocol.data_received(self, data)

    def send_datagram(self, data: Datagram):
        ToontownProtocol.send_datagram(self, data)
        print('sent data:', data.get_message().tobytes(), self.transport)

    async def handle_datagrams(self):
        while True:
            data: bytes = await self.incoming_q.get()
            print('got datagram!!!!', self.service)
            dg = Datagram()
            dg.add_bytes(data)
            await self.receive_datagram(dg)


from panda3d.core import UniqueIdAllocator
from dc.parser import parse_dc_file
import queue


class AIRepository:
    def __init__(self):
        self.connection = None
        self.queue = queue.Queue()

        base_channel = 4000000

        max_channels = 1000000
        self.channel_allocator = UniqueIdAllocator(base_channel, base_channel + max_channels - 1)

        self._registered_channels = set()

        self.__contextCounter = 0
        self.__callbacks = {}

        self.our_channel = self.allocate_channel()

        self.do_table = {}

        self.dc_file = parse_dc_file('toon.dc')

        self.current_sender = None
        self.loop = None
        self.net_thread = None

    def run(self):
        from threading import Thread
        self.net_thread = Thread(target=self.__event_loop)
        self.net_thread.start()

    def _on_net_except(self, loop, context):
        print('err', context)

    def __event_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.set_exception_handler(self._on_net_except)
        self.loop.run_until_complete(self.loop.create_connection(self._on_connect, '127.0.0.1', 46668))
        self.create_objects()
        self.loop.run_forever()

    def _on_connect(self):
        self.connection = AIProtocol(self)
        return self.connection

    def read_until_empty(self, task):
        while True:
            try:
                dg = self.queue.get(timeout=0.05)
            except queue.Empty:
                break
            else:
                self.handle_datagram(dg)

        return task.cont

    def handle_datagram(self, dg):
        dgi = dg.iterator()
        print('handle_datagram', dg.get_message())

        recipient_count = dgi.get_uint8()
        recipients = [dgi.get_channel() for _ in range(recipient_count)]
        self.current_sender = dgi.get_channel()
        msg_type = dgi.get_uint16()

        print(recipients, recipient_count, self.current_sender, msg_type)

        if msg_type == STATESERVER_OBJECT_ENTER_AI_RECV:
            if self.current_sender == self.our_channel:
                return
            self.handle_obj_entry(dgi)
        elif msg_type == STATESERVER_OBJECT_DELETE_RAM:
            pass
        elif msg_type == STATESERVER_OBJECT_LEAVING_AI_INTEREST:
            pass
        elif msg_type == STATESERVER_OBJECT_CHANGE_ZONE:
            print('got change zone upoate', dg.get_message())
            self.handle_change_zone(dgi)
        elif msg_type == STATESERVER_OBJECT_UPDATE_FIELD:
            print('GOT FIELD UPDATE')
            self.handle_update_field(dgi)
        else:
            print('Unhandled msg type: ', msg_type)

    def handle_change_zone(self, dgi):
        do_id = dgi.get_uint32()
        new_parent = dgi.get_uint32()
        new_zone = dgi.get_uint32()
        old_parent = dgi.get_uint32()
        old_zone = dgi.get_uint32()

    def handle_update_field(self, dgi):
        do_id = dgi.get_uint32()
        field_number = dgi.get_uint16()

        field = self.dc_file.fields[field_number]()

        if field.is_airecv and 'clsend' in field.keywords:
            self.current_sender = self.current_sender & 0xffffffff

        print(field.name, do_id, self.current_sender)

    def handle_obj_entry(self, dgi):
        print('pre ai entry', dgi.remaining())
        do_id = dgi.get_uint32()
        parent_id = dgi.get_uint32()
        zone_id = dgi.get_uint32()
        dc_id = dgi.get_uint16()
        print('ai_entry', do_id, parent_id, zone_id, dc_id)

        dclass = self.dc_file.classes[dc_id]

        if dclass.name == 'DistributedToon':
            from .DistributedToon import DistributedToonAI

            obj = DistributedToonAI(self)
            obj.do_id = do_id
            obj.parent_id = parent_id
            obj.zone_id = zone_id
            dclass.receive_update_all_required(obj, dgi)
            # dclass.receive_update_other(obj, dgi)

            self.do_table[obj.do_id] = obj

            obj.send_update('arrivedOnDistrict', [self.district.do_id, ])

    def context(self):
        self.__contextCounter = (self.__contextCounter + 1) & 0xFFFFFFFF
        return self.__contextCounter

    def allocate_channel(self):
        return self.channel_allocator.allocate()

    def deallocate_channel(self, channel):
        self.channel_allocator.free(channel)

    def register_for_channel(self, channel):
        if channel in self._registered_channels:
            return
        self._registered_channels.add(channel)

        dg = Datagram()
        dg.add_server_control_header(CONTROL_SET_CHANNEL)
        dg.add_channel(channel)
        print('ai register for channel', channel, dg.get_message().tobytes())
        self.send(dg)

    def unregister_for_channel(self, channel):
        if channel not in self._registered_channels:
            return
        self._registered_channels.remove(channel)

        dg = Datagram()
        dg.add_server_control_header(CONTROL_REMOVE_CHANNEL)
        dg.add_channel(channel)
        self.send(dg)

    def send(self, dg):
        self.connection.send_datagram(dg)

    def generate_with_required(self, do, parent_id, zone_id, optional=()):
        do_id = self.allocate_channel()
        self.generate_with_required_and_id(do, do_id, parent_id, zone_id, optional)

    def generate_with_required_and_id(self, do, do_id, parent_id, zone_id, optional=()):
        do.do_id = do_id
        #self.addDOToTables(do, location=(parent_id, zone_id))
        self.do_table[do_id] = do
        dg = do.dclass.ai_format_generate(do, do_id, parent_id, zone_id, STATESERVERS_CHANNEL, self.our_channel, optional)
        self.send(dg)

    def create_objects(self):
        self.register_for_channel(self.our_channel)

        self.district = ToontownDistrictAI(self)
        self.generate_with_required(self.district, OTP_DO_ID_TOONTOWN, OTP_ZONE_ID_DISTRICTS)

        dg = Datagram()
        dg.add_server_header([STATESERVERS_CHANNEL], self.our_channel, STATESERVER_ADD_AI_RECV)
        dg.add_uint32(self.district.do_id)
        dg.add_channel(self.our_channel)
        self.send(dg)

        stats = ToontownDistrictStatsAI(self)
        self.generate_with_required(stats, OTP_DO_ID_TOONTOWN, OTP_ZONE_ID_DISTRICTS_STATS)

        dg = Datagram()
        dg.add_server_header([STATESERVERS_CHANNEL], self.our_channel, STATESERVER_ADD_AI_RECV)
        dg.add_uint32(stats.do_id)
        dg.add_channel(self.our_channel)
        self.send(dg)

        ingame_news = DistributedInGameNewsMgrAI(self)
        self.generate_with_required(ingame_news, self.district.do_id, OTP_ZONE_ID_MANAGEMENT)

        news_mgr = NewsManagerAI(self)
        self.generate_with_required(news_mgr, self.district.do_id, OTP_ZONE_ID_MANAGEMENT)


def main():
    print('running main')
    simbase = AIBase()
    simbase.run()


if __name__ == '__main__':
    main()