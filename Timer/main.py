import machine
import utime
from display import LCD
from rotary_irq_rp2 import RotaryIRQ

increment = 0.2
max_time = 120
test_time = 2
delay_int = 74500
test_loop = 0

relay = machine.Pin(10, machine.Pin.OUT)
focus_button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
enlarge_button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
test_button = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)
r_button = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)
r = RotaryIRQ(pin_num_clk=13, pin_num_dt=12, min_val=0, max_val=max_time*(1/increment), range_mode=RotaryIRQ.RANGE_BOUNDED)
display = LCD()

display.init()
display.set_line(0)
display.set_string("Time: " + str(0.0) + "s")
val_old = r.value()
focus = False
relay.value(0)

if test_loop >> 0:
    test_times = []
    for _ in range(test_loop):
        countdown = round(test_time, 1)
        display.clear()
        display.set_line(1)
        display.set_string("Teststrip: " + str(countdown) + "s")
        start_time = utime.ticks_us()
        relay.value(1)
        while countdown >= 0:
            countdown -= 0.2
            display.set_line(0)
            display.set_string("Time: " + str(countdown) + "s")
            if r_button.value() == 0:
                break
            utime.sleep_us(delay_int)
            
        relay.value(0)
        test_times.append(utime.ticks_diff(utime.ticks_us(), start_time) / 1000000)
        display.clear()
        display.set_line(0)
        display.set_string("Time: " + str(round(val_old/(1/increment), 1)) + "s")
        
    print(test_times)
    test_average = 0
    for i in test_times:
        test_average += i
    test_average = test_average/len(test_times)
    print(test_average)

else:
    while True:
        val_new = r.value()
        
        if val_old != val_new:
            val_old = val_new
            display.set_line(0)
            display.set_string("Time: " + str(round(val_old/(1/increment), 1)) + "s")
            
        if focus_button.value() == 0:
            focus = not(focus)
            if focus:
                relay.value(1)
                display.set_line(1)
                display.set_string("Focusing")
            
            else:
                relay.value(0)
                display.clear()
                display.set_line(0)
                display.set_string("Time: " + str(round(val_old/(1/increment), 1)) + "s")
            
            while focus_button.value() == 0:
                utime.sleep_ms(1)
            
        if enlarge_button.value() == 0:
            if val_old >> 0 and not focus:
                countdown = round(val_old/(1/increment), 1)
                display.clear()
                display.set_line(1)
                display.set_string("Enlarging: " + str(countdown) + "s")
                start_time = utime.ticks_us()
                relay.value(1)
                while countdown >= 0:
                    countdown -= 0.2
                    display.set_line(0)
                    display.set_string("Time: " + str(countdown) + "s")
                    if r_button.value() == 0:
                        break
                    utime.sleep_us(delay_int)
                    
                relay.value(0)
                print(utime.ticks_diff(utime.ticks_us(), start_time) / 1000000)
                display.clear()
                display.set_line(0)
                display.set_string("Time: " + str(round(val_old/(1/increment), 1)) + "s")
                
        if test_button.value() == 0 and not focus:
            countdown = round(test_time, 1)
            display.clear()
            display.set_line(1)
            display.set_string("Teststrip: " + str(countdown) + "s")
            start_time = utime.ticks_us()
            relay.value(1)
            while countdown >= 0:
                countdown -= 0.2
                display.set_line(0)
                display.set_string("Time: " + str(countdown) + "s")
                if r_button.value() == 0:
                    break
                utime.sleep_us(delay_int)
                
            relay.value(0)
            print(utime.ticks_diff(utime.ticks_us(), start_time) / 1000000)
            display.clear()
            display.set_line(0)
            display.set_string("Time: " + str(round(val_old/(1/increment), 1)) + "s")
        utime.sleep_ms(20)

