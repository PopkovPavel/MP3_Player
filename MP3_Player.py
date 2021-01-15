import keyboard as keyboard
import pygame
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.messagebox as tkMessageBox
import mutagen.mp3
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from pathlib import Path
from decimal import *
from PIL import ImageTk, Image
from PIL.ImageTk import PhotoImage
import os
import random
import ctypes

root = Tk()
backgroundImage = PhotoImage(file=Path("images/bg.png"))
backgroundLabel = Label(image=backgroundImage)
backgroundLabel.place(x=-2, y=-2)
root.overrideredirect(0)
root.title("MP3_Player")
root.iconbitmap(Path("images/icon.ico"))
root.geometry("1000x500")
root.resizable(0, 0)

ListOfSongs = []
RealNames = []
LengthFiles = []
PathToFiles = []
NamesList = []
AuthorsList = []

index = 0
vol = 0.33
vol2 = 0
ListSize = 0
playing = False
repeat = 0
loopID = 0

"""Играющий трек"""
TrackName = StringVar()
TrackName_Label = Label(root,
                        justify="center",
                        anchor="s",
                        textvariable=TrackName,
                        bg="black",
                        fg="royalblue",
                        font=("Arial", 18, "bold"),
                        width=36)
TrackName_Label.place(x=450, y=150)

"""Играющий автор"""
TrackAuthor = StringVar()
TrackAuthor_Label = Label(root,
                          justify="center",
                          textvariable=TrackAuthor,
                          bg="black",
                          fg="royalblue",
                          font=("Arial", 12, "bold"),
                          width=36)
TrackAuthor_Label.place(x=540, y=190)

"""Предыдущий Трек"""
PreviousTrackName = StringVar()
PreviousTrack_Label = Label(root,
                            justify="center",
                            anchor="e",
                            textvariable=PreviousTrackName,
                            bg="black",
                            fg="royalblue",
                            font=("Arial", 8, "bold"),
                            width=28)
PreviousTrack_Label.place(x=435, y=348)

"""Предыдущий Автор"""
PreviousTrackAuthor = StringVar()
PreviousTrackAuthor_Label = Label(root,
                                  justify="center",
                                  anchor="e",
                                  textvariable=PreviousTrackAuthor,
                                  bg="black",
                                  fg="royalblue",
                                  font=("Arial", 7, "bold"),
                                  width=28)
PreviousTrackAuthor_Label.place(x=463, y=368)

"""Следующий Трек"""
NextTrackName = StringVar()
NextTrack_Label = Label(root,
                        justify="center",
                        anchor="w",
                        textvariable=NextTrackName,
                        bg="black",
                        fg="royalblue",
                        font=("Arial", 8, "bold"),
                        width=28)
NextTrack_Label.place(x=803, y=348)

"""Следующий Автор"""
NextTrackAuthor = StringVar()
NextTrackAuthor_Label = Label(root,
                              justify="center",
                              anchor="w",
                              textvariable=NextTrackAuthor,
                              bg="black",
                              fg="royalblue",
                              font=("Arial", 7, "bold"),
                              width=28)
NextTrackAuthor_Label.place(x=803, y=368)

"""Громкость (Число)"""
Volume = StringVar()
Volume_Label = Label(root,
                     justify="center",
                     textvariable=Volume,
                     bg="black",
                     fg="royalblue",
                     font=("Arial", 14, "bold"),
                     width=3)
Volume_Label.place(x=898, y=34)

"""Громкость (%)"""
VolumePercent = StringVar()
VolumePercent_Label = Label(root,
                            justify="center",
                            textvariable=VolumePercent,
                            bg="black",
                            fg="royalblue",
                            font=("Arial", 14, "bold"),
                            width=1)
VolumePercent_Label.place(x=935, y=34)

"""Повтор (Надпись)"""
Repeat = StringVar()
Repeat_Label = Label(root,
                     justify="center",
                     anchor="w",
                     textvariable=Repeat,
                     bg="black",
                     fg="royalblue",
                     font=("Arial", 8, "bold"),
                     width=12)
Repeat_Label.place(x=785, y=427)

