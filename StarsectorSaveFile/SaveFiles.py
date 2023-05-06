import os.path
import threading
from datetime import datetime, timedelta
from typing import Dict, List

import lxml.etree

from .PersonUnit import *
from .PortraitModUnit import portraitModUnit

__all__ = ['saveFileManager', 'portraitModUnit', 'saveFileUnit', 'cache_PublicModPortraits',
           'AIAdminPerson', 'NexAgentPerson']

# 固定名称区
const_campaignName = 'campaign.xml'
const_descriptionName = 'descriptor.xml'
# 公共缓冲区
cache_PublicModPortraits: Dict[str, portraitModUnit] = {}  # 有头像可以使用的mod
hasInitedModIDs: List[str] = []  # 已经进行了初始化加载的mod


def openXMLFile(xmlPath: str) -> lxml.etree._ElementTree:
    """打开一个XML存档文件，并使用lxml来解析它"""
    return lxml.etree.parse(xmlPath, lxml.etree.XMLParser('UTF-8'))


class saveFileUnit:
    def __init__(self, folderName: str):
        """
        存档文件管理单元。

        :param folderName: 存档文件所在的目录。不能处理压缩存档。
        """
        self.__saveFileName = os.path.join(folderName, const_campaignName)
        self.__descriptionName = os.path.join(folderName, const_descriptionName)
        # 打开描述文件以获取基本信息
        tFile = openXMLFile(self.__descriptionName)
        isTF = lambda x: True if x == 'true' else False
        self.__descriptionInfo: Dict[str, str | bool | datetime | int] = {  # 基本描述信息
            'portraitPath': tFile.xpath('/SaveGameData/portraitName')[0].text,  # 头像特质
            'characterName': tFile.xpath('/SaveGameData/characterName')[0].text,  # 角色名称
            'characterLevel': int(tFile.xpath('/SaveGameData/characterLevel')[0].text),  # 角色等级
            'compressed': isTF(tFile.xpath('/SaveGameData/compressed')[0].text),  # 是否压缩
            'isIronMode': isTF(tFile.xpath('/SaveGameData/isIronMode')[0].text),  # 是否为铁人模式
            'difficulty': tFile.xpath('/SaveGameData/difficulty')[0].text,  # 难度等级
            'gameDate': datetime(1970, 1, 1) + timedelta(
                seconds=int(tFile.xpath('/SaveGameData/gameDate/timestamp')[0].text) / 1000),  # 游戏当前运行时间
            'saveDate': datetime.fromisoformat(tFile.xpath('/SaveGameData/saveDate')[0].text[:-4]),  # 游戏保存时间
        }
        # 获取mod信息以便预加载
        self.__modsInfo: Dict[str, Dict[str, str]] = {}
        for unit in tFile.xpath(
                '/SaveGameData/allModsEverEnabled//com.fs.starfarer.campaign.ModAndPluginData_-EnabledModData/spec'):
            # assert isinstance(unit, lxml.etree._Element)
            modPath: str = unit.xpath('path')[0].text
            if not os.path.isdir(modPath):
                continue
            self.__modsInfo[unit.xpath('id')[0].text] = {
                'id': unit.xpath('id')[0].text,
                'path': modPath.strip().replace(r'\starsector-core\..', ''),  # Mod的工作路径
                'name': unit.xpath('name')[0].text,  # 名称
                'description': unit.xpath('desc')[0].text,  # 描述
                'version': unit.xpath('versionInfo/string')[0].text,  # 版本号
                'author': unit.xpath('author')[0].text,  # 作者
            }
        # const定义区
        self.__const_saveDelay = 10  # 单位为秒
        # 标志区
        self.__flag_inited = False
        self.__flag_hasLoadedMod = False
        self.__event_endAllSync = threading.Event()
        self.__event_saveDelay = threading.Event()
        # 变量存储区
        self.__cache_hasPortraitsMod = ['core']
        self.__func_toSyncPerson = []  # 这个列表存储待执行的同步函数，然后后台定时调度
        self.__saveFileNode: lxml.etree._ElementTree = None
        self.__AIAdmin_persons: List[AIAdminPerson] = []
        self.__NexAgent_persons: List[NexAgentPerson] = []

    def GetModInfoByID(self, modID: str):
        return self.__modsInfo.get(modID, {})

    def LoadModIntoCache(self):
        """将该存档的mod内容载入缓存"""
        if self.__flag_hasLoadedMod:
            return
        for unitKey in self.__modsInfo:
            if unitKey not in hasInitedModIDs:
                tVar = portraitModUnit(**self.__modsInfo[unitKey])
                hasInitedModIDs.append(unitKey)
                if tVar.HasPortraits:  # 只载入有头像的mod
                    cache_PublicModPortraits[unitKey] = tVar
                    self.__cache_hasPortraitsMod.append(unitKey)
        self.__flag_hasLoadedMod = True

    def GetPortraitAbsolutePath(self) -> str | None:
        """返回当前存档的玩家所使用头像的绝对路径，主要是为了显示。如果找不到，就返回None"""
        for unit in self.__cache_hasPortraitsMod:
            if unit in cache_PublicModPortraits and cache_PublicModPortraits[unit].IsIncludePortrait(self.PortraitPath):
                return cache_PublicModPortraits[unit].PathJoin(self.PortraitPath)
        return None

    def OpenSaveFile(self):
        """打开这个存档文件并安排具体事务运行"""
        if self.__flag_inited:
            return
        self.__saveFileNode = openXMLFile(self.__saveFileName)
        for unit in self.__saveFileNode.xpath('//Person[@pst="administrator"]/aiCoreId/..'):
            self.__AIAdmin_persons.append(AIAdminPerson(unit, self.__func_toSyncPerson))
        if 'nexerelin' in self.__modsInfo:  # 势力争霸mod存在时才检测特工情况
            for unit in self.__saveFileNode.xpath('//NexAgntIntl/agent[@pst="agent"]'):
                self.__NexAgent_persons.append(NexAgentPerson(unit, self.__func_toSyncPerson))
        self.__flag_inited = True
        threading.Thread(target=self.__thread_saveInfoDelay, daemon=True).start()

    def CloseSaveFile(self, noSave: bool = False):
        """
        关闭当前存档。

        :param noSave: 是否不保存存档。
        """
        if self.__saveFileNode is None:
            return
        self.__flag_inited = False
        self.__event_saveDelay.set()
        if not noSave:
            self.__event_endAllSync.wait()
            self.__saveFileNode.write(self.__saveFileName, 'UTF-8', standalone=False)

    def __thread_saveInfoDelay(self):
        """后台调度线程，用于定时将个人属性同步至XML文件中"""
        while self.__flag_inited:
            self.__event_saveDelay.wait(timeout=self.__const_saveDelay)
            for unitFunc in self.__func_toSyncPerson:
                try:
                    unitFunc()
                except:
                    pass
            self.__func_toSyncPerson.clear()
        self.__event_endAllSync.set()

    # 参数区
    @property
    def PortraitPath(self) -> str:
        """头像路径"""
        return self.__descriptionInfo['portraitPath']

    @property
    def CharacterName(self) -> str:
        """玩家名称"""
        return self.__descriptionInfo['characterName']

    @property
    def CharacterLevel(self) -> int:
        """角色等级"""
        return self.__descriptionInfo['characterLevel']

    @property
    def IsIronMode(self) -> bool:
        """是否为铁人模式"""
        return self.__descriptionInfo['isIronMode']

    @property
    def Difficulty(self) -> str:
        """游戏难度"""
        return self.__descriptionInfo['difficulty']

    @property
    def GameRunningDate(self) -> datetime:
        """游戏的当前运行时间"""
        return self.__descriptionInfo['gameDate']

    @property
    def SaveDate(self) -> datetime:
        """存档的保存日期"""
        return self.__descriptionInfo['saveDate']

    @property
    def ModInfoIDs(self):
        return list(self.__modsInfo.keys())


