import pygame
import numpy
import os
import random
import neat
import math

WIN_WIDTH = 600
WIN_HEIGHT = 400
SQR_SIZE = 25

#C:\Users\Bruno\PycharmProjects\tensorEnvV2\games\Snake
SNAKE_IMGS = [
    pygame.transform.scale(pygame.image.load(os.path.join("","head2.png")), (25,25)),
    pygame.transform.scale(pygame.image.load(os.path.join("", "body.png")), (25,25)),
    pygame.transform.scale(pygame.image.load(os.path.join("", "head2best.png")), (25,25)),
    ]

FRUIT_IMGS = [
    pygame.transform.scale(pygame.image.load(os.path.join("","apple.png")), (25,25)),
    ]

DIRECTIONS = {
    "UP": (0, -1),
    "LEFT": (-1, 0),
    "DOWN": (0, 1),
    "RIGHT": (1, 0)}

    #TURN LEFT
    # (x1, y1) = (y1, x1)
    #TURN RIGHT
    # (x1, y1) = (-y1, x1)

class Snake:
    IMGS = SNAKE_IMGS[0]

    class BodyPart:
        def __init__(self, image, x , y):
            self.x = x
            self.y = y
            self.img = image

    def __init__(self, x, y):
        head = self.BodyPart(SNAKE_IMGS[0], x , y)
        self.points = 0
        self.x = x
        self.y = y
        self.vel = 25
        self.body = [head]
        self.size = 1
        self.direction = DIRECTIONS["UP"]

    def move(self, win):
        x1, y1 = self.direction
        if len(self.body) > 1:
            item = 0
            for item in range(len(self.body) - 1):
                length = len(self.body)
                self.body[length - item - 1].x = self.body[length - item - 2].x
                self.body[length - item - 1].y = self.body[length - item - 2].y
                (x_pos, y_pos) = (self.body[length - item - 1].x, self.body[length - item - 1].y)
                draw_image(win,self.body[length - item - 1].img, x_pos, y_pos)
        self.x = (self.x + self.vel * x1)
        self.y = (self.y + self.vel * y1)
        head_image = self.body[0].img
        if get_key(self.direction) == "UP":
            self.body[0].img = SNAKE_IMGS[0]
        elif get_key(self.direction) == "DOWN":
            self.body[0].img = rotate_image(SNAKE_IMGS[0], 180)
        elif get_key(self.direction) == "LEFT":
            self.body[0].img = rotate_image(SNAKE_IMGS[0], 90)
        elif get_key(self.direction) == "RIGHT":
            self.body[0].img = rotate_image(SNAKE_IMGS[0], -90)
        self.body[0].x = self.x
        self.body[0].y = self.y
        draw_image(win, self.body[0].img, self.x, self.y)

    def change_direction(self, new_direction):
        x_new, y_new = DIRECTIONS[new_direction]
        x_old, y_old = self.direction
        if x_new * -1 != x_old or y_new * -1 != y_old:
            self.direction = DIRECTIONS[new_direction]

    def grow(self):
        x_last = self.body[-1].x
        y_last = self.body[-1].y
        x_dir, y_dir = self.direction
        new_body_part = self.BodyPart(SNAKE_IMGS[1], x_last + self.vel * x_dir , y_last + self.vel * y_dir )
        self.body.append(new_body_part)
        self.increase_points()

    def increase_points(self):
        self.points = self.points + 1



    def can_turn_to(self, new_direction):
        (x1, y1) = DIRECTIONS[new_direction]
        x_dir, y_dir = self.direction
        x = self.x
        y = self.y
        if x_dir == 0:
            x = (self.x - self.vel * x1 * y_dir)
            return not check_if_out_of_bounds(x, y)
        else:
            y = (self.y - self.vel * x1 )
            return not check_if_out_of_bounds(x, y)

    def get_pos_if_turn(self, new_direction):
        (x1, y1) = DIRECTIONS[new_direction]
        x_dir, y_dir = self.direction
        x = self.x
        y = self.y
        if x_dir == 0:
            x = (self.x - self.vel * x1)
            return x, y
        else:
            y = (self.y - self.vel * x1)
            return x, y

    def get_dir_to_left(self):
        for x, direction in enumerate(DIRECTIONS):
            if get_key(self.direction) == direction:
                next_index = (x + 1) % 4
                return list(DIRECTIONS)[next_index]

    def get_dir_to_right(self):
        for x, direction in enumerate(DIRECTIONS):
            if get_key(self.direction) == direction:
                next_index = (x - 1) % 4
                return list(DIRECTIONS)[next_index]



