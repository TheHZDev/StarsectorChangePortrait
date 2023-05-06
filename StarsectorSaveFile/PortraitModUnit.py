import os.path
import random
from typing import List

import json5

__all__ = ['portraitModUnit']


class portraitModUnit:
    """专用于管理头像Mod的类模式"""

    def __init__(self, **kwargs):
        self.__modName = kwargs.get('name')
        self.__modPath = kwargs.get('path')
        self.__modDesc = kwargs.get('desc')
        self.__portraits_global_men: List[str] = []  # 全局头像
        self.__portraits_global_women: List[str] = []
        self.__portraits_player_men: List[str] = []  # 玩家派系特属头像
        self.__portraits_player_women: List[str] = []
        # 实际加载mod
        factionFolder = os.path.join(self.__modPath, 'data', 'world', 'factions')
        if os.path.isdir(factionFolder):
            for unit in os.scandir(factionFolder):
                if unit.name.endswith('.faction') and unit.is_file():
                    tContent: dict = self.__loadJSON5(unit.path)
                    # 判断是否有头像
                    if 'portraits' not in tContent:
                        continue
                    self.__portraits_global_men += tContent.get('portraits', {}).get('standard_male', [])
                    self.__portraits_global_women += tContent.get('portraits', {}).get('standard_female', [])
                    if unit.name == 'player.faction':
                        # 录入玩家头像数据
                        self.__portraits_player_men = tContent.get('portraits', {}).get('standard_male', [])
                        self.__portraits_player_women = tContent.get('portraits', {}).get('standard_female', [])
            # 精简化数据存储
            self.__portraits_global_men = list(set(self.__portraits_global_men))
            self.__portraits_global_women = list(set(self.__portraits_global_women))

    def ListPlayerFactionPortraits(self, genderMan: bool = True, ignoreGender: bool = False) -> List[str]:
        """
        列出玩家势力的头像。

        :param genderMan: 列出男性的头像，否则列出女性的。
        :param ignoreGender: 无视genderMan参数，调出所有头像包。
        :return: 头像包。
        """
        if ignoreGender:
            return self.__portraits_player_women + self.__portraits_player_men
        elif genderMan:
            return self.__portraits_player_men.copy()
        else:
            return self.__portraits_player_women.copy()

    def RandomPlayerFactionPortrait(self, genderMan: bool = True, ignoreGender: bool = False) -> str | None:
        """
        随机从玩家派系里选择一个头像。

        :param genderMan: 选择男性的头像。
        :param ignoreGender: 忽略性别，使得genderMan参数无效。
        :return: 头像路径，如果没有可选的就返回None
        """
        try:
            return random.choice(self.ListPlayerFactionPortraits(genderMan, ignoreGender))
        except IndexError:
            return None

    # 以下的两个函数是上面两个函数的扩展
    def ListGlobalPortraits(self, genderMan: bool = True, ignoreGender: bool = False) -> List[str]:
        """列出该mod的所有头像包"""
        if ignoreGender:
            return self.__portraits_global_women + self.__portraits_global_men
        elif genderMan:
            return self.__portraits_global_men.copy()
        else:
            return self.__portraits_global_women.copy()

    def RandomGlobalPortrait(self, genderMan: bool = True, ignoreGender: bool = False) -> str | None:
        """随机一个全局头像"""
        try:
            return random.choice(self.ListGlobalPortraits(genderMan, ignoreGender))
        except IndexError:
            return None

    def PathJoin(self, portraitPath: str):
        """
        将相对的头像路径转为绝对路径访问。

        :param portraitPath: 相对头像路径
        :return: 绝对路径。
        """
        return os.path.join(self.__modPath, *portraitPath.split('/'))

    def IsIncludePortrait(self, portraitPath: str):
        """查询该mod是否包含该头像"""
        if not self.HasPortraits:
            return False
        return portraitPath in self.__portraits_global_women or portraitPath in self.__portraits_global_men

    @property
    def Description(self) -> str:
        return self.__modDesc

    @property
    def Name(self) -> str:
        return self.__modName

    @property
    def HasPortraits(self) -> bool:
        """是否包含头像内容"""
        return len(self.__portraits_global_women) + len(self.__portraits_global_men) > 0

    @property
    def HasPlayerFactionPortraits(self) -> bool:
        """如果不存在玩家势力的头像，则直接启用全局势力头像"""
        return len(self.__portraits_player_men) + len(self.__portraits_player_women) > 0

    # 辅助参数区
    @staticmethod
    def __loadJSON5(jsonFilePath: str) -> dict:
        with open(jsonFilePath, encoding='UTF-8') as tFile:
            tList = []
            tVar = tFile.read().strip()
            if tVar.endswith(','):  # 把末尾莫名其妙的逗号除去
                tVar = tVar[:-1]
            for line in tVar.splitlines():
                tList.append(line.strip().replace('#', '//'))
            result = '\r\n'.join(tList)
        return json5.loads(result)
