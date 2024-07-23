import requests
import cv2
import numpy as np
import os
import time

def get_from_camera():
    # הגדרות
    input_folder = 'frames'  # תיקיית התמונה
    output_video_file = 'output_video.mp4'  # שם קובץ הווידאו

    # משך הזמן של הסרטון בשניות
    duration = 10  # אורך הסרטון ב-שניות

    # מספר הפריימים לשנייה
    fps = 30  # מספר פריימים לשנייה

    # יצירת תיקיה לשמירת פריימים
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)

    # התחלת הבקשה לזרם הוידאו
    camera_url = "http://192.168.1.101/"
    stream = requests.get(camera_url, stream=True)

    # בדוק שהבקשה הצליחה
    if stream.status_code == 200:
        bytes_data = b''
        start_time = time.time()
        frame_count = 0
        for chunk in stream.iter_content(chunk_size=1024):
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')  # חיפוש תחילת JPEG
            b = bytes_data.find(b'\xff\xd9')  # חיפוש סיום JPEG
            if a != -1 and b != -1:
                jpg = bytes_data[a:b + 2]  # קבלת התמונה
                bytes_data = bytes_data[b + 2:]  # עדכון הנתונים שנשארו

                # המרת התמונה למערך NumPy
                image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                # שמירת התמונה לקובץ
                frame_filename = os.path.join(input_folder, f'frame_{frame_count:04d}.jpg')
                cv2.imwrite(frame_filename, image)
                frame_count += 1

                # בדוק אם עברו 10 שניות
                if time.time() - start_time > 10:
                    break

    else:
        print("Failed to connect to the camera stream.")

    # קריאה לפונקציה עם תיקיית הפריימים ושם הקובץ של הוידאו
    import out_video
    out_video.frames_to_video(input_folder, output_video_file, duration=duration, fps=fps)

    # הרצת YOLO
    import run_yolo
    run_yolo.yolo()
    print("run yolo")

    #אבחון
    import diagnosis
    mone=diagnosis.num_tounge_out()
    if(mone==0):
        return 0
    elif(mone<10):
        return 1
    else:
        return 2

print(get_from_camera())