# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
PAD_VEL = 8
LEFT = False
RIGHT = True

paddle1_pos = paddle2_pos = HEIGHT/2
paddle1_vel = paddle2_vel = 0
score1 = score2 = 0

ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [0, 0]

# re-calculate paddle vertical position in case it go out of the table
def fix_paddle_pos(paddle_pos):
    # paddle_pos is the vertical center of a paddle
    if paddle_pos < HALF_PAD_HEIGHT:
        paddle_pos = HALF_PAD_HEIGHT
        
    if paddle_pos > HEIGHT - HALF_PAD_HEIGHT:
        paddle_pos = HEIGHT - HALF_PAD_HEIGHT
        
    return paddle_pos
# tests whether the ball touches with the left and right gutters
def check_gutter():
    global score1, score2
    # touches left gutter
    if ball_pos[0] - BALL_RADIUS < PAD_WIDTH:
        if paddle1_pos-HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos+HALF_PAD_HEIGHT:
            ball_vel[0] = ball_vel[0] * -1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            score2 = score2 + 1
            spawn_ball(RIGHT)
    # right gutter touched
    if ball_pos[0] + BALL_RADIUS > WIDTH - PAD_WIDTH:
        if paddle2_pos-HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos+HALF_PAD_HEIGHT:
            ball_vel[0] = ball_vel[0] * -1.1
            ball_vel[1] = ball_vel[1] * 1.1
        else:
            score1 = score1 + 1
            spawn_ball(LEFT)
        

# draw paddle based on its postion
def draw_paddle(canvas, center):
    upper_left = [center[0]-HALF_PAD_WIDTH, center[1]-HALF_PAD_HEIGHT]
    lower_left = [center[0]-HALF_PAD_WIDTH, center[1]+HALF_PAD_HEIGHT]
    lower_right = [center[0]+HALF_PAD_WIDTH, center[1]+HALF_PAD_HEIGHT]
    upper_right = [center[0]+HALF_PAD_WIDTH, center[1]-HALF_PAD_HEIGHT]

    canvas.draw_polygon([upper_left, lower_left, lower_right, upper_right], 1, 'White', 'White')
    
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    # spawn ball upwards and towards to "LEFT" by default
    ball_vel[0] = random.randrange(120, 240) / -60.0 
    ball_vel[1] = random.randrange(60, 180) / -60.0
    if direction:
        ball_vel[0] = ball_vel[0] * -1

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = paddle2_pos = HEIGHT/2
    paddle1_vel = paddle2_vel = 0
    score1 = score2 = 0
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] = ball_pos[0] + ball_vel[0]
    ball_pos[1] = ball_pos[1] + ball_vel[1]
    
    # bounces off of the top and bottom walls
    if ball_pos[1]<=BALL_RADIUS or ball_pos[1]>=HEIGHT-BALL_RADIUS:
        ball_vel[1] = ball_vel[1] * -1
        
    # check if gutter touched/collided
    check_gutter()

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = fix_paddle_pos(paddle1_pos + paddle1_vel)
    paddle2_pos = fix_paddle_pos(paddle2_pos + paddle2_vel)
    
    # draw paddles
    draw_paddle(canvas, [HALF_PAD_WIDTH, paddle1_pos])
    draw_paddle(canvas, [WIDTH-HALF_PAD_WIDTH, paddle2_pos])

    # draw scores
    canvas.draw_text(str(score1), [WIDTH/4, HEIGHT/8], 40, "White")
    canvas.draw_text(str(score2), [WIDTH/4 * 3, HEIGHT/8], 40, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -1 * PAD_VEL
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = PAD_VEL
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -1 * PAD_VEL
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = PAD_VEL
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", new_game)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
