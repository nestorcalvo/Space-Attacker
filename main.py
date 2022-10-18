"""
Por Ing. Nestor Calvo Ariza  nestor.calvo@udea.edu.co    CC 1118871837
"""

"""
1. Importamos las librerias necesarias
"""
import pygame # Libreria para crear juegos en Python
import cv2 # Libreria para operar la camara y la deteccion de la mano
import os # Libreria para operar con archivos de sistema
import random # Libreria para generar numeros aleatoreos
import mediapipe as mp # Libreria para obtener landmarks de la mano
import math # Libreria para realizar opreaciones matematicas

from pygame.locals import ( # Libreria para obtener y manejar teclas
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
"""
2. Definicion de variables importantes
"""
pygame.init()       # Inicializamos nuestro constructor de pygame
pygame.display.set_caption("Space Attacker") # Titulo del juego
clock = pygame.time.Clock()     # Tiempo de nuestro juego para limitar en fps

WINDOWWIDTH = 620       # Se define el ancho de la pantalla
WINDOWHEIGHT = 620          # Se define el alto de la pantalla
shipX_new = int(WINDOWWIDTH/2) # Posicion inicial de la nave en X
shipY_new = 550 # Posicion inicial de la nave en Y

FPS = 60    # Se fijan los valores de los frames por segundo
ship = pygame.image.load("./sprites/MainShipBaseFullhealth.png") # Se carga la imagen de la nave
ship = pygame.transform.scale(ship,(int(WINDOWWIDTH/6),int(WINDOWWIDTH/6))) # Se realiza un re escalado 
enemy = pygame.image.load("./sprites/Ship1.png") # Se carga la imagen de la nave enemiga
path_background = "./sprites/background" # Se inicializa el path donde se encuentra la sequencia para el fondo 

background =  [pygame.image.load(os.path.join(dirpath,f)) for (dirpath, dirnames, filenames) in os.walk(path_background) for f in filenames] # Cargar todos los fondos de pantallas
background = [pygame.transform.scale(i,(WINDOWWIDTH,WINDOWHEIGHT)) for i in background] # Se realiza un escalado para que ocupen toda la pantalla

cap = cv2.VideoCapture(0) # Activar la camara
hands = mp.solutions.hands.Hands() # Llamar al paquete para la captura de las manos

pantalla = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])  # Creamos una pantalla de 960x620
running = True # Variable para manejar estado del juego 
"""
3. Definicion de datos basicos del laser
"""
laser_img = pygame.image.load("./sprites/charged2.png") # Se carga la imagen del disparo
laser_img = pygame.transform.rotate(laser_img, 90) # Esta imagen es horizontal por ende se rota para que sea vertical
laser_X = shipX_new + 30 # Se inicia su posicion en X
laser_Y = shipY_new # Se inicia su posicion en Y
laserX_speed = 0 # La velocidad que tendrá en X siempre es 0 porque ella no se mueve en X
laserY_speed = 30 # Se define una velocidad en Y

"""
4. Definicion de datos basicos del enemigo
"""
enemyImg = [] # Lista para almacenar todas las imagenes de la nave enemiga 
enemyX = [] # Lista para almacenar todas las posiciones en X
enemyY = [] # Lista para almacenar todas las posiciones en Y
enemyX_change = [] # Lista para almacenar todas las velocidades en X
enemyY_change = [] # Lista para almacenar todas las velocidades en Y
num_of_enemies = 6 # Numero de enemigos en pantalla


for i in range(num_of_enemies): # Para cada enemigo
    enemyImg.append(enemy) # Se agrega su imagen
    enemyX.append(random.randint(40, WINDOWHEIGHT-40)) # Se escogue una posicion aleatorea en X
    enemyY.append(random.randint(40, 80)) # Se escogue una posicion aleatorea en Y
    enemyX_change.append(4) # Se establecen las velocidades en X
    enemyY_change.append(40) # Se establecen las velocidades en Y

"""
5. Funcion para extraer dedo indice
"""
def extract_index_finger():
    
    while 1: # Ejecutar un buqle infinto
        _, frame = cap.read() # Capturar un frame
        frame = cv2.flip(frame,1)
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convertirlo a RGB (opencv por defecto trabaja en BGR)
        
        hand_check = hands.process(image) # Solicitar al paquete que busque las manos en el frame
        if hand_check.multi_hand_landmarks: # Revisar multiples manos simultaneas
            for i in hand_check.multi_hand_landmarks: # Para cada mano realizamos el calculo de los landmakrs
                
                for index, pos in enumerate(i.landmark): # Para cada landmark de la mano calculamos lo siguiente
                    
                    h, w, c = image.shape # Se toma informacion de la imagen para poder graficar el punto donde se encuentran los landmarks
                    pos_x, pos_y = int(pos.x * w), int(pos.y * h) # posicion en x y y del landmark
                    
                    if index == 8: # Si encontramos el dedo indice (landmakr #8)
                        #cv2.circle(image, (pos_x, pos_y), 25, (255, 0, 255), cv2.FILLED) # Graficar el landmark del dedo indice
                        pos_x_final = int(pos.x * WINDOWWIDTH) # Se calculan las posicones en X de la nave dependiendo de la posicion del indice
                        pos_y_final = int(pos.y * WINDOWHEIGHT) # Se calculan las posicones en Y de la nave dependiendo de la posicion del indice
        else:
            pos_x_final = False # En caso de que no se detecte indice, no se modifica la posicion en X
            pos_y_final = False # En caso de que no se detecte indice, no se modifica la posicion en Y
        #cv2.imshow("Output", image) # Mostrar la imagen con las modificaciones
        k = cv2.waitKey(20)     # Esperamos 20 milisegundos para saber si la tecla ESC se presionó
        if k > 0:    #Si se presiona tecla
            break   # Se interrumpe el ciclo
        return pos_x_final, pos_y_final  # Se retorna la posicion de el indice
    cap.release()    # Se apaaga la camara
    cv2.destroyAllWindows()   #Se cierran las ventanas creadas

