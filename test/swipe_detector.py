import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x = None
prev_y = None
gesture = ""
gesture_time = time.time()

def detect_swipe(x, y):
    global prev_x, prev_y, gesture, gesture_time
    if prev_x is None or prev_y is None:
        prev_x, prev_y = x, y
        return

    dx = x - prev_x
    dy = y - prev_y

    if abs(dx) > 50 and abs(dx) > abs(dy):
        if dx > 0:
            gesture = "Swipe Right"
        else:
            gesture = "Swipe Left"
        gesture_time = time.time()
    elif abs(dy) > 50 and abs(dy) > abs(dx):
        if dy < 0:
            gesture = "Swipe Up"
        gesture_time = time.time()

    prev_x, prev_y = x, y

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x_tip = int(hand_landmarks.landmark[8].x * w)
            y_tip = int(hand_landmarks.landmark[8].y * h)

            cv2.circle(frame, (x_tip, y_tip), 10, (0, 255, 0), -1)
            detect_swipe(x_tip, y_tip)

    if time.time() - gesture_time < 1.0:
        cv2.putText(frame, f"{gesture}", (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

    cv2.imshow("Swipe Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
