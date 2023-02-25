from PyQt5 import QtWidgets, uic
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice


app = QtWidgets.QApplication([])
ui = uic.loadUi("design.ui")
ui.setWindowTitle("поворотный стол")

serial = QSerialPort()
serial.setBaudRate(115200)
portList = []
ports = QSerialPortInfo().availablePorts()
for port in ports:
    portList.append(port.portName())
ui.comL.addItems(portList)

posX = 200
posY = 100
listX = []
for x in range(100): listX.append(x)
listY = []
for x in range(100): listY.append(0)

#с ардуино на пк, терминтаор \n
# 0,
# 1,
# 2,

# с пк на ардуино, терминтаор ;
#
# 1,servo1,servo2,speed
# 2,servo2
# 3
# 4,servo1
# 5,speed

def onRead():
    if not serial.canReadLine(): return     # выходим если нечего читать
    rx = serial.readLine()
    rxs = str(rx, 'utf-8').strip()
    data = rxs.split(',')
    if data[0] == '1':
        ui.textB.setText(str(rxs))
def onOpen():
    serial.setPortName(ui.comL.currentText())
    serial.open(QIODevice.ReadWrite)


def serialSend(data):
    txs = ""
    for val in data:
        txs += str(val)
        txs += ','
    txs = txs[:-1]
    txs += ';'
    serial.write(txs.encode())


def onClose():
    serial.close()



def multicontrol():
    ui.servo1SB.setValue(ui.servo1S.value())
    ui.servo2SB.setValue(ui.servo2S.value())
    ui.speedSB.setValue(ui.speedS.value())
    servo1 = ui.servo1SB.value()
    servo2 = ui.servo2SB.value()
    speed = ui.speedSB.value()
    serialSend([0, servo1, servo2, speed])
    ui.lcdservo1.display(servo1)
    ui.lcdservo2.display(servo2)
    ui.lcdspeed.display(speed)


serial.readyRead.connect(onRead)
ui.openB.clicked.connect(onOpen)
ui.closeB.clicked.connect(onClose)

ui.servo1S.valueChanged.connect(multicontrol)
ui.servo2S.valueChanged.connect(multicontrol)
ui.speedS.valueChanged.connect(multicontrol)


ui.show()
app.exec()