if starting:

	profile_name = 'DCS_F16.json'
	profile_path = 'D:\Programs\Controller\scripts\\'

	from mouse_flight_common import *
	settings_profile = import_json(profile_path + profile_name)

	mouse_StickSensitivity = settings_profile["mouse_StickSensitivity"]
	mouse_LookSensitivity = settings_profile["mouse_LookSensitivity"]
	enable_freelook = settings_profile["enable_freelook"]

	offsetSteer_x = settings_profile["offsetSteer_x"]
	offsetSteer_y = settings_profile["offsetSteer_y"]
	offsetLook_x = settings_profile["offsetLook_x"]
	offsetLook_y = settings_profile["offsetLook_y"]

	stick_recenterSpeed = settings_profile["stick_recenterSpeed"]
	look_recenterSpeed = settings_profile["look_recenterSpeed"]
	
	DeviceNumber = settings_profile["DeviceNumber"]	#0 means device 1, 1 means device 2, etc.
	window_name = settings_profile["window_name"]

	switch = False
	active = True
	freeLook= True
	stickSteering = True
	thorttle_enable = True
	do_recenter = True

	int32_max = (2 ** 14) - 1
	int32_min = (( 2** 14) * -1) + 1
	mouse_sensitivity = 0.5
	steering_x = 0.0
	steering_y = 0.0
	steering_max = float(int32_max)
	steering_min = float(int32_min)
	steering_center_reduction = 1.0
	steering_center_reduction_l = 1.0
	steering_center_reduction_lx=1.0
	steering_center_reduction_ly=1.0
	sensitivity_center_reduction = 0.1
	
	v = vJoy[DeviceNumber]
	v.x = offsetSteer_x
	v.y = offsetSteer_y
	v.rx = offsetLook_x
	v.ry = offsetLook_y
	v.rz = 0

	system.setThreadTiming(TimingTypes.HighresSystemTimer)
	system.threadExecutionInterval = 5
	
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
		if str>offset:
			if str<offset+speed:
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
slewHold = keyboard.getKeyDown(Key.LeftControl)
freeLookToggle = keyboard.getPressed(Key.Grave)
throttleToggle = keyboard.getPressed(Key.PrintScreen)
stickHold = mouse.getButton(2)

if is_window_active(window_name):
	

	if active:

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


		if stickSteering and not slewHold:
			mouse_sensitivity=mouse_StickSensitivity
			if(switch==True):
				steering_x=v.x
				steering_y=v.y
			switch=False
			
			v.x = int(round(steering_x))
			v.y= int(round(steering_y))

			v.rx=recenter(v.rx,look_recenterSpeed,offsetLook_x)
			v.ry=recenter(v.ry,look_recenterSpeed,offsetLook_y)
			
			if do_recenter:
				steering_x=recenter(steering_x,stick_recenterSpeed, offsetSteer_x)
				steering_y=recenter(steering_y,stick_recenterSpeed, offsetSteer_y)
		elif not stickSteering and not slewHold:
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
		if thorttle_enable and not freeLook and not freeLookHold and mouse.wheelUp and v.z>-15000:
			v.z-=1500

		if thorttle_enable and not freeLook and not freeLookHold and mouse.wheelDown and v.z<15000:
			v.z+=1500

		if stickSteering==True:	
			if(mouse.leftButton==True):
				v.setButton(0, True)
			else:v.setButton(0, False)

		if mouse.rightButton==True:
			v.setButton(1, True)
		else:v.setButton(1, False)

	if throttleToggle: 
		thorttle_enable = not thorttle_enable

	if freeLookHold and mouse.wheelUp and v.rz>-15000:
		v.rz -= 1500

	if freeLookHold and mouse.wheelDown and v.rz<15000:
		v.rz += 1500

	if freeLookToggle:
		freeLook = not freeLook
		set_cursor_pos(1920/2, 1080/2)

	if freeLookHold or freeLook:
		stickSteering = False
	else:
		stickSteering= True
		
	if stickHold:
		do_recenter = False
	else:
		do_recenter = True

	if keyboard.getPressed(Key.ScrollLock):
		active = True
		freeLook = False
		stickSteering = True
		
		steering_x=offsetSteer_x
		steering_y=offsetSteer_y

	if keyboard.getPressed(Key.F10) or keyboard.getPressed(Key.Escape):
		active = not active

	if keyboard.getPressed(Key.F1):
		steering_x=offsetSteer_x
		steering_y=offsetSteer_y
		active = True
        
	if keyboard.getKeyDown(Key.NumberPad5):
		steering_y = 0
		steering_x = 0

#watches
diagnostics.watch(v.x)
diagnostics.watch(v.y)
diagnostics.watch(v.rx)
diagnostics.watch(v.ry)
diagnostics.watch(v.z)
diagnostics.watch(v.rz)
diagnostics.watch(freeLook)
diagnostics.watch(stickHold)
diagnostics.watch(stickSteering)
diagnostics.watch(thorttle_enable)
diagnostics.watch(active)
diagnostics.watch(get_active_window_name())