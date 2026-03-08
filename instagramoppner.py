import cv2
import mediapipe as mp
import pyautogui
import webbrowser
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

last_time = 0
cooldown = 1.5  # well nigga this for how much ur camera will read the postion (dont make it too small IT WILL BE BAD)
five_checks = 0  # this for ur fingers nigga (if isnt obvvious)


def count_fingers(landmarks):
    """
    Returns number of extended fingers (ignores thumb for simplicity).
    """
    tips = [8, 12, 16, 20]  # index, middle, ring, pinky
    count = 0
    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:  # when ur fingers are up
            count += 1
    return count


try:
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)  

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        now = time.time()

        if results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0].landmark
            finger_count = count_fingers(lm)

            if now - last_time > cooldown:
                if finger_count == 1:
                    print("SCROLL DOWN")
                    pyautogui.scroll(-800)
                    last_time = now

                elif finger_count == 2:
                    print("SCROLL UP")
                    pyautogui.scroll(800)
                    last_time = now

                elif finger_count == 3:
                    print("OPENING INSTAGRAM")
                    webbrowser.open("https://www.instagram.com/reels", new=2)
                    last_time = now

                elif finger_count == 4:
                    print("CLOSING INSTAGRAM TAB")
                    pyautogui.hotkey("ctrl", "w")
                    last_time = now

            # --- safe check with 5 fingers  to close the program cuz it  can somtimes spamm shit ---
            if finger_count == 5:
                five_checks += 1
                print(f"5 fingers detected ({five_checks}/3)")
                if five_checks >= 3:
                    print("EXIT PROGRAM ")
                    break
            else:
                five_checks = 0  # will comeback as 0

        cv2.imshow("Finger Gesture Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # this to capture shit dw about
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
