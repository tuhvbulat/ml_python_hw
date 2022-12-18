import pygame as pg
from sklearn.svm import SVC
import numpy as np

BLACK = (50, 50, 50)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 500
DOT_RADIUS = 7
LINE_WIDTH = 5


def draw_dot(pos, colour):
    new_pos = [pos[0], DISPLAY_HEIGHT - pos[1]]
    val = pg.draw.circle(sc, colour, new_pos, DOT_RADIUS)
    pg.display.update(val)


def draw_line(colour, p1, p2):
    p1 = [p1[0], DISPLAY_HEIGHT - p1[1]]
    p2 = [p2[0], DISPLAY_HEIGHT - p2[1]]
    pg.draw.line(sc, colour, p1, p2, width=LINE_WIDTH)
    pg.display.update()


def get_dimension_array(array, dim):
    return [item[dim] for item in array]


def get_dots():
    reds = []
    blues = []
    getting_dots_running = True
    while getting_dots_running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                quit_app()
            elif e.type == pg.KEYDOWN and e.key == pg.K_RETURN:
                getting_dots_running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                pos = [pos[0], DISPLAY_HEIGHT - pos[1]]
                if e.button == 1:
                    draw_dot(pos, RED)
                    reds.append(pos)
                elif e.button == 3:
                    draw_dot(pos, BLUE)
                    blues.append(pos)

    return reds, blues


def get_dot():
    result = []
    getting_dot_running = True
    while getting_dot_running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                quit_app()
            elif e.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                pos = pos[0], DISPLAY_HEIGHT - pos[1]
                if e.button == 2:
                    draw_dot(pos, BLACK)
                    result = pos
                    getting_dot_running = False

    return result


def get_dot_and_predict(w, b, bigger_for_red):
    dot = get_dot()
    predict_dot_running = True
    while predict_dot_running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                quit_app()
            elif e.type == pg.KEYDOWN and e.key == pg.K_RETURN:
                RED
                if get_b(dot, w) > b:
                    if bigger_for_red:
                        colour = RED
                    else:
                        colour = BLUE
                else:
                    if bigger_for_red:
                        colour = BLUE
                    else:
                        colour = RED
                draw_dot(dot, colour)
                predict_dot_running = False


def get_b(dot, w):
    return - w[0] * dot[0] - w[1] * dot[1]


def svm(reds, blues):
    X = reds.copy()
    X.extend(blues)
    X = np.array(X)
    y = [0 for _ in reds]
    y.extend([1 for _ in blues])
    y = np.array(y)
    clf = SVC(kernel='linear').fit(X, y)
    x1 = 0
    x2 = DISPLAY_WIDTH
    w = clf.coef_[0]
    b = clf.intercept_[0]
    y1 = -(w[0] / w[1]) * x1 - b / w[1]
    y2 = -(w[0] / w[1]) * x2 - b / w[1]

    draw_line(BLACK, (x1, y1), (x2, y2))
    bigger_for_red = get_b(reds[0], w) > b
    get_dot_and_predict(w, b, bigger_for_red)
    predict_running = True
    while predict_running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                quit_app()
            elif e.type == pg.KEYDOWN and e.key == pg.K_RETURN:
                get_dot_and_predict(w, b, bigger_for_red)
            elif e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                predict_running = False


def quit_app():
    pg.quit()
    quit()


if __name__ == "__main__":
    pg.init()
    sc = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    sc.fill((245, 245, 245))
    pg.display.flip()
    reds, blues = get_dots()
    svm(reds, blues)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_app()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                sc.fill((245, 245, 245))
                pg.display.flip()
                reds, blues = get_dots()

                svm(reds, blues)
