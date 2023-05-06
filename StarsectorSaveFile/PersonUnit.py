import lxml.etree

__all__ = ['AIAdminPerson', 'NexAgentPerson']


def GetLocationName(locationID: str, node: lxml.etree._Element) -> str:
    """从一个市场ID找出市场的所在地的名称，可惜不能找出星系名。"""
    xpath_list = [f'//market[@z="{locationID}"]/name', f'//Market[@z="{locationID}"]/name',
                  f'//gatheringPoint[@z="{locationID}"]/name', f'//m[@z="{locationID}"]/name']
    for xpathStr in xpath_list:
        tVar = node.xpath(xpathStr)
        if len(tVar) > 0:
            return tVar[0].text
    return '未找到'


class AIAdminPerson:

    def __init__(self, node: lxml.etree._Element, func_List: list):
        """殖民地，A核行政官"""
        self.__delayFuncList = func_List
        self.__node = node
        self.__flag_needUpdate = False
        # 数据
        self.__name: str = ' '.join((node.attrib['f'], node.attrib['l']))
        self.__portraitPath: str = node.attrib['spr']
        self.__location = GetLocationName(node.xpath('market')[0].attrib['ref'], node)

    def UpdateInfo(self):
        if self.__flag_needUpdate:
            if self.__syncToXML in self.__delayFuncList:
                self.__delayFuncList.remove(self.__syncToXML)
            self.__delayFuncList.append(self.__syncToXML)

    def __syncToXML(self):
        self.__flag_needUpdate = False
        self.__node.attrib['l'] = ''
        self.__node.attrib['f'] = self.__name
        self.__node.attrib['spr'] = self.__portraitPath

    @property
    def Name(self):
        return self.__name

    @property
    def PortraitPath(self):
        return self.__portraitPath

    @property
    def Location(self):
        return self.__location

    @Name.setter
    def Name(self, value):
        if isinstance(value, str) and value != self.__name:
            if len(value) == 0:
                value = ' '
            self.__name = value
            self.__flag_needUpdate = True

    @PortraitPath.setter
    def PortraitPath(self, value):
        if isinstance(value, str) and value != self.__portraitPath:
            self.__portraitPath = value
            self.__flag_needUpdate = True


class NexAgentPerson:
    const_Man = "MALE"  # 男
    const_Woman = "FEMALE"  # 女

    def __init__(self, node: lxml.etree._Element, func_List: list):
        """势力争霸，特工"""
        __const_specializations = {
            "negotiator": "谈判代表",
            "saboteur": "破坏分子",
            "hybrid": "多面好手",
            "master": "大师"
        }
        self.__delayFuncList = func_List
        self.__node = node
        self.__flag_needUpdate = False
        # 数据
        self.__name: str = ' '.join((node.attrib['f'], node.attrib['l']))
        self.__portraitPath: str = node.attrib['spr']
        self.__level = int(node.xpath('../level')[0].text)
        self.__gender: str = node.attrib['g']  # 性别，用MALE或者FEMALE取代
        self.__specialization = __const_specializations.get(  # 这项指的是特工的专长
            node.xpath('../specializations/exerelin.campaign.intel.agents.AgentIntel_-Specialization')[0].text.lower())
        self.__location = GetLocationName(node.xpath('../market')[0].attrib['ref'], node)

    def UpdateInfo(self):
        if self.__flag_needUpdate:
            if self.__syncToXML in self.__delayFuncList:
                self.__delayFuncList.remove(self.__syncToXML)
            self.__delayFuncList.append(self.__syncToXML)

    def __syncToXML(self):
        self.__flag_needUpdate = False
        self.__node.attrib['l'] = ''
        self.__node.attrib['f'] = self.__name
        self.__node.attrib['spr'] = self.__portraitPath
        self.__node.attrib['g'] = self.__gender

    @property
    def Name(self):
        return self.__name

    @property
    def PortraitPath(self):
        return self.__portraitPath

    @property
    def Gender(self):
        return self.__gender

    @property
    def Location(self):
        return self.__location

    @property
    def Level(self):
        return self.__level

    @property
    def Specialization(self):
        return self.__specialization

    @Name.setter
    def Name(self, value):
        if isinstance(value, str) and value != self.__name:
            if len(value) == 0:
                value = ' '
            self.__name = value
            self.__flag_needUpdate = True

    @PortraitPath.setter
    def PortraitPath(self, value):
        if isinstance(value, str) and value != self.__portraitPath:
            self.__portraitPath = value
            self.__flag_needUpdate = True

    @Gender.setter
    def Gender(self, value):
        if value in ('MALE', 'FEMALE') and value != self.__gender:
            self.__gender = value
            self.__flag_needUpdate = True

    def TranslateGender(self, toTranslate: str) -> str:
        """
        将代码翻译为中文，或者反过来。

        :param toTranslate: 需要转换的词。
        :return: 转换后的词。
        """
        match toTranslate:
            case self.const_Man:
                return '男'
            case self.const_Woman:
                return '女'
            case '男':
                return self.const_Man
            case '女':
                return self.const_Woman
            case _:
                return ''
