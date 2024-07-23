import subprocess
import os

def yolo():
    # הגדרת הנתיבים
    command = (
        'python detect.py --weight runs/train/Model6/weights/last.pt '
        '--img-size 640 --source "C:/Users/user1/Documents/CAMERA_PROJECT/python/Camera/output_video.mp4" --save-csv'
        '>> C:/Users/user1/Documents/CAMERA_PROJECT/python/Camera/results.txt 2>&1'
    )
    path = r'C:\Users\user1\yolov5-master'

    # שינוי תיקיית העבודה
    os.chdir(path)

    # הרצת הפקודה
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # קריאת הפלט והטעויות
    stdout, stderr = process.communicate()

    # (אופציונלי) הדפסת הפלט וטעויות ל-console
    print(stdout)
    if stderr:
        print(f"Errors: {stderr}")

    # (אופציונלי) המתנה לסיום התהליך
    process.wait()
