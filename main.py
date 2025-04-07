import cv2 as cv
import mediapipe as mp
import math
# import paho.mqtt.client as mqtt

# client = mqtt.Client(client_id="angle_detector")
# client.connect("127.0.0.1", 1883, 15)

video = cv.VideoCapture(0)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
mp_pose = mp.solutions.pose

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    while True:
        istrue, frame = video.read()
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame.flags.writeable = False
        results_h = hands.process(frame)
        results_p = pose.process(frame)
        frame.flags.writeable = True
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        if results_h.multi_hand_landmarks and results_p:
            for hand_landmark, handedness in zip(results_h.multi_hand_landmarks, results_h.multi_handedness):
                mp_draw.draw_landmarks(frame, hand_landmark, mp_hand.HAND_CONNECTIONS)
                mp_draw.draw_landmarks(frame, results_p.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                height, width, _ = frame.shape
                
                landmark0 = hand_landmark.landmark[0]
                landmark1 = hand_landmark.landmark[5]

                if handedness.classification[0].label == 'Left' and results_p.pose_landmarks:
                    elbow = results_p.pose_landmarks.landmark[14]
                else:
                    elbow = results_p.pose_landmarks.landmark[13]
                
                x0, y0 = int(landmark0.x * width), int(landmark0.y * height)
                x1, y1 = int(landmark1.x * width), int(landmark1.y * height)
                x2, y2 = int(elbow.x * width), int(elbow.y * height)
                
                # cv.line(frame, (x0, y0), (x1, y1), (0, 0, 255), 3)
                # cv.line(frame, (x0, y0), (x2, y2), (0, 0, 255), 3)
                # cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

                delta_x_a = x0 - x1
                delta_y_a = y0 - y1
                delta_x_b = x1 - x2
                delta_y_b = y1 - y2

                dot_product = delta_x_a * delta_x_b + delta_y_a * delta_y_b

                magnitude_a = math.hypot(delta_x_a, delta_y_a)
                magnitude_b = math.hypot(delta_x_b, delta_y_b)

                if magnitude_a == 0 or magnitude_b == 0:
                    magnitude_a+=0.01
                    magnitude_b+=0.01
                
                cos_theta = dot_product / (magnitude_a * magnitude_b)
                cos_theta = max(min(cos_theta, 1.0), -1.0)  # Corrige possíveis erros numéricos

                angle_rad = math.acos(cos_theta)
                angle_deg = math.degrees(angle_rad)

                # angle_rad = math.atan2(delta_y, delta_x)
                # angle_deg = math.degrees(angle_rad)

                # angle_deg = angle_deg % 360
                
                angle_deg = round(angle_deg, 2)
                cos_theta = round(cos_theta, 3)
                
            cv.putText(frame, f"Angulo: {angle_deg} graus", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv.putText(frame, f'Cos: {cos_theta}', (10,60), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # client.publish("dev9840ss", str(cos))
            
        if istrue:
            cv.imshow("it's you", frame)
            if cv.waitKey(100) & 0xFF==ord('d'):
                break
        else:
            break

video.release()
cv.destroyAllWindows()