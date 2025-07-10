import cv2
import mediapipe as mp
import time
import threading

class SwipeDetector:
    def __init__(self):
        self.gesture = None
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.prev_x = None
        self.prev_y = None
        self.gesture_time = 0

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

    def detect_swipe(self, x, y):
        if self.prev_x is None:
            self.prev_x, self.prev_y = x, y
            return

        dx = x - self.prev_x
        dy = y - self.prev_y

        if abs(dx) > 50 and abs(dx) > abs(dy):
            if dx > 0:
                self.gesture = "right"
            else:
                self.gesture = "left"
            self.gesture_time = time.time()
        elif abs(dy) > 50 and abs(dy) > abs(dx):
            if dy < 0:
                self.gesture = "up"
                self.gesture_time = time.time()

        self.prev_x, self.prev_y = x, y

    def start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(img_rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    x_tip = int(hand_landmarks.landmark[8].x * w)
                    y_tip = int(hand_landmarks.landmark[8].y * h)
                    self.detect_swipe(x_tip, y_tip)

            # Reset gesture after 0.5s
            if time.time() - self.gesture_time > 0.5:
                self.gesture = None

        self.cap.release()
        cv2.destroyAllWindows()

    def get_gesture(self):
        return self.gesture

    def stop(self):
        self.running = False