class Fruit:
    IMAGE =  pygame.transform.scale(pygame.image.load(os.path.join("","apple.png")), (25,25))

    def __init__(self, x, y):
        self.x = x
        self.y = y


def draw_image(win, image, x, y):
    win.blit(image, (x, y))



def draw_window(win, snake, apples):
    draw_fruits(win, apples)
    snake.move(win)
    pygame.display.update()


def draw_fruits(win,apples):
    for apple in apples:
        draw_image(win, FRUIT_IMGS[0], apple.x, apple.y)


def draw_grid(win):
    white = (0,0,0)
    for x in range(int(WIN_WIDTH/SQR_SIZE)):
        for y in range(int(WIN_HEIGHT/SQR_SIZE)):
            rect = pygame.Rect(x * SQR_SIZE, y * SQR_SIZE, SQR_SIZE, SQR_SIZE)
            pygame.draw.rect(win, white, rect, 2)


def rotate_image(image, angle):
    return pygame.transform.rotate(image, angle)


def get_key(val):
    for key, value in DIRECTIONS.items():
        if val == value:
            return key

    return "key doesn't exist"


def catch_event(event, snake):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            snake.change_direction("LEFT")
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            snake.change_direction("RIGHT")
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            snake.change_direction("UP")
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            snake.change_direction("DOWN")


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    paused = False

def spawn_fruits(apples, snakes):
    if len(apples) == 0:
        """
        x_rand = random.randint(1, (WIN_WIDTH/25) - 1)*25
        y_rand = random.randint(1, (WIN_HEIGHT/25) - 1)*25
        colour = pygame.Surface.get_at((x_rand, y_rand))
        white = (255, 255, 255)
        while colour != white:
            x_rand = random.randint(1, (WIN_WIDTH / 25) - 1) * 25
            y_rand = random.randint(1, (WIN_HEIGHT / 25) - 1) * 25
            colour = pygame.Surface.get_at((x_rand, y_rand))
        """

        apple = Fruit(random.randint(1, (WIN_WIDTH/25) - 1)*25, random.randint(1, (WIN_HEIGHT/25) - 1)*25)
        apples.append(apple)



def check_if_caught_fruit(win, snake, apples):
    for apple in apples:
        if apple.x == snake.x and apple.y == snake.y:
            apples.remove(apple)
            snake.grow()
            return True
    return False


def check_if_lost(snake):
    black = (0, 0, 0)
    if check_if_out_of_bounds(snake.x, snake.y):
        return True
    for body_part in snake.body[1:]:
        if snake.body[0].x == body_part.x and snake.body[0].y == body_part.y:
            return True
    return False


def check_will_hit_body(snake, x_next, y_next):
    for body_part in snake.body[1:]:
        if x_next == body_part.x and y_next == body_part.y:
            return True
    return False


def check_if_out_of_bounds(x,y):
    if x < 0 or y < 0 or x > WIN_WIDTH - SQR_SIZE or y > WIN_HEIGHT - SQR_SIZE:
        return True
    return False


def can_move_to_front(direction, x, y, snake):
    (x1, y1) = DIRECTIONS[direction]
    if x1 == 0:
        y = (y + SQR_SIZE * y1)
        if y < 0 or y > WIN_HEIGHT - SQR_SIZE:
            return 0
        if check_will_hit_body(snake, x, y):
            return 0
    else:
        x = (x + SQR_SIZE * x1)
        if x < 0 or x > WIN_WIDTH - SQR_SIZE:
            return 0
        if check_will_hit_body(snake, x, y):
            return 0
    return 1


