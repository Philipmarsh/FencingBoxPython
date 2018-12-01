import winsound
from tkinter import *
import threading
import time



window = Tk()
window.title("Fencing Box")
label = Label(window, text="3:00")
label.pack()
canvas = Canvas(window, width=1520, height=500, background='white')
line1 = canvas.create_line(760, 0, 760, 500)
txt = canvas.create_text(330, 330, text="Green", font="Arial 16", fill="green")
txt1 = canvas.create_text(1190, 330, text="Red", font="Arial 16", fill="red")
canvas.pack()


#This section defines the menu bar
menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Epee")
menu1.add_separator()
menu1.add_command(label="Quit")
menubar.add_cascade(label="File", menu=menu1)
window.config(menu=menubar)

#This section describes how the box actually works
#This needs to be fixed to allow the box to reinitialize each colour after a hit has been scored
def set_g():
    canvas.bind('<g>', green)
def double_search_red():

   timer1 = time.time()
   def greenhit(r):
       nonlocal timer1
       timer2 = time.time()
       time_elapsed = timer2 - timer1
       
       if time_elapsed <= 0.125:
           print(time_elapsed)
           window.greenbox = canvas.create_rectangle(0, 0, 760, 500, fill="green")
           window.update_idletasks()
           canvas.after(1000, canvas.delete(window.greenbox))
           canvas.bind('<g>', green)
       
   canvas.after(1000, set_g) 
   canvas.bind('<g>', greenhit)
def set_r():
    canvas.bind('<r>', red)
def double_search_green():
   #i = 0
   timer1 = time.time()

   #def counter():
   #   def num():
   #        nonlocal i
   #        i +=1

   #    nonlocal i
   #    while i <126:
   #        canvas.after(1, num)
   #        print(i)

   def redhit(r):
       nonlocal timer1
       timer2 = time.time()
       time_elapsed = timer2 - timer1
       
       
       if time_elapsed <= 0.125:
           print(time_elapsed)
           window.redbox = canvas.create_rectangle(760, 0, 1520, 500, fill="red")
           window.update_idletasks()
           canvas.after(1000, canvas.delete(window.redbox))
           canvas.bind('<r>', red)
       
   canvas.after(1000, set_r) 
   canvas.bind('<r>', redhit)




def red(event):
    def redlight():

        window.redbox = canvas.create_rectangle(760, 0, 1520, 500, fill="red")
        window.update_idletasks()
        touche = event.keysym
        print(touche)
        winsound.Beep(5000, 1000)
        canvas.after(500, canvas.delete(window.redbox))
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
def green(event):

    
    def greenlight():
        window.greenbox = canvas.create_rectangle(0, 0, 760, 500, fill="green")
        window.update_idletasks()
        touche = event.keysym
        print(touche)
        winsound.Beep(5000, 1000)
        canvas.after(1000, canvas.delete(window.greenbox))
    t2 = threading.Thread(target=double_search_green, name='thread1')
    t3 = threading.Thread(target=greenlight, name='thread2')
    t2.start()
    t3.start()
    window.update_idletasks()

    #canvas.greenbox = canvas.create_rectangle(0, 0, 760, 500, fill="green")
    global running
    if running:
        running = False
        start['state'] = 'normal'
        stop['state'] = 'disabled'
        Reset['state'] = 'normal'
    else:
        print("The timer was not running")


canvas.focus_set()
canvas.bind("<r>", red)
canvas.bind("<g>", green)

canvas.pack()



counter = 180

running = False


def counter_label(label):
    def count():

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
            elif counter2 == 0 or counter2 == 1 or counter2 ==2 or counter2 == 3 or counter2 ==4 or counter2== 5 or counter2==6 or counter2==7 or counter2==8 or counter2==9:
                display = str(int(counter1)) + ":" + "0" + str(int(counter2))
                label['text'] = display  # Or label.config(text=display)
                label.after(1000, count)
                counter -= 1
            else:
                display = str(int(counter1)) + ":" + str(int(counter2))
                label['text'] = display  # Or label.config(text=display)
                label.after(1000, count)
                counter -= 1
        # label.after(arg1, arg2) delays by

    # first argument given in milliseconds
    # and then calls the function given as second argument.
    # Generally like here we need to call the
    # function in which it is present repeatedly.
    # Delays by 1000ms=1 seconds and call count again.

    # Triggering the start of the counter.
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

    # If rest is pressed after pressing stop.
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
#green_score_up_button.pack(side=LEFT)
#green_score_label.pack(side=LEFT)
#green_score_down_button.pack(side=LEFT)

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


