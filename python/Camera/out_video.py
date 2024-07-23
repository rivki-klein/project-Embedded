import os
import cv2


def frames_to_video(frames_folder, output_file, duration=10, fps=30):
    # קבלת רשימת כל הקבצים בתיקיית הפריימים
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.png') or f.endswith('.jpg')])

    if len(frame_files) == 0:
        raise ValueError("לא נמצאו פריימים בתיקיה")

    # קביעת נתוני הווידאו מהפריים הראשון
    first_frame_path = os.path.join(frames_folder, frame_files[0])
    first_frame = cv2.imread(first_frame_path)

    if first_frame is None:
        raise ValueError("לא ניתן לקרוא את התמונה הראשונה")

    height, width, _ = first_frame.shape

    # יצירת אובייקט לכתיבת הווידאו
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # פורמט MP4
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # מספר הפריימים בתיקיה
    num_frames = len(frame_files)

    # פרק זמן שנדרש עבור כל פריים
    frame_interval = duration / num_frames  # משך הזמן הכולל לחלק לפי מספר הפריימים

    for frame_file in frame_files:
        frame_path = os.path.join(frames_folder, frame_file)
        frame = cv2.imread(frame_path)

        if frame is not None:
            # החזרת כל פריים מספר פעמים לפי הצורך
            for _ in range(int(fps * frame_interval)):
                video_writer.write(frame)
        else:
            print(f"לא ניתן לקרוא את התמונה {frame_file}")

    # סגירת אובייקט הווידאו
    video_writer.release()
    print(f"הוידאו נשמר ל-{output_file}")
