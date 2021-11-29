if starting:   
	global mouse_sensitivity, sensitivity_center_reduction
	global recenterSpeed, steering_x, steering_y, steering_max, steering_min, steering_center_reduction, steering_center_reduction_l,activae_V,steering_center_reduction_lx,steering_center_reduction_ly 
	
	# =============================================================================================
	# //////////////////////////////////////// SETTINGS ///////////////////////////////////////////
	# =============================================================================================
	mouse_StickSensitivity = 1.2
	mouse_LookSensitivity = 1.5
	enable_freelook = True
	
	offsetSteer_x = 0
	offsetSteer_y = 200	#6400 for a 10
	offsetLook_x = 0
	offsetLook_y = 0		#-800 for a 10
	
	stick_recenterSpeed = 10	#0 to disable recentering
	look_recenterSpeed = 130
	
	DeviceNumber = 0 			#Counting starts from 0 so, 0 means device 1, 1 means device 2, etc.
	#==============================================================================================
	# /////////////////////////////////////////////////////////////////////////////////////////////
	# =============================================================================================

	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 5
	
	int32_max = (2 ** 14) - 1
	int32_min = (( 2** 14) * -1) + 1
	steering_x = 0.0
	steering_y = 0.0
	steering_max = float(int32_max)
	steering_min = float(int32_min)
	steering_center_reduction = 1.0
	steering_center_reduction_l = 1.0
	steering_center_reduction_lx=1.0
	steering_center_reduction_ly=1.0
	mouse_sensitivity = 0.5
	sensitivity_center_reduction =from dcs_common import *

if starting:   
	global mouse_sensitivity, sensitivity_center_reduction
	global recenterSpeed, steering_x, steering_y, steering_max, steering_min, steering_center_reduction, steering_center_reduction_l,activae_V,steering_center_reduction_lx,steering_center_reduction_ly 
	
	# =============================================================================================
	# //////////////////////////////////////// SETTINGS ///////////////////////////////////////////
	# =============================================================================================
	mouse_StickSensitivity = 1
	mouse_LookSensitivity = 0.7
	enable_freelook = True 		#Change to False if you want to disable free look
	
	offsetSteer_x = 0
	offsetSteer_y = 0	
	offsetLook_x = 0
	offsetLook_y = 0	
	
	stick_recenterSpeed = 10	#0 to disable recentering
	look_recenterSpeed = 200
	
	DeviceNumber = 0 			#Counting starts from 0 so, 0 means device 1, 1 means device 2, etc.
	#==============================================================================================
	# /////////////////////////////////////////////////////////////////////////////////////////////
	# =============================================================================================

	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 5
	
	int32_max = (2 ** 14) - 1
	int32_min = (( 2** 14) * -1) + 1
	steering_x = 0.0
	steering_y = 0.0
	steering_max = float(int32_max)
	steering_min = float(int32_min)
	steering_center_reduction = 1.0
	steering_center_reduction_l = 1.0
	steering_center_reduction_lx=1.0
	steering_center_reduction_ly=1.0
	mouse_sensitivity = 0.5
	sensitivity_center_reduction = 0.1
	switch = False
	active = True
	freeLook=False
	stickSteering = True
	v = vJoy[DeviceNumber]
	v.x = offsetSteer_x
	v.y = offsetSteer_y
	v.rx = offsetLook_x
	v.ry = offsetLook_y
	v.rz = 0
	
	def set_button(button, key):
		if keyboard.getKeyDown(key):
			v.setButton(button, True)
		else:
			v.setButton(button, False)
	
	def calculate_rate(max, time):
		if time > 0:
			return max / (time / system.threadExecutionInterval)
		else:
			return max
	
	def recenter(str, speed, offset):
		if(str>offset):
			if(str<offset+speed):
				str=offset
				return str
			else:
				str-=speed
				return str
		elif(str<offset):
			if(str>offset-speed):
				str=offset
				return str
			else:
				str+=speed
				return str
		return str
	
# =================================================================================================
# steering logic
# =================================================================================================
#freelook switching
freeLookHold = keyboard.getKeyDown(Key.LeftAlt)
freeLookToggle = keyboard.getPressed(Key.Grave)