"""Случайный трек (Надпись)"""
RandomTrack = StringVar()
RandomTrack_Label = Label(root,
                          justify="center",
                          anchor="e",
                          textvariable=RandomTrack,
                          bg="black",
                          fg="royalblue",
                          font=("Arial", 8, "bold"),
                          width=12)
RandomTrack_Label.place(x=565, y=427)

"""Номер трека (Надпись)"""
NumberTrack = StringVar()
NumberTrack_Label = Label(root,
                          justify="center",
                          anchor="n",
                          textvariable=NumberTrack,
                          bg="black",
                          fg="royalblue",
                          font=("Arial", 10, "bold"),
                          width=10)
NumberTrack_Label.place(x=680, y=235)

"""Таймер трека"""
TimeTrack = StringVar()
TimeTrack_Label = Label(root,
                        justify="center",
                        anchor="w",
                        textvariable=TimeTrack,
                        bg="black",
                        fg="royalblue",
                        font=("Arial", 8, "bold"),
                        width=6)
TimeTrack_Label.place(x=511, y=290)

"""Время трека"""
FullTimeTrack = StringVar()
FullTimeTrack_Label = Label(root,
                            justify="center",
                            anchor="e",
                            textvariable=FullTimeTrack,
                            bg="black",
                            fg="royalblue",
                            font=("Arial", 8, "bold"),
                            width=6)
FullTimeTrack_Label.place(x=886, y=290)

"""Текущая папка (Надпись)"""
CurrentFolder = StringVar()
CurrentFolder_Label = Label(root,
                            justify="center",
                            anchor="w",
                            textvariable=CurrentFolder,
                            bg="black",
                            fg="royalblue",
                            font=("Arial", 10, "bold"),
                            width=30)
CurrentFolder_Label.place(x=600, y=25)

image = Image.open(Path("C:/MP3_Player/images/Albumart_default.jpg"))
pic = ImageTk.PhotoImage(image.resize((400, 400)))
Picture_Label = Label(root, image=pic, bg="black")
Picture_Label.place(x=50, y=50)

MessageBox = ctypes.windll.user32.MessageBoxW

"""""""""Функции"""""""""


def DirectoryChooser():
    """Выбор директории"""
    global ListSize, directory
    try:
        directory = askdirectory()
        os.chdir(directory)
    except (ValueError, Exception):
        MessageBox(None, "Choose correct directory.\nThe app will close.", "Error", 0)
        root.destroy()

    # APIC - picture / TIT2 - name / TPE1 - author
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            #print("-mp3 file found")
            realdir = os.path.realpath(files)
            audio = MP3(files)
            LengthFiles.append(round(audio.info.length))
            PathToFiles.append(os.path.realpath(files))
            ListSize = ListSize + 1
            try:
                audio = ID3(realdir)
                try:
                    RealNames.append(audio["TIT2"].text[0] + " - " + audio["TPE1"].text[0])
                except (ValueError, Exception):
                    RealNames.append(audio["TIT2"].text[0] + " - " + "<unknown>")
            except (ValueError, Exception):
                os.path.splitext(files)
                RealNames.append(os.path.splitext(files)[0])
            ListOfSongs.append(files)
            """Проверка на сущ. название и автора"""
            try:
                audio = ID3(realdir)
                try:
                    NamesList.append(audio["TIT2"].text[0])
                except (ValueError, Exception):
                    # NamesList.append(files)
                    NamesList.append(os.path.splitext(files)[0])
                try:
                    AuthorsList.append(audio["TPE1"].text[0])
                except (ValueError, Exception):
                    AuthorsList.append("<unknown>")
            except (ValueError, Exception):
                """Unknown name & author"""
                NamesList.append(os.path.splitext(files)[0])
                AuthorsList.append("<unknown>")
    #print(LengthFiles)
    #print(PathToFiles)
    #print(str(ListOfSongs))
    try:
        pygame.mixer.init()
        #print("Attempt to load ListOfSongs...")
        pygame.mixer.music.load(ListOfSongs[0])
        #print("Success!")

    except (ValueError, Exception):
        #print("Failed!")
        #print("Probably missing libmpg123-0.dll in system32 directory.")
        MessageBox(None, "Choose correct directory", "Error", 0)
        DirectoryChooser()