def get_point_with_dir(direction, x, y):
    x_aux, y_aux = DIRECTIONS[direction]
    new_x = (x + SQR_SIZE * x_aux)
    new_y = (y + SQR_SIZE * y_aux)
    return new_x, new_y


def get_inputs(snake, apple):
    Inputs =[0, 0, 0, 0, 0, 0]
    direction = get_key(snake.direction)
    dir_to_left = snake.get_dir_to_left()
    dir_to_right = snake.get_dir_to_right()
    x = snake.x
    y = snake.y
    x_aux, y_aux = get_point_with_dir(direction, x, y)
    Inputs[0] = can_move_to_front(direction, x_aux, y_aux, snake)
    Inputs[1] = can_move_to_front(dir_to_left, x, y, snake)
    Inputs[2] = can_move_to_front(dir_to_right, x, y, snake)
    #front
    dist_before = dist_to_fruit(x, y, apple)
    xafter , yafter = get_point_with_dir(direction, x, y)
    dist_after = dist_to_fruit(xafter, yafter, apple)
    if dist_before > dist_after and can_move_to_front(direction, x_aux, y_aux, snake):
        Inputs[3] = 1
    xafter , yafter =  get_point_with_dir(snake.get_dir_to_left(), x, y)
    dist_after = dist_to_fruit(xafter, yafter, apple)
    if dist_before > dist_after and can_move_to_front(dir_to_left, x, y, snake):
        Inputs[4] = 1
    xafter , yafter =  get_point_with_dir(snake.get_dir_to_right(), x, y)
    dist_after = dist_to_fruit(xafter, yafter, apple)
    if dist_before > dist_after and can_move_to_front(dir_to_right, x, y, snake):
        Inputs[5] = 1
    return Inputs


def dist_to_fruit(x, y, apple):
    return math.sqrt(
        ((x - apple.x) ** 2) + ((y - apple.y) ** 2))


def main(genomes, config):
    pygame.init()
    nets = []
    ge = []
    snakes = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        new_snake = Snake(200,200)
        new_snake.grow()
        new_snake.grow()
        new_snake.grow()
        new_snake.grow()
        snakes.append(new_snake)
        g.fitness = 0
        ge.append(g)

    apples = []
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    contador = 1
    while running:
        clock.tick(30)
        contador += 0.1
        spawn_fruits(apples, snakes)
        white = (255, 255, 255)
        win.fill(white)
        if len(snakes) == 0:
            break

        for x, snake in enumerate(snakes):
            out_of_bounds = check_if_lost(snake)

            #IF THE SNAKE WENT OUT OF BOUNDS
            if out_of_bounds or ge[x].fitness < -10:
                snakes.pop(x)
                nets.pop(x)
                ge.pop(x)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_o:
                            pause()
                        if event.key == pygame.K_RETURN:
                            return

                    catch_event(event, snake)

                dist_before = dist_to_fruit(snake.x, snake.y, apples[0])
                inputs = get_inputs(snake, apples[0])
                output = nets[x].activate((inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5]))
                #print(inputs)
                #front left right
                actual_dir = snake.direction
                indice_best = output.index(numpy.amax(output))
                if indice_best == 1:
                    next_dir = snake.get_dir_to_left()
                elif indice_best == 2:
                    next_dir = snake.get_dir_to_right()
                else:
                    next_dir = get_key(snake.direction)
                best_direction = list(DIRECTIONS)[indice_best]
                snake.change_direction(next_dir)

                #IF SNAKE HAS CAUGHT THE APPLE
                if check_if_caught_fruit(win, snake, apples):
                    ge[x].fitness += 10
                    spawn_fruits(apples, snakes)

                draw_window(win, snake, apples)

                distance_after = dist_to_fruit(snake.x, snake.y, apples[0])
                # If snake has made a diferent move than the previous and it was a good one
                if dist_before < distance_after:
                    ge[x].fitness -= 2
                else:
                    ge[x].fitness += 1





def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)


    winner = p.run(main, 100)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

