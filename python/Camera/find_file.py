import os
import glob


def get_latest_predictions_csv(base_path):
    base_path = 'C:/Users/user1/yolov5-master/runs/detect'

    # קבל את רשימת התיקיות בנתיב
    all_entries = os.listdir(base_path)

    # סנן רק את התיקיות (לא קבצים)
    folders = [entry for entry in all_entries if os.path.isdir(os.path.join(base_path, entry))]

    # סדר את התיקיות לפי תאריך יצירה ולקחת את התיקיה האחרונה
    if folders:
        # סידור התיקיות לפי תאריך יצירה (תיקיה אחרונה לפי התאריך)
        last_folder = max(folders, key=lambda folder: os.path.getctime(os.path.join(base_path, folder)))
        return last_folder