def LabelsLength():
    """Регулировка длины названий и авторов"""
    if 32 <= len(str(NamesList[index])) < 39:
        TrackName_Label.config(font=("Arial", 14, "bold"), width=36)
        TrackName_Label.place(x=500, y=155)
        TrackName.set(NamesList[index])
    elif len(str(NamesList[index])) >= 39:
        TrackName_Label.config(font=("Arial", 10, "bold"), width=60)
        TrackName_Label.place(x=480, y=160)
        TrackName.set(NamesList[index])
    else:
        TrackName_Label.config(font=("Arial", 18, "bold"), width=36)
        TrackName_Label.place(x=450, y=150)
        TrackName.set(NamesList[index])
    """Регулировка длины автора трека"""
    if len(str(AuthorsList[index])) >= 37:
        TrackAuthor_Label.config(font=("Arial", 10, "bold"), width=60)
        TrackAuthor_Label.place(x=480, y=192)
        TrackAuthor.set(AuthorsList[index])
    else:
        TrackAuthor_Label.config(font=("Arial", 12, "bold"), width=36)
        TrackAuthor_Label.place(x=540, y=190)
        TrackAuthor.set(AuthorsList[index])
    try:
        """Регулировка длины названия пред. трека"""
        if len(str(NamesList[index - 1])) >= 30:
            psn = str(NamesList[index - 1])
            PreviousTrackName.set(psn[0:25] + "...")
        else:
            PreviousTrackName.set(NamesList[index - 1])
        """Регулировка длины названия пред. автора"""
        if len(str(AuthorsList[index - 1])) >= 30:
            psa = str(AuthorsList[index - 1])
            PreviousTrackAuthor.set(psa[0:22] + "...")
        else:
            PreviousTrackAuthor.set(AuthorsList[index - 1])
    except (ValueError, Exception):
        PreviousTrackName.set(NamesList[ListSize - 1])
        PreviousTrackAuthor.set(AuthorsList[ListSize - 1])
    try:
        """Регулировка длины названия след. трека"""
        if len(str(NamesList[index + 1])) >= 30:
            psn = str(NamesList[index + 1])
            NextTrackName.set(psn[0:25] + "...")
        else:
            NextTrackName.set(NamesList[index + 1])
        """Регулировка длины названия след. автора"""
        if len(str(AuthorsList[index + 1])) >= 30:
            psa = str(AuthorsList[index + 1])
            NextTrackAuthor.set(psa[0:22] + "...")
        else:
            NextTrackAuthor.set(AuthorsList[index + 1])
    except (ValueError, Exception):
        NextTrackName.set(NamesList[0])
        NextTrackAuthor.set(AuthorsList[0])


def UpdateLabel():
    """Обновление надписей"""
    global index
    global ListSize
    if index == ListSize:
        index = -1
    if index < 0:
        index = ListSize - 1
    LabelsLength()


def NextSong(_event):
    """Следующий трек"""
    global index, playing, playtime, ListSize, NumberTrack
    if index + 1 == ListSize:
        index += 1
        #print("ListID: 0")
    else:
        index += 1
        #print("ListID: " + str(index))
    try:
        pygame.mixer.music.load(ListOfSongs[index])
    except (ValueError, Exception):
        index = 0
        pygame.mixer.music.load(ListOfSongs[index])
    root.after_cancel(loopID)
    Stop()
    slider_value.set(0)
    playtime = slider_value.get()
    TrackSec(playtime)
    TrackSecFull(playtime)
    Play()
    PUbutton.config(text="Pause")
    PUbutton.config(image=Player_pause)
    slider.config(to=LengthFiles[index])
    UpdateLabel()
    ImagePutter()
    playing = True
    NumberTrack.set("Track №" + str(index + 1))
    print("Now playing: " + NamesList[index] + " - " + AuthorsList[index] + " | #" + str(index + 1))


