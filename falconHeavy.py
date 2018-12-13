#!/usr/bin/python
#coding: utf8
#Authors: Alex Viñas, Aaron Jimenez, Jaume Pladevall, Pol Casasayas


"""
Imports
"""
import time

import serial

import math

"""
Imports de Teclado
"""
import os
import sys, tty, termios
from select import select
# To import the function "envia" from the file "test_NeatoCommands.py"
from test_NeatoCommands import envia
from falconHeavyLaser import enable_laser
from falconHeavyLaser import get_laser
from corners import *


'''def gotoPoint(goto_x, goto_y):
	L_act, R_act = get_motors()
	odometry(L_act, R_act)
	distance = math.sqrt(math.pow(goto_x - x_word, 2) + math.pow(goto_y - y_word, 2))
	while distance > 120:
		L_act, R_act = get_motors()
		odometry(L_act, R_act)

		diff = math.atan2(goto_x - x_word, goto_y - y_word) - theta_word
		direc = ((diff + math.pi) % (2*math.pi)) - math.pi
		distance = math.sqrt(math.pow(goto_x - x_word, 2) + math.pow(goto_y - y_word,2))

		velocity = 100

		dist_R = (velocity + (S*0.6*direc))
		dist_L = (velocity + (-S*0.6*direc))

		print(distance, x_word, y_word)
		set_motors(dist_L, dist_R, velocity)

	print("Arrived at the destination")
'''

def stop_motors():
	direccion = 0
	speed = 0
	tita_dot = 0
	distancia_L = 0
	distancia_R = 0
	envia(ser, 'SetMotor LWheelDisable RWheelDisable', 0.2)
	envia(ser, 'SetMotor RWheelEnable LWheelEnable', 0.2)


def gotoPoint(goto_x, goto_y):
	# velocity = how_far * 0.5
	velocity = 150  # en mm/s
	tita_dot = 0
	tiempo = 20
	direccion = 0

	L_act, R_act = get_motors()
	odometry(L_act, R_act)

	# robot orientation
	distance = math.sqrt(math.pow(goto_x - x_word, 2) + math.pow(goto_y - y_word, 2))
	targetAngle = math.atan2(goto_x - x_word, goto_y - y_word) - theta_word

	distancia_R = (((velocity * pow(-1, direccion)) + (S * targetAngle)) * tiempo)
	distancia_L = (((velocity * pow(-1, direccion)) + (-S * targetAngle)) * tiempo)

	print(distance, x_word, y_word)
	print(targetAngle)
	set_motors(distancia_L, distancia_R, velocity)

	# go up

	while abs(distance) > 120:
		L_act, R_act = get_motors()
		odometry(L_act, R_act)

		diff = math.atan2(goto_x - x_word, goto_y - y_word) - theta_word
		direc = ((diff + math.pi) % (2 * math.pi)) - math.pi
		distance = math.sqrt(math.pow(goto_x - x_word, 2) + math.pow(goto_y - y_word, 2))

		velocity = 100

		dist_R = (velocity + (S * 0.6 * direc))
		dist_L = (velocity + (-S * 0.6 * direc))

		print(distance, x_word, y_word)
		set_motors(dist_L, dist_R, velocity)

		L_act, R_act = get_motors()
		odometry(L_act, R_act)

		distance = math.sqrt(math.pow(goto_x - x_word, 2) + math.pow(goto_y - y_word, 2))

		distancia_R = (((velocity * pow(-1, direccion)) + (S * tita_dot)) * tiempo) * pow(-1, 0)
		distancia_L = (((velocity * pow(-1, direccion)) + (-S * tita_dot)) * tiempo) * pow(-1, 0)

		print(targetAngle)
		print(distance, x_word, y_word)
		set_motors(distancia_L, distancia_R, velocity)
	# stop_motors()
	print  ("\n FINISH")


def polars_escalars(punts):  # Passa de coord. polars a coord. escalars
	llista = []
	for l in punts:
		angle = float(l[0])*math.pi/180
		r = float(l[1])
		#if r != 0:
		#	print(r)
		x = math.cos(angle)*r
		y = math.sin(angle)*r
		llista.append([x, y])
	return llista


def trans_l_to_w(punts):  # Transforma de coord. del Làser a coord. del World
	llista = []
	for l in punts:
		x_est = math.cos(theta_word)*l[0] - math.sin(theta_word)*l[1] + x_word
		y_est = math.sin(theta_word)*l[0] + math.cos(theta_word)*l[1] + y_word
		# Afegit per comprobar que no generi punts (0, 0)
		print("x: " + str(x_est) + " y: " + str(y_est))
		llista.append([x_est, y_est])
	return llista


def guardar_punts(punts):  # Guarda els punts el fitxer vista_robot.txt
	for xy in punts:
		f.write(str(xy[0])+","+str(xy[1])+";\n")


def get_motors():
	""" Ask to the robot for the current state of the motors. """
	msg = envia(ser, 'GetMotors LeftWheel RightWheel').split('\n')
	# For better understanding see the neato commands PDF.
	l = int(msg[4].split(',')[1])
	r = int(msg[8].split(',')[1])
	return l, r


def set_motors(L, R, velocity):
	order = 'SetMotor LWheelDist ' + str(L) + ' RWheelDist ' + str(R) + ' Speed ' + str(velocity)
	msg = envia(ser, order)


