import pygame
import numpy as np
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800,600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('3D Rendering with Rotation and Projection')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

angle = 0
points = [
    np.array([-0.5, -0.5, -0.5]),
    np.array([0.5, -0.5, -0.5]),
    np.array([0.5, 0.5, -0.5]),
    np.array([-0.5, 0.5, -0.5]),
    np.array([-0.5, -0.5, 0.5]),
    np.array([0.5, -0.5, 0.5]),
    np.array([0.5, 0.5, 0.5]),
    np.array([-0.5, 0.5, 0.5])
]

def matmul(a, b):
    return np.dot(a, b)

def rotate(points, angle):
    rotationZ = np.array([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])

    rotationX = np.array([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])

    rotationY = np.array([
        [math.cos(angle), 0, math.sin(angle)],
        [0, 1, 0],
        [-math.sin(angle), 0, math.cos(angle)]
    ])

    rotated_points = []
    for point in points:
        rotated = matmul(rotationY, point)
        rotated = matmul(rotationX, rotated)
        rotated = matmul(rotationZ, rotated)
        rotated_points.append(rotated)

    return rotated_points

def project(points):
    projected_points = []
    distance = 2
    for point in points:
        z = 1 / (distance - point[2])
        projection = np.array([
            [z, 0, 0],
            [0, z, 0]
        ])
        projected2d = matmul(projection, point[:3])
        projected2d *= 200
        projected_points.append(projected2d)
    return projected_points

def connect_points(i, j, points):
    pygame.draw.line(screen, WHITE, (points[i][0] + width / 2, points[i][1] + height / 2),
                     (points[j][0] + width / 2, points[j][1] + height / 2), 1)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    rotated_points = rotate(points, angle)
    projected_points = project(rotated_points)

    for p in projected_points:
        pygame.draw.circle(screen, WHITE, (int(p[0] + width / 2), int(p[1] + height / 2)), 4)

    for i in range(4):
        connect_points(i, (i + 1) % 4, projected_points)
        connect_points(i + 4, ((i + 1) % 4) + 4, projected_points)
        connect_points(i, i + 4, projected_points)

    angle += 0.03
    pygame.display.flip()
    clock.tick(60)

pygame.quit()