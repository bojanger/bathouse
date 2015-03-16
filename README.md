This repo contains all the files for a bat house project at Valencia College West Campus.
The bat house is located approximately 20 feet in the air. It's powered by two solar panels charging a 12 volt car battery.
The bat house is also isolated from any Wi-Fi signals, so a means to communicate remotely is necessary.

The current hardware of the bat house consists of:

  Raspberry Pi Model B
  Arduino MEGA with 4 temperature sensors, 2 line break sensors, RTC Module, and 4 PIR Sensors (Bat house sensor controller)
  Arduino UNO clone with Seeed Studio GPRS Shield 1.0 loaded with T-Mobile SIM card (data only)
  
Raspberry Pi is coded to handle all logic. Sensor data is transmitted through serial via USB to the Pi. 
The Pi sends AT commands, which allows communication by TCP on GSM 3G, through serial via USB to the GPRS shield.

This current project is still under development. All the files in the repo may or may not run/compile. 
They're mainly used to test the Arduino hardware.


Devloping by:
toannguyen (at) knights.ucf.edu

Issues:

AT Commands need an intelligent timeout method
