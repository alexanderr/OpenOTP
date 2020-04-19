from ai.AIStart import DistributedObjectAI


class DistributedAvatarAI(DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        self.name = 'Toon'

    def setName(self, name):
        self.name = name

    def getName(self):
        return 'Toon'


class DistributedPlayerAI(DistributedAvatarAI):
    def __init__(self, air):
        DistributedAvatarAI.__init__(self, air)


    def getAccountName(self):
        return 'username'

    def getFriendsList(self):
        return []

    def getDISLid(self):
        return 0

    def getPreviousAccess(self):
        # AccessFull = 2
        return 2

    def getAccess(self):
        return 2

    def getAsGM(self):
        return False


class DistributedToonAI(DistributedPlayerAI):
    def getDNAString(self):
        return 't\x1b\x01\x01\x01\x12\x05\x0c\x05\x03\x05\x10\x00\x12\x11'

    def getGM(self):
        return False

    def getMaxBankMoney(self):
        return 0

    def getBankMoney(self):
        return 0

    def getMaxMoney(self):
        return 0

    def getMoney(self):
        return 0

    def getMaxHp(self):
        return 15

    def getHp(self):
        return 15

    def getBattleId(self):
        return 0

    def getExperience(self):
        return b'\x00\x00' * 7

    def getMaxCarry(self):
        return 20

    def getTrackAccess(self):
        return [0, 0, 0, 0, 1, 1, 0]

    def getTrackProgress(self):
        return 0, 0

    def getTrackBonusLevel(self):
        return [0, 0, 0, 0, 0, 0, 0]

    def getInventory(self):
        return b''

    def getMaxNPCFriends(self):
        return 8

    def getNPCFriendsDict(self):
        return []

    def getDefaultShard(self):
        return 0

    def getDefaultZone(self):
        return 2000

    def getShtickerBook(self):
        return b''

    def getZonesVisited(self):
        return []

    def getHoodsVisited(self):
        return []

    def getInterface(self):
        return b''

    def getLastHood(self):
        return 0

    def getTutorialAck(self):
        return 1

    def getMaxClothes(self):
        return 0

    def getClothesTopsList(self):
        return []

    def getClothesBottomsList(self):
        return []

    def getMaxAccessories(self):
        return 0

    def getHatList(self):
        return []

    def getGlassesList(self):
        return []

    def getBackpackList(self):
        return []

    def getShoesList(self):
        return []

    def getHat(self):
        return 0, 0, 0

    def getGlasses(self):
        return 0, 0, 0

    def getBackpack(self):
        return 0, 0, 0

    def getShoes(self):
        return 0, 0, 0

    def getGardenSpecials(self):
        return []

    def getEmoteAccess(self):
        return [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def getCustomMessages(self):
        return []

    def getResistanceMessages(self):
        return []

    def getPetTrickPhrases(self):
        return []

    def getCatalogSchedule(self):
        return 0, 0

    def getCatalog(self):
        return b'', b'', b''

    def getMailboxContents(self):
        return b''

    def getDeliverySchedule(self):
        return b''

    def getGiftSchedule(self):
        return b''

    def getAwardMailboxContents(self):
        return b''

    def getAwardSchedule(self):
        return b''

    def getAwardNotify(self):
        return 0

    def getCatalogNotify(self):
        return 0, 0

    def getSpeedChatStyleIndex(self):
        return 1

    def getTeleportAccess(self):
        return []

    def getCogStatus(self):
        return [0] * 32

    def getCogCount(self):
        return [0] * 32

    def getCogRadar(self):
        return [0] * 4

    def getBuildingRadar(self):
        return [0] * 4

    def getCogLevels(self):
        return [0] * 4

    def getCogTypes(self):
        return [0] * 4

    def getCogParts(self):
        return [0] * 4

    def getCogMerits(self):
        return [0] * 4

    def getHouseId(self):
        return 0

    def getQuests(self):
        return []

    def getQuestHistory(self):
        return []

    def getRewardHistory(self):
        return 0, []

    def getQuestCarryLimit(self):
        return 1

    def getCheesyEffect(self):
        return 0, 0, 0

    def getPosIndex(self):
        return 0

    def getFishCollection(self):
        return [], [], []

    def getMaxFishTank(self):
        return 20

    def getFishTank(self):
        return [], [], []

    def getFishingRod(self):
        return 0

    def getFishingTrophies(self):
        return []

    def getFlowerCollection(self):
        return [], []

    def getFlowerBasket(self):
        return [], []

    def getMaxFlowerBasket(self):
        return 20

    def getGardenTrophies(self):
        return []

    def getShovel(self):
        return 0

    def getShovelSkill(self):
        return 0

    def getWateringCan(self):
        return 0

    def getWateringCanSkill(self):
        return 0

    def getPetId(self):
        return 0

    def getPetTutorialDone(self):
        return 0

    def getFishBingoTutorialDone(self):
        return 0

    def getFishBingoMarkTutorialDone(self):
        return 0

    def getKartBodyType(self):
        return -1

    def getKartBodyColor(self):
        return -1

    def getKartAccessoryColor(self):
        return -1

    def getKartEngineBlockType(self):
        return -1

    def getKartSpoilerType(self):
        return -1

    def getKartFrontWheelWellType(self):
        return -1

    def getKartBackWheelWellType(self):
        return -1

    def getKartRimType(self):
        return -1

    def getKartDecalType(self):
        return -1

    def getTickets(self):
        return 200

    def getKartingHistory(self):
        return [0] * 16

    def getKartingTrophies(self):
        return [0] * 33

    def getKartingPersonalBest(self):
        return [0] * 6

    def getKartingPersonalBest2(self):
        return [0] * 12

    def getKartAccessoriesOwned(self):
        return [0] * 16

    def getCogSummonsEarned(self):
        return [0] * 32

    def getGardenStarted(self):
        return 0

    def getGolfHistory(self):
        return [0] * 18

    def getPackedGolfHoleBest(self):
        return [0] * 18

    def getGolfCourseBest(self):
        return [0] * 3

    def getPinkSlips(self):
        return 0

    def getNametagStyle(self):
        return 0