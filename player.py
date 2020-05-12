import os
import threading
from tkinter import *
from tkinter import filedialog
from mutagen.mp3 import MP3
import tkinter.messagebox
import time
from tkinter import ttk
from ttkthemes import ThemedTk as tk
from pygame import mixer
import sqlite3
conn=sqlite3.connect('users.db')
c=conn.cursor()


# ---- Initialization -------------
root = tk(theme='equilux')
root.get_themes()
root.set_theme("arc")
playlist = []
# --- Menubar ---
menubar = Menu(root)
root.config(menu=menubar)
# -------------------
# creating submenu
submenu = Menu(menubar, tearoff=0)

def listofplaylist():
    query1="SELECT * FROM list"
    c.execute(query1)
    playlist_list=c.fetchall()
    i=0
    length=len(playlist)
    # while length :
    #     playlist_list_box1.delete(length)
    #     #playlist_list_box1.pop(length)
    #     length=length-1
    
    for item in playlist_list:
        name=item[0]
        playlist_list_box1.insert(i,name)
        i=i+1

def add_to_playlist(f):
    f = os.path.basename(browseFile.fileName)
    index = 0
    playlistbox.insert(index,f)
    playlist.insert(index,browseFile.fileName)
    index = index + 1

def browseFile():
    browseFile.fileName = filedialog.askopenfilename()
    add_to_playlist(browseFile.fileName)
    insertintoplaylist()

def loadfromdb():
    user_name = userentry.get()
    sql="SELECT * FROM "+user_name
    try:
        c.execute(sql)
    except:
        tkinter.messagebox.showerror(title="ERROR", message="No Playlist found")    
    songlist=c.fetchall()
    i=0
    while i<len(songlist) :
        browseFile.fileName=songlist[i][0]
        add_to_playlist(browseFile.fileName)
        playlist=songlist[i][0]
        i+=1

def newplaylist():
    user_name=userentry.get()
    sql="CREATE TABLE "+user_name+' ("filepath"	TEXT)'
    sql2="INSERT INTO list(playlist) VALUES (?)"
    c.execute(sql)
    c.execute(sql2,(user_name,))
    conn.commit()
    listofplaylist()

def insertintoplaylist():
    user_name=userentry.get()
    sql="INSERT INTO "+user_name+"(filepath) VALUES (?)"
    c.execute(sql,(browseFile.fileName,))
    conn.commit()


def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)
#### future work delete the song from database #####
    # user_name=userentry.get()
    # conn=sqlite3.connect('users.db')
    # c=conn.cursor()
    # sql="SELECT * FROM "+user_name
    # c.execute(sql)
    # songlist=c.fetchall()
    # for item in songlist:
    #     browseFile.fileName=item[0]
    #     f=os.path.basename(browseFile.fileName)
    #     if f == selected_song:
    #         query = " DELETE FROM " +user_name+ " WHERE filepath = '"+item[0]+"' "
    #         c.execute(query)
    #         conn.commit()
    #         print("commmit")

# --- Left Frame ---
leftframe = ttk.Frame(root)
leftframe.pack(side=LEFT, padx = 20, pady = 10)

addPhoto = PhotoImage(file="Images/add.png")
delPhoto = PhotoImage(file="Images/minus.png")
addBtn = Button(leftframe, image=addPhoto, command = browseFile)
delBtn = Button(leftframe, image=delPhoto, command = del_song)

label3=ttk.Label(leftframe,text="Current Songs")
label3.pack()

playlistbox = Listbox(leftframe)
playlistbox.pack()



addBtn.pack()
delBtn.pack(pady=10)

# --- Right Frame ---
rightframe = ttk.Frame(root)
rightframe.pack()
#--------------------

# --- Top Frame -----
topframe = ttk.Frame(root)
topframe.pack(pady = 20)
#---------------


# ----------------

# --- Submenu ---

menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browseFile)
submenu.add_command(label="Load Playlist", command=loadfromdb)
submenu.add_command(label="Exit", command=root.destroy)
# ----------------
#--- Info about us ---

def aboutUs():
    tkinter.messagebox.showinfo('About Us', 'This Project is made by : \n1) Parth (18CE2019) \n2) Sushil (18CE2011) \n3) Prithvi (18CE2007)\n4) Samiksha(18C32030)')

# -------------------

submenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About Us", command=aboutUs)

# ---------------



# MAIN
mixer.init()
root.title("MP3 Player")
root.iconbitmap(r'icon.ico')

