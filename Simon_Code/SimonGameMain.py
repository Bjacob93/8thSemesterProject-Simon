from gpiozero import LED, Button
from random import randint
from time import sleep
import time
import datetime
import pygame
from neopixel import *
import argparse
import serial

# Connect to an open serial port in the arduione (actual port changes sporadically, hence the double try
serial
try:
	serial = serial.Serial('/dev/ttyACM1', 9600)
except Exception as e:
	try:
		serial = serial.Serial('/dev/ttyACM0', 9600)
	except Exception as x:
		print(e)

# Wait for the arduino to reset, which is does on new serial connections.
sleep(5)

# Initiate the audio mixer
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.mixer.init()

# Function for initiating the Log file
def initiate_log():
	log = open('LogFile', 'a')
	log.write('Date' + '\t' + 'Time' + '\t' + 'Game Over Cause' + '\t' + 'Score' + '\t' + 'Continuation \n')
	log.flush()
	log.close()
	
# Function for writing to the log file
def write_to_log(game_over_cause, score):
	date_time = datetime.datetime.now()
	date = str(date_time.year) + '-' + str(date_time.month) + '-' + str(date_time.day)
	f = open('LogFile', 'a')
	continuation = 'N'
	if time_since_last_gameover < 30000:
		continuation = 'Y'
	f.write(date + '\t' + game_start_time + '\t' + str(game_over_cause) + '\t'+ str(score) + '\t'+ str(continuation) + '\n')
	f.flush()
	f.close()

# Get current time in millis
def millis():
	millis = int(round(time.time() * 1000))
	return millis

# Randomly generate the sequence for this run
def generate_sequence():	
	sequence = [randint(1, 4) for i in range(max_level)]
	global sequence

# Display the sequence to the players
def show_sequence():
	for i in range(current_level): # Turn on the correct led and play the audio
		if sequence[i] == 1:
			pygame.mixer.music.load(root_path + "Blue.mp3")
			pygame.mixer.music.set_volume(blue_audio_level)
			pygame.mixer.music.play()
			sleep(audio_sleep_time)
			led_blue.on()
			serial.write(b'4')
			
		elif sequence[i] == 2:
			pygame.mixer.music.load(root_path + "Red.mp3")
			pygame.mixer.music.set_volume(red_audio_level)
			pygame.mixer.music.play()
			sleep(audio_sleep_time)
			led_red.on()
			serial.write(b'1')
		
		elif sequence[i] == 3:
			pygame.mixer.music.load(root_path + "Yellow.mp3")
			pygame.mixer.music.set_volume(yellow_audio_level)
			pygame.mixer.music.play()
			sleep(audio_sleep_time)
			led_yellow.on()
			serial.write(b'2')
		
		elif sequence[i] == 4:
			pygame.mixer.music.load(root_path + "Green.mp3")
			pygame.mixer.music.set_volume(green_audio_level)
			pygame.mixer.music.play()
			sleep(audio_sleep_time)
			led_green.on()
			serial.write(b'3')
					
		sleep(difficulty)	# Wait, then turn off the led.
		
		led_blue.off()
		led_red.off()
		led_yellow.off()
		led_green.off()
		level_shown = True
		sleep(0.1)
		
		global level_shown

