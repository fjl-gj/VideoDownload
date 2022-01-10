# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pagesfAmbsx.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject)
from PySide6.QtWidgets import (QStackedWidget, QVBoxLayout,
                               QWidget)

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(861, 537)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.home_page.setStyleSheet(u"font-size: 14pt")
        self.page_1_layout = QVBoxLayout(self.home_page)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.home_page_all_config = QVBoxLayout()
        self.home_page_all_config.setObjectName(u"home_page_all_config")

        self.page_1_layout.addLayout(self.home_page_all_config)

        self.pages.addWidget(self.home_page)
        self.download_page = QWidget()
        self.download_page.setObjectName(u"download_page")
        self.page_2_layout = QVBoxLayout(self.download_page)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.download_page_all_config = QVBoxLayout()
        self.download_page_all_config.setObjectName(u"download_page_all_config")

        self.page_2_layout.addLayout(self.download_page_all_config)

        self.pages.addWidget(self.download_page)
        self.version_page = QWidget()
        self.version_page.setObjectName(u"version_page")
        self.version_page.setStyleSheet(u"QFrame {\n"
"                                font-size: 16pt;\n"
"                                }\n"
"                            ")
        self.page_3_layout = QVBoxLayout(self.version_page)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.pages.addWidget(self.version_page)
        self.setting_page = QWidget()
        self.setting_page.setObjectName(u"setting_page")
        self.verticalLayout_2 = QVBoxLayout(self.setting_page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.setting_page_all_config = QVBoxLayout()
        self.setting_page_all_config.setObjectName(u"setting_page_all_config")

        self.verticalLayout_2.addLayout(self.setting_page_all_config)

        self.pages.addWidget(self.setting_page)

        self.main_pages_layout.addWidget(self.pages)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
    # retranslateUi