def odometry(L_act, R_act):
	# Implement the pos integration. Assume initial conditions [0,0,0].
	# Use global variables, discoment this line
	global x_word, y_word, theta_word, dist
	new_L, new_R = L_act - L_ini, R_act - R_ini

	delta_th = (new_R-new_L)/0.52
	delta_d = (new_R+new_L)/2

	x_word = x_word + delta_d*math.cos(theta_word)
	y_word = y_word + delta_d*math.sin(theta_word)
	theta_word = (theta_word+delta_th) % 2*math.pi

	dist = dist + delta_d


def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	print(ch)
	return ch


# Crida a la funcio main
if __name__ == '__main__':
	global ser, f
	global x_word, y_word, dist, theta_word
	L_ini = R_ini = suma_theta = 0
	x_word = y_word = theta_word = dist = 0.0
	L, R = 0, 0
	# Open the Serial Port.
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
	# ser = serial.Serial(port='/dev/ttyAMA0', baudrate=115200, timeout=1)
	punts = []
	
	fitxer = "vista_robot.txt"
	if os.path.exists(fitxer):	
		os.remove(fitxer)	
	f = open(fitxer, "a+")
	
	L_ini, R_ini = get_motors()
	L_ant, R_ant = L_ini, R_ini

	envia(ser, 'TestMode On', 0.2)

	envia(ser, 'PlaySound 1', 0.3)

	envia(ser, 'SetMotor RWheelEnable LWheelEnable', 0.2)

	# Parametros Robot.
	S = 121.5		# en mm
	distancia_L = 0		# en mm
	distancia_R = 0		# en mm
	speed = 0 		# en mm/s
	tita_dot = 0
	tiempo = 20
	direccion = 0
	b = False

	print("########################")
	print('Speed = ' + str(speed))
	print("Tita_dot = " + str(tita_dot))

	if direccion == 0:
		print("Direction: fordward.")
	else:
		print("Direction: backward.")

	print("q to exit.")
	print("########################")

	# Tecla a leer.
	tecla = ''
	comando = ''
	#
	while tecla != "q":

		# Leemos la tecla.
		print("Write command: ")
		tecla = getch()

		if tecla == 'w' or tecla == 's':

			if tecla == 'w':
				speed = speed + 50
			else:
				speed = speed - 50

			if speed >= 0:
				direccion = 0
			else:
				direccion = 1

			if speed == 0:

				envia(ser, 'SetMotor LWheelDisable RWheelDisable', 0.2)
				envia(ser, 'SetMotor RWheelEnable LWheelEnable', 0.2)

			else:
				distancia_R = (((speed * pow(-1, direccion) ) + (S * tita_dot)) * tiempo) * pow(-1, direccion)
				distancia_L = (((speed * pow(-1, direccion) ) + (-S * tita_dot)) * tiempo) * pow(-1, direccion)

				comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(speed * pow(-1, direccion))
				envia(ser, comando, 0.2)

		elif tecla == 'd' or tecla == 'a':

			if tecla == 'd':
				tita_dot = tita_dot + (3.1415/10)
			else:
				tita_dot = tita_dot - (3.1415/10)

			distancia_R = (((speed * pow(-1, direccion) ) + (S * tita_dot)) * tiempo) * pow(-1, direccion)
			distancia_L = (((speed * pow(-1, direccion) ) + (-S * tita_dot)) * tiempo) * pow(-1, direccion)

			comando = 'SetMotor LWheelDist ' + str(distancia_L) + ' RWheelDist ' + str(distancia_R) + ' Speed ' + str(speed * pow(-1, direccion))
			envia(ser, comando, 0.2)

		elif tecla == 'p':  # Parada de motors

			direccion = 0
			speed = 0
			tita_dot = 0
			distancia_L = 0
			distancia_R = 0
			envia(ser, 'SetMotor LWheelDisable RWheelDisable', 0.2)
			envia(ser, 'SetMotor RWheelEnable LWheelEnable', 0.2)

		elif tecla == 'l':  # Activar el laser

			if b:
				b = False
			else:
				b = True
			enable_laser(ser, b)

		elif tecla == 'g':  # Anar al punt mig entre dues cantonades

			punts = clean(punts)
			punts = corners(punts)
			punts = cluster(punts)

			print("Cantonades: ")
			print(str(punts))

			distEntrePunts = 500  # 800
			b = False
			for i in punts:
				for j in punts:
					dist = math.sqrt(math.pow(i[0] - j[0], 2) + math.pow(i[1] - j[1], 2))
					if dist > distEntrePunts:
						print("Triats: " + str(i) + " " + str(j))
						print("Desti: " + str((i[0]+j[0])/2) + " " + str((i[1]+j[1])/2))
						gotoPoint(1000, 1000)
						b = True
						break
				if b:
					break

		if tecla == 'w' or tecla == 'a' or tecla == 's' or tecla == 'd' or tecla == 'p':

			L_act, R_act = get_motors()
			odometry(L_act, R_act)

			print("########################")
			print("########################")
			print("Speed = " + str(speed))
			print("Tita_dot = " + str(tita_dot))
			print("Posicio : " + str(x_word) + str(y_word))
			print("Distancia : " + str(dist))

			if direccion == 0:
				print("Direction: fordward.")
			else:
				print("Direction: backward.")
			print("########################")

		if b and tecla == 'm':  # Si el laser esta activat, guardar punts detectats pel laser

			L_act, R_act = get_motors()
			odometry(L_act, R_act)
			punts = trans_l_to_w(polars_escalars(get_laser(ser)))
			print("laser scan finished")
			guardar_punts(punts)

	f.close()