# Register the players' button presses	
def get_sequence():
	flag = 0 # Used for making sure you cannot press two buttons simultaneously
	
	a_button_is_pressed = False
	
	# Make the game more difficult at higher levels
	if current_level < 10 and not current_level == 1:
			time_limit = time_limit * time_limit_reduction_factor
			
	for i in range(current_level): # For each step of the sequence this level
		flag = 0
		
		# Keep track on the timer for the level
		level_time = 0
		start_time = millis()
		
		# Varialbles for the 'time-limit' ticking sound
		divisor = 1.2
		x = time_limit / divisor
		last_click = 0
		since_last_click = 0
		number_ticks = 0
		
		# Wait for a button press
		while flag == 0:
			
			since_last_click = millis() - last_click
			
			# Tick tock
			if level_time >= time_limit - x and since_last_click > 160:
				pygame.mixer.music.load(tick_path)
				pygame.mixer.music.set_volume(tick_audio_volume)
				pygame.mixer.music.play()
				print number_ticks, time_limit - x
				number_ticks = number_ticks + 1
				last_click = millis()
				x = x/divisor
			
			# Make sure no buttons are being held down
			if not button_blue.is_pressed and not button_red.is_pressed and not button_yellow.is_pressed and not button_green.is_pressed:
				a_button_is_pressed = False
			
			# Time limit
			level_time = millis() - start_time
			if level_time > time_limit and flag == 0:  # If above the threshold, lose the game and return
				write_to_log('Timeout', current_level)
				lose_game()
				return
							
			# Check if one of the buttons are pressed	
			if button_blue.is_pressed and flag == 0 and a_button_is_pressed == False:
				a_button_is_pressed = True
				flag = 1
				active_sequence[i] = 1
				pygame.mixer.music.load(root_path + "Blue.mp3")
				pygame.mixer.music.set_volume(blue_audio_level)
				pygame.mixer.music.play()
				sleep(audio_sleep_time)
				led_blue.on()
				serial.write(b'8')
			
			if button_red.is_pressed and flag == 0 and a_button_is_pressed == False:
				a_button_is_pressed = True
				flag = 1
				active_sequence[i] = 2
				pygame.mixer.music.load(root_path + "Red.mp3")
				pygame.mixer.music.set_volume(red_audio_level)
				pygame.mixer.music.play()
				sleep(audio_sleep_time)
				led_red.on()
				serial.write(b'5')
			
			if button_yellow.is_pressed and flag == 0 and a_button_is_pressed == False:
				a_button_is_pressed = True
				flag = 1
				active_sequence[i] = 3
				pygame.mixer.music.load(root_path + "Yellow.mp3")
				pygame.mixer.music.set_volume(yellow_audio_level)
				pygame.mixer.music.play()
				sleep(audio_sleep_time)
				led_yellow.on()
				serial.write(b'6')
				
			if button_green.is_pressed and flag == 0 and a_button_is_pressed == False:
				a_button_is_pressed = True
				flag = 1
				active_sequence[i] = 4
				pygame.mixer.music.load(root_path + "Green.mp3")
				pygame.mixer.music.set_volume(green_audio_level)
				pygame.mixer.music.play()
				sleep(audio_sleep_time)
				led_green.on()
				serial.write(b'7')				
	
		sleep(delay_for_sequence_correctness_check)	
		led_blue.off()
		led_red.off()
		led_yellow.off()
		led_green.off()

		# If the wrong button was pressed, lose the game
		if not active_sequence[i] == sequence[i]:
			write_to_log('Wrong Sequence', current_level)
			lose_game()
			return
			
	win_game() 	#Go on to next level
	level_shown = False
	global level_time, time_limit, level_shown
	
def lose_game():
	print 'You got to level:', current_level
	pygame.mixer.music.load(root_path + "Lose.mp3")		# Play the loss audio
	pygame.mixer.music.set_volume(victory_loss_audio_level)
	pygame.mixer.music.play()
	level_shown = False
	serial.write(b'0')

	# Blink LEDs
	for i in range(3):
		led_blue.on()
		led_red.on()
		led_yellow.on()
		led_green.on()
		sleep(0.5)
		
		led_blue.off()
		led_red.off()
		led_yellow.off()
		led_green.off()
		sleep(0.5)
	
	# Update highscore if it was beaten
	if all_time_high < current_level - 1:
		all_time_high = current_level - 1
	
	# Reset variables
	current_level = 1
	difficulty = 1.0
	time_limit = 8000.0
	high_score_set_this_game = False
	last_gameover_millis = millis()
	global current_level, difficulty, level_shown, time_limit, all_time_high, high_score_set_this_game, last_gameover_millis

def win_game():
	pygame.mixer.music.load(root_path + "Victory.mp3") # Play victory audio
	pygame.mixer.music.set_volume(victory_loss_audio_level)
	pygame.mixer.music.play()
	serial.write(b'9')
	
	# Blink LEDs
	for i in range(10):
		led_blue.on()
		led_red.on()
		led_yellow.on()
		led_green.on()
		sleep(0.1)
	
		led_blue.off()
		led_red.off()
		led_yellow.off()
		led_green.off()
		sleep(0.1)
	
	# Make the game more difficult
	if current_level < 11:
		difficulty = difficulty - 0.07
	elif current_level < 16:
		difficulty = difficulty - 0.04
	if difficulty < 0.10:
		difficulty = 0.10
	
	# If you beat the previous highscore, play audio
	if all_time_high < current_level and not high_score_set_this_game:
		pygame.mixer.music.load(high_score_audio_path)
		pygame.mixer.music.set_volume(high_score_audio_level)
		pygame.mixer.music.play()
		high_score_set_this_game = True
		sleep(3)
	
	current_level = current_level + 1
	sleep(1)
	global current_level, difficulty, high_score_set_this_game

# Red pins
led_red = LED(14)
button_red = Button(15)

# Yellow pins
led_yellow = LED(23)
button_yellow = Button(24)

