from PyQt4.QtGui import *
from PyQt4.QtCore import *

from lib import newIcon, labelValidator

BB = QDialogButtonBox

class LabelDialog(QDialog):

    def __init__(self, text="", parent=None, listItem=['Unknown'], poseListItem=['Unspecified']):
        super(LabelDialog, self).__init__(parent)

        self.truncatedCheckBox = QCheckBox('Truncated', self)
        self.truncatedCheckBox.setTristate(False)
        self.truncatedCheckBox.setCheckState(Qt.Unchecked)

        self.occludedCheckBox = QCheckBox('Occluded', self)
        self.occludedCheckBox.setTristate(False)
        self.occludedCheckBox.setCheckState(Qt.Unchecked)
        
        self.listWidget = QListWidget(self)
        for item in listItem:
            self.listWidget.addItem(item)
            
        self.poseListWidget = QListWidget(self)
        for item in poseListItem:
            self.poseListWidget.addItem(item)
        self.poseListWidget.setCurrentRow(0)

        self.edit = QLineEdit()
        self.edit.setValidator(labelValidator())

        self.pose = QLineEdit()
        self.pose.setValidator(labelValidator())

#        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
#        bb.button(BB.Ok).setIcon(newIcon('done'))
#        bb.button(BB.Cancel).setIcon(newIcon('undo'))
#        bb.accepted.connect(self.accept)
#        bb.rejected.connect(self.reject)
        
        # Layout
        layout = QVBoxLayout()
        
        listWidgets = QHBoxLayout()
        listWidgets.addWidget(self.listWidget)
        listWidgets.addWidget(self.poseListWidget)
        layout.addLayout(listWidgets)

        editWidgets = QHBoxLayout()
        editWidgets.addWidget(self.edit)
        editWidgets.addWidget(self.pose)
        layout.addLayout(editWidgets)

        checkBoxes = QHBoxLayout()
        checkBoxes.addWidget(self.occludedCheckBox)
        checkBoxes.addWidget(self.truncatedCheckBox)
        layout.addLayout(checkBoxes)

#        layout.addWidget(bb)
        
        self.setLayout(layout)

    def keyPressEvent(self, tQKeyEvent):
        k = tQKeyEvent.key()
        if k == Qt.Key_Enter or k == Qt.Key_Return:
            if self.pose.text().trimmed() or self.edit.text().trimmed():
                self.addItemToList(self.poseListWidget, self.pose)
                self.addItemToList(self.listWidget, self.edit)
            else:
                self.accept()
        elif k == Qt.Key_Escape:
            self.reject()

            
#    def validate(self):
#        if self.edit.text().trimmed():
#            self.accept()
#        self.reject()
        
    def addItemToList(self, tQListWidget, tQLineEdit):
        if tQLineEdit.text().trimmed():
            tQListWidget.insertItem(0, tQLineEdit.text().trimmed())
            tQListWidget.setCurrentRow(0)
            tQLineEdit.clear()
        
    def popUp(self, text='', attr=None, move=True):
#        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)

        if attr is not None:
#            self.pose.setText(attr['pose'])
            self.occludedCheckBox.setCheckState(Qt.Checked if 1 == attr['occluded'] else Qt.Unchecked)
            self.truncatedCheckBox.setCheckState(Qt.Checked if 1 == attr['truncated'] else Qt.Unchecked)
            items = self.poseListWidget.findItems(attr['pose'], Qt.MatchExactly)
            if len(items) > 0:
                self.poseListWidget.setCurrentItem(items[0])
        
        if move:
            self.move(QCursor.pos())

        if self.exec_():
            cls = self.listWidget.currentItem().text().trimmed()
            pose = self.poseListWidget.currentItem().text().trimmed()
            occluded = int(self.occludedCheckBox.isChecked())
            truncated = int(self.truncatedCheckBox.isChecked())
            return cls, {'pose': pose, 'occluded': occluded, 'truncated': truncated}
        else:
            return None, {}

            
