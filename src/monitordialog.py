from datetime import datetime
import sys

from globalsignals import global_signals
from ui_monitordialog import Ui_MonitorDialogClass

import ax25
from PySide6 import QtWidgets
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QDialog, QInputDialog

class MonitorDialog(QDialog,Ui_MonitorDialogClass):
    def __init__(self,pd,parent=None):
        super().__init__(parent)
        self.pd = pd
        self.setupUi(self)
        global_signals.signal_monitor_msg_ax25.connect(self.on_msg)
        self.c_text.setReadOnly(True)

    def on_msg(self,msg:bytes):
        frame = ax25.Frame.unpack(msg)
        now = datetime.now()
        line = f"[{now.strftime("%H:%M:%S.%f")}] {frame.src.call}"
        if frame.src.ssid: line += f"-{frame.src.ssid}"
        line += f">{frame.dst.call}"
        if frame.dst.ssid: line += f"-{frame.dst.ssid}"
        via = frame.via
        if via:
            line += " via "
            line += " ".join([str(v) for v in via])
        control = frame.control
        ft = control.frame_type
        line += f":({ft.name}"
        if frame.dst.command_response and not frame.src.command_response: line += " cmd"
        elif not frame.dst.command_response and frame.src.command_response: line += " res"
        else: line += " !!!"
        if ft.is_I():
            line += f", n(s)={control.send_seqno}"
        if not ft.is_U():
            line += f", n(r)={control.recv_seqno}"
        line += f", p={1 if control.poll_final else 0}"
        if ft is ax25.FrameType.I or ft is ax25.FrameType.UI:
            line += f", pid={frame.pid:02X}, len={len(frame.data)}) {frame.data}"
        else:
            line += ")"
        line += "\r\n"
        self.c_text.textCursor().movePosition(QTextCursor.End)
        self.c_text.insertPlainText(line)
        self.c_text.ensureCursorVisible()


