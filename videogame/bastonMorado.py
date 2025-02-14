import pygame
import constante
import math

class BastonMorado():
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        # Bastón
        self.imagen_original = image
        self.update_time = pygame.time.get_ticks()
        self.angulo = 180
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.imagen.get_rect()

    def obtener_objetivo_mas_cercano(self, enemigos):
        # Buscar el enemigo más cercano
        enemigo_cercano = None
        distancia_minima = float('inf')  # Establecemos una distancia mínima muy alta
        
        for enemigo in enemigos:
            # Calculamos la distancia entre el proyectil y el enemigo
            dx = enemigo.forma.centerx - self.forma.centerx
            dy = enemigo.forma.centery - self.forma.centery
            distancia = math.sqrt(dx**2 + dy**2)

            if distancia < distancia_minima:
                enemigo_cercano = enemigo
                distancia_minima = distancia

        return enemigo_cercano

    def update(self, personaje, enemigos, grados):
        bala = None
        self.forma.center = personaje.forma.center
        self.forma.x += personaje.forma.width / 1.5
        self.forma.y -= personaje.forma.height / 2

        # Mover la rotación del arma
        self.angulo = grados
        self.imagen = pygame.transform.rotate(self.imagen_original, 360 - self.angulo)

        # Disparar   
        cooldown_animacion = 200
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            # Obtener el enemigo más cercano
            enemigo_cercano = self.obtener_objetivo_mas_cercano(enemigos)

            if enemigo_cercano:
                # Crear el proyectil y darle la posición inicial y objetivo
                bala = Pro(self.imagen_bala, self.forma.centerx, self.forma.centery, enemigo_cercano.forma.center, 5)  # Velocidad 5
                print("Se creó un proyectil en:", self.forma.centerx, self.forma.centery, "Ángulo hacia enemigo:", enemigo_cercano.forma.center)
                self.update_time = pygame.time.get_ticks()

        return bala
    
    def dibujar(self, ventana):
        pygame.draw.rect(ventana, constante.NEGRO, self.forma, 1)
        self.imagen = pygame.transform.rotate(self.imagen_original, 360 - self.angulo)
        ventana.blit(self.imagen, self.forma)

class Pro(pygame.sprite.Sprite):
    def __init__(self, image, x, y, objetivo, velocidad):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_ori = image
        self.image = self.imagen_ori
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = velocidad  # Velocidad del movimiento
        self.objetivo = objetivo  # El objetivo al que se dirige el proyectil (una posición)

    def calcular_angulo(self):
        # Calculamos el ángulo entre la posición actual y la posición del objetivo
        dx = self.objetivo[0] - self.rect.centerx
        dy = self.objetivo[1] - self.rect.centery
        angulo = math.degrees(math.atan2(dy, dx))  # Convertimos de radianes a grados
        return angulo

    def update(self):
        # Calculamos el ángulo hacia el objetivo
        angulo = self.calcular_angulo()

        # Calculamos las componentes del movimiento en x e y
        delta_x = math.cos(math.radians(angulo)) * self.velocidad
        delta_y = math.sin(math.radians(angulo)) * self.velocidad

        # Actualizamos la posición
        self.rect.x += delta_x
        self.rect.y += delta_y

    def dibujar(self, ventana):
        ventana.blit(self.image, (self.rect.centerx - self.image.get_width() // 2, 
                                  self.rect.centery - self.image.get_height() // 2))
