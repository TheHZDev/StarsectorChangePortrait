import os
import sys
from os.path import isdir, isfile
from threading import Thread as QThread
from typing import List

from PyQt6 import QtCore, QtGui, QtWidgets

from StarsectorSaveFile import *


class Thread(QThread):
    endSignal = QtCore.pyqtBoundSignal()

    def __init__(self, target, *args, **kwargs):
        super().__init__()
        self.__toExecFunc = target
        self.__args = args
        self.__kwargs = kwargs

    def run(self):
        self.__toExecFunc(*self.__args, **self.__kwargs)
        self.endSignal.emit()


class preDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(504, 386)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setWindowTitle("选择要载入的存档")
        self.__selectSaveFile = QtWidgets.QListWidget(parent=self)
        self.__selectSaveFile.setGeometry(QtCore.QRect(10, 50, 481, 91))
        self.__selectSaveFile.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        label = QtWidgets.QLabel(parent=self)
        label.setGeometry(QtCore.QRect(20, 10, 331, 31))
        label.setText("请选择要载入的存档，点击可以查看具体信息")
        groupBox = QtWidgets.QGroupBox(parent=self)
        groupBox.setGeometry(QtCore.QRect(10, 150, 341, 221))
        groupBox.setTitle("存档基本信息")
        label_2 = QtWidgets.QLabel(parent=groupBox)
        label_2.setGeometry(QtCore.QRect(20, 30, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        label_2.setFont(font)
        label_2.setText("玩家名称")
        label_3 = QtWidgets.QLabel(parent=groupBox)
        label_3.setGeometry(QtCore.QRect(20, 60, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        label_3.setFont(font)
        label_3.setText("玩家等级")
        label_4 = QtWidgets.QLabel(parent=groupBox)
        label_4.setGeometry(QtCore.QRect(20, 90, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        label_4.setFont(font)
        label_4.setText("铁人模式")
        label_5 = QtWidgets.QLabel(parent=groupBox)
        label_5.setGeometry(QtCore.QRect(20, 120, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        label_5.setFont(font)
        label_5.setText("游戏难度")
        label_6 = QtWidgets.QLabel(parent=groupBox)
        label_6.setGeometry(QtCore.QRect(20, 150, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        label_6.setFont(font)
        label_6.setText("游戏日期")
        label_7 = QtWidgets.QLabel(parent=groupBox)
        label_7.setGeometry(QtCore.QRect(20, 180, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        label_7.setFont(font)
        label_7.setText("保存日期")
        self.__showPlayerName = QtWidgets.QLineEdit(parent=groupBox)
        self.__showPlayerName.setGeometry(QtCore.QRect(120, 30, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.__showPlayerName.setFont(font)
        self.__showPlayerName.setFrame(True)
        self.__showPlayerName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__showPlayerName.setReadOnly(True)
        self.__showPlayerLevel = QtWidgets.QLineEdit(parent=groupBox)
        self.__showPlayerLevel.setGeometry(QtCore.QRect(120, 60, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.__showPlayerLevel.setFont(font)
        self.__showPlayerLevel.setFrame(True)
        self.__showPlayerLevel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__showPlayerLevel.setReadOnly(True)
        self.__showIsIronManMode = QtWidgets.QLineEdit(parent=groupBox)
        self.__showIsIronManMode.setGeometry(QtCore.QRect(120, 90, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.__showIsIronManMode.setFont(font)
        self.__showIsIronManMode.setFrame(True)
        self.__showIsIronManMode.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__showIsIronManMode.setReadOnly(True)
        self.__showGameDifficulty = QtWidgets.QLineEdit(parent=groupBox)
        self.__showGameDifficulty.setGeometry(QtCore.QRect(120, 120, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.__showGameDifficulty.setFont(font)
        self.__showGameDifficulty.setFrame(True)
        self.__showGameDifficulty.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__showGameDifficulty.setReadOnly(True)
        self.__showGameRunningDate = QtWidgets.QLineEdit(parent=groupBox)
        self.__showGameRunningDate.setGeometry(QtCore.QRect(120, 150, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.__showGameRunningDate.setFont(font)
        self.__showGameRunningDate.setFrame(True)
        self.__showGameRunningDate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__showGameRunningDate.setReadOnly(True)
        self.__showGameSaveDate = QtWidgets.QLineEdit(parent=groupBox)
        self.__showGameSaveDate.setGeometry(QtCore.QRect(120, 180, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.__showGameSaveDate.setFont(font)
        self.__showGameSaveDate.setFrame(True)
        self.__showGameSaveDate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__showGameSaveDate.setReadOnly(True)
        groupBox_2 = QtWidgets.QGroupBox(parent=self)
        groupBox_2.setGeometry(QtCore.QRect(360, 150, 131, 141))
        groupBox_2.setTitle("头像")
        self.__showPlayerPortrait = QtWidgets.QLabel(parent=groupBox_2)
        self.__showPlayerPortrait.setGeometry(QtCore.QRect(10, 20, 111, 111))
        self.__showPlayerPortrait.setText("")
        self.__showPlayerPortrait.setScaledContents(True)
        self.__loadSaveButton = QtWidgets.QPushButton(parent=self)
        self.__loadSaveButton.setGeometry(QtCore.QRect(360, 300, 131, 31))
        self.__loadSaveButton.setText("载入存档")
        self.__exitButton = QtWidgets.QPushButton(parent=self)
        self.__exitButton.setGeometry(QtCore.QRect(360, 340, 131, 31))
        self.__exitButton.setText("退出程序")
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setModal(True)  # 将自己设置为模态窗口来抢占
        self.__loadSaveButton.setEnabled(False)
        # 事件绑定操作
        self.__loadSaveButton.clicked['bool'].connect(lambda b: self.__loadSaveFile())
        self.__exitButton.clicked['bool'].connect(lambda b: exit(0))
        self.__selectSaveFile.currentRowChanged['int'].connect(lambda b: self.__flashInfo())
        # 具体事务操作
        self.__saveFileManager: saveFileManager = None
        self.__flag_init = False
        self.__cache_listItems: List[saveFileUnit] = []
        self.__flag_exit = True
        QThread(target=self.__initData).start()

    def __loadSaveFile(self):
        mainWin.OpenSaveFile(self.__cache_listItems[self.__selectSaveFile.currentRow()])
        self.accept()
        self.__flag_init = False
        self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        a0.accept()
        if self.__flag_exit:
            exit(0)

    def __flashInfo(self):
        currentUnit = self.__cache_listItems[self.__selectSaveFile.currentRow()]
        self.__showPlayerName.setText(currentUnit.CharacterName)
        self.__showPlayerLevel.setText(str(currentUnit.CharacterLevel))
        self.__showGameDifficulty.setText(currentUnit.Difficulty)
        self.__showGameRunningDate.setText(
            f"{currentUnit.GameRunningDate.year} 年 {currentUnit.GameRunningDate.month} 月 {currentUnit.GameRunningDate.day} 日")
        self.__showGameSaveDate.setText(currentUnit.SaveDate.strftime("%Y-%m-%d %H:%M:%S"))
        self.__showIsIronManMode.setText('是' if currentUnit.IsIronMode else '否')
        # 显示头像
        tVar = QtGui.QPixmap(currentUnit.GetPortraitAbsolutePath())
        self.__showPlayerPortrait.setPixmap(tVar)

    def __initData(self):
        """用来初始化数据"""
        self.__saveFileManager = saveFileManager(os.path.join(os.getcwd(), 'saves'),
                                                 func_showProgress=self.setWindowTitle)
        self.setWindowTitle('请选择要载入的存档')
        self.__flag_init = True
        self.__loadSaveButton.setEnabled(True)
        self.__cache_listItems = self.__saveFileManager.ListSaveInfoOrderBySaveDateDesc()
        # 绘制列表
        showList = []
        for unit in self.__cache_listItems:
            showList.append(
                f"{unit.CharacterName}[等级：{unit.CharacterLevel}，难度：{unit.Difficulty}，游戏日期：{unit.GameRunningDate.year} 年{unit.GameRunningDate.month} 月{unit.GameRunningDate.day} 日]")
        self.__selectSaveFile.addItems(showList)
        self.__selectSaveFile.setCurrentRow(0)


class starsectorSaveEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(612, 600)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.setFont(font)
        self.setWindowTitle("远行星号 存档头像修改工具")
        centralwidget = QtWidgets.QWidget(parent=self)
        self.__selectFunction = QtWidgets.QTabWidget(parent=centralwidget)
        self.__selectFunction.setGeometry(QtCore.QRect(10, 10, 591, 301))
        tab = QtWidgets.QWidget()
        groupBox = QtWidgets.QGroupBox(parent=tab)
        groupBox.setGeometry(QtCore.QRect(190, 10, 381, 241))
        groupBox.setTitle("基本信息")
        label = QtWidgets.QLabel(parent=groupBox)
        label.setGeometry(QtCore.QRect(10, 40, 131, 21))
        label.setText("姓名（可修改）")
        self.__editAIAdminName = QtWidgets.QLineEdit(parent=groupBox)
        self.__editAIAdminName.setGeometry(QtCore.QRect(10, 70, 181, 31))
        self.__editAIAdminName.setMaxLength(12)
        self.__editAIAdminName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__showAIAdminLocation = QtWidgets.QLineEdit(parent=groupBox)
        self.__showAIAdminLocation.setGeometry(QtCore.QRect(10, 180, 181, 31))
        self.__showAIAdminLocation.setMaxLength(12)
        self.__showAIAdminLocation.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__showAIAdminLocation.setReadOnly(True)
        label_2 = QtWidgets.QLabel(parent=groupBox)
        label_2.setGeometry(QtCore.QRect(10, 150, 151, 21))
        label_2.setText("所治理的殖民地")
        groupBox_2 = QtWidgets.QGroupBox(parent=tab)
        groupBox_2.setGeometry(QtCore.QRect(400, 40, 151, 171))
        groupBox_2.setTitle("头像")
        self.__showAIAdminPortrait = QtWidgets.QLabel(parent=groupBox_2)
        self.__showAIAdminPortrait.setGeometry(QtCore.QRect(10, 30, 131, 131))
        self.__showAIAdminPortrait.setText("")
        self.__showAIAdminPortrait.setScaledContents(True)
        self.__selectAIAdmin = QtWidgets.QListWidget(parent=tab)
        self.__selectAIAdmin.setGeometry(QtCore.QRect(10, 10, 171, 241))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.__selectAIAdmin.setFont(font)
        self.__selectAIAdmin.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__selectAIAdmin.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.__selectFunction.addTab(tab, "A核行政官头像修改")
        tab_2 = QtWidgets.QWidget()
        self.__selectNexAgent = QtWidgets.QListWidget(parent=tab_2)
        self.__selectNexAgent.setGeometry(QtCore.QRect(10, 10, 171, 241))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.__selectNexAgent.setFont(font)
        self.__selectNexAgent.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__selectNexAgent.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        groupBox_3 = QtWidgets.QGroupBox(parent=tab_2)
        groupBox_3.setGeometry(QtCore.QRect(190, 10, 381, 241))
        groupBox_3.setTitle("基本信息")
        self.__editNexAgentName = QtWidgets.QLineEdit(parent=groupBox_3)
        self.__editNexAgentName.setGeometry(QtCore.QRect(10, 60, 181, 31))
        self.__editNexAgentName.setText("")
        self.__editNexAgentName.setMaxLength(12)
        self.__editNexAgentName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label_3 = QtWidgets.QLabel(parent=groupBox_3)
        label_3.setGeometry(QtCore.QRect(10, 30, 131, 21))
        label_3.setText("姓名（可修改）")
        label_4 = QtWidgets.QLabel(parent=groupBox_3)
        label_4.setGeometry(QtCore.QRect(10, 100, 151, 21))
        label_4.setText("特工专长及等级")
        self.__showNexAgentSpecialization = QtWidgets.QLineEdit(parent=groupBox_3)
        self.__showNexAgentSpecialization.setGeometry(QtCore.QRect(10, 130, 181, 31))
        self.__showNexAgentSpecialization.setText("")
        self.__showNexAgentSpecialization.setMaxLength(12)
        self.__showNexAgentSpecialization.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__showNexAgentSpecialization.setReadOnly(True)
        self.__showNexAgentLocation = QtWidgets.QLineEdit(parent=groupBox_3)
        self.__showNexAgentLocation.setGeometry(QtCore.QRect(10, 200, 181, 31))
        self.__showNexAgentLocation.setText("")
        self.__showNexAgentLocation.setMaxLength(12)
        self.__showNexAgentLocation.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__showNexAgentLocation.setReadOnly(True)
        label_5 = QtWidgets.QLabel(parent=groupBox_3)
        label_5.setGeometry(QtCore.QRect(10, 170, 131, 21))
        label_5.setText("所处殖民地")
        self.__selectNexAgentGender = QtWidgets.QComboBox(parent=groupBox_3)
        self.__selectNexAgentGender.setGeometry(QtCore.QRect(260, 200, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.__selectNexAgentGender.setFont(font)
        self.__selectNexAgentGender.addItem("男")
        self.__selectNexAgentGender.addItem("女")
        groupBox_4 = QtWidgets.QGroupBox(parent=tab_2)
        groupBox_4.setGeometry(QtCore.QRect(400, 30, 151, 171))
        groupBox_4.setTitle("头像")
        self.__showNexAgentPortrait = QtWidgets.QLabel(parent=groupBox_4)
        self.__showNexAgentPortrait.setGeometry(QtCore.QRect(10, 30, 131, 131))
        self.__showNexAgentPortrait.setText("")
        self.__showNexAgentPortrait.setScaledContents(True)
        label_6 = QtWidgets.QLabel(parent=tab_2)
        label_6.setGeometry(QtCore.QRect(400, 210, 51, 31))
        label_6.setText("性别")
        self.__selectFunction.addTab(tab_2, "[势力争霸]特工头像修改")
        groupBox_5 = QtWidgets.QGroupBox(parent=centralwidget)
        groupBox_5.setGeometry(QtCore.QRect(10, 320, 591, 271))
        groupBox_5.setTitle("头像更换管理")
        label_7 = QtWidgets.QLabel(parent=groupBox_5)
        label_7.setGeometry(QtCore.QRect(10, 30, 161, 21))
        label_7.setText("Mod选择")
        label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label_8 = QtWidgets.QLabel(parent=groupBox_5)
        label_8.setGeometry(QtCore.QRect(190, 30, 161, 21))
        label_8.setText("头像选择")
        label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.__selectModList = QtWidgets.QListWidget(parent=groupBox_5)
        self.__selectModList.setGeometry(QtCore.QRect(10, 60, 161, 201))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.__selectModList.setFont(font)
        self.__selectModList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.__selectPortraitInMod = QtWidgets.QListWidget(parent=groupBox_5)
        self.__selectPortraitInMod.setGeometry(QtCore.QRect(190, 60, 161, 201))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.__selectPortraitInMod.setFont(font)
        self.__selectPortraitInMod.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.__selectPortraitInMod.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        groupBox_6 = QtWidgets.QGroupBox(parent=groupBox_5)
        groupBox_6.setGeometry(QtCore.QRect(360, 30, 221, 61))
        groupBox_6.setTitle("性别筛选")
        self.__radioGender_man = QtWidgets.QRadioButton(parent=groupBox_6)
        self.__radioGender_man.setGeometry(QtCore.QRect(10, 30, 61, 19))
        self.__radioGender_man.setText("男性")
        self.__radioGender_woman = QtWidgets.QRadioButton(parent=groupBox_6)
        self.__radioGender_woman.setGeometry(QtCore.QRect(80, 30, 61, 19))
        self.__radioGender_woman.setText("女性")
        self.__radioGender_all = QtWidgets.QRadioButton(parent=groupBox_6)
        self.__radioGender_all.setGeometry(QtCore.QRect(150, 30, 61, 19))
        self.__radioGender_all.setText("所有")
        genderGroup = QtWidgets.QButtonGroup(groupBox_6)
        genderGroup.addButton(self.__radioGender_man, 0)
        genderGroup.addButton(self.__radioGender_all, 2)
        genderGroup.addButton(self.__radioGender_woman, 1)
        groupBox_7 = QtWidgets.QGroupBox(parent=groupBox_5)
        groupBox_7.setGeometry(QtCore.QRect(360, 90, 221, 61))
        groupBox_7.setTitle("势力筛选")
        self.__radioFaction_player = QtWidgets.QRadioButton(parent=groupBox_7)
        self.__radioFaction_player.setGeometry(QtCore.QRect(10, 30, 101, 19))
        self.__radioFaction_player.setText("仅限玩家")
        self.__radioFaction_all = QtWidgets.QRadioButton(parent=groupBox_7)
        self.__radioFaction_all.setGeometry(QtCore.QRect(150, 30, 61, 19))
        self.__radioFaction_all.setText("所有")
        factionGroup = QtWidgets.QButtonGroup(groupBox_7)
        factionGroup.addButton(self.__radioFaction_player, 0)
        factionGroup.addButton(self.__radioFaction_all, 1)
        self.__randomSelectPortraitButton = QtWidgets.QPushButton(parent=groupBox_5)
        self.__randomSelectPortraitButton.setGeometry(QtCore.QRect(370, 160, 201, 41))
        self.__randomSelectPortraitButton.setText("随机挑选头像")
        self.__saveAndExitButton = QtWidgets.QPushButton(parent=groupBox_5)
        self.__saveAndExitButton.setGeometry(QtCore.QRect(370, 220, 201, 41))
        self.__saveAndExitButton.setText("保存存档并退出")
        self.setCentralWidget(centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)
        # 事件绑定区
        factionGroup.idClicked['int'].connect(lambda i: self.__factionSelection(i))
        genderGroup.idClicked['int'].connect(lambda i: self.__genderSelection(i))
        self.__randomSelectPortraitButton.clicked['bool'].connect(lambda b: self.__randomChoicePortrait())
        self.__saveAndExitButton.clicked['bool'].connect(lambda b: self.__saveAndExit())
        self.__selectAIAdmin.currentRowChanged['int'].connect(lambda i: self.__showPersonInfo())
        self.__selectNexAgent.currentRowChanged['int'].connect(lambda i: self.__showPersonInfo())
        self.__selectModList.currentRowChanged['int'].connect(lambda i: self.__flashModPortraits())
        self.__selectPortraitInMod.currentRowChanged['int'].connect(lambda i: self.__showSelectPortrait())
        self.__selectNexAgentGender.currentIndexChanged['int'].connect(lambda i: self.__updatePersonInfo('gender'))
        self.__editNexAgentName.textEdited['QString'].connect(lambda s: self.__updatePersonInfo('name'))
        self.__editAIAdminName.textEdited['QString'].connect(lambda s: self.__updatePersonInfo('name'))
        # 变量储存区
        self.__currentSaveFile: saveFileUnit = None
        self.__genderID = 0
        self.__factionID = 0
        self.__cache_nameToIDs = {}
        self.__cache_AIAdmins: List[AIAdminPerson] = []
        self.__cache_NexAgents: List[NexAgentPerson] = []
        self.__cache_currentPortraitMod: portraitModUnit = None
        self.__cache_AllPortraitsIndex = []
        self.__cache_AllPortraits_show = []
        # 标志区
        self.__flag_progressing = False # 临界区标志，作用是临时关闭对应事件的处理
        self.__flag_reduceRadio = False

    def __genderSelection(self, selectID: int):
        if self.__flag_reduceRadio:
            return
        self.__genderID = selectID
        self.__flashModPortraits()

    def __factionSelection(self, selectID: int):
        if self.__flag_reduceRadio:
            return
        self.__factionID = selectID
        self.__flashModPortraits()

    def __randomChoicePortrait(self):
        pass

    def __saveAndExit(self):
        if self.__currentSaveFile is not None:
            self.__currentSaveFile.CloseSaveFile()
        self.close()
        mainApp.exit(0)

    def __flashModPortraits(self):
        """设计用于用户选择mod名字后，填充mod的头像列表到可选部分，并设置第一位"""
        currentRowStr = self.__selectModList.currentItem().text()
        self.__selectPortraitInMod.clear()
        if currentRowStr == '所有':
            self.__selectPortraitInMod.addItems(self.__cache_AllPortraits_show)
            self.SetFactionRadioGroupEnable(False)
            self.SetGenderRadioGroupEnable(False)
            self.__flag_reduceRadio = True
            self.__radioFaction_all.setChecked(True)
            self.__factionID = 1
            self.__radioGender_all.setChecked(True)
            self.__genderID = 2
            self.__flag_reduceRadio = False
        elif self.__cache_nameToIDs.get(currentRowStr) in cache_PublicModPortraits:
            self.__cache_currentPortraitMod = cache_PublicModPortraits[self.__cache_nameToIDs.get(currentRowStr)]


    def __showSelectPortrait(self):
        """选择具体的头像名字后，显示出来，改动即时生效"""
        if self.__selectModList.currentRow() != 0:
            if self.__cache_currentPortraitMod is not None:
                dataList = self.__easyGetListData(self.__cache_currentPortraitMod)
                dataUnit = dataList[self.__selectPortraitInMod.currentRow()]
                portraitPath = self.__cache_currentPortraitMod.PathJoin(dataUnit)
                if self.__selectFunction.currentIndex() == 1:
                    self.__showNexAgentPortrait.setPixmap(QtGui.QPixmap(portraitPath))
                else:
                    self.__showAIAdminPortrait.setPixmap(QtGui.QPixmap(portraitPath))

    def __showPersonInfo(self):
        pass

    def __updatePersonInfo(self, toUpdate: str):
        """
        更新个人信息，通过使用currentIndex来区分。

        :param toUpdate: 一些辅助信息（因为所有文本框都关联到同一个函数来了）
        """
        pass

    def OpenSaveFile(self, newSaveFile: saveFileUnit):
        """
        打开一个指定的存档文件，这是前台与后台的协同。

        :param newSaveFile: 待打开的存档文件。
        """
        self.__currentSaveFile = newSaveFile
        newSaveFile.OpenSaveFile()
        self.show()
        self.__cache_AIAdmins = newSaveFile.GetAIAdminData()
        self.__cache_NexAgents = newSaveFile.GetNexAgentData()
        cache_modIDs = newSaveFile.GetPortraitsModIDs()
        cache_modIDs.append('core')
        offset = 0
        # 填充Mod列表
        for unit in cache_modIDs:
            if unit in cache_PublicModPortraits:
                self.__cache_nameToIDs[cache_PublicModPortraits[unit].Name] = unit
                dataList = cache_PublicModPortraits[unit].ListGlobalPortraits(ignoreGender=True)
                self.__cache_AllPortraitsIndex.append({'id': unit, 'offset': offset, 'data': dataList})
                offset += len(dataList)
                self.__cache_AllPortraits_show += dataList
        # 产生适用于“所有”的特殊portrait列表
        self.__selectModList.addItem('所有')  # 特殊选项，将会有特殊效果
        self.__selectModList.addItems(list(self.__cache_nameToIDs.keys()))
        self.__selectModList.setCurrentRow(0)

    def SetGenderRadioGroupEnable(self, enable: bool = True):
        self.__radioGender_all.setEnabled(enable)
        self.__radioGender_man.setEnabled(enable)
        self.__radioGender_woman.setEnabled(enable)

    def SetFactionRadioGroupEnable(self, enable: bool = True):
        self.__radioFaction_all.setEnabled(enable)
        self.__radioFaction_player.setEnabled(enable)

    def __easyGetListData(self, toGetUnit: portraitModUnit):
        if self.__genderID == 2:
            match self.__factionID:
                case 0:
                    return toGetUnit.ListPlayerFactionPortraits(ignoreGender=True)
                case 1:
                    return toGetUnit.ListGlobalPortraits(ignoreGender=True)
        else:
            match self.__factionID:
                case 0:
                    return toGetUnit.ListPlayerFactionPortraits(genderMan=True if self.__genderID == 0 else False)
                case 1:
                    return toGetUnit.ListGlobalPortraits(genderMan=True if self.__genderID == 0 else False)


if __name__ == '__main__':
    mainApp = QtWidgets.QApplication(sys.argv)
    mainWin = starsectorSaveEditor()
    # 先进行一个内容判断
    if not (isfile('starsector.exe') and isdir('starsector-core') and isfile('vmparams')):
        QtWidgets.QMessageBox.critical(mainWin, '错误', '请将本程序放入远行星号游戏的根目录！')
        exit(0)
    elif not isdir('saves'):
        QtWidgets.QMessageBox.information(mainWin, '问题', '没有找到存档文件夹，无需采取进一步操作。')
        exit(0)
    loadDialog = preDialog(mainWin)
    loadDialog.show()
    mainApp.exec()
