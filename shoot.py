#FINAL PROJECT / TOMATO TRUMP/STARMER

from graphics import Canvas
import random 
import time
    
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
BULLSEYE_SIZE = 20
SHOT_SIZE = 5
CENTRE_SCORE = 5
MIDDLE_SCORE = 3
OUTER_SCORE = 1
TIME_LIMIT = 60
TARGETS_START_MOVE = 5
INITIAL_SPEED = 5
MAX_SPEED = 25
SPEED_UP = 0.5

def main():
    # initialize variables
    # TO ADD - Choice of Trump or Starmer
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    outer_circle, middle_circle, bullseye, trump = create_target(canvas)
    game_time = TIME_LIMIT * 10
    score = 0
    targets_hit = 0
    x_speed = INITIAL_SPEED
    y_speed = INITIAL_SPEED
    time_text = canvas.create_text(5, 5, text='')
    score_text = canvas.create_text(CANVAS_WIDTH - 100, 5, text='Score: ' + str(score) + ' points')
 
    # Game loop while less than time limit x 10
    while game_time >= 0:
        # restart variables - might add missed score
        shot = 0
        result = 0
        add_score_text = 0
        
        # animate trump and targets
        if targets_hit >= TARGETS_START_MOVE:
            x_speed, y_speed = animate_target(canvas, outer_circle, middle_circle, bullseye, trump, x_speed, y_speed)
        
        # Get last player click
        click = canvas.get_last_click()
        
        # If player clicked, shoot
        if click:
            shot, result = shoot(click, canvas, outer_circle, middle_circle, bullseye, trump)
            
            # If player hit a target, add score and update score text
            if result > 0:
                score += result
                canvas.change_text(score_text, 'Score: ' + str(score) + ' points')
                add_score_text = canvas.create_text(CANVAS_WIDTH - 65, 20, text='+' + str(result), color='red')
                
                # If targets are moving, update targets animation
                if targets_hit >= TARGETS_START_MOVE:
                    x_speed = update_speed(x_speed)
                    y_speed = update_speed(y_speed)
                targets_hit += 1
        
        # End game loop once hit and wait 10th second
        time.sleep(0.1)
        
        # update countdown
        canvas.change_text(time_text, 'Time remaining: ' + str(game_time / 10) + ' seconds')
        game_time -= 1
        
        # delete temporary objects and create new target if target was shot
        if shot:
            canvas.delete(shot)
            if result > 0:
                delete_target(canvas, outer_circle, middle_circle, bullseye,trump)
                outer_circle, middle_circle, bullseye, trump= create_target(canvas)
                canvas.delete(add_score_text)
          
    # Game over shows the final points (add time if we change to 10 losses)     
    canvas.clear()
    canvas.create_text(CANVAS_WIDTH / 2 - 170, CANVAS_HEIGHT / 2 - 20, text='Game Over!\n Score: ' + str(score) + ' points', font_size=25)
                
# Creates a target in a random position, returns the three parts of the target hidden behind trump. Shoot in between eyes
def create_target(canvas):
    target_x = random.randint(0, CANVAS_WIDTH - BULLSEYE_SIZE * 5)
    target_y = random.randint(15, CANVAS_HEIGHT - BULLSEYE_SIZE * 5)
    outer_circle = canvas.create_oval(target_x, target_y, target_x + BULLSEYE_SIZE * 5, target_y + BULLSEYE_SIZE * 5, "white")
    middle_circle = canvas.create_oval(target_x + BULLSEYE_SIZE, target_y + BULLSEYE_SIZE, target_x + BULLSEYE_SIZE * 4, target_y + BULLSEYE_SIZE * 4, "white")
    bullseye = canvas.create_oval(target_x + BULLSEYE_SIZE * 2, target_y + BULLSEYE_SIZE * 2, target_x + BULLSEYE_SIZE * 3, target_y + BULLSEYE_SIZE * 3, "white")
    trump = canvas.create_image(target_x, target_y,"trump1s.gif")
    return outer_circle, middle_circle, bullseye, trump
    
# shoot in the defined position of the canvas when its moving faster
def shoot(click, canvas, outer_circle, middle_circle, bullseye,trump):
    result = 0
    shot = canvas.create_image(click[0] - SHOT_SIZE * 3, click[1] - SHOT_SIZE * 3,"tomato.gif")
    #shot = canvas.create_oval(click[0] - SHOT_SIZE / 2, click[1] - SHOT_SIZE / 2, click[0] + SHOT_SIZE / 2, click[1] + SHOT_SIZE / 2)
    overlapping_objects = canvas.find_overlapping(click[0], click[1], click[0], click[1])
    if bullseye in overlapping_objects:
        result = CENTRE_SCORE
    elif middle_circle in overlapping_objects:
        result = MIDDLE_SCORE
    elif outer_circle in overlapping_objects:
        result = OUTER_SCORE
    elif trump in overlapping_objects:
        result = OUTER_SCORE
    return shot, result
    
# Animate the target bouncing off the wallsss
def animate_target(canvas, outer_circle, middle_circle, bullseye, trump, x_speed, y_speed):
    target_x = canvas.get_left_x(outer_circle)
    target_y = canvas.get_top_y(outer_circle)
    if (target_x <= 0) or (target_x + BULLSEYE_SIZE * 5 >= CANVAS_WIDTH):
        x_speed = -x_speed
    if (target_y <= 15) or (target_y + BULLSEYE_SIZE * 5 >= CANVAS_HEIGHT):
        y_speed = -y_speed
    target_x += x_speed
    target_y += y_speed
    canvas.moveto(outer_circle, target_x, target_y)
    canvas.moveto(middle_circle, target_x + BULLSEYE_SIZE, target_y + BULLSEYE_SIZE)
    canvas.moveto(bullseye, target_x + BULLSEYE_SIZE * 2, target_y + BULLSEYE_SIZE * 2)
    canvas.moveto(trump, target_x, target_y)
    return x_speed, y_speed
    
# speed up if not max, and randomly set new direction
def update_speed(speed):
    speed = abs(speed)
    if (speed < MAX_SPEED):
        speed = speed + SPEED_UP
    speed = speed * random.choice([-1, 1])
    return speed
 
# delete the target from the canvas
def delete_target(canvas, outer_circle, middle_circle, bullseye, trump):
    canvas.delete(outer_circle)
    canvas.delete(middle_circle)
    canvas.delete(bullseye)
    canvas.delete(trump)

if __name__ == '__main__':
    main()
