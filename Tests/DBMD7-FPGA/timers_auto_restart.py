
## Test ID:
USER_NAME = 'Bar'
FOLDER_PATH = r"C:\\Users\bar.kristal\Documents\GitHub\Python\Tests\DBMD7-FPGA\timers"
TEST_NAME = "timers_auto_restart"


#call the init.py module:
execfile(r"C:\Users\bar.kristal\Documents\GitHub\Python\init.py")
#######################################################################################



###### defines: ######

TIMER0_BASE = '50'
TIMER1_BASE = '58'
TIMER2_BASE = '90'
TIMER3_BASE = '98'

timer = 1   #set the TIMER to be tested
ITERATIONS = 3

if timer == 0:
	BASE = TIMER0_BASE
	MASK = 0x10
else:
	if timer == 1:
		BASE = TIMER1_BASE
		MASK = 0x8
	else:
		if timer == 2:
			BASE = TIMER2_BASE
			MASK = 0x400
		else:
			BASE = TIMER3_BASE
			MASK = 0x800

D7 = UartDeviceD7FPGA('DBMD4', 'COM5', baudrate=912600, bytesize=8, parity='N', stopbits=1,timeout=1)





#enable TIMERS_LP_EN and TIMERS23_EN:
D7.setbits('3000024', '110')




## auto restart count mode :
write_to_log("####auto-restart mode test on TIMER%d:####"%timer)

#TIMER_OUT_R cleared by setting CT, auto_restart mode:
D7.write_register(BASE +'00000', '4')
D7.setbits(BASE +'00004', '8')

#set timer value:
D7.write_register(BASE +'0000c', "8000000")
time.sleep(1)
write_to_log( D7.read_register(BASE +'00010') )
#start counting down
D7.setbits(BASE +'00004', '1')
time.sleep(1)

#clear TC:
D7.setbits(BASE + '00004', '4')
#clear TIMER0 interrupt at EICR
D7.write_register('200000c', 'ffff')
time.sleep(0.01)
interrupt0 = int(D7.read_register('2000004'),16)

timer_cc = D7.read_register(BASE +'00010')
timer_cc_prev = timer_cc
itr = 0
while (itr < ITERATIONS):
	time.sleep(1)
	write_to_log(timer_cc)
	timer_cc = D7.read_register(BASE +'00010')
	if (int(timer_cc, 16) > int(timer_cc_prev, 16)):
		itr += 1
		interrupt1 = int(D7.read_register('2000004'), 16)
		write_to_log("interrupt0: %x" % (interrupt0))
		write_to_log("interrupt1: %x" % (interrupt1))

		if (interrupt0 & MASK == 0 and interrupt1 & MASK == MASK):

			write_to_log("timer0 on single count mode PASSED")
		else:
			write_to_log("timer0 on single count mode FAILED")

		#clear TIMER0 interrupt at EICR
		D7.setbits(BASE + '00004', '4')
		D7.write_register('200000c', 'ffff')

	else:
		interrupt0 = int(D7.read_register('2000004'), 16)

	timer_cc_prev = timer_cc




