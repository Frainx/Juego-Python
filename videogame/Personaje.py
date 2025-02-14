import pygame
import math

class Personaje():
    def __init__(self, x, y, animaciones):
        self.flip = False
        self.animaciones = animaciones
        #Animaciones del personaje
        self.frame_index = 0
        #Aqui se almacena la hora actual (en milisegundos desde que se inicio 'pygame')
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def movimiento(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        self.forma.x += delta_x
        self.forma.y += delta_y        

    def andar(self, nueva_animacion):
        self.animaciones = nueva_animacion

    def update(self):
        cooldown_animacion = 200  # Ajusta el cooldown a un valor más bajo
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0 

    def autoaim(self, enemigos):
        if enemigos:
            # Encontrar el enemigo más cercano basado en la distancia
            closest_enemy = min(enemigos, key=lambda enemigos: math.dist((self.forma.x, self.forma.y), (enemigos.forma.x, enemigos.forma.y)))
            
            # Obtener coordenadas del enemigo (por ejemplo, golem)
            enemy_x, enemy_y = closest_enemy.forma.x, closest_enemy.forma.y
            
            # Calcular el ángulo hacia ese enemigo
            dx = enemy_x - self.forma.x
            dy = enemy_y - self.forma.y
            angle = math.degrees(math.atan2(dy, dx))  # Ángulo en radianes
            return angle
        return None

    def dibujar(self, ventana):
        #pygame.draw.rect(ventana, constante.ROJO, self.forma, 1)
        imagen_dibujar=pygame.transform.flip(self.image, self.flip, False)
        ventana.blit(imagen_dibujar, self.forma)