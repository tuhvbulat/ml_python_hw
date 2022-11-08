import numpy as np
import pygame
import random
import time

RADIUS = 7
CIRCLES_DISTANCE = 50


def calculate_distance(point_a, point_b):
    return np.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


def closest_point(point, points):
    point1 = None
    min_dist = -1

    for point2 in points:
        dist = calculate_distance(point2, point)
        if min_dist == -1 or dist < min_dist:
            min_dist = dist
            point1 = point2

    return point1


def get_near_points(point, points):
    near_points = []
    for point1 in points:
        if point == point1:
            continue
        if calculate_distance(point1, point) < CIRCLES_DISTANCE:
            near_points.append(point1)
    return near_points


def find_all_near_green_points(point, green_points, founded_points=None):
    all_near_green_points = []
    if founded_points is None:
        founded_points = [point]
    near_green_points = get_near_points(point, [item for item in green_points if item not in founded_points])
    if len(near_green_points) == 0:
        return []
    founded_points.extend(near_green_points)
    all_near_green_points.extend(near_green_points)
    for point1 in near_green_points:
        external_green_points = find_all_near_green_points(point1, green_points, founded_points)
        founded_points.extend(external_green_points)
        all_near_green_points.extend(external_green_points)
    return all_near_green_points



def get_all_of_color_points(points, flags, color):
    color_points = []
    for i, point in enumerate(points):
        if flags[i] == color:
            color_points.append(point)
    return color_points


def give_flags(points):
    min_points = 3
    flags = ['' for _ in range(len(points))]
    for i, point in enumerate(points):
        near_points_count = 0
        for j in range(len(points)):
            if i != j and calculate_distance(point, points[j]) < CIRCLES_DISTANCE:
                near_points_count += 1
        if near_points_count >= min_points:
            flags[i] = 'green'

    for i, point in enumerate(points):
        if flags[i] != 'green':
            for j, pnt in enumerate(points):
                if flags[j] == 'green' and calculate_distance(point, pnt) < CIRCLES_DISTANCE:
                    flags[i] = 'yellow'
                    break

    for i in range(len(points)):
        if flags[i] == '':
            flags[i] = 'red'

    return flags


def random_points(points, cursor_point):
    k = 7
    area_radius = 35
    new_points = []
    for i in range(k):
        x = np.random.randint(cursor_point[0] - area_radius, cursor_point[0] + area_radius)
        y = np.random.randint(cursor_point[1] - area_radius, cursor_point[1] + area_radius)
        new_point = [x, y]
        should_add = True
        for point in new_points:
            if calculate_distance(point, new_point) <= 2 * RADIUS + 1:
                should_add = False
                break
        for point in points:
            if calculate_distance(point, new_point) <= 2 * RADIUS + 1:
                should_add = False
                break
        if should_add:
            new_points.append([x, y])
    return new_points


def random_color():
    return [random.randint(0, 255), random.randint(0, 9), random.randint(0, 255)]


def get_closest_cluster(point, clusters, green_points):
    closest_cluster = None
    _closest_point = closest_point(point, green_points)

    for cluster in clusters:
        cluster_points = cluster["points"]
        if _closest_point in cluster_points:
            closest_cluster = cluster
            break

    return closest_cluster


def draw():
    points = []
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    screen.fill(color='white')
    pygame.display.update()
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # pygame.draw.circle(screen, color = 'black', center = event.pos, radius = RADIUS)
                # pygame.display.update()
                # points.append(list(event.pos))
                new_points = random_points(points, list(event.pos))
                for i in range(len(new_points)):
                    points.append(new_points[i])
                    pygame.draw.circle(screen, color='black', center=new_points[i], radius=RADIUS)
                    pygame.display.update()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                screen.fill(color='white')
                pygame.display.update()

                flags = give_flags(points)
                for i, point in enumerate(points):
                    pygame.draw.circle(screen, color=flags[i], center=point, radius=RADIUS)

                pygame.display.update()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                clusters = []
                flags = give_flags(points)
                iterate_points = points.copy()
                all_green_points = get_all_of_color_points(points, flags, 'green')
                green_points_for_yellow = all_green_points.copy()
                all_yellow_points = get_all_of_color_points(points, flags, 'yellow')
                all_red_points = get_all_of_color_points(points, flags, 'red')

                while len(all_green_points) != 0:
                    init_green_point = random.choice(all_green_points)
                    all_near_green_points = find_all_near_green_points(init_green_point, all_green_points)
                    all_near_green_points.append(init_green_point)
                    all_green_points = [item for item in all_green_points if item not in all_near_green_points]
                    cluster = {
                            "color": random_color(),
                            "points": all_near_green_points
                        }
                    for i, point in enumerate(all_near_green_points):
                        color = cluster["color"]
                        pygame.draw.circle(screen, color=(color[0], color[1], color[2]), center=point, radius=RADIUS)
                        pygame.display.update()
                        time.sleep(0.1)
                    clusters.append(cluster)

                for point in all_yellow_points:
                    cluster = get_closest_cluster(point, clusters, green_points_for_yellow)
                    cluster["points"].append(point)
                    color = cluster["color"]
                    pygame.draw.circle(screen, color=(color[0], color[1], color[2]), center=point, radius=RADIUS)
                    pygame.display.update()
                    time.sleep(0.1)

                print(clusters)


if __name__ == '__main__':
    draw()
