import csv
import pygame
class Node():
    def __init__(self, parent = None, position = None, elevation = None):
        self.parent = parent
        self.position = position
        self.elevation = elevation
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    start_node = Node(None, start, maze[start[0]][start[1]])
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open_list = []
    closed_list = []
    open_list.append(start_node)
    while len(open_list) > 0:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)
        #print(current_node.position)
        if current_node.position[1] == end_node.position[1]:
            path = []
            current = current_node
            while current is not None:
                e = list(current.position)
                e.append(current.elevation)
                e.append(current.g)
                e = tuple(e)
                path.append(e)
                current = current.parent
            return path[::-1]
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            node_elevation = maze[node_position[0]][node_position[1]]


            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            # Create new node
            new_node = Node(current_node, node_position, node_elevation)

            # Append
            children.append(new_node)

            # Loop through children
        for child in children:
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            child.g = current_node.g + 1 + (abs(child.elevation - current_node.elevation)*2)
            child.h = ((child.position[1] - end_node.position[1]) ** 2) * 2
            child.f = child.g + child.h

            #child.g = start_node.position[0] abs(current_node.elevation - child.elevation)
            #child.h = abs(end_node.position[0] - current_node.position[0]) ** 2
            #child.f = child.g + child.h


            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)



class MapDataDrawer():
    def __init__(self, filename, rows, cols):
        self.filename = filename
        self.rows = rows
        self.cols = cols
        self.data = []
        self.surface = pygame.display.set_mode((self.cols, self.rows))
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((self.cols, self.rows))
        with open("Colorado_844x480.dat") as inputFile:
            """my_reader = csv.reader(inputFile, delimiter = "\t")
            for x in my_reader:
                self.data.append(x)
            for row in range(len(self.data)):
                for x in range(len(self.data[row])):
                    self.data[row][x] = int(self.data[row][x])"""
            for x in inputFile:
                self.data.append(x.strip().split("   "))
        for row in range(len(self.data)):
            for column in range(len(self.data[row])):
                self.data[row][column] = int(self.data[row][column])
        pygame.init()
        print(len(self.data))




    def findMin(self):
        min = 1000000000000000000000000
        for row in self.data:
            for x in row:
                if x < min:
                    min = x
        return min

    def findMax(self):
        max = 0
        for row in self.data:
            for x in row:
                if x > max:
                    max = x
        return max
    def drawMap(self):
        #pygame.draw.rect(self.surface, (255,255,255), pygame.Rect(20,5, 5,5))

        max = self.findMax() - self.findMin()
        min = self.findMin()
        for row in range(len(self.data)):
            for column in range(len(self.data[row])):
                c = (((self.data[row][column]- min)/max * 255) // 1)
                place = pygame.Rect(column, row, 1, 1)
                place.center = (column, row)
                pygame.draw.rect(self.surface, (c, c, c), place)
        pygame.display.flip()


    def drawLowestElevPath(self):
        count = 0
        paths = []
        deltas = []
        min_delta_index = 0
        min_delta = 100000000
        while count<477:
            path = astar(self.data, (count, 0), (0, 843))
            paths.append(path)
            for x in path:
                place = pygame.Rect(x[1], x[0], 1, 1)
                place.center = (x[1], x[0])
                pygame.draw.rect(self.surface, (100, 255, 100), place)
                pygame.display.flip()
            print("Path " + str(count + 1) + " done")
            count+=1


        #path = astar(self.data, (200,0), (0,843))
        #print(path)
        elev = []
        """for path in paths:
            for x in path:
                place = pygame.Rect(x[1], x[0], 1, 1)
                place.center = (x[1], x[0])
                pygame.draw.rect(self.surface, (100, 255, 100), place)
        """


        for path in paths:
            count = 0
            delta = 0

            while count < len(path) - 1:
                delta += abs(path[count][2] - path[count+1][2])
                count+=1
            deltas.append(delta)


        for x in range(len(deltas)):
            if(deltas[x] < min_delta):
                min_delta = deltas[x]
                min_delta_index = x
        for x in paths[min_delta_index]:
            place = pygame.Rect(x[1], x[0], 1, 1)
            place.center = (x[1], x[0])
            pygame.draw.rect(self.surface, (255, 100, 100), place)
        print("Minimum elevation change: " + (str(min_delta)))
        print("Row of ideal path: " + str(min_delta_index) + " ,Path " + str(min_delta_index + 1))








    def run(self):
        self.drawMap()
        self.drawLowestElevPath()
        while not False:
            pygame.display.update()




if __name__ == '__main__':
    p = MapDataDrawer("Colorado_844x480.dat",480,844)
    p.run()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
