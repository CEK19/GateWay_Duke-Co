function vDHT11 () {
    dht11_dht22.queryData(
    DHTtype.DHT11,
    DigitalPin.P0,
    true,
    false,
    true
    )
    humid_var = dht11_dht22.readData(dataType.humidity)
    temp_var = dht11_dht22.readData(dataType.temperature)
    NPNLCD.ShowString("Temp: " + ("" + temp_var) + " ", 0, 0)
    NPNLCD.ShowString("Humid: " + ("" + humid_var) + " ", 0, 1)
    serial.writeString("!VISUAL_TEMP:" + ("" + temp_var) + "#")
    serial.writeString("!VISUAL_HUMID:" + ("" + humid_var) + "#")
}
function toggleSignal (oldSign: number) {
    if (oldSign == 1) {
        return 0
    }
    return 1
}
serial.onDataReceived(serial.delimiters(Delimiters.Hash), function () {
    // rcvMsg = !FIED:VALUE#
    receivedMsg = serial.readUntil(serial.delimiters(Delimiters.Hash))
    receivedMsg = "" + receivedMsg.slice(1)
    splitData = receivedMsg.split(":")
    if (splitData[0] == "CTRL_LOCK") {
        if (splitData[1] == "0") {
            vCtrlLock(false)
        } else {
            vCtrlLock(true)
        }
    }
    if (splitData[0] == "CTRL_FRBUZZ") {
        if (splitData[1] == "0") {
            NPNLCD.ShowString("CLOSE-FR" + " ", 0, 0)
            buzzFraud = 0
        } else {
            NPNLCD.ShowString("OPEN-FR" + " ", 0, 0)
            buzzFraud = 1
        }
        vCheckFraud()
    }
    if (splitData[0] == "CTRL_FBUZZ") {
        if (splitData[1] == "0") {
            NPNLCD.ShowString("CLOSE-F" + " ", 0, 0)
            buzzFire = 0
        } else {
            NPNLCD.ShowString("OPEN-F" + " ", 0, 0)
            buzzFire = 1
        }
        vFireNotify()
    }
})
function vCtrlLock (open2: boolean) {
    if (open2) {
        servos.P2.setAngle(180)
        lockState = 1
    } else {
        servos.P2.setAngle(0)
        lockState = 0
    }
}
function vFireNotify () {
    ana_gasSignal = pins.analogReadPin(AnalogPin.P3)
    serial.writeString("!VISUAL_GAS:" + ("" + ana_gasSignal) + "#")
    if (ana_gasSignal >= 400) {
        serial.writeString("!VISUAL_WARFIRE:" + "1" + "#")
        if (buzzFire == 1) {
            // Chỗ này cắm Buzzer vô
            pins.analogWritePin(AnalogPin.P4, 700)
        } else {
            pins.analogWritePin(AnalogPin.P4, 0)
        }
    } else {
        serial.writeString("!VISUAL_WARFIRE:" + "0" + "#")
        pins.analogWritePin(AnalogPin.P4, 0)
    }
}
function vCheckFraud () {
    if (NPNBitKit.ButtonDoorOpen(DigitalPin.P6) && lockState == 0) {
        serial.writeString("!VISUAL_WARFRAUD:" + "1" + "#")
        if (buzzFraud == 1) {
            // Chỗ này cắm Buzzer vô
            pins.analogWritePin(AnalogPin.P10, 487)
        } else {
            // Chỗ này cắm Buzzer vô
            pins.analogWritePin(AnalogPin.P10, 0)
        }
    } else {
        serial.writeString("!VISUAL_WARFRAUD:" + "0" + "#")
        // Chỗ này cắm Buzzer vô
        pins.analogWritePin(AnalogPin.P10, 0)
    }
}
let clk_count = 0
let ana_gasSignal = 0
let splitData: string[] = []
let temp_var = 0
let humid_var = 0
let buzzFraud = 0
let buzzFire = 0
let lockState = 0
let receivedMsg = ""
// Để có thêm tài nguyên cho chuyện khác
led.enable(false)
NPNLCD.LcdInit()
servos.P2.setAngle(0)
lockState = 0
buzzFire = 1
buzzFraud = 1
basic.forever(function () {
    clk_count = (clk_count + 1) % 3
    if (clk_count == 0) {
        vDHT11()
    }
    if (clk_count == 1) {
        vFireNotify()
    }
    if (clk_count == 2) {
        vCheckFraud()
    }
    basic.pause(7000)
})