if is_dcs_active():
	if active:
		if keyboard.getKeyDown(Key.NumberPad5):
			steering_y = 0
			steering_x = 0

		if steering_x > 0:
			steering_center_reduction = sensitivity_center_reduction ** (1 - (steering_x / steering_max))
		elif steering_x < 0:
			steering_center_reduction = sensitivity_center_reduction ** (1 - (steering_x / steering_min))
		steering_x = steering_x + ((float(mouse.deltaX) * mouse_sensitivity) / steering_center_reduction)
		if steering_x > steering_max:
			steering_x = steering_max
		elif steering_x < steering_min:
			steering_x = steering_min

		if steering_y > 0:
			steering_center_reduction_l = sensitivity_center_reduction ** (1 - (steering_y / steering_max))
		elif steering_y < 0:
			steering_center_reduction_l = sensitivity_center_reduction ** (1 - (steering_y / steering_min))
		steering_y = steering_y + ((float(mouse.deltaY) * mouse_sensitivity) / steering_center_reduction_l)
		if steering_y > steering_max:
			steering_y = steering_max
		elif steering_y < steering_min:
			steering_y = steering_min


		if(stickSteering):
			mouse_sensitivity=mouse_StickSensitivity
			if(switch==True):
				steering_x=v.x
				steering_y=v.y
			switch=False

			v.x = int(round(steering_x))
			v.y= int(round(steering_y))

			v.rx=recenter(v.rx,look_recenterSpeed,offsetLook_x)
			v.ry=recenter(v.ry,look_recenterSpeed,offsetLook_y)

			steering_x=recenter(steering_x,stick_recenterSpeed, offsetSteer_x)
			steering_y=recenter(steering_y,stick_recenterSpeed, offsetSteer_y)
		else:
			mouse_sensitivity=mouse_LookSensitivity
			if(switch==False):
				steering_x=v.rx
				steering_y=v.ry
			switch=True

			if(enable_freelook==True):
				v.rx = int(round(steering_x))
				v.ry = int(round(steering_y))

			v.x=recenter(v.x, stick_recenterSpeed, offsetSteer_x)
			v.y=recenter(v.y, stick_recenterSpeed, offsetSteer_y)


		#firing modes
		if not freeLookHold and mouse.wheelUp and v.z>-15000:
			v.z-=1500

		if not freeLookHold and mouse.wheelDown and v.z<15000:
			v.z+=1500

		if(stickSteering==True):	
			if(mouse.leftButton==True):
				v.setButton(0, True)
			else:v.setButton(0, False)

		if(mouse.rightButton==True):
			v.setButton(1, True)
		else:v.setButton(1, False)



	if freeLookHold and mouse.wheelUp and v.rz>-15000:
		v.rz -= 1500

	if freeLookHold and mouse.wheelDown and v.rz<15000:
		v.rz += 1500

	if(freeLookToggle):
		freeLook = not freeLook

	if freeLookHold or freeLook:
		stickSteering = False
	else:
		stickSteering= True

	if(keyboard.getPressed(Key.ScrollLock)):
		active = not active
		steering_x=offsetSteer_x
		steering_y=offsetSteer_y

	if(keyboard.getPressed(Key.F10) or keyboard.getPressed(Key.Escape)):
		active = not active

	if(keyboard.getPressed(Key.F1)):
		steering_x=offsetSteer_x
		steering_y=offsetSteer_y
		active = True

#watches
diagnostics.watch(v.x)
diagnostics.watch(v.y)
diagnostics.watch(v.rx)
diagnostics.watch(v.ry)
diagnostics.watch(v.z)
diagnostics.watch(v.rz)
diagnostics.watch(freeLook)
diagnostics.watch(stickSteering)
diagnostics.watch(active)
diagnostics.watch(get_active_window_name()) 0.1
	switch = False
	active = True
	freeLook=True
	stickSteering = True
	v = vJoy[DeviceNumber]
	v.x = offsetSteer_x
	v.y = offsetSteer_y
	v.rx = offsetLook_x
	v.ry = offsetLook_y
	
	
	def set_button(button, key):
		if keyboard.getKeyDown(key):
			v.setButton(button, True)
		else:
			v.setButton(button, False)
	
	def calculate_rate(max, time):
		if time > 0:
			return max / (time / system.threadExecutionInterval)
		else:
			return max
	
	def recenter(str, speed, offset):
		if(str>offset):
			if(str<offset+speed):
				str=offset
				return str
			else:
				str-=speed
				return str
		elif(str<offset):
			if(str>offset-speed):
				str=offset
				return str
			else:
				str+=speed
				return str
		return str
	
