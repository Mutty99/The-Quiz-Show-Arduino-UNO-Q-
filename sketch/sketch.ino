#include <Arduino_RouterBridge.h>
#include <Arduino_Modulino.h>
#include <Button2.h>
#include <ArduinoGraphics.h>
#include <Arduino_LED_Matrix.h>

// ── Objects ───────────────────────────────────
ModulinoButtons modulinoButtons;
Button2 btn[3];
ArduinoLEDMatrix matrix;

// ── Variables to animate board led matrix ──
unsigned long feedback_timer = 0;
bool feedback_active = false;

// ── Led status ─────────────────────────────────
bool ledState[3] = {false, false, false};

void applyLeds() {
  modulinoButtons.setLeds(ledState[0], ledState[1], ledState[2]);
}

String rpc_set_led(int index, int newState) {
  if (index < 0 || index > 2) return "{\"ok\":false}";
  ledState[index] = (newState != 0);
  applyLeds();
  return "{\"ok\":true}";
}

// ── Functions for board led matrix ────────────────────

void drawCircle() {
  matrix.beginDraw();
  matrix.clear();
  matrix.stroke(0xFFFFFFFF);
  matrix.line(4, 1, 7, 1);
  matrix.line(4, 6, 7, 6);
  matrix.line(2, 3, 2, 4);
  matrix.line(9, 3, 9, 4);
  matrix.point(3, 2);
  matrix.point(8, 2);
  matrix.point(3, 5);
  matrix.point(8, 5);
  matrix.endDraw();
}

void drawCross() {
  matrix.beginDraw();
  matrix.clear();
  matrix.stroke(0xFFFFFFFF);
  matrix.line(3, 1, 8, 6);
  matrix.line(8, 1, 3, 6);
  matrix.endDraw();
}

void clearMatrix() {
  matrix.beginDraw();
  matrix.clear();
  matrix.endDraw();
}

// ── Interface for board led matrix ────────────────────

String rpc_show_feedback(int type, int dummy) {
  if (type == 1) {
    drawCircle();
    feedback_timer = millis();
    feedback_active = true;
  } else if (type == 0) {
    drawCross();
    feedback_timer = millis();
    feedback_active = true;
  }
  else {
    clearMatrix();
    feedback_active = false;
  }
  return "{\"ok\":true}";
}

// ── State handlers ────────────────────
uint8_t btn0State() { return modulinoButtons.isPressed(0) ? LOW : HIGH; }
uint8_t btn1State() { return modulinoButtons.isPressed(1) ? LOW : HIGH; }
uint8_t btn2State() { return modulinoButtons.isPressed(2) ? LOW : HIGH; }

int btnIndex(Button2& b) {
  for (int i = 0; i < 3; i++) if (&b == &btn[i]) return i;
  return -1;
}

void onPress(Button2& b) {
  int i = btnIndex(b);
  if (i >= 0) Bridge.notify("button_event", i, "press");
}

void onRelease(Button2& b) {
  int i = btnIndex(b);
  if (i >= 0) Bridge.notify("button_event", i, "release");
}

void onDoubleClick(Button2& b) {
  int i = btnIndex(b);
  if (i >= 0) Bridge.notify("button_event", i, "double_tap");
}

void setup() {
  Bridge.begin();
  Modulino.begin();
  modulinoButtons.begin();

  matrix.begin();
  applyLeds();

  typedef uint8_t (*StateFunc)();
  StateFunc stateFuncs[3] = {btn0State, btn1State, btn2State};

  for (int i = 0; i < 3; i++) {
    btn[i].setDebounceTime(20);
    btn[i].setButtonStateFunction(stateFuncs[i]);
    btn[i].setPressedHandler(onPress);
    btn[i].setReleasedHandler(onRelease);
    btn[i].setDoubleClickHandler(onDoubleClick);
    btn[i].begin(BTN_VIRTUAL_PIN);
  }

  Bridge.provide("set_led", rpc_set_led);
  Bridge.provide("show_feedback", rpc_show_feedback);
}

void loop() {
  modulinoButtons.update();

  for (int i = 0; i < 3; i++) btn[i].loop();

  if (feedback_active && (millis() - feedback_timer > 1500)) {
    feedback_active = false;
    clearMatrix();
  }

  delay(10);
}
