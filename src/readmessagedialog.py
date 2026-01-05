import sys

from PySide6 import QtWidgets
from PySide6.QtCore import QDateTime, Signal
from PySide6.QtWidgets import QMainWindow

from globalsignals import global_signals
from persistentdata import PersistentData
from sql_mailbox import MailBoxHeader
from ui_readmessagedialog import Ui_ReadMessageDialogClass

class ReadMessageDialog(QMainWindow,Ui_ReadMessageDialogClass):
    def __init__(self,pd,parent=None):
        super().__init__(parent)
        self.pd = pd
        self.setupUi(self)
        self.actionSave.triggered.connect(self.on_save)
        self.actionSame_Message_ID.triggered.connect(lambda: self.on_resend(False))
        self.actionNew_Message_ID.triggered.connect(lambda: self.on_resend(True))
        self.mbh = None
        self.m = None

    def on_save(self):
        pass

    def on_resend(self,newid): # new IF not yet supported
        global_signals.signal_resend_text_messasge.emit(self.mbh,self.m)
        self.close()

    def prepopulate(self,mbh:MailBoxHeader,m:str):
        self.c_bbs.setText(mbh.bbs)
        self.c_from.setText(mbh.from_addr)
        self.c_to.setText(mbh.to_addr)
        self.c_subject.setText(mbh.subject)
        self.c_received.setText(MailBoxHeader.to_outpost_date(mbh.date_received))
        self.c_sent.setText(MailBoxHeader.to_outpost_date(mbh.date_sent))
        self.c_local_id.setText(mbh.local_id)
        self.c_message_body.setPlainText(m)
        self.mbh = mbh 
        self.m = m


    def resizeEvent(self,event):
        self.c_message_body.resize(event.size().width()-20,event.size().height()-120)
        # these are a binch of attempts to fix up the scrollbars after a size change, none of them worked
        # self.c_message_body.document().adjustSize()
        # self.c_message_body.viewport().update()
        # self.c_message_body.updateGeometry()
        return super().resizeEvent(event)
    
