/*
	Code for the arudino operating the sensors inside the bathouse.
	The bathouse has 2 sets of line-break sensors, 3 temperature sensors, and 2 PIR sensors.
	Arduino commmunicates over serial at 9600 BAUD.

	Written by Toan Nguyen, January 2015
	toannguyen@knights.ucf.edu
*/

#include <stdio.h>
#include <time.h>

//Define pins for temperature sensors
#define TEMPSENSOR_1 52
#define TEMPSENSOR_2 53
#define TEMPSENSOR_3 22

//Define pins for line-break sensors
#define LBREAK_1 NULL
#define LBREAK_2 NULL
#define LBREAK_3 NULL
#define LBREAK_4 NULL

//Define pins for PIR sensors
#define PIR_1 NULL
#define PIR_2 NULL

void setup() {
	Serial.begin(9600);

	//Set all line-break sensors to go off when LOW
	pinMode(LBREAK_1, INPUT_PULLUP);
	pinMode(LBREAK_2, INPUT_PULLUP);
	pinMode(LBREAK_3, INPUT_PULLUP);
	pinMode(LBREAK_4, INPUT_PULLUP);

	//Set all PIR sensors to go off when LOW
	pinMode(PIR_1, INPUT_PULLUP);
	pinMode(PIR_2, INPUT_PULLUP);

	int lineBreak1, lineBreak2, lineBreak3, lineBreak4, PIR1, PIR2, Temp1, Temp2, Temp3;
	time_t t = now();
}

void loop() {



}