def PreviousSong(_event):
    """Предыдущий трек"""
    global index, playing, playtime, ListSize, NumberTrack
    if index - 1 == -1:
        index -= 1
        #print("ListID: " + str(ListSize - 1))
    else:
        index -= 1
        #print("ListID: " + str(index))
    try:
        pygame.mixer.music.load(ListOfSongs[index])
    except (ValueError, Exception):
        index = ListSize - 1
        pygame.mixer.music.load(ListOfSongs[index])
    root.after_cancel(loopID)
    Stop()
    slider_value.set(0)
    playtime = slider_value.get()
    TrackSec(playtime)
    TrackSecFull(playtime)
    Play()
    PUbutton.config(text="Pause")
    PUbutton.config(image=Player_pause)
    slider.config(to=LengthFiles[index])
    UpdateLabel()
    ImagePutter()
    playing = True
    NumberTrack.set("Track №" + str(index + 1))

    print("Now playing: " + NamesList[index] + " - " + AuthorsList[index] + " | #" + str(index + 1))


def PauseUnpause():
    """Пауза & продолжение"""
    global playing, playtime
    if not playing:
        playing = True
        playtime = slider_value.get()
        pygame.mixer.music.play()
        #print("ListID: " + str(index))
        print("Now playing: " + NamesList[index] + " - " + AuthorsList[index] + " | #" + str(index + 1))
    if PUbutton.config("text")[-1] == "Pause":
        PUbutton.config(text="Play")
        PUbutton.config(image=Player_play)
        Stop()
        root.after_cancel(loopID)
        # print("Pause...")
    else:
        PUbutton.config(text="Pause")
        PUbutton.config(image=Player_pause)
        Stop()
        playtime = slider_value.get()
        TrackSec(playtime)
        TrackSecFull(playtime)
        Play()
        playing = True
        # print("Unpause...")


def UpdateVolume():
    """Обновление звука"""
    global vol
    vol = vol * 100
    vol = int(vol)
    Volume.set(vol)
    vol = vol / 100


def SetVolume(_var):
    """Установка звука"""
    global vol
    vol = Decimal(_var) / 100
    pygame.mixer.music.set_volume(vol)
    UpdateVolume()
    if vol == 0:
        VolumeButton.config(image=Volume_Off, text="Off")
        VolumeButton.place(x=824, y=1)
    elif vol < 0.33:
        VolumeButton.config(image=Volume_Low, text="On")
        VolumeButton.place(x=816, y=1)
    elif vol < 0.66:
        VolumeButton.config(image=Volume_Medium, text="On")
        VolumeButton.place(x=820, y=1)
    elif vol <= 1:
        VolumeButton.config(image=Volume_High, text="On")
        VolumeButton.place(x=824, y=1)


def OffOnVolume():
    """Вкл/выкл звука"""
    global vol2
    if VolumeButton.config("text")[-1] == "Off":
        VolumeButton.config(text="Off")
        VolumeButton.config(image=Player_play)
        VolumeScale.set(vol2)
        VolumeButton.config(image=Volume_Medium)
    else:
        VolumeButton.config(text="On")
        vol2 = vol * 100
        VolumeButton.config(image=Player_pause)
        VolumeScale.set(0)
        VolumeButton.config(image=Volume_Off)
    UpdateVolume()


def SongRepeat(_event):
    """Повтор списка треков"""
    global repeat
    if RepeatButton.config("text")[-1] == "Repeat: Off":
        RepeatButton.config(text="Repeat: On", image=Player_repeat_on)
        repeat = 1
        Repeat.set("Repeat: On")
        #print("Repeat: On")
    elif RepeatButton.config("text")[-1] == "Repeat: On":
        RepeatButton.config(text="Repeat: Once", image=Player_repeat_once)
        repeat = 2
        Repeat.set("Repeat: Once")
        #print("Repeat: Once")
    elif RepeatButton.config("text")[-1] == "Repeat: Once":
        RepeatButton.config(text="Repeat: Off", image=Player_repeat_off)
        repeat = 0
        Repeat.set("Repeat: Off")
        #print("Repeat: Off")


def RandomTrackPlay(_event):
    """Случайный трек"""
    global index, playtime
    randtrack = random.randint(0, ListSize - 1)
    if index == randtrack:
        RandomTrackPlay(event)
        #print("Random picked the same number")
    else:
        index = randtrack
        pygame.mixer.music.load(ListOfSongs[randtrack])
        PUbutton.config(text="Pause", image=Player_pause)
        slider.config(to=LengthFiles[index])
        ImagePutter()
        root.after_cancel(loopID)
        Stop()
        slider_value.set(0)
        playtime = slider_value.get()
        TrackSec(playtime)
        TrackSecFull(playtime)
        Play()
        LabelsLength()
        NumberTrack.set("Track №" + str(index + 1))
        print("Random Picked: " + NamesList[randtrack] + " - " + AuthorsList[randtrack] + " | #" + str(randtrack + 1))


