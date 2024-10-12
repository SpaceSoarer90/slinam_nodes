#include <TimerOne.h>
#include "slinam.h"

float average = 0;
int average_cnt = 1;
float rps = 0;
uint32_t last_time;

Encoders enc = { 0 };
Twist msg = { 0 };
MotorDriver mot;

char dbg_out[128];

void setup() {
  Serial.begin(115200);
  Serial.println("Initializing...");

  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(2), encoder_left_interrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(3), encoder_right_interrupt, RISING);
  
  //for every 1ms = 1000us
  Timer1.initialize(10 * 1000);
  Timer1.attachInterrupt(encoder_delta_pulses);
  Timer1.start();

  pinMode(MOTOR_A_PINA, OUTPUT);
  pinMode(MOTOR_A_PINB, OUTPUT);

  digitalWrite(MOTOR_A_PINA, LOW);
  digitalWrite(MOTOR_A_PINB, LOW);

  msg.l_x.f = 1.0;
}

void loop() {

  // only start reading when there are two floats (4 bytes)
  // in the serial buffer
  if (Serial.available() >= 8) {
    // Initialize to zero (because the or-ing doesn't remove the bits)
    msg = { 0 };
    for (int i = 0; i < sizeof(float); i++) {
      uint32_t data = (uint32_t)Serial.read() << 8 * i;
      msg.l_x.u |= data;
    }
    for (int i = 0; i < sizeof(float); i++) {
      uint32_t data = (uint32_t)Serial.read() << 8 * i;
      msg.a_z.u |= data;
    }
    // change pwm when twist messages are received (velocity has changed)
    mot = twist_to_rpm(msg.l_x.f, msg.a_z.f);
    motor_change_state(mot);
  }
  // Serial.print(mot.l.rpm);
  // Serial.print(",");
  // Serial.print(mot.r.rpm);

  // delay(1000);
  // detachInterrupt(digitalPinToInterrupt(2));
  // detachInterrupt(digitalPinToInterrupt(3));

  // last_time = millis(); 

  // attachInterrupt(digitalPinToInterrupt(2), encoder_left_interrupt, RISING);
  // attachInterrupt(digitalPinToInterrupt(3), encoder_right_interrupt, RISING);
}