# -- Images -------
playPhoto = PhotoImage(file="Images/play.png")
pausePhoto = PhotoImage(file="Images/pause.png")
stopPhoto = PhotoImage(file="Images/Stop.png")
unmutePhoto = PhotoImage(file="Images/lmute.png")
mutePhoto = PhotoImage(file="Images/mute.png")

# --------------
usernamelabel = ttk.Label(topframe, text='Play List:')
usernamelabel.pack()

userentry = ttk.Entry(topframe)
userentry.pack()

usernamelabel1 = ttk.Label(topframe)
usernamelabel1.pack()

loadbtn=ttk.Button(topframe,command=loadfromdb,text='''Load''')
loadbtn.pack()

usernamelabel2 = ttk.Label(topframe)
usernamelabel2.pack()

newplaylist=ttk.Button(topframe,command=newplaylist,text='''New Playlist''')
newplaylist.pack()

usernamelabel2 = ttk.Label(topframe,text="")
usernamelabel2.pack()

lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
lengthlabel.pack()

currentlabel = ttk.Label(topframe, text="Current Time : --:-- ")
currentlabel.pack()


# --- Middle Frame ---

middleFrame = ttk.Frame(root, relief=RAISED, borderwidth=1)
middleFrame.pack(padx = 30, pady = 20)

#----Playlist List Box ----#
label4=ttk.Label(leftframe,text="List of playlist")
label4.pack()
playlist_list_box1 = Listbox(leftframe)
playlist_list_box1.pack()


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] ==".mp3":
        audio = MP3(play_song)
        total_length=audio.info.length

    else:
        tkinter.messagebox.showerror('Error 000002x', 'Use a mp3 file only')

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1= threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currentlabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time = current_time+1



# --- Play music ---
def playFunction():
    global paused
    if paused:
        mixer.music.unpause()
#        playBtn.configure(image=pausePhoto)
        paused = FALSE

    else:
        try:
            stopFunction()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            show_details(play_it)

            paused = FALSE


        except FileNotFoundError:
            tkinter.messagebox.showerror('Error 000001x ', 'The file could not be found or is corrupted.')

        else:
            print("No error")


playBtn = Button(middleFrame, image=playPhoto, command=playFunction, highlightthickness = 0, bd = 0)
playBtn.grid(row=2, column=0, padx = 10)
# --------------------
paused = FALSE
# --- Pause music ---
def pauseFunction():
    global paused
    paused = TRUE
    mixer.music.pause()

pauseBtn = Button(middleFrame, image = pausePhoto, command = lambda : pauseFunction(), highlightthickness = 0, bd = 0)
pauseBtn.grid(row = 2,column=1, padx = 10)
# --------------------
# --- Unpause Function -----




# ----------------------------
# --- Stop music -----
def stopFunction():
    global stopped
    stopped = TRUE
    mixer.music.stop()


stopBtn = Button(middleFrame, image=stopPhoto, command=lambda:stopFunction(), highlightthickness=0, bd=0)
stopBtn.grid(row = 2,column=2, padx = 10)

# ---------------------
# --- Bottom Frame -----

bottomframe = ttk.Frame(root, relief=RAISED, borderwidth=1)
bottomframe.pack(padx = 30, pady=20)


# ----------------------
# --- mute and unmute ----
muted = FALSE
def muteFunction():
    global muted
    if muted :
        unmuteBtn.configure(image=unmutePhoto)
        mixer.music.set_volume(0.5)
        muted = FALSE
        scale.set(50)
    else:
        unmuteBtn.configure(image=mutePhoto)
        mixer.music.set_volume(0)
        scale.set(0)
        muted = TRUE


unmuteBtn = Button(bottomframe, image=unmutePhoto, command=muteFunction, highlightthickness=0, bd=0)
unmuteBtn.grid(row=0, column=1)
# ----------------------------

# --- Volume Slider ---
def setVolume(val):
    vol = float(val)/100
    mixer.music.set_volume(vol)
    if vol > 0:
        unmuteBtn.configure(image=unmutePhoto)
        muted = FALSE

    if vol == 0:
        unmuteBtn.configure(image=mutePhoto)
        muted = TRUE


scale = ttk.Scale(bottomframe, from_ = 0, to = 100, orient=HORIZONTAL, command =setVolume)
scale.set(50)
mixer.music.set_volume(0.5)
scale.grid(row = 0, column = 2,pady = 15)

listofplaylist()

# ----------
def on_closing():
    stopFunction()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
# def start():
#     root.protocol("WM_DELETE_WINDOW", on_closing)
#     root.mainloop()
