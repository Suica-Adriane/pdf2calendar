import pdf2image
import os
from PIL import Image
import PIL
import sys
import PIL.Image
import PIL.ImageDraw
import OCR as OCR
import datetime
import numpy as np
import icalendar
import arrow


#5x5のarrayを作る
jikanwari = np.zeros((5,5),dtype = object)

#次に指定した曜日が来る日付を返す
def weekday_to_datetime(day):
    today = datetime.date.today()
    weekday = today.weekday()
    if day >= weekday:
        return today + datetime.timedelta(days = day - weekday)
    else:
        return today + datetime.timedelta(days = 7 - weekday + day)
    

#pdfを画像に変換
def convert2img(filepath):

    if "./1.png" not in os.listdir("."):
        print("creating images")
        pdf2image.convert_from_path(filepath, output_folder=".",output_file = "1" ,fmt="png",single_file=True,dpi=300)
    else:
        print("images already exist")


#画像を指定された範囲で切り取る→5つの列に分割→行に分割
def crop(xl,yt,xr,yb,row,col,hiruyasumi):
    print("bunkatu")

    image = Image.open('./1.png')
    x, y = image.size
    crop_area = (xl, yt, xr, yb)
    image = image.crop(crop_area)
    image.save('./1.png')
    image = Image.open('./1.png')
    x, y = image.size
    single_column_width = col
    single_row_height = row
    rows_border = (0, single_row_height, single_row_height*2, single_row_height*2+hiruyasumi, single_row_height*3+hiruyasumi, single_row_height*4+hiruyasumi, single_row_height*5+hiruyasumi)
    columns = []
    for i in range(5):
        columns.append(image.crop((single_column_width * i, 0, single_column_width * (i+1), y)))
        columns[i].save(f'./column{i}.png')

    colimgs = []
    trim = 10
    for i in range(5):
        colimgs.append(Image.open(f'./column{i}.png'))
        x, y = colimgs[i].size
        for j in range(2):
            colimgs[i].crop((0 +trim ,rows_border[j]+trim , x-trim , rows_border[j+1]-trim )).save(f'./{j}_{i}.png')
        for j in range(3):
            colimgs[i].crop((0+trim ,rows_border[j+3]+trim , x-trim , rows_border[j+4]-trim )).save(f'./{j+2}_{i}.png')

    print("done")

#OCRで文字を抽出
def extract():
    print("OCR")
    for i in range(5):
        for j in range(5):
            print("column",i,"row",j)
            jikanwari[j,i] = OCR.scan_txt(Image.open(f'./{j}_{i}.png'),'jpn')
    print("done")


#icalファイルを作成
def create_ical():
    #time table
    classstarttimes = ("8:50","10:30","13:00","14:40","16:20")
    classendtimes = ("10:20","12:00","14:30","16:10","17:50")

    print("converting to ical format")
    file = open("./jikanwari.ical","w")
    cal = icalendar.Calendar()

    for i in range(5):
        for j in range(5):
            line = jikanwari[j,i].split("\n")
            print(j,i,line)
            if len(line) >= 2:
                if line[1] =="(":
                    line = line[0]+line[1]
                else:
                    line = line[0]
            else:
                continue
            event = icalendar.Event()
            event.add('summary', line)
            event.add('dtstart', arrow.get(weekday_to_datetime(i)).replace(hour=int(classstarttimes[j].split(":")[0]),minute=int(classstarttimes[j].split(":")[1]),tzinfo="Asia/Tokyo").datetime)
            event.add('dtend', arrow.get(weekday_to_datetime(i)).replace(hour=int(classendtimes[j].split(":")[0]),minute=int(classendtimes[j].split(":")[1]),tzinfo="Asia/Tokyo").datetime)
            event.add('rrule', {'freq': 'weekly'})
            event.add('description', jikanwari[j,i])
            cal.add_component(event)
    file.write(cal.to_ical().decode('utf-8'))
    file.close()

    print("done")

#画像を削除
def cleanup():
    for i in range(5):
        os.remove(f'./column{i}.png')
        for j in range(5):
            os.remove(f'./{j}_{i}.png')
    os.remove('./1.png')