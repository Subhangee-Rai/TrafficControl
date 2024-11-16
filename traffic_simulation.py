import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Traffic Light Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
ROAD_COLOR = (50, 50, 50)
AMBULANCE_COLOR = (0, 255, 255)  # Cyan for ambulance

# Clock
clock = pygame.time.Clock()

# Traffic Light Class
class TrafficLight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = "RED"  # RED or GREEN
        self.timer = 0

    def draw(self):
        color = GREEN if self.state == "GREEN" else RED
        pygame.draw.circle(screen, color, (self.x, self.y), 20)

# Vehicle Class
class Vehicle:
    def __init__(self, x, y, direction, is_ambulance=False):
        self.x = x
        self.y = y
        self.direction = direction  # "N", "S", "E", "W"
        self.is_ambulance = is_ambulance

    def move(self):
        if self.direction == "N":
            self.y -= 2
        elif self.direction == "S":
            self.y += 2
        elif self.direction == "E":
            self.x += 2
        elif self.direction == "W":
            self.x -= 2

    def draw(self):
        color = AMBULANCE_COLOR if self.is_ambulance else WHITE
        pygame.draw.rect(screen, color, (self.x, self.y, 20, 20))

# Initialize Traffic Lights
lights = [
    TrafficLight(400, 200),  # North
    TrafficLight(600, 400),  # East
    TrafficLight(400, 600),  # South
    TrafficLight(200, 400),  # West
]

# Vehicle Spawning
vehicles = []

def spawn_vehicle():
    directions = ["N", "S", "E", "W"]
    direction = random.choice(directions)
    is_ambulance = random.random() < 0.1  # 10% chance of being an ambulance
    if direction == "N":
        vehicles.append(Vehicle(390, 800, "N", is_ambulance))
    elif direction == "S":
        vehicles.append(Vehicle(410, 0, "S", is_ambulance))
    elif direction == "E":
        vehicles.append(Vehicle(0, 390, "E", is_ambulance))
    elif direction == "W":
        vehicles.append(Vehicle(800, 410, "W", is_ambulance))

# Traffic Light Logic
current_light = 0  # Start with light 0 (North)
light_timer = 0

def update_traffic_lights():
    global current_light, light_timer

    # Ambulance priority logic
    for i, direction in enumerate(["N", "E", "S", "W"]):
        for v in vehicles:
            if v.is_ambulance and (v.direction == direction) and (
                (v.direction == "N" and v.y > 200) or
                (v.direction == "S" and v.y < 600) or
                (v.direction == "E" and v.x < 600) or
                (v.direction == "W" and v.x > 200)
            ):
                # Give priority to the road with the ambulance
                for light in lights:
                    light.state = "RED"
                lights[i].state = "GREEN"
                light_timer = 0  # Reset timer for fairness
                return  # Exit the function, ambulance has priority

    # If no ambulance is present, calculate density
    counts = {
        "N": sum(1 for v in vehicles if v.direction == "N" and 200 < v.y < 600),
        "S": sum(1 for v in vehicles if v.direction == "S" and 200 < v.y < 600),
        "E": sum(1 for v in vehicles if v.direction == "E" and 200 < v.x < 600),
        "W": sum(1 for v in vehicles if v.direction == "W" and 200 < v.x < 600),
    }

    # Find the road with the maximum vehicles
    max_direction = max(counts, key=counts.get)

    # Update traffic light states dynamically for max traffic density
    for i, direction in enumerate(["N", "E", "S", "W"]):
        if direction == max_direction:
            lights[i].state = "GREEN"
        else:
            lights[i].state = "RED"

# Draw Roads
def draw_roads():
    screen.fill(GRAY)  # Background
    pygame.draw.rect(screen, ROAD_COLOR, (300, 0, 200, 800))  # Vertical road
    pygame.draw.rect(screen, ROAD_COLOR, (0, 300, 800, 200))  # Horizontal road

# Main Loop
running = True
last_spawn_time = time.time()

while running:
    draw_roads()  # Draw the roads

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn vehicles every 2 seconds
    if time.time() - last_spawn_time > 2:
        spawn_vehicle()
        last_spawn_time = time.time()

    # Update traffic lights
    update_traffic_lights()

    # Move and draw vehicles
    for vehicle in vehicles:
        # Move only if the light for their direction is green
        if (vehicle.direction == "N" and lights[0].state == "GREEN" and vehicle.y > 200) or \
           (vehicle.direction == "E" and lights[1].state == "GREEN" and vehicle.x < 600) or \
           (vehicle.direction == "S" and lights[2].state == "GREEN" and vehicle.y < 600) or \
           (vehicle.direction == "W" and lights[3].state == "GREEN" and vehicle.x > 200):
            vehicle.move()
        vehicle.draw()

    # Draw traffic lights
    for light in lights:
        light.draw()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