# Green pins
led_green = LED(8)
button_green = Button(7)

# Blue pins
led_blue = LED(20)
button_blue = Button(21)

# Level and Sequence variables
current_level = 1
max_level = 100
sequence = [0 for i in range(max_level)]
active_sequence = [0 for i in range(max_level)]

# Timer variables
level_time = 0.0
time_limit = 8000.0
time_limit_reduction_factor = 0.88
difficulty = 1.0
delay_for_sequence_correctness_check = 0.3
audio_sleep_time = 0.0

button_is_pressed = False
level_shown = False

# Root path for audio files
root_path = "/home/pi/Desktop/Simon_Code/Audio/"
tick_path = root_path + "Tick_audio.mp3"

# Audio volume levels
victory_loss_audio_level = 0.5
red_audio_level = 1
blue_audio_level = 1
yellow_audio_level = 1
green_audio_level = 1
high_score_audio_level = 0.7
tick_audio_volume = 1

# High-score variables
all_time_high = 2
high_score_set_this_game = False
high_score_audio_path = "/home/pi/Desktop/Simon_Code/Audio/High_Score.mp3"

# Tutorial Variables
last_gameover_millis = 0
time_since_last_gameover = 0
last_lure_millis = 0
time_since_last_lure = 0
first_time_game_starts = True
lure_sound_path = "/home/pi/Desktop/Simon_Code/Audio/Lure_lyd.mp3"
tutorial_sound_path = "/home/pi/Desktop/Simon_Code/Audio/Tutorial.mp3"
start_simon_sound_path = "/home/pi/Desktop/Simon_Code/Audio/Ready_audio.mp3"
lure_audio_volume = 1
tutorial_audio_volume = 1
tutorial_and_lure_timer = 30000
start_simon_audio_volume = 1

game_start_time = ""
initiate_log()
print 'Ready'

high_score_reset_timer_start = millis()
high_score_reset_timer = 0
high_score_reset_threshold = 2700000 # reset high-score every 45 minutes

# Set these to true or false to enable or disable lure and tutorial.
lure_is_enabled = True
tutorial_is_enabled = True

while True:
	
	high_score_reset_timer = millis() - high_score_reset_timer_start
	
	# Reseting the high-score
	if time_since_last_gameover > tutorial_and_lure_timer and high_score_reset_timer > high_score_reset_threshold:
		high_score_reset_timer = 0
		high_score_reset_timer_start = millis()
		all_time_high = 2
	
	if current_level == 1:	# Starting a new game
		last_lure_millis = millis()
		time_since_last_gameover = 0
		
		while True: 
			if button_blue.is_pressed: break
			if button_red.is_pressed: break
			if button_yellow.is_pressed: break
			if button_green.is_pressed: break
			
			time_since_last_lure = millis() - last_lure_millis
			time_since_last_gameover = millis() - last_gameover_millis
			if time_since_last_lure > tutorial_and_lure_timer and lure_is_enabled:
				pygame.mixer.music.load(lure_sound_path)
				pygame.mixer.music.set_volume(lure_audio_volume)
				pygame.mixer.music.play()
				time_since_last_lure = 0
				last_lure_millis = millis()

		# If enough time has passed since the game was lost, assume the players need a small tutorial, and play it.
		if (time_since_last_gameover > tutorial_and_lure_timer or first_time_game_starts) and tutorial_is_enabled:
			pygame.mixer.music.load(tutorial_sound_path)
			pygame.mixer.music.set_volume(tutorial_audio_volume)
			pygame.mixer.music.play()
			if first_time_game_starts:
				first_time_game_starts = False

			tutorial_wait_timer_start = millis()
			tutorial_wait_timer_run = 0
		
			sleep(1) # Tutorial cannot be skipped for the first second (damn fiddlyness)
		
			# Skip the rest of the tutorial on button press
			while tutorial_wait_timer_run < 5000:
				if button_blue.is_pressed: break
				if button_red.is_pressed: break
				if button_yellow.is_pressed: break
				if button_green.is_pressed: break
				tutorial_wait_timer_run = millis() - tutorial_wait_timer_start
		
		# Save the datetime for when the game started - used in logging
		date_time = datetime.datetime.now()
		game_start_time = str(date_time.hour) + ':' + str(date_time.minute) + ':' + str(date_time.second)
		generate_sequence()	# Generate a new puxxle sequence for the game.
	
	# If the sequence for the current level has not been shown
	if not level_shown:
		if current_level == 1:	# Reset time limit
			sleep(0.5)
			timer_limit = 8.0
		
		show_sequence()			# Show the current sequence
		get_sequence()			# Wait for user input
