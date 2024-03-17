import sys
import random

cell_size = 10 #mm
wall_height = 10 #mm
wall_thickness = 1 #mm

strategy_choice = 1

class Strategy : # abstract class
    def __init__(self):
        pass

    def Apply(self):
        print("Applying Abstract Strategy")

    def DoSomething(self):
        print("Do Something")

class Algorithm1(Strategy) : # subclass of Strategy where it implements the methods
    def Apply(self):
        #super().Apply()
        print("Applying Algorithm1")
        algorithm1(5, 5);


class Algorithm2(Strategy) :

    def Apply(self):
        #super().Apply()
        print("Applying Algorithm2")

class Generator() :
    strategy = None

    def __init__(self):
        pass

    def SetStrategy(self, new_strategy): #setStrategy to one of the subclasses of Strategy
        self.strategy = new_strategy

    def Generate(self):
        self.strategy.Apply()
        self.strategy.DoSomething()

class Creator() :
    def __init__(self):
        pass

    def PrintLabyrinth(self):
        pass

def algorithm1(largeur, hauteur ):
    # construire le labyrinthe (grid of walls & cells)
    chemin = ' ' # couloirs/chemins visités
    laby = init_labyrinthe(largeur,hauteur) # labyrinthe sans chemins (juste des murs) = grille
    
    # le point d'entrée sera le coin en haut à droite du labyrinthe
    # donc on enlève le coin là bas
    laby[0][1] = chemin
    laby[1][1] = chemin
    printLaby(laby);

    avancer(1,1,laby, chemin)
    
    # une fois qu'on a rempli le labyrinthe par des murs & chemins, ajouter une sortie
    index = list(range(1, len(laby) - 2))
    random.shuffle(index)
    exit = False
    for i in index:
        if laby[len(laby) - 2][i] == chemin:
            laby[len(laby)-1][i] = chemin
            exit = True
        if exit:
            break

     # afficher le laby pour voir si ca marche
    printLaby(laby);

    ecrireOpenSCAD(laby, "test.txt")
    return

# avancer dans le labyrinthe (algo 1)
def avancer(x, y, laby, chemin):
    directions = [ [-2, 0, -1, 0], [0,2, 0, 1], [2,0, 1, 0], [0,-2, 0, -1]] # directions possibles de déplacement: e, s, w, n
    random.shuffle(directions) # choisir une direction aléatoire
    c = chemin
    
    for dir in directions:
        nouvX = x + dir[0]
        nouvY = y + dir[1]
        if (1 <= nouvY < len(laby)-1 and 1 <= nouvX < len(laby[0]) - 1) and laby[nouvY][nouvX] != c:
            xMur = x + dir[2]
            yMur = y + dir[3]
            # supprimer le mur et passer à la prochaine case
            laby[yMur][xMur] = c
            laby[nouvY][nouvX] = c
            avancer(nouvX, nouvY, laby, c)
            
    return

def printLaby(laby):
    for i in range(len(laby)):
        for j in range(len(laby[0])):
            print(laby[i][j], end=' ')
        print('\n')
    return

# initialise un labyrinthe vide de hauteur l x h
def init_labyrinthe(l, h):
    chemin = '_'  # couloirs/chemins visités
    mur = '#'     # murs du labyrinthe
    unvisited = 'u'
    laby = []
    for i in range(2 * h + 1):
        ligne = []
        for j in range(2 * l + 1):
            if i % 2 == 0 or j % 2 == 0:
                ligne.append(mur)
            else:
                ligne.append(unvisited)
        laby.append(ligne)
    
    return laby

def ecrireOpenSCAD(laby, outputFileName):
    file = open(outputFileName, "w")
    print("Writing...")
    # for y in laby: # pr chaque ligne du labyrinthe
    #     for x in y:
    #         if x == '#':
    #             string = "translate(["+ str(y.index(x) *cell_size) +", " + str(laby.index(y) * cell_size )+ ", 0]){cube([" + str(cell_size) + ", " + str(wall_thickness) + ", " + str(wall_thickness) + "]);}\n"
    #             file.write(string)
    strings = []
    for i in range(0, len(laby), 2):
        for j in range(0, len(laby[0]), 2):
            # 1 cell
            if i+2 < len(laby) and (j+2 <  len(laby[0])):
                middle_top = laby[i][j + 1]
                middle_left = laby[i+1][j]
                middle_bottom = laby[i+2][j+1]
                middle_right = laby[i+1][j+2]
                sides = [middle_top, middle_bottom, middle_left, middle_right]
                bools = ['false', 'false', 'false', 'false']
                for s in sides:
                    if s == '#':
                        bools[sides.index(s)] = 'true'
                string = "translate([" + str(j *cell_size) + "," + str(i *cell_size) + ",0])cell(" + bools[0]+ "," + bools[1]+ "," +bools[2] + "," + bools[3] + ");\n"
                file.write(string)
                
    # for i in range(len(laby)-1):
    #     for j in range(1,len(laby[0])-1): # look at each character in each line
            # if i%2 == 0 and laby[i][j] == '#':
            #     string = "translate(["+ str(j *cell_size) +", " + str(i * cell_size )+ ", 0]){cube([" + str(cell_size) + ", " + str(wall_thickness) + ", " + str(wall_height) + "]);} \n"
            #     file.write(string)
            #     j += 2
            # elif i%2 != 0 and laby[i][j] == '#':
            #     string = "translate(["+ str(j *cell_size) +", " + str(i * cell_size )+ ", 0]){rotate([0,0,90]){cube([" + str(cell_size) + ", " + str(wall_thickness) + ", " + str(wall_height)  + "]);}} \n"
            #     file.write(string)
            #     j += 2
    #     i += 2

    file.close()

# main call
def main():
    global strategy_choice
    # args = sys.argv[:]
    # if len(args) >= 2 :
    #     strategy_choice = int(args[1])
    
    strategy_choice = int(1)
    # Generator
    my_generator = Generator()
    if strategy_choice == 1:
        my_generator.SetStrategy(Algorithm1())
    elif strategy_choice == 2:
        my_generator.SetStrategy(Algorithm2())
    else :
        print("error strategy choice")
    my_generator.Generate()

    #Creator
    my_creator = Creator()
    my_creator.PrintLabyrinth()


if __name__ == "__main__":
    main()

# sources pour l'algo 1
# https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
# https://www.jamisbuck.org/presentations/rubyconf2011/index.html 
