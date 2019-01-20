import motorlib

import math

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox, QComboBox
from PyQt5.QtCore import pyqtSignal

class propertyEditor(QWidget):

    valueChanged = pyqtSignal()

    def __init__(self, parent, prop, preferences):
        super(propertyEditor, self).__init__(QWidget(parent))
        self.preferences = preferences
        self.setLayout(QVBoxLayout())
        self.prop = prop

        if self.preferences is not None:
            self.dispUnit = self.preferences.getUnit(self.prop.unit)
        else:
            self.dispUnit = self.prop.unit

        if type(prop) is motorlib.propellantProperty:
            pass

        elif type(prop) is motorlib.floatProperty:
            self.editor = QDoubleSpinBox()
            self.editor.setValue(motorlib.convert(self.prop.getValue(), prop.unit, self.dispUnit))
            self.editor.setSuffix(' ' + self.dispUnit)

            convMin = motorlib.convert(self.prop.min, self.prop.unit, self.dispUnit)
            convMax = motorlib.convert(self.prop.max, self.prop.unit, self.dispUnit)
            self.editor.setRange(convMin, convMax)

            self.editor.setDecimals(6) # Large number of decimals for now while I pick a better method
            self.editor.setSingleStep(10 ** (int(math.log(convMax, 10) - 4)))

            self.editor.valueChanged.connect(self.valueChanged.emit)
            self.layout().addWidget(self.editor)

        elif type(prop) is motorlib.intProperty:
            self.editor = QSpinBox()
            self.layout().addWidget(self.editor)

        elif type(prop) is motorlib.enumProperty:
            self.editor = QComboBox()

            self.editor.addItems(self.prop.values)
            self.editor.setCurrentText(self.prop.value)
            self.editor.currentTextChanged.connect(self.valueChanged.emit)

            self.layout().addWidget(self.editor)


    def getValue(self):
        if type(self.prop) is motorlib.propellantProperty:
            pass

        elif type(self.prop) is motorlib.floatProperty:
            return motorlib.convert(self.editor.value(), self.dispUnit, self.prop.unit)

        elif type(self.prop) is motorlib.intProperty:
            pass

        elif type(self.prop) is motorlib.enumProperty:
            return self.editor.currentText()