class saveFileManager:

    def __init__(self, saveFolder: str):
        """
        存档文件总管理器，负责统筹管理。

        :param saveFolder: 总存档目录，通常是saves文件夹。
        """
        assert os.path.isdir(saveFolder), "不是一个有效的存档目录！"
        self.__saveFiles = []
        for dirPath, _, fileNames in os.walk(saveFolder):
            if const_descriptionName and const_campaignName in fileNames:
                try:
                    self.__saveFiles.append(saveFileUnit(dirPath))
                    # 传入存档后会读取有效信息，读取失败就主动报错
                except:
                    pass
        for unit in self.__saveFiles:
            unit.LoadModIntoCache()
        # 加载原版数据
        cache_PublicModPortraits['core'] = portraitModUnit(name='远行星号 原版', desc='原版头像库',
                                                           path=os.path.join(saveFolder, '..', 'starsector-core'))

    def GetLatestSaveFile(self):
        """返回最新的存档，这是通过判定保存时间来处理的"""
        if len(self.__saveFiles) == 0:
            return None
        maxSaveFile = self.__saveFiles[0]
        for unit in self.__saveFiles:
            if unit.SaveDate > maxSaveFile.SaveDate:
                maxSaveFile = unit
        return maxSaveFile

    def ListAllSaveInfo(self):
        return self.__saveFiles.copy()
