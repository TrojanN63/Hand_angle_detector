import cv2 as cv
import mediapipe as mp
import math
import paho.mqtt.client as mqtt

client = mqtt.Client(client_id="angle_detector")
client.connect("127.0.0.1", 1883, 15)

video = cv.VideoCapture(0)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        istrue, frame = video.read()
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results = hands.process(frame)
        frame.flags.writeable = True
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmark, mp_hand.HAND_CONNECTIONS)
                height, width, _ = frame.shape
                
                landmark0 = hand_landmark.landmark[0]
                landmark1 = hand_landmark.landmark[5]
                
                x0, y0 = int(landmark0.x * width), int(landmark0.y * height)
                x1, y1 = int(landmark1.x * width), int(landmark1.y * height)
                
                cv.line(frame, (x0, y0), (x1, y1), (0, 0, 255), 3)

                delta_x = x1 - x0
                delta_y = y0 - y1
                angle_rad = math.atan2(delta_y, delta_x)
                angle_deg = math.degrees(angle_rad)

                angle_deg = angle_deg % 360
                
                angle_deg = round(angle_deg, 2)

                cos = round(math.cos(angle_rad), 3)
                
            cv.putText(frame, f"Angulo: {angle_deg} graus", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(frame, f'Cos: {cos}', (10,60), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            client.publish("dev9840ss", str(cos))
            
        if istrue:
            cv.imshow("it's you", frame)
            if cv.waitKey(100) & 0xFF==ord('d'):
                break
        else:
            break

video.release()
cv.destroyAllWindows()