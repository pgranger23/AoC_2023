import numpy as np

def parse_input(fname:str):
    with open(fname, 'r') as f:
        lines = f.readlines()

    inputs = []
    for line in lines:
        pos, velocity = line.strip('\n').split('@')
        pos = tuple(map(int, pos.split(',')))
        velocity = tuple(map(int, velocity.split(',')))
        inputs.append((pos, velocity))
    return inputs

def prob1():
    print("##########First part of the problem##########")
    trajectories = parse_input('input.1')
    nb_intersections = 0
    window = (200000000000000, 400000000000000)
    for i, (pos, velocity) in enumerate(trajectories):
        for j in range(i + 1, len(trajectories)):
            pos2, velocity2 = trajectories[j]

            a = velocity[1]
            b = -velocity[0]
            c = -(a*pos[0] + b*pos[1])

            a2 = velocity2[1]
            b2 = -velocity2[0]
            c2 = -(a2*pos2[0] + b2*pos2[1])

            if b2*a - b*a2 == 0: #parallel
                continue

            intersect_y = (a*c2 - a2*c)/(a2*b - a*b2)
            intersect_x = (b*c2 - b2*c)/(b2*a - b*a2)

            if (intersect_x - pos[0])*velocity[0] + (intersect_y - pos[1])*velocity[1] < 0:
                continue #Intersection in past for traj1
            if (intersect_x - pos2[0])*velocity2[0] + (intersect_y - pos2[1])*velocity2[1] < 0:
                continue #Intersection in past for traj2

            if window[0] <= intersect_x <= window[1]:
                if window[0] <= intersect_y <= window[1]:
                    nb_intersections += 1
    print(f"Number of intersections is: {nb_intersections}")




def prob2():
    print("##########Second part of the problem##########")
    trajectories = parse_input('input.1')

    A = np.zeros((6, 6), dtype=int)
    B = np.zeros((6), dtype = int)

    (x0, y0, z0), (vx0, vy0, vz0) = trajectories[0]
    for j in range(1, 4):
        (xj, yj, zj), (vxj, vyj, vzj) = trajectories[j]
        line = 2*(j - 1)

        A[line, 0] = vy0 - vyj
        A[line + 1, 0] = vz0 - vzj

        A[line, 1] = vxj - vx0
        A[line + 1, 2] = vxj - vx0

        A[line, 3] = yj - y0
        A[line + 1, 3] = zj - z0

        A[line, 4] = x0 - xj
        A[line + 1, 5] = x0 - xj

        B[line] = yj*vxj + x0*vy0 - y0*vx0 - xj*vyj
        B[line + 1] = zj*vxj + x0*vz0 - z0*vx0 - xj*vzj

    X = np.linalg.solve(A, B)
    print(f"Result is: {int(np.sum(X[0:3]))}")



if __name__ == '__main__':
    prob1()
    prob2()