def QuitConfirm():
    """Подтверждение выхода"""
    if tkMessageBox.askokcancel("Message", "Exit MP3_Player?"):
        pygame.mixer.stop()
        pygame.mixer.quit()
        root.destroy()


def apic_extract(mp3, jpg=None):
    """Извлечение картинки из .mp3 файла"""
    try:
        tags = mutagen.mp3.Open(mp3)
    except (ValueError, Exception):
        return False
    data = ""
    for i in tags:
        if i.startswith("APIC"):
            data = tags[i].data
            break
    if not data:
        return None
    if jpg is not None:
        out = open(jpg, "wb")
        out.write(data)
        out.close()
        return True
    return data


def ImagePutter():
    """Вставка картинки в слой"""
    global image, pic
    mp3_filename = PathToFiles[index]
    jpg_filename = Path("C:/MP3_Player/images/Albumart.jpg")
    status = apic_extract(mp3_filename, jpg_filename)
    if status is None:
        image = Image.open(Path("C:/MP3_Player/images/Albumart_default.jpg"))
        pic = ImageTk.PhotoImage(image.resize((400, 400)))
        Picture_Label.config(image=pic)
    else:
        image = Image.open(jpg_filename)
        pic = ImageTk.PhotoImage(image.resize((400, 400)))
        Picture_Label.config(image=pic)


def Play():
    global playtime
    """Запуск трека"""
    playtime = slider_value.get()
    pygame.mixer.music.play(start=playtime)
    TrackPlay(playtime)


def Stop():
    """Остановка трека"""
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()


def TrackSec(_playtime):
    """Секунды трека"""
    seconds = int(_playtime)
    m, s = divmod(seconds, 60)
    if s < 10:
        timer = (str(m) + ":0" + str(s))
    else:
        timer = (str(m) + ":" + str(s))
    TimeTrack.set(timer)


def TrackSecFull(_playtime):
    """Длина трека"""
    m2, s2 = divmod(LengthFiles[index], 60)
    if s2 < 10:
        timer2 = (str(m2) + ":0" + str(s2))
    else:
        timer2 = (str(m2) + ":" + str(s2))
    FullTimeTrack.set(timer2)


