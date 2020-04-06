import naver_shopping.stage_naver_shopping as ns
import libs.naver_shopping.parser as par
import sys
# GUI 를 구성하기 위한 라이브러리
from PyQt5.QtWidgets import *
# GUI 에 아이콘을 넣기 위한 라이브러리
from PyQt5.QtGui import QIcon
# UI 가 없는 응용프로그램의 상태를 조작하기 위한 라이브러리
from PyQt5.QtCore import QCoreApplication


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 조건에 따른 라디오 버튼 및 그룹 생성
        global choose

        self.radioButton1 = QRadioButton('기본')
        self.radioButton1.setChecked(True)
        self.radioButton1.clicked.connect(self.radioFunction)
        self.radioButton2 = QRadioButton('낮은 가격순')
        self.radioButton2.clicked.connect(self.radioFunction)
        self.radioButton3 = QRadioButton('등록일순')
        self.radioButton3.clicked.connect(self.radioFunction)
        self.radioButton4 = QRadioButton('리뷰 많은순')
        self.radioButton4.clicked.connect(self.radioFunction)

        self.vBox = QVBoxLayout()
        self.vBox.addWidget(self.radioButton1)
        self.vBox.addWidget(self.radioButton2)
        self.vBox.addWidget(self.radioButton3)
        self.vBox.addWidget(self.radioButton4)

        self.radioGroup = QGroupBox('조건선택', self)
        self.radioGroup.setLayout(self.vBox)

        # 검색어 입력칸 생성
        self.inputKeyword = QLineEdit()

        # 검색어 출력칸 생성
        self.outputKeyword = QTextBrowser()
        self.outputKeyword.setAcceptRichText(True)
        self.outputKeyword.setOpenExternalLinks(True)

        # 개발자 정보칸 생성
        self.infoKeyword = QTextBrowser()
        self.infoKeyword.setAcceptRichText(True)
        self.infoKeyword.setOpenExternalLinks(True)

        info1 = "개발자 메일 : wjehd9@naver.com\n"
        info2 = "<다음과 같은 순서를 반드시 지켜주세요!>\n"
        info3 = "1. 저장할 파일의 위치 지정을 먼저합니다.\n"
        info4 = "2. 검색어에 원하는 내용을 입력합니다.\n"
        info5 = "3. 검색할 조건을 지정합니다.\n"
        info6 = "4. 검색 및 저장 버튼을 누릅니다.\n"
        info7 = "# 초기화 버튼으로 연관 검색어 기록을 없앨 수 있습니다.\n"
        info8 = "사용 환경에 따라 멈춤 현상이 일어날 수 있습니다.\n"
        info9 = "기타 문의 사항은 위 메일로 보내주시기 바랍니다.\n"
        info10 = "*너무 자주 실행 시 네이버에서 DDOS로 인식될 수 있습니다.*\n"
        info11 = "제작일 : 2020.04.06\n"

        self.infoKeyword.append(info1)
        self.infoKeyword.append(info2)
        self.infoKeyword.append(info3)
        self.infoKeyword.append(info4)
        self.infoKeyword.append(info5)
        self.infoKeyword.append(info6)
        self.infoKeyword.append(info7)
        self.infoKeyword.append(info8)
        self.infoKeyword.append(info9)
        self.infoKeyword.append(info10)
        self.infoKeyword.append(info11)

        # Quit 버튼 생성
        self.quitButton = QPushButton('종료', self)
        self.quitButton.resize(self.quitButton.sizeHint())
        self.quitButton.clicked.connect(QCoreApplication.instance().quit)

        # Search 버튼 생성
        self.searchButton = QPushButton('검색 및 저장', self)
        self.searchButton.resize(self.searchButton.sizeHint())
        self.searchButton.pressed.connect(self.search_object)
        self.searchButton.setEnabled(False)

        # clear 버튼 생성
        self.clearButton = QPushButton('초기화', self)
        self.clearButton.resize(self.clearButton.sizeHint())
        self.clearButton.pressed.connect(self.clear_object)

        # 저장 버튼 생성
        self.saveButton = QPushButton('위치 지정', self)
        self.saveButton.resize(self.saveButton.sizeHint())
        self.saveButton.pressed.connect(self.save_directory)

        # Grid 레이아웃 생성
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.grid.addWidget(QLabel('검색어'), 0, 0)
        self.grid.addWidget(QLabel('검색 조건'), 1, 0)
        self.grid.addWidget(QLabel('연관 검색어'), 2, 0)
        self.grid.addWidget(self.quitButton, 3, 0)

        self.grid.addWidget(self.inputKeyword, 0, 1)
        self.grid.addWidget(self.radioGroup, 1, 1)
        self.grid.addWidget(self.outputKeyword, 2, 1)
        self.grid.addWidget(self.searchButton, 3, 1)

        self.grid.addWidget(self.saveButton, 0, 2)
        self.grid.addWidget(self.infoKeyword, 1, 2, 2, 2)
        self.grid.addWidget(self.clearButton, 3, 2)

        # GUI 의 크기와 위치, 이름을 정의
        self.setWindowTitle('Naver Shopping Crawler (made by Aerotic)')
        self.setWindowIcon(QIcon('A.png'))
        self.setGeometry(300, 300, 700, 500)
        self.show()

    def radioFunction(self):
        if self.radioButton1.isChecked():
            self.choose = 1
        if self.radioButton2.isChecked():
            self.choose = 2
        if self.radioButton3.isChecked():
            self.choose = 3
        if self.radioButton4.isChecked():
            self.choose = 4

    def search_object(self):
        self.outputKeyword.clear()
        text = self.inputKeyword.text()
        condition = self.choose
        ns.doing(text, condition, position)
        for p in par.relation:
            self.outputKeyword.append(p)
        self.inputKeyword.clear()

    def clear_object(self):
        self.outputKeyword.clear()

    def save_directory(self):
        global position
        position = QFileDialog.getExistingDirectory(self, self.tr("Open"), "./", QFileDialog.ShowDirsOnly)
        self.searchButton.setEnabled(True)


# __main__ :  현재 모듈의 이름이 저장되는 내장 변수
# 다른 파일의 코드를 가져오기 위해서는 import 작업이 우선되어야 한다.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

    # pyinstaller -w -F --icon=test.ico --onefile test.py
