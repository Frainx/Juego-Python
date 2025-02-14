import pygame
import constante
import random
from Personaje import Personaje
from bastonMorado import BastonMorado

pygame.init()

ventana = pygame.display.set_mode((constante.ANCHO_VENTANA,constante.ALTO_VENTANA))

pygame.display.set_caption("Lariux")

def escalar_img(image, escala):
    w = image.get_width()
    h = image.get_height()

    nueva_imagen = pygame.transform.scale(image, (w * escala, h * escala))
    return nueva_imagen

#Importar imagenes
#personaje
animaciones = []
for i in range (4):
    img = pygame.image.load(f"Assets//Andar{i}.png")
    img = escalar_img(img, constante.ESCALA_PERSONAJE)
    animaciones.append(img)

#enemigos
animaciones_enemigos = []
for i in range (10):
     img_enemigos = pygame.image.load(f"Assets//Enemigos//Golem{i}walk.png")
     img_enemigos = escalar_img(img_enemigos, constante.ESCALA_ENEMIGO)
     animaciones_enemigos.append(img_enemigos)
     
#arma
img_b_Morado = pygame.image.load(f"Assets//Armas//B_Morado.png")

#crear enemigo de la clase personaje
golem = Personaje (400, 300, animaciones_enemigos)
golem_1 = Personaje (0, 150, animaciones_enemigos)
#crear un jugador de la clase personaje
jugador = Personaje(50,50,animaciones)

#crear un arma de la clase bastonMorado
img_proyectil = pygame.image.load(f"Assets//Armas//Proyectil_Bas_Morado//001.png")
img_proyectil = escalar_img(img_proyectil, constante.ESCALA_PROYECTIL)
basMorado = BastonMorado(img_b_Morado,img_proyectil)

#crear grupo de proyectiles
grupo_proyectiles = pygame.sprite.Group()

run = True


#definir las variables de movimiento del jugador
mover_arriba = False;
mover_abajo = False;
mover_izquierda = False;
mover_derecha = False;

 #Calcular el movimiento del jugador, velocidad
delta_x = 0
delta_y = 0

#crear lista de enemigos
enemigos = []
for i in range(random.randint(1,10)):
    enemigo = Personaje(random.randint(0, constante.ANCHO_VENTANA), random.randint(0, constante.ALTO_VENTANA), animaciones_enemigos)
    enemigos.append(enemigo)


reloj = pygame.time.Clock()


#While del juego
while run == True:
    #Controlar los frames 
    reloj.tick(constante.FPS)

    ventana.fill(constante.BG_NEGRO)

    #Calcular el movimiento del jugador, velocidad
    delta_x = 0
    delta_y = 0


    #actualiza jugador
    jugador.update()

    #actualizar enemigo
    for personajes in enemigos:
         personajes.update()

    #actualiza el estado del arma
    grados = jugador.autoaim(enemigos) #Autoapuntado
    proyectil = basMorado.update(jugador,enemigos ,grados)
    if proyectil:
        grupo_proyectiles.add(proyectil)

    for proyectil in grupo_proyectiles:
        proyectil.update()

    
    #dibujar balas
    for proyectil in grupo_proyectiles:
        proyectil.dibujar(ventana)


    #dibujar al enemigo
    for personaje in enemigos:
        personaje.dibujar(ventana)

    #dibuja al jugador
    jugador.dibujar(ventana,)

    #dibuja arma
    basMorado.dibujar(ventana)

    #Cerrar el juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Inputs para moverse
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True

    #Para cuando se suelta la tecla
    if event.type == pygame.KEYUP:
         if event.key == pygame.K_a:
                mover_izquierda = False
         if event.key == pygame.K_d:
                mover_derecha = False
         if event.key == pygame.K_w:
                mover_arriba = False
         if event.key == pygame.K_s:
                mover_abajo = False

    if mover_derecha == True:
        delta_x = constante.VELOCIDAD_PERSONAJE
    if mover_izquierda == True:
        delta_x = -constante.VELOCIDAD_PERSONAJE
    if mover_arriba == True:
        delta_y = -constante.VELOCIDAD_PERSONAJE
    if mover_abajo == True:
        delta_y = constante.VELOCIDAD_PERSONAJE

    #mover al jugador
    jugador.movimiento(delta_x, delta_y)


    pygame.display.update()

pygame.quit()