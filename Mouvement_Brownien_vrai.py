import random
import math
import pygame
import colorsys
import time
import matplotlib.pyplot as plt
import numpy as np


class Particle:
    def __init__(self):
        self.color = (255,0,0)
        self.INITAL_POSITION=  None
        self.position = None
        self.last_position = None


    def move(self,steps = ((1,0),(0,1),(-1,0),(0,-1))):
        self.last_position = self.position
        self.dx, self.dy = random.choice(steps)
        self.position = self.position[0]+self.dx, self.position[1]+self.dy





def random_spawn_cercle(self,radius):
    random_theta = random.uniform(0, 2*math.pi) # Angle aléatoire entre 0 et 2*pi
    x = (radius+1) * math.cos(random_theta) # Coordonnée x du point
    y = (radius+1) * math.sin(random_theta) # Coordonnée y du point
    self.x, self.y =  int(x), int(y)




class Simulation_Random_Walk:
    def __init__(self, length, hight, n = None):
        self.n = n
        self.count = 0
        self.LIGHT_YELLOW = (255,255,102)
        self.RED = (204,0,0)
        self.BLACK = (0,0,0)
        self.length = length
        self.hight = hight
        self.grid = [[self.BLACK for i in range(self.length)] for j in range(self.hight)]
        self.grid[self.length//2][self.hight//2] = Particle()
        self.Particle = self.grid[self.length//2][self.hight//2]
        self.Particle.position = (self.length//2, self.hight//2)
        self.Particle.color = self.RED
        self.end = False


    def reset(self):
        self.count = 0
        self.grid = [[self.BLACK for i in range(self.length)] for j in range(self.hight)]
        self.grid[self.hight//2][self.length//2] = Particle()
        self.Particle = self.grid[self.length//2][self.hight//2]
        self.Particle.position = (self.length//2, self.hight//2)
        self.Particle.color = self.RED


    def next_step(self):
        self.Particle.move()
        if self.n == None or self.count <= self.n:
            self.count +=1
            # Déplacement impossible
            if self.Particle.position[0] > self.length-1 or self.Particle.position[0] < 0 or self.Particle.position[1] > self.hight-1 or self.Particle.position[1] < 0:
                self.Particle.position = (self.Particle.last_position[0], self.Particle.last_position[1])
                self.count -= 1
            # Couleur de la grille
            if self.grid[self.Particle.position[0]][self.Particle.position[1]] != self.BLACK:
                self.grid[self.Particle.position[0]][self.Particle.position[1]] = self.LIGHT_YELLOW
            else:
                self.grid[self.Particle.position[0]][self.Particle.position[1]] = self.Particle.color
        else:
            self.end = True


    def get_distance(self):
        '''
        Cette fonction retourne un tuple de la distance entre la Particlee et son point de départ
        (x,y)
        '''
        return self.Particle.position[0]-self.length//2, self.Particle.position[1]-self.hight//2
        


class Simulation_DLA_1:
    def __init__(self, length, hight):
        self.age = 0
        self.rate = 0.2
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)
        self.length = length
        self.hight = hight
        self.grid = [[self.BLACK for i in range(self.length)] for j in range(self.hight)]
        self.Particle = Particle()
        self.Particle.color = colorsys.hsv_to_rgb((240-self.rate*self.age)/360,1,1)
        self.Particle.color = tuple(255 * elem for elem in self.Particle.color)
        self.end = False
        # Active ou désactive l'aparition des Particlee sur un cercle
        self.spawn_cercle = True
        if self.spawn_cercle:
            position = self.random_spawn_cercle(self.length//2)
            self.Particle.position = (position[0], position[1])
        else:
            self.Particle.position = (self.length//2, self.hight//2)
        

    def random_spawn_cercle(self,radius):
        random_theta = random.uniform(0, 2*math.pi) # Angle aléatoire entre 0 et 2*pi
        x = (radius+1) * math.cos(random_theta) # Coordonnée x du point
        y = (radius+1) * math.sin(random_theta) # Coordonnée y du point
        return int(x+self.length//2), int(y+self.hight//2)

    def shortest_radius(self,center, points):
        shortest_distance = self.length//2
        for point in points:
            distance = math.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2)
            if distance < shortest_distance:
                shortest_distance = distance
        return int(shortest_distance)-2
    
    def is_in_circle(self, radius, position):
        coords = []
        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1):
                if math.sqrt(x*x + y*y) <= radius:
                    coords.append((x+self.length//2, y+self.hight//2))
        if position in coords:
            return True
        else:
            return False
    
    def new_spawn(self):
        if self.spawn_cercle:
            print(self.Particle.position)
            not_black = []
            for y in range(self.hight):
                for x in range(self.length):
                    if self.grid[y][x] != self.BLACK:
                        not_black.append((x,y))
            self.Particle.position = self.random_spawn_cercle((self.shortest_radius((self.length//2,self.hight//2),not_black)))
            print(self.Particle.position)
            print(f'Radius: {self.shortest_radius((self.length//2,self.hight//2),not_black)}')
        else:
            self.Particle.position = (self.length,self.hight)
            

    def reset(self):
        self.age = 0
        # Création de la grille avec une Particlee au centre
        self.grid = [[self.BLACK for i in range(self.length)] for j in range(self.hight)]
        self.Particle = Particle()
        # Localisation de la Particlee sur un cercle
        self.new_spawn()
        # Couleur de la Particlee
        self.Particle.color = colorsys.hsv_to_rgb((240-self.rate*self.age)/360,1,1)
        self.Particle.color = tuple(255 * elem for elem in self.Particle.color)


    def next_step(self):
        """
        Cette fonction produit des modification sur la variable self.grid pour que celle-ci affiche la prochaine grille
        """
        self.Particle.move()

        # Contact entre les Particlee
        if self.grid[self.Particle.position[0]][self.Particle.position[1]] != self.BLACK:
            self.age += 1
            self.grid[self.Particle.last_position[0]][self.Particle.last_position[1]] = self.Particle.color

            # Couleur de la prochaine Particlee
            if self.age*self.rate <= 240:
                self.Particle.color = colorsys.hsv_to_rgb((240-self.rate*self.age)/360,1,1)
                self.Particle.color = tuple(255 * elem for elem in self.Particle.color)
            else:
                self.crystalColor = (255,0,0)

            # Localisation de la nouvelle Particlee
            self.new_spawn()
        
        # Contact avec un mure
        elif self.Particle.position[0] >= self.length-1 or self.Particle.position[0] <= 0 or self.Particle.position[1] >= self.hight-1 or self.Particle.position[1] <= 0:
            self.age += 1
            self.grid[self.Particle.position[0]][self.Particle.position[1]] = self.Particle.color
            self.grid[self.Particle.last_position[0]][self.Particle.last_position[1]] = self.BLACK

            # Couleur de la prochaine Particlee
            if self.age*self.rate <= 240:
                self.Particle.color = colorsys.hsv_to_rgb((240-self.rate*self.age)/360,1,1)
                self.Particle.color = tuple(255 * elem for elem in self.Particle.color)
            else:
                self.crystalColor = (255,0,0)
            
            # Localisation de la nouvelle Particlee
            self.new_spawn()
        
        # Déplacement normale de la Particlee
        elif self.grid[self.Particle.position[0]][self.Particle.position[1]] == self.BLACK:
            not_black = []
            for y in range(self.hight):
                for x in range(self.length):
                    if self.grid[y][x] != self.BLACK and self.grid[y][x] != self.RED:
                        not_black.append((x,y))
            if self.is_in_circle(self.shortest_radius((self.length//2,self.hight//2),not_black)//2,self.Particle.position):
                self.grid[self.Particle.last_position[0]][self.Particle.last_position[1]] = self.BLACK
                self.new_spawn()
                #self.grid[self.Particle.position[0]][self.Particle.position[1]] = self.BLACK
                #self.Particle.position = self.Particle.last_position
                #self.grid[self.Particle.position[0]][self.Particle.position[1]] = self.RED
            else:
                self.grid[self.Particle.last_position[0]][self.Particle.last_position[1]] = self.BLACK
                self.grid[self.Particle.position[0]][self.Particle.position[1]] = self.RED


class Simulation_DLA_2:
    def __init__(self,length,hight):
        self.age = 0
        self.rate = 0.2
        self.BLACK = (0,0,0)
        self.RED = (255,0,0)
        self.length = length
        self.hight = hight
        self.grid = [[self.BLACK for i in range(self.length)] for j in range(self.hight)]
        self.Particle = Particle()
        self.Particle.color = colorsys.hsv_to_rgb((240-self.rate*self.age)/360,1,1)
        self.Particle.color = tuple(255 * elem for elem in self.Particle.color)
        self.grid[self.hight//2][self.length//2] = self.RED
        self.end = False
        self.long_radius = 1
        # Active ou désactive l'aparition des Particlee sur un cercle
        self.spawn_cercle = True
        self.Particle.position = (self.length//2, self.hight//2)

    def random_spawn_perimiter(self):
        side = random.choice(['top', 'right', 'bottom', 'left'])
        if side == 'top':
            x = random.uniform(0, self.length-1)
            y = 0
        elif side == 'right':
            x = self.length-1
            y = random.uniform(0, self.hight-1)
        elif side == 'bottom':
            x = random.uniform(0, self.length-1)
            y = self.hight-1
        else:
            x = 0
            y = random.uniform(0, self.hight-1)
        return int(x), int(y)
    
    def longest_radius(self):
        distance = math.sqrt((self.Particle.position[0] - self.length//2)**2 + (self.Particle.position[1] - self.hight//2)**2)
        if distance > self.long_radius:
            self.long_radius = int(distance)
        return self.long_radius
    
    def random_spawn_cercle(self,radius):
            random_theta = random.uniform(0, 2*math.pi) # Angle aléatoire entre 0 et 2*pi
            x = (radius+1) * math.cos(random_theta) # Coordonnée x du point
            y = (radius+1) * math.sin(random_theta) # Coordonnée y du point
            return int(x+self.length//2), int(y+self.hight//2)   
     
    def new_spawn(self):
        if self.spawn_cercle:
            if self.Particle.position == None:
                self.Particle.position = (self.length//2, self.hight//2)
            new_pos = self.random_spawn_cercle(self.longest_radius())
            if new_pos[0] >= 0 or new_pos[0] <= self.length or new_pos[1] >= 0 or new_pos[1] <= self.hight:
                self.Particle.position = new_pos
            else:
                self.new_spawn()
        else:
            self.Particle.position = self.random_spawn_perimiter()

    def is_in_circle(self, radius, position):
        coords = []
        for x in range(-radius, radius+1):
            for y in range(-radius, radius+1):
                if math.sqrt(x*x + y*y) <= radius:
                    coords.append((x+self.length//2, y+self.hight//2))
        if position in coords:
            return True
        else:
            return False

    def reset(self):
        self.age = 0
        # Création de la grille avec une Particlee au centre
        self.grid = [[self.BLACK for i in range(self.length)] for j in range(self.hight)]
        self.Particle = Particle()
        self.Particle.position = (self.length//2, self.hight//2)
        # Localisation de la Particlee sur un cercle
        self.new_spawn()
        # Couleur de la Particlee
        self.Particle.color = colorsys.hsv_to_rgb((240-self.rate*self.age)/360,1,1)
        self.Particle.color = tuple(255 * elem for elem in self.Particle.color)
        # Particlee central
        self.grid[self.hight//2][self.length//2] = self.RED

    def next_step(self):
        self.Particle.move()
        # Contact avec un mure
        if self.Particle.position[0] >= self.length or self.Particle.position[0] <= -1 or self.Particle.position[1] >= self.hight or self.Particle.position[1] <= -1:
            self.grid[self.Particle.last_position[0]][self.Particle.last_position[1]] = self.RED
            self.Particle.position = self.Particle.last_position

        # Contact entre les Particlee
        elif self.grid[self.Particle.position[0]][self.Particle.position[1]] != self.BLACK:
            self.age += 1
            self.grid[self.Particle.last_position[0]][self.Particle.last_position[1]] = self.Particle.color

            # Couleur de la prochaine Particlee
            if self.age*self.rate <= 240:
                self.Particle.color = colorsys.hsv_to_rgb((240-self.rate*self.age)/360,1,1)
                self.Particle.color = tuple(255 * elem for elem in self.Particle.color)
            else:
                self.crystalColor = (255,0,0)

            # Localisation de la nouvelle Particlee
            self.new_spawn()

        # Déplacement normale de la Particlee
        elif self.grid[self.Particle.position[0]][self.Particle.position[1]] == self.BLACK:
            if self.is_in_circle(self.long_radius*2, self.Particle.position) == False:
                self.grid[self.Particle.last_position[0]][self.Particle.last_position[1]] = self.BLACK
                self.Particle.position = self.random_spawn_cercle(self.long_radius)
            else:
                self.grid[self.Particle.last_position[0]][self.Particle.last_position[1]] = self.BLACK
                self.grid[self.Particle.position[0]][self.Particle.position[1]] = self.RED

    

class Interface:
    def __init__(self, length=501, hight=501):
        # Initialisation de Pygame
        pygame.init()

        # Simulation 
        self.sim1 = Simulation_Random_Walk(101,101)
        self.sim2 = Simulation_DLA_1(51,51)
        self.sim3 = Simulation_DLA_2(51,51)
        self.main_sim = self.sim1

        # Définition des couleurs
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (120, 204, 0)
        self.RED = (204, 0, 0)
        self.BLUE = (102, 178, 255)
        self.GREY = (160, 160, 160)
        self.DARK_GREY = (96, 96, 96)
        self.LIGHT_GREY = (224, 224, 224)

        # Définition de la taille de la fenêtre
        self.LENGTH = length
        self.HIGHT = hight
        self.window_size = (self.LENGTH+100, self.HIGHT+100)

        # Création de la fenêtre
        self.window = pygame.display.set_mode(self.window_size)

        # Variable du bouton Pause Play
        font = pygame.font.Font(None, 36)
        self.play_text = font.render("Play", True, (224,255,224))
        self.pause_text = font.render("Pause", True, (255,224,224))
        self.button_pause_play = pygame.Rect(10, 10, 80, 30)
        self.is_playing = False
        # Variable du bouton Reset
        self.reset_text = font.render("Reset", True, (224,224,255))
        self.button_color = self.BLUE
        self.button_reset = pygame.Rect(100, 10, 80, 30)
        self.is_reset = False

        # Variable du bouton Simulation 1
        self.sim1_text = font.render("Sim 1", True, self.LIGHT_GREY)
        self.button_color = self.GREY
        self.button_sim1 = pygame.Rect(200, 10, 80, 30)
        self.is_sim1 = True
        # Variable du bouton Simulation 2
        self.sim2_text = font.render("Sim 2", True, self.LIGHT_GREY)
        self.button_color = self.GREY
        self.button_sim2 = pygame.Rect(300, 10, 80, 30)
        self.is_sim2 = False
        # Variable du bouton Simulation 3
        self.sim3_text = font.render("Sim 3", True, self.LIGHT_GREY)
        self.button_color = self.GREY
        self.button_sim3 = pygame.Rect(400, 10, 80, 30)
        self.is_sim3 = False

    def reset(self):
        '''
        Cette fonction permet de reset l'afichage à zéro. (l'écrant devient complètement noir)
        '''
        if self.is_reset:
            pygame.draw.rect(self.window, self.BLUE, self.button_reset)
            self.window.blit(self.reset_text, (self.button_reset.x, self.button_reset.y))
            #
            # Action de reset
            self.window.fill(self.BLACK)
            self.main_sim.reset()
            #
            self.is_reset = False
        else:
            pygame.draw.rect(self.window, self.BLUE, self.button_reset)
            self.window.blit(self.reset_text, (self.button_reset.x, self.button_reset.y))

    def play(self):
        '''
        Cette fonction permet de démarer ou de mettre sur pause tout simulation
        '''
        # Si le bouton afiche Pause la simulation est en action
        if self.is_playing:
            pygame.draw.rect(self.window, self.RED, self.button_pause_play)
            self.window.blit(self.pause_text, (self.button_pause_play.x, self.button_pause_play.y))
            self.update_grid(self.main_sim.grid)
        # Si le bouton affiche Play la simulation est arrèter
        else:
            pygame.draw.rect(self.window, self.GREEN, self.button_pause_play)
            self.window.blit(self.play_text, (self.button_pause_play.x, self.button_pause_play.y))


    def simulation(self):
        '''
        Cette fonction permet de modifier l'affichage des bouton pour chacune des simulation
        '''
        # Simulation 1
        if self.is_sim1 == True:
            self.main_sim = self.sim1
            # Changement de couleur des boutons
            pygame.draw.rect(self.window, self.DARK_GREY, self.button_sim1)
            self.window.blit(self.sim1_text, (self.button_sim1.x, self.button_sim1.y))
            pygame.draw.rect(self.window, self.GREY, self.button_sim2)
            self.window.blit(self.sim2_text, (self.button_sim2.x, self.button_sim2.y))
            pygame.draw.rect(self.window, self.GREY, self.button_sim3)
            self.window.blit(self.sim3_text, (self.button_sim3.x, self.button_sim3.y))
        # Simulation 2
        if self.is_sim2 == True:
            self.main_sim = self.sim2
            # Changement de couleur des boutons
            pygame.draw.rect(self.window, self.GREY, self.button_sim1)
            self.window.blit(self.sim1_text, (self.button_sim1.x, self.button_sim1.y))
            pygame.draw.rect(self.window, self.DARK_GREY, self.button_sim2)
            self.window.blit(self.sim2_text, (self.button_sim2.x, self.button_sim2.y))
            pygame.draw.rect(self.window, self.GREY, self.button_sim3)
            self.window.blit(self.sim3_text, (self.button_sim3.x, self.button_sim3.y))
        # Simulation 3    
        if self.is_sim3 == True:
            self.main_sim = self.sim3
            # Changement de couleur des boutons
            pygame.draw.rect(self.window, self.GREY, self.button_sim1)
            self.window.blit(self.sim1_text, (self.button_sim1.x, self.button_sim1.y))
            pygame.draw.rect(self.window, self.GREY, self.button_sim2)
            self.window.blit(self.sim2_text, (self.button_sim2.x, self.button_sim2.y))
            pygame.draw.rect(self.window, self.DARK_GREY, self.button_sim3)
            self.window.blit(self.sim3_text, (self.button_sim3.x, self.button_sim3.y))

    def update_grid(self, grid):
        """
        Dessine une grille sur l'écran donné avec la couleur, la largeur et la hauteur spécifiées.
        La grille aura le nombre de cases spécifié en X et Y.
        """
        if self.is_playing:
            self.grid = grid
            grid_background = pygame.Rect((self.window_size[0]-500//len(self.grid[0])*len(self.grid[0]))//2-1,
                                        (self.window_size[1]-500//len(self.grid)*len(self.grid))//2-1,
                                        500//len(self.grid[0])*len(self.grid[0])+2,
                                        500//len(self.grid)*len(self.grid)+2)
            pygame.draw.rect(self.window, self.WHITE, grid_background)
            for y in range(len(self.grid)):
                for x in range(len(self.grid[0])):
                    rect = pygame.Rect((self.window_size[0]-500//len(self.grid[0])*len(self.grid[0]))//2+500//len(self.grid[0])*y,
                                    (self.window_size[1]-500//len(self.grid)*len(self.grid))//2+500//len(self.grid)*x,
                                    500//len(self.grid), 500//len(self.grid))
                    if type(self.grid[y][x]) == tuple:
                        pygame.draw.rect(self.window, self.grid[y][x], rect)
                    else:
                        pygame.draw.rect(self.window, self.grid[y][x].color, rect)
        self.main_sim.next_step()
                        


    def loop(self):
        # Boucle principale du jeu
        while True:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_pause_play.collidepoint(event.pos):
                        self.is_playing = not self.is_playing
                    if self.button_reset.collidepoint(event.pos):
                        self.is_reset = not self.is_reset
                    if self.button_sim1.collidepoint(event.pos):
                        self.is_reset = True
                        self.is_sim1 = True
                        self.is_sim2 = False
                        self.is_sim3 = False
                    if self.button_sim2.collidepoint(event.pos):
                        self.is_reset = True
                        self.is_sim1 = False
                        self.is_sim2 = True
                        self.is_sim3 = False
                    if self.button_sim3.collidepoint(event.pos):
                        self.is_reset = True
                        self.is_sim1 = False
                        self.is_sim2 = False
                        self.is_sim3 = True
            # Vérifit si la simulation est en action ou non
            self.simulation()
            self.play()
            self.reset()
            # Rafraîchissement de l'écran
            pygame.display.flip()

if __name__ == "__main__":
    # Création de l'instance de la simulation
    sim = Interface()

    # Lancement de la simulation
    sim.loop()

""" all_pos = []
for j in range(20,101,20):
    final_pos = []
    print(j)
    for i in range(1000):
        sim = Simulation_Random_Walk(101,101,n=j)
        while sim.end == False:
            sim.next_step()
        final_pos.append(sim.get_distance())

    distances = []
    for pos in final_pos:
        radius = math.sqrt(pos[0]**2 + pos[1]**2)
        distances.append(radius)

    x = []
    y = []
    for i in final_pos:
        x.append(i[0])
        y.append(i[1])
        all_pos.append(i)
    # création du diagramme à bande
    plt.hist(distances, alpha=0.5)
    #plt.hist(distances, 10, density=True, label=f'{j} step')

# ajout des étiquettes des axes
plt.xlabel('Distance parcourrue')
plt.ylabel('Probability')
plt.legend()

# affichage du diagramme
plt.show()

# Grille d'afichage
grid = [[0 for i in range(101)] for j in range(101)]
p = []
# Nombre de fois 
for i in range(-101//2,101//2+1):
    for j in range(-101//2,101//2+1):
        nb = all_pos.count((i,j))
        grid[i+50][j+50] = nb

print(grid)


plt.colorbar(plt.imshow(grid))
plt.show() """

