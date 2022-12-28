import hid      #allows access to every HID. to use, run pip install hidapi
import vgamepad #allows interface to the ViGEm driver. to use, run pip install vgamepad and run the installer (windows only)
import time

analog_brake = False

#run this to find the VID and PID of your device:
#for device in hid.enumerate():
#    print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

pedals = hid.device()
pedals.open(0x06a3, 0x2586)
pedals.set_nonblocking(True)
if(not pedals):
    print("SAITEK ERROR")
    exit()

virt_ctrler = vgamepad.VX360Gamepad()
if(not virt_ctrler):
    print("VIRTUAL CONTROLLER ERROR")
    exit()

while(True):
    report = pedals.read(64)
    if(not report):
        time.sleep(0.01) #sleep 10ms
        continue
    #run this to find the output format of your device:
    #print(report)
    
    #pedals go 52 (unpressed) to 0 (pressed)
    #rudder goes 52 to -52
    #brake goes 0 to 104
    left_pedal = 52-report[2]
    right_pedal = 52-report[3]
    rudder = left_pedal - right_pedal
    brake = left_pedal + right_pedal - abs(rudder)
    print(rudder , " " , brake)

    #the joystick accepts +32767 to -32768, so 32767 / 52 = 630
    #the trigger accepts 0 to 255, so 255 / 104 = 2.45
    virt_ctrler.left_joystick(rudder * 630, 0)
    if(analog_brake):
        virt_ctrler.left_trigger(int(brake * 2.45))
    else:
        if(brake > 52):
            virt_ctrler.press_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        else:
            virt_ctrler.release_button(button=vgamepad.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        
    virt_ctrler.update()
