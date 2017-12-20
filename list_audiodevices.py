import pyo

def list_audiodev():
	devices = pyo.pa_get_output_devices()
	#default_device = pyo.pa_get_default_output()

	i = 0
	print("ATTACHED AUDIO DEVICES:")
	for device in devices[0]:
		print("%s: %s" %(i, device))
		i+=1

list_audiodev()