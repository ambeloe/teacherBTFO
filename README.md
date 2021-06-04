# teacherBTFO (abandoned)
hcpss google meet automation

uses folder %appdata%/teacherBTFO/ on windows

# suggested usage:
	* schedule task to run script at midnight every day
	* alternatively, run the loop script

# schedule format(json):
	* hcpss_username: string containing the hcpss username you want to use
	* hcpss_password: string containing the hcpss password you want to use
	* one key for each day of the week(monday is 0) containing an array of class dictionaries
		+ class dictionary:
			* code: string containing the google meet code
			* starttime: string containing the time the class starts (24 hour format)
			* maxduration: int containing the max length of the class (minutes)
			* record: boolean of whether or not to record the class (now works) (presses f9 at start and f10 at end)
			* name: string containing the display name of the class
