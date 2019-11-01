import math
import random
import pygame
import tkinter as interfaz
from tkinter import messagebox

class cubo(object):
    """Objeto cubo """
    filas = 30
    altura = 600
    def __init__(self,comienzo,dirx=1,diry=0,color=(102,205,0)):
        self.pos = comienzo
        self.dirx = 1
        self.diry = 0
        self.color = color
    def mover(self,dirx,diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)
    def dibujar(self,superficie,ojos=False):
        dis = self.altura // self.filas
        #posicion actual
        i = self.pos[0]
        j= self.pos[1]

        pygame.draw.rect(superficie,self.color,(i*dis+1,j*dis+1,dis-2,dis-2))
        #al multipicar fila y columna por el ancho  ya ltura determinamos donde pintarlo
        if ojos :
            centro = dis//2
            radio = 3
            cM= (i*dis+centro-radio,j*dis+8)
            cM2 = (i*dis + dis - radio*2, j*dis+8)
            pygame.draw.circle(superficie,(0,0,0),cM,radio)
            pygame.draw.circle(superficie,(0,0,0),cM2,radio)

class serpiente(object):
    """Objeto serpiente para emular el protagonista"""
    cuerpo = []
    giros = {}
    def __init__(self,color,pos):
        self.color = color
        self.cabeza = cubo(pos) # la cabeza es el principio
        self.cuerpo.append(self.cabeza) #añadimos la cabeza al cuerpo
        self.dirx = 0
        self.diry = 0 #direccion de la serpiente
    def mover(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:     #comprueba que el usuario sale
                pygame.quit()
            teclas = pygame.key.get_pressed() #ver que tecla se pulso
            #ahora segun la tecla actualizamos el giro en la cola
            for tecla in teclas:
                if teclas[pygame.K_LEFT]:
                    self.dirx=-1
                    self.diry=0
                    self.giros[self.cabeza.pos[:]] = [self.dirx,self.diry]
                elif teclas[pygame.K_RIGHT]:
                    self.dirx=1
                    self.diry=0
                    self.giros[self.cabeza.pos[:]] = [self.dirx,self.diry]
                elif teclas[pygame.K_UP]:
                    self.dirx=0
                    self.diry=-1
                    self.giros[self.cabeza.pos[:]] = [self.dirx,self.diry]
                elif teclas[pygame.K_DOWN]:
                    self.dirx=0
                    self.diry=1
                    self.giros[self.cabeza.pos[:]] = [self.dirx,self.diry]
        for i,c in enumerate (self.cuerpo): #recorremos el cuerpo
            p = c.pos[:] #guarda la posicion en la malla
            if p in self.giros: #si la posicion del cubo esta en los giros
                giro = self.giros[p] #cogemos la direccion para girar
                c.mover(giro[0],giro[1]) #movemos el cubo en esa direccion
                if i == len(self.cuerpo)-1: # si este es el ultimo cubo
                    self.giros.pop(p)
            else :
                    #si no estamos girando el cubo
                    #si el cubo llega al borde  aparece en el otro lado
                if c.dirx == -1 and c.pos[0] <= 0:
                     c.pos = (c.filas -1,c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.filas -1 :
                     c.pos = (0,c.pos[1])
                elif c.diry == 1 and c.pos[1] >= c.filas -1 :
                     c.pos = (c.pos[0],0)
                elif c.diry == -1 and c.pos[1] <= 0 :
                     c.pos = (c.pos[0],c.filas-1)
                else:
                    c.mover(c.dirx,c.diry) #si no lo dejamos en su direccion




    def resetear(self,posicion):
        self.cabeza = cubo(posicion)
        self.cuerpo = []
        self.cuerpo.append(self.cabeza)
        self.giros = {}
        self.dirx = 0
        self.diry=1
    def annadirCubo(self):
        cola =self.cuerpo[-1]
        dx,dy = cola.dirx,cola.diry
        #añadiremos el cubo a la izquierda, a la dercha , arriba , abajo
        if dx ==1 and dy == 0:
            self.cuerpo.append(cubo((cola.pos[0]-1,cola.pos[1])))
        elif dx == -1 and dy == 0:
            self.cuerpo.append(cubo((cola.pos[0]+1,cola.pos[1])))
        elif dx == 0 and dy == 1:
            self.cuerpo.append(cubo((cola.pos[0],cola.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.cuerpo.append(cubo((cola.pos[0],cola.pos[1]+1)))
        #ponemos la direccion del cubo en la direccion que lleve la serpiente
        self.cuerpo[-1].dirx = dx
        self.cuerpo[-1].diry = dy

    def dibujar(self,superficie):
        for i,c in enumerate(self.cuerpo):
            if i == 0: # si es el primer cubo dibujamos ojos
                c.dibujar(superficie,True)
            else:
                c.dibujar(superficie)  #si no solo el cubo



def dibujarMalla(altura,filas,superficie):
    """Metodo para dibujar el fondo del juego"""
    tamLineas = altura // filas # tamaño entre lineas

    x = 0 #eje x
    y = 0 #eje y
    for i in range(filas):
        x=x + tamLineas
        y=y + tamLineas

        pygame.draw.line(superficie,(30,30,30),(x,0),(x,altura))
        pygame.draw.line(superficie,(30,30,30),(0,y),(altura,y))


def refrescarPantalla(superficie):
    """Metodo para recargar la pantalla del juego"""
    global filas, altura, serp
    superficie.fill((139,69,0)) #llena la pantalla de negro
    serp.dibujar(superficie)
    dibujarMalla(altura,filas,superficie) #dibuja la malla
    snack.dibujar(superficie)
    pygame.display.update()#actualiza la pantalla

def randomSn(filas,elemento):
    posiciones = elemento.cuerpo #cogemos todos los cubos del cuerpo
    while True: #generamos posiciones random
        x = random.randrange(filas)
        y = random.randrange(filas)
        if len(list(filter(lambda z:z.pos == (x,y),posiciones)))>0:
            #comprueba si la posicion esta ocupada por la serpiente
            continue
        else:
            break
    return (x,y)

def mensaje(sujeto, contenido):
    root = interfaz.Tk()
    root.title("SNAKE")
    root.withdraw()
    messagebox.showinfo(sujeto,contenido)
    try:
        root.destroy()
    except:
        pass

def main():
    global anchura,filas,serp,altura,snack
    anchura = 600 #anchura de la pantalla
    altura = 600 #altura de la pantalla500
    filas = 30#filas de la pantalla 20
    retardo= 190
    pantalla = pygame.display.set_mode((anchura,altura)) #creamos nuestro objeto pantalla

    serp = serpiente((102,205,0),(10,10))#creamos la serpiente

    snack = cubo(randomSn(filas,serp),color = (255,255,0))
    scnackPremium  = cubo(randomSn(filas,serp),color = (153,50,204))
    reloj = pygame.time.Clock() #creamos un reloj
    premio = False
    seguir = True
    #comienza el bucle que simula el juego

    while seguir:
        pygame.time.delay(retardo) #pausara tiempo para que no se ejecute demasiado rapido
        reloj.tick(10) #actualiza el reloj
        serp.mover()
        if serp.cuerpo[0].pos == snack.pos: #cuando la serpiente se come el cubo
        #si toca premio
            if premio == True:
                for i in range(0,5): #añadimos 5 cubos
                    serp.annadirCubo()
                premio= False        # ponemos premio a false
            else :
                serp.annadirCubo() # solo añadimos 1 de normal

            if len(serp.cuerpo )% 12 == 0: # si aumentamos en diez la score
                retardo-=35            # aumentamos la velocidad
                snack  = cubo(randomSn(filas,serp),color = (153,50,204)) #ponemos cubo lila
                premio=True  #activamos el premio
            else:
                snack = cubo(randomSn(filas,serp),color = (255,255,0)) # sino cubo normal

        for x in range(len(serp.cuerpo)):


            if serp.cuerpo[x].pos in list(map(lambda z:z.pos,serp.cuerpo[x+1:])) :
                #comprueba si se choca

                men = "Score: (" + str(len(serp.cuerpo)) +") -> Prueba de nuevo"
                mensaje("GAME OVER",men)
                serp.resetear((10,10))
                break


        refrescarPantalla(pantalla) #refresca la pantalla
