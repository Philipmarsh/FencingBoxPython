import winsound
from tkinter import *
import threading
import time

#TODO work out what the lockout time actually is
#Not as important is to allow doubles to keep going off if epees are continually pressed
full_screen_bool = False
window = Tk()
window.overrideredirect(full_screen_bool)
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
window.title("Fencing Box")
label = Label(window, text="3:00")
label.pack()
canvas = Canvas(window, width=1520, height=500, background='white')
line1 = canvas.create_line(760, 0, 760, 500)
txt = canvas.create_text(330, 330, text="Green", font="Arial 16", fill="green")
txt1 = canvas.create_text(1190, 330, text="Red", font="Arial 16", fill="red")
canvas.pack()

def not_full_screen(event):
    global full_screen_bool
    full_screen_bool = False
    window.overrideredirect(full_screen_bool)

def full_screen(event):
    global full_screen_bool
    full_screen_bool = True
    window.overrideredirect(full_screen_bool)

canvas.bind('<Escape>', not_full_screen)
canvas.bind('f', full_screen)
#To make the red and green lights not break the program, use the same logic for the grounding wires, ie bool 
#to be true or false. then use an after function to allow the bool to change back and the button to be pressed again
red_allowed = True
green_allowed = True

def reset_both():
    global green_allowed
    global red_allowed
    canvas.bind('2', green)
    canvas.bind('1', red)
    try:
      canvas.delete(window.greenbox)
    except:
      print('does not exist')
    try:
      canvas.delete(window.redbox)
    except: 
      print("doesnt exist")
    green_allowed = True
    red_allowed = True
    
    

#defining the grounding wires
xgrounding = False
zgrounding = False

def xground(event):
    global xgrounding
    if xgrounding == False:
        xgrounding = True
        print(xgrounding)
    else: return

def xgroundfinish(event):
    global xgrounding
    xgrounding = False
    print(xgrounding)

def zground(event):
    global zgrounding
    if zgrounding == False:
        zgrounding = True
        print(zgrounding)
    else: return
def zgroundfinish(event):
    global zgrounding
    zgrounding = False
    print(zgrounding)

canvas.bind('<x>', xground )
canvas.bind('<z>', zground)
canvas.bind('<KeyRelease-x>', xgroundfinish)
canvas.bind('<KeyRelease-z>', zgroundfinish)
#This section defines the menu bar
menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Epee")
menu1.add_command(label="Foil")
menu1.add_command(label="Sabre")
if full_screen_bool == False:
    menu1.add_command(label="Enter Full Screen mode (f)")
#elif full_screen_bool == True:
#    menu1.add_command(label="Exit Full Screen mode (Esc)")
menu1.add_separator()
menu1.add_command(label="Quit")
menubar.add_cascade(label="File", menu=menu1)
window.config(menu=menubar)

#This section describes how the box actually works


def double_search_red():

   timer1 = time.perf_counter_ns()
   def greenhit(r):
       global xgrounding
       global green_allowed
       if xgrounding == False and green_allowed == True :
           green_allowed = False
           nonlocal timer1
           timer2 = time.perf_counter_ns()
           time_elapsed = timer2 - timer1
       
           if time_elapsed <= 80000000:
               green_allowed = False
               print(time_elapsed)
               window.greenbox = canvas.create_rectangle(0, 0, 760, 500, fill="green")
               window.update_idletasks()
              
       else: return
       
   canvas.bind('2', greenhit)

def double_search_green():
   
   timer1 = time.perf_counter_ns()

  

   def redhit(r):
       global zgrounding
       global red_allowed
       if zgrounding == False and red_allowed == True:
           red_allowed = False
           nonlocal timer1
           timer2 = time.perf_counter_ns()
           time_elapsed = timer2 - timer1
       
       
           if time_elapsed <= 80000000:
               print(time_elapsed)
               window.redbox = canvas.create_rectangle(760, 0, 1520, 500, fill="red")
               window.update_idletasks()
           

              
       else: return
        
   canvas.bind('1', redhit)




def red(event):

    global zgrounding
    global red_allowed

    def redlight():

        window.redbox = canvas.create_rectangle(760, 0, 1520, 500, fill="red")
        window.update_idletasks()
        touche = event.keysym
        print(touche)
        winsound.Beep(5000, 1000)
        canvas.after(1000, reset_both)
    if zgrounding == False and red_allowed == True:
        red_allowed = False
        t = threading.Thread(target=double_search_red, name='thread1')
        t1 = threading.Thread(target=redlight, name='thread2')
        t.start()
        t1.start()
        window.update_idletasks()



        global running
        if running:
            running = False
            start['state'] = 'normal'
            stop['state'] = 'disabled'
            Reset['state'] = 'normal'
        else:
            print("The timer was not running")

    else:
        return


     
