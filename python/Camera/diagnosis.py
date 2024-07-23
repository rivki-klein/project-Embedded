import csv

def num_tounge_out():
    # הנתיב לקובץ ה-CSV שלך
    #csv_file_path = 'C:/Users/user1/yolov5-master/runs/detect/exp46/predictions.csv'

    csv_file_path = 'C:/Users/user1/yolov5-master/runs/detect/'
    import find_file
    name_folder = find_file.get_latest_predictions_csv(csv_file_path)
    csv_file_path=csv_file_path+''+name_folder+'/predictions.csv'
    degel='false'
    mone = 0
    while(degel=='false'):
        try:
            # פותח את הקובץ לקריאה
            with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file)
                degel='true'
                # דילוג על הכותרת (שורה ראשונה)
                next(csv_reader)

                # מעבר על כל השורות בעמודה השנייה
                for row in csv_reader:
                    # קורא את הנתונים בעמודה השנייה
                    if (row[1] == 'in'):
                        mone = mone + 1

            # break  # יצא מהלולאה אם הקובץ נקרא בהצלחה

        except FileNotFoundError:
            mone=0
    print(mone)
    return mone