# =================================================================================================
# steering logic
# =================================================================================================
toggle1 = keyboard.getKeyDown(Key.LeftAlt)
combo = keyboard.getPressed(Key.Grave)

if(active):
	if keyboard.getKeyDown(Key.NumberPad5):
		steering_y=0
		steering_x =0
	
	if steering_x > 0:
		steering_center_reduction = sensitivity_center_reduction ** (1 - (steering_x / steering_max))
	elif steering_x < 0:
		steering_center_reduction = sensitivity_center_reduction ** (1 - (steering_x / steering_min))
	steering_x = steering_x + ((float(mouse.deltaX) * mouse_sensitivity) / steering_center_reduction)
	if steering_x > steering_max:
		steering_x = steering_max
	elif steering_x < steering_min:
		steering_x = steering_min
	
	if steering_y > 0:
		steering_center_reduction_l = sensitivity_center_reduction ** (1 - (steering_y / steering_max))
	elif steering_y < 0:
		steering_center_reduction_l = sensitivity_center_reduction ** (1 - (steering_y / steering_min))
	steering_y = steering_y + ((float(mouse.deltaY) * mouse_sensitivity) / steering_center_reduction_l)
	if steering_y > steering_max:
		steering_y = steering_max
	elif steering_y < steering_min:
		steering_y = steering_min
		
	
	if(stickSteering):
		mouse_sensitivity=mouse_StickSensitivity
		if(switch==True):
			steering_x=v.x
			steering_y=v.y
		switch=False
	
		v.x = int(round(steering_x))
		v.y= int(round(steering_y))
		
		v.rx=recenter(v.rx,look_recenterSpeed,offsetLook_x)
		v.ry=recenter(v.ry,look_recenterSpeed,offsetLook_y)
		
		steering_x=recenter(steering_x,stick_recenterSpeed, offsetSteer_x)
		steering_y=recenter(steering_y,stick_recenterSpeed, offsetSteer_y)
	else:
		mouse_sensitivity=mouse_LookSensitivity
		if(switch==False):
			steering_x=v.rx
			steering_y=v.ry
		switch=True
		
		if(enable_freelook==True):
			v.rx = int(round(steering_x))
			v.ry = int(round(steering_y))
		
		v.x=recenter(v.x, stick_recenterSpeed, offsetSteer_x)
		v.y=recenter(v.y, stick_recenterSpeed, offsetSteer_y)
		
	
	#firing modes
	if not toggle1 and mouse.wheelUp and v.z>-15000:
		v.z-=1500
		
	if not toggle1 and mouse.wheelDown and v.z<15000:
		v.z+=1500
	
	if(stickSteering==True):	
		if(mouse.leftButton==True):
			v.setButton(0, True)
		else:v.setButton(0, False)
		
	if(mouse.rightButton==True):
		v.setButton(1, True)
	else:v.setButton(1, False)
	

	if(mouse.getButton(3)):
		v.setButton(2,True)
	else:v.setButton(2,False)
		
	
#freelook switching
if toggle1 and mouse.wheelUp and v.rz>-15000:
	v.rz -= 1500
	
if toggle1 and mouse.wheelDown and v.rz<15000:
	v.rz += 1500

if(combo):
	freeLook = not freeLook
	ctypes.windll.user32.SetCursorPos(1920/2, 1080/2)
		
if toggle1 or freeLook:
	stickSteering = False
else:
	stickSteering= True

#pause the script
if(keyboard.getPressed(Key.ScrollLock)):
	active = not active
	steering_x=offsetSteer_x
	steering_y=offsetSteer_y
	
if(keyboard.getPressed(Key.F10) or keyboard.getPressed(Key.Escape)):
	active = not active
	
if(keyboard.getPressed(Key.F1)):
	steering_x=offsetSteer_x
	steering_y=offsetSteer_y
	active = True

#watches
diagnostics.watch(v.x)
diagnostics.watch(v.y)
diagnostics.watch(v.rx)
diagnostics.watch(v.ry)
diagnostics.watch(v.z)
diagnostics.watch(freeLook)
diagnostics.watch(stickSteering)
diagnostics.watch(active)