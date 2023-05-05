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
        # 数据
        self.__name: str = ' '.join((node.attrib['f'], node.attrib['l']))
        self.__portraitPath: str = node.attrib['spr']
        self.__location = GetLocationName(node.xpath('market')[0].attrib['ref'], node)

    def UpdateInfo(self):
        self.__delayFuncList.append(self.__syncToXML)

    def __syncToXML(self):
        self.__node.attrib['l'] = ''
        self.__node.attrib['f'] = self.__name
        self.__node.attrib['spr'] = self.__portraitPath


class NexAgentPerson:

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
        # 数据
        self.__name: str = ' '.join((node.attrib['f'], node.attrib['l']))
        self.__portraitPath: str = node.attrib['spr']
        self.__level = int(node.xpath('../level')[0].text)
        self.__gender = node.attrib['g']
        self.__specialization = __const_specializations.get(  # 这项指的是特工的专长
            node.xpath('../specializations/exerelin.campaign.intel.agents.AgentIntel_-Specialization')[0].text.lower())
        self.__location = GetLocationName(node.xpath('../market')[0].attrib['ref'], node)

    def UpdateInfo(self):
        self.__delayFuncList.append(self.__syncToXML)

    def __syncToXML(self):
        self.__node.attrib['l'] = ''
        self.__node.attrib['f'] = self.__name
        self.__node.attrib['spr'] = self.__portraitPath
        self.__node.attrib['g'] = self.__gender