def KeyboardChecker():
    """Кнопки вверх, вниз, влево, вправо"""
    global loopID2, vol, event, playtime, is_toplevel, _event
    event = None
    root.update_idletasks()
    width, height, x, y = root.winfo_width(), root.winfo_height(), root.winfo_rootx(), root.winfo_rooty()
    if (width, height, x, y) != (1, 1, 0, 0):
        is_toplevel = root.winfo_containing(x + (width // 2), y + (height // 2)) is not None
        #print('is_toplevel: {}'.format(is_toplevel))
    if is_toplevel:
        """Громкость тише на 5% [down]"""
        if keyboard.is_pressed("down"):
            vol = vol * 100
            vol = int(vol)
            if vol - 5 <= 0:
                vol = 0
            else:
                vol = vol - 5
            VolumeScale.set(vol)
            Volume.set(vol)
            vol = vol / 100
        """Громкость выше на 5% [up]"""
        if keyboard.is_pressed("up"):
            vol = vol * 100
            vol = int(vol)
            if vol + 5 >= 100:
                vol = 100
            else:
                vol = vol + 5
            VolumeScale.set(vol)
            Volume.set(vol)
            vol = vol / 100
        """Перемотать назад на 5 сек [left]"""
        if keyboard.is_pressed("left"):
            playtime = slider_value.get()
            UpdateSlider(playtime-5)
        """Перемотать вперёд на 5 сек [right]"""
        if keyboard.is_pressed("right"):
            playtime = slider_value.get()
            UpdateSlider(playtime + 5)
        """Пауза/продолжить [space]"""
        if keyboard.is_pressed("space"):
            PauseUnpause()
        """Предыдущий трек [a]"""
        if keyboard.is_pressed("a"):
            PreviousSong(0)
        """Следующий трек [d]"""
        if keyboard.is_pressed("d"):
            NextSong(0)
        """Повтор [r]"""
        if keyboard.is_pressed("r"):
            SongRepeat(0)
        """Случайный трек [q]"""
        if keyboard.is_pressed("q"):
            RandomTrackPlay(0)
        """Выбор папки [f]"""
        if keyboard.is_pressed("f"):
            FolderChoose(0)
        """Выход из приложения [esc]"""
        if keyboard.is_pressed("esc"):
            QuitConfirm()
    else:
        pass

    loopID2 = root.after(70, lambda: KeyboardChecker())


def TrackPlay(_playtime):
    """Цикл воспроизведения"""
    global loopID, event
    event = None
    if pygame.mixer.music.get_busy():
        slider_value.set(_playtime)
        _playtime += 1.0
        TrackSec(_playtime - 1)
        TrackSecFull(_playtime)

        loopID = root.after(1000, lambda: TrackPlay(_playtime))
    else:
        """Если трек закончился"""
        if repeat == 0:
            if index + 1 == ListSize:
                NextSong(event)
                root.after_cancel(loopID)
                Stop()
                PUbutton.config(text="Play")
                PUbutton.config(image=Player_play)
                #print("List Ended")
            else:
                NextSong(event)
                #print("Track Ended")
        elif repeat == 1:
            NextSong(event)
            #print("Track Ended")
        elif repeat == 2:
            root.after_cancel(loopID)
            Stop()
            slider_value.set(0)
            _playtime = slider_value.get()
            TrackSec(_playtime)
            TrackSecFull(_playtime)
            Play()
            #print("ListID: " + str(index))
            print("Now playing: " + NamesList[index] + " - " + AuthorsList[index] + " | #" + str(index + 1))


def UpdateSlider(value):
    """Обновление слайдера трека"""
    global loopID, playtime

    if pygame.mixer.music.get_busy():
        root.after_cancel(loopID)
        # slider_value.set(value)
        playtime = slider_value.get()
        TrackSec(playtime)
        if PUbutton.config("text")[-1] == "Pause":
            slider_value.set(value)
            Play()
    else:
        playtime = slider_value.get()
        TrackSec(playtime)
        slider_value.set(value)


def FolderChoose(_event):
    """Повторный выбор директории"""
    global ListOfSongs, RealNames, LengthFiles, PathToFiles, NamesList, AuthorsList, \
        index, vol, vol2, ListSize, playing, repeat, loopID, loopID2, playtime
    try:
        root.after_cancel(loopID)
        #root.after_cancel(loopID2)
        Stop()
        PUbutton.config(text="Play")
        PUbutton.config(image=Player_play)
        ListOfSongs = []
        RealNames = []
        LengthFiles = []
        PathToFiles = []
        NamesList = []
        AuthorsList = []
        index = 0
        vol2 = 0
        ListSize = 0
        playing = False
        loopID = 0

        DirectoryChooser()

        _cur_fol = str(os.path.basename(os.path.normpath(os.getcwd())))
        if len(_cur_fol) >= 35:
            CurrentFolder.set(_cur_fol[0:33] + "...")
        else:
            CurrentFolder.set(_cur_fol)
        UpdateLabel()
        UpdateVolume()
        ImagePutter()
        slider_value.set(0)
        playtime = slider_value.get()
        TrackSec(playtime)
        TrackSecFull(playtime)
        Play()
        Stop()
        root.after_cancel(loopID)
        #KeyboardChecker()
        NumberTrack.set("Track №" + str(index + 1))
    except (ValueError, Exception):
        pygame.mixer.quit()
        root.destroy()


Player_fwd = PhotoImage(file=Path("images/skip-forward.png"))
Player_rew = PhotoImage(file=Path("images/skip-backward.png"))
Player_play = PhotoImage(file=Path("images/play.png"))
Player_pause = PhotoImage(file=Path("images/pause.png"))
Player_repeat_off = PhotoImage(file=Path("images/repeat-off.png"))
Player_repeat_on = PhotoImage(file=Path("images/repeat-on.png"))
Player_repeat_once = PhotoImage(file=Path("images/repeat-once.png"))
Player_random_track = PhotoImage(file=Path("images/random-track.png"))
Volume_Off = PhotoImage(file=Path("images/volume-off.png"))
Volume_Low = PhotoImage(file=Path("images/volume-low.png"))
Volume_Medium = PhotoImage(file=Path("images/volume-medium.png"))
Volume_High = PhotoImage(file=Path("images/volume-high.png"))
Folder = PhotoImage(file=Path("images/folder-music.png"))

"""Выбор директории"""
DirectoryChooser()

NextButton = Button(root,
                    bd=0,
                    relief="flat",
                    bg="black",
                    activebackground="black",
                    image=Player_fwd)
NextButton.place(x=768, y=350)

PreviousButton = Button(root,
                        bd=0,
                        relief="flat",
                        bg="black",
                        activebackground="black",
                        image=Player_rew)
PreviousButton.place(x=638, y=350)

PUbutton = Button(root,
                  text="Play",
                  command=PauseUnpause,
                  bd=0,
                  relief="flat",
                  bg="black",
                  activebackground="black",
                  image=Player_play)
PUbutton.place(x=688, y=334)

VolumeButton = Button(root,
                      text="On",
                      bd=0,
                      relief="flat",
                      bg="black",
                      activebackground="black",
                      command=OffOnVolume)
VolumeButton.place(x=940, y=1)

RandomTrackButton = Button(root,
                           bd=0,
                           relief="flat",
                           bg="black",
                           activebackground="black",
                           image=Player_random_track)
RandomTrackButton.place(x=658, y=420)

RepeatButton = Button(root,
                      bd=0,
                      text="Repeat: Off",
                      relief="flat",
                      bg="black",
                      activebackground="black",
                      image=Player_repeat_off)
RepeatButton.place(x=748, y=420)

FolderButton = Button(root,
                      bd=0,
                      relief="flat",
                      bg="black",
                      activebackground="black",
                      image=Folder)
FolderButton.place(x=530, y=1)

NextButton.bind("<Button-1>", NextSong)
PreviousButton.bind("<Button-1>", PreviousSong)
RandomTrackButton.bind("<Button-1>", RandomTrackPlay)
RepeatButton.bind("<Button-1>", SongRepeat)
FolderButton.bind("<Button-1>", FolderChoose)

"""Вывод текущей директории"""
cur_fol = str(os.path.basename(os.path.normpath(os.getcwd())))
if len(cur_fol) >= 35:
    CurrentFolder.set(cur_fol[0:31] + "...")
else:
    CurrentFolder.set(cur_fol)

"""Слайдер для громкости"""
var = DoubleVar()
VolumeScale = Scale(root,
                    bg="royalblue",
                    fg="royalblue",
                    highlightbackground="royalblue",
                    highlightcolor="royalblue",
                    troughcolor="black",
                    showvalue="0",
                    sliderlength="20",
                    sliderrelief="flat",
                    activebackground="white",
                    bd=0,
                    font=("Arial", 14, "bold"),
                    command=SetVolume,
                    variable=var,
                    resolution=1,
                    from_=0,
                    to=100,
                    orient="horizontal")
VolumeScale.place(x=880, y=17)

"""Слайдер для трека"""
slider_value = DoubleVar()
slider = Scale(root,
               bg="white",
               fg="royalblue",
               highlightbackground="royalblue",
               highlightcolor="royalblue",
               troughcolor="black",
               showvalue="0",
               sliderlength="20",
               sliderrelief="flat",
               activebackground="white",
               bd=0,
               font=("Arial", 8, "bold"),
               from_=0,
               to=LengthFiles[index],
               orient="horizontal",
               length=420,
               resolution=1,
               variable=slider_value,
               command=UpdateSlider)
slider.place(x=510, y=270)

VolumeScale.set(30)
VolumePercent.set("%")
Repeat.set("Repeat: Off")
RandomTrack.set("Random Track")
NumberTrack.set("Track №" + str(index + 1))
UpdateLabel()
UpdateVolume()
ImagePutter()
Play()
Stop()
root.after_cancel(loopID)
KeyboardChecker()
"""Подтверждение выхода"""
root.protocol("WM_DELETE_WINDOW", QuitConfirm)

root.mainloop()
