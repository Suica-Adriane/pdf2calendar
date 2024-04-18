import simpleexec as simpleexec
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

#メインウィンドウ作成
root = tk.Tk()
root.title("PDF Cropper")
root.minsize(1050, 1000)

#画像の拡大率
scale = 3

#ファイルを開く関数
def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        simpleexec.convert2img(file_path)
        pic = Image.open('./1.png')
        pic = pic.resize((pic.width//scale, pic.height//scale))
        pic = ImageTk.PhotoImage(pic)
        canvas.itemconfig(image_container, image=pic)
        canvas.image = pic
        canvas.lower(image_container)

#実行ボタンを押したときの関数
def execute():
    xl = paddle_x.get()*scale
    yt = paddle_y.get()*scale
    xr = val_col.get()*scale*5+paddle_x.get()*scale
    yb = val_row.get()*scale*5+paddle_y.get()*scale+hiru.get()*scale
    row = val_row.get()*scale
    col = val_col.get()*scale
    hiruyasumi = hiru.get()*scale
    simpleexec.crop(xl,yt,xr,yb,row,col,hiruyasumi)
    simpleexec.extract()
    simpleexec.create_ical()
    simpleexec.cleanup()
    messagebox.showinfo("Done", "The process has been completed successfully.")


#終了ボタンを押したときの関数
def quit():
    root.quit()

#線を描く関数
def drawlines():
    for i in range(3):
        canvas.moveto("line_"+str(i),0+paddle_x.get(),val_row.get()*i+paddle_y.get())
    for i in range(4):
        canvas.moveto("line_"+str(i+3),0+paddle_x.get(),(val_row.get()*(i+2))+hiru.get()+paddle_y.get())
    for i in range(6):
        canvas.moveto("line_"+str(i+7),val_col.get()*i+paddle_x.get(),0+paddle_y.get())

#サブウィンドウ作成
window1 = tk.Frame(root, bg="white", width=800, height=1000)
window2 = tk.Frame(root, bg="white",width = 200,height = 800)
window1.place(relx=0.01, rely=0)
window2.place(relx=0.8, rely=0.05)

#ボタン作成
button1 = tk.Button(window2, text="PDFをえらぶ", command=open_file)
button1.place(relx=0.1, rely=0.05)
button2 = tk.Button(window2, text="実行", command=execute)
button2.place(relx=0.1, rely=0.1)
exitbutton = tk.Button(window2, text="Exit", command=root.quit)
exitbutton.place(relx=0.1, rely=0.95)

#変数作成
val_col= tk.IntVar()
val_row= tk.IntVar()
hiru = tk.IntVar()
paddle_x = tk.IntVar()
paddle_y = tk.IntVar()
val_col.set(115)
val_row.set(142)
hiru.set(20)
paddle_x.set(68)
paddle_y.set(136)

#スライダー作成
rowslider = tk.Scale(window2, label="Row", orient="horizontal", from_=0, to=500, variable=val_row,length=180)
rowslider.place(relx=0.1, rely=0.15)
colslider = tk.Scale(window2, label="Column", orient="horizontal", from_=0, to=500, variable=val_col,length=180)
colslider.place(relx=0.1, rely=0.25)
hiruyasumislider = tk.Scale(window2, label="Hiruyasumi", orient="horizontal", from_=0, to=200,variable=hiru,length=180)
hiruyasumislider.place(relx=0.1, rely=0.35)
px_slider = tk.Scale(window2, label="Paddle X", orient="horizontal", from_=0, to=200,variable=paddle_x,length=180)
px_slider.place(relx=0.1, rely=0.45)
py_slider = tk.Scale(window2, label="Paddle Y", orient="horizontal", from_=0, to=200,variable=paddle_y,length=180)
py_slider.place(relx=0.1, rely=0.55)

#キャンバス作成
canvas = tk.Canvas(window1, bg="white", width=800, height=1000)
canvas.place(relx=0, rely=0)

#線を初期化
for i in range(7):
    canvas.create_line(paddle_x.get(), val_row.get() * (i+1)+paddle_y.get(), 800+paddle_x.get(), val_row.get() * (i+1)+paddle_y.get(), fill="red",tags="line_"+str(i))
for i in range(6):
    canvas.create_line(val_col.get() * (i+1)+paddle_x.get(), paddle_y.get(), val_col.get() * (i+1)+paddle_x.get(), 1000+paddle_y.get(), fill="red",tags="line_"+str(i+7))

#スライダーが動いたときに線を描く
val_col.trace_add("write", lambda name, index, mode: drawlines())
val_row.trace_add("write", lambda name, index, mode: drawlines())
hiru.trace_add("write", lambda name, index, mode: drawlines())
paddle_x.trace_add("write", lambda name, index, mode: drawlines())
paddle_y.trace_add("write", lambda name, index, mode: drawlines())


#画像を表示
image_container = canvas.create_image(0,0, image=None, anchor="nw", tags="1")

#メインループ
root.mainloop()