def green(event):
    global green_allowed
    global xgrounding
    def greenlight():
        window.greenbox = canvas.create_rectangle(0, 0, 760, 500, fill="green")
        window.update_idletasks()
        touche = event.keysym
        print(touche)
        winsound.Beep(5000, 1000)
        canvas.after(1000, reset_both)
    if xgrounding == False and green_allowed == True:
        green_allowed = False
        t2 = threading.Thread(target=double_search_green, name='thread1')
        t3 = threading.Thread(target=greenlight, name='thread2')
        t2.start()
        t3.start()
        window.update_idletasks()

    
        global running
        if running:
            running = False
            start['state'] = 'normal'
            stop['state'] = 'disabled'
            Reset['state'] = 'normal'
        else:
            print("The timer was not running")
    else:
        return 


canvas.focus_set()
canvas.bind("1", red)
canvas.bind("2", green)

canvas.pack()



counter = 180

running = False


def counter_label(label):
    def count():
        rangelist = [0,1,2,3,4,5,6,7,8,9]
        global counter
        counter1 = counter / 60
        counter2 = counter % 60
        if running:
            if counter == -1:
                stop()
                start['state'] = 'disabled'
                stop['state'] = 'disabled'
                Reset['state'] = 'normal'
                winsound.Beep(5000, 1000)
            elif counter2 in rangelist :
                display = str(int(counter1)) + ":" + "0" + str(int(counter2))
                label['text'] = display  
                label.after(1000, count)
                counter -= 1
            else:
                display = str(int(counter1)) + ":" + str(int(counter2))
                label['text'] = display  
                label.after(1000, count)
                counter -= 1
        
    count()


# start function of the stopwatch
def Start(label):
    global running
    running = True
    counter_label(label)
    start['state'] = 'disabled'
    stop['state'] = 'normal'
    reset['state'] = 'normal'


# Stop function of the stopwatch
def stop():
    global running
    start['state'] = 'normal'
    stop['state'] = 'disabled'
    Reset['state'] = 'normal'
    running = False


# Reset function of the stopwatch
def reset(label):
    global counter
    counter = 180

    # If reset is pressed after pressing stop.
    if running == False:
        Reset['state'] = 'disabled'
        label['text'] = '3:00'

    # If reset is pressed while the stopwatch is running.
    else:
        label['text'] = 'Starting...'


# Fixing the window size.

start = Button(window, text='Start',
               width=15, command=lambda: Start(label))
stop = Button(window, text='Stop',
              width=15, state='disabled', command=stop)
Reset = Button(window, text='Reset time',
               width=15, state='disabled', command=lambda: reset(label))
#start.pack()
#stop.pack()
#Reset.pack()

#Scoring part of display
green_score = 0
red_score = 0

def green_score_up():
    global green_score
    green_score += 1
    display = str(green_score)
    green_score_label['text'] = display

def green_score_down():
    global green_score
    if green_score < 1:
        pass
    else:
        green_score -= 1
        display = str(green_score)
        green_score_label['text'] = display

green_score_up_button = Button(window, text='˄', width=15,command=green_score_up)
green_score_down_button = Button(window, text='˅', width=15, command=green_score_down)
green_score_label = Label(window, text= str(green_score))


def red_score_up():
    global red_score
    red_score += 1
    display = str(red_score)
    red_score_label['text'] = display

def red_score_down():
    global red_score
    if red_score < 1:
        pass
    else:
        red_score -= 1
        display = str(red_score)
        red_score_label['text'] = display
def score_reset():
    global red_score
    global green_score
    red_score = green_score = 0
    display = str(red_score)
    red_score_label['text'] = display
    display1 = str(green_score)
    green_score_label['text'] = display1


red_score_up_button = Button(window, text='˄', width=15,command=red_score_up)
red_score_down_button = Button(window, text='˅', width=15, command=red_score_down)
red_score_label = Label(window, text= str(green_score))
score_reset_button = Button(window, text='Reset score', width=15, command=score_reset)

green_score_up_button.pack(side=LEFT)
red_score_up_button.pack(side=RIGHT)
green_score_label.pack(side=LEFT)
red_score_label.pack(side=RIGHT)
green_score_down_button.pack(side=LEFT)
red_score_down_button.pack(side=RIGHT)
start.pack()
stop.pack()
Reset.pack()
score_reset_button.pack()

window.mainloop()


