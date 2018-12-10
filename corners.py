import math


def clean(punts):
    llista = []
    for i in range(290, 359):  # 290, 359
        if punts[i][0] != 0 and punts[i][1] != 0:
            llista.append(punts[i])
    for i in range(0, 90):  # 0 , 70
        if punts[i][0] != 0 and punts[i][1] != 0:
            llista.append(punts[i])
    print(llista)
    return llista


def corners(points):
    xy = []
    w = 16  # 6
    max_dist = 10000000  # 5000;
    for i in range(0, len(points)-w):
        dist = math.sqrt((points[i+w][0] - points[i][0]) ** 2 + (points[i+w][1] - points[i][1]) ** 2)
        if dist < max_dist:
            ux = points[i+w][0] - points[i+w/2][0]
            uy = points[i+w][1] - points[i + w / 2][1]
            vx = points[i + w / 2][0] - points[i][0]
            vy = points[i + w / 2][1] - points[i][1]
            pas2 = (ux * vx) + (uy * vy)
            pas3 = math.sqrt(ux ** 2 + uy ** 2) * math.sqrt(vx ** 2 + vy ** 2)
            pas1 = pas2 / pas3
            beta = math.acos(pas1) * (180 / math.pi)
            if (beta > 60 and beta < 120) or (beta > 240 and beta < 300):
                xy.append(points[i+w/2])
    return xy


def cluster(points):
    for i in points:
        cont = 0
        for j in points:
            dist = math.sqrt((i[0] - j[0]) ** 2 + (i[1] - j[1]) ** 2)
            if dist < 10000 and i[0] != j[0] and i[1] != j[1] and dist != 0:
                cont = cont + 1
        if cont < 3:  # 4
            points.remove(i)
    return points



