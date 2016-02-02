# Stopwatch: The Game

# imports
import simplegui

# global variables
ticks = 0
stops = 0
hits = 0

# helper functions
def format_ticks(n):
    tenthsOfSecond = n % 10
    seconds = n / 10 % 60
    minutes = n / 600
    op = "%d:%d%d.%d" % (minutes, seconds/10, seconds%10, tenthsOfSecond)
    return op

def format_hits():
    return "%d/%d" % (hits, stops)

# event handlers
def tick():
    global ticks
    ticks += 1
    
def draw(canvas):
    canvas.draw_text(format_ticks(ticks), [110,100], 24, "White")
    canvas.draw_text(format_hits(), [230,20], 24, "Green")
    
def start_timer():
    if not timer.is_running():
        timer.start()
    
def stop_timer():
    global stops, hits
    if timer.is_running():
        timer.stop()
        stops += 1
        if ticks % 10 == 0:
            hits += 1
        
def reset_timer():
    global ticks, stops, hits
    timer.stop()
    ticks, stops, hits = 0, 0 ,0

# create frame and register event handlers
frame = simplegui.create_frame("Stop Watch Game", 280, 200)
frame.set_draw_handler(draw)
frame.add_button("Start", start_timer, 100)
frame.add_button("Stop", stop_timer, 100)
frame.add_button("Reset", reset_timer, 100)

# create timer
timer = simplegui.create_timer(100, tick)

# start frame and timer
frame.start()