"""
5. Ejecución del juego 
"""
a = 0 # Contador basico para cambios de background
score_value = 0 # Contador del score
while running: # Bucle infinito
    pygame.time.delay(2) # Introducimos un pequeño delay de 2 ms
    pantalla.blit(background[a//20],(0,0)) # Se elige un fondo de pantalla, se va moviendo la lista cada 20 ciclos
    if a//20== len(background)-1: # Cuando se llega al tope de la lista
        a=0 # Se resetea el contador
    else: # En caso contrario
        a+=1 # Se va aumentando de 1 en 1 el contador
    for event in pygame.event.get(): # Se revisan eventos como 

        if event.type == KEYDOWN: # Si una tecla se presiona
            if event.key == K_ESCAPE: # Se verifica si es la tecla ESC
                running = False # La variable que permite mantener el bucle infinito se setea a falso

        elif event.type == QUIT: # Si el evento es cerrar la aplicacion ocurre lomismo 
            running = False # La variable que permite mantener el bucle infinito se setea a falso
            
    shipX, shipY = extract_index_finger() # Extraer la posicion del indice
    if shipX: # Si la respuesta es un numero entonces se actualiza la variable
        shipX_new = shipX # Almacenamos el nuevo valor, en caso contrario no se modifica
        
    for i in range(num_of_enemies): # Se cuenta la cantidad de enemigos que se decidió agregar al juego 
        enemyX[i] += enemyX_change[i] # A cada uno se le modifica su posicion en X
         
        if enemyY[i] >= WINDOWHEIGHT-60: # Si llegan a la parte mas baja
            
            over = pygame.font.Font('freesansbold.ttf', 80).render("PERDISTE", True, (255, 255, 255)) # Se renderiza el mensaje de perdiste
            pantalla.blit(over, (int(WINDOWWIDTH/4), int(WINDOWWIDTH/4))) # Se coloca la posicion del mensaje
            running = False # Se cambia la variable que permite seguir jugando
            break # Se acaba el for para acabar con el juego
        
        if enemyX[i] <= 60: # Si la nave enemiga llega a el tope de la izquierda
            
            enemyX_change[i] = 10 + score_value//2 # Se le cambia el sentido de orientación y la velociad tambien 
            enemyY[i] += enemyY_change[i] # Se actualiza el vector de posiciones
            
        elif enemyX[i] >= WINDOWWIDTH-60: # Si la nave enemiga llega a el tope de la derecha
            
            enemyX_change[i] = -10 - score_value//2 # Se le cambia el sentido de orientación y la velociad tambien 
            enemyY[i] += enemyY_change[i] # Se actualiza el vector de posiciones
        
        distance = math.sqrt(math.pow(enemyX[i] - laser_X, 2) + (math.pow(enemyY[i] - laser_Y, 2))) # Se calcula la distancia entre la bala y las naves
        if distance<50: # Si la distancia es menor a 50 entonces se puede asumir un choque 
            
            laser_Y = shipY_new # Se genera nuevo laser con una nueva posicion en Y
            laser_X = shipX_new + 30 # Se genera nuevo laser con una nueva posicion en X
            score_value +=1 # Se aumenta en 1 el puntaje de la persona
            enemyX[i] = random.randint(40, WINDOWHEIGHT-40) # Se crea un nuevo enemigo, se elige su poscion en X aleatorea
            enemyY[i] = random.randint(40, 80) # Se crea un nuevo enemigo, se elige su poscion en Y aleatorea
        
        pantalla.blit(enemyImg[i], (enemyX[i], enemyY[i])) # Se agregan los enemigos a la pantalla
    
    
    if laser_Y<=40: # Si el laser llega a su tope en Y
        
        laser_X = shipX_new + 30 # Se genera un nuevo laser en X
        laser_Y = shipY_new # Se genera un nuevo laser en Y
        
    else:   # Si el laser no ha llegdo entonces se sigue disminuyendo su posicion para que llegue hasta el tope
        
        laser_Y = laser_Y-laserY_speed # Se disminuye su posicion dependiendo de la velocidad
        
    pantalla.blit(laser_img, (laser_X, laser_Y)) # Se agregan los laseres a la imagen
    pantalla.blit(ship, (shipX_new,shipY_new)) # Se agrega la nave 
    score = pygame.font.Font('freesansbold.ttf', 20).render("Score : " + str(score_value), True, (255, 255, 255)) #muestra el puntaje
    pantalla.blit(score, (0, 0)) # Se muestra en la esquina superior izquierda
    pygame.display.flip()
