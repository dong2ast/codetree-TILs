import sys
from collections import deque

input = sys.stdin.readline

n, m = map(int, input().split())

field = [[-1 for _ in range(n + 1)]]

for _ in range(n):
    field.append([-1] + list(map(int, input().split())))

target = [(-1, -1)]

for _ in range(m):
    target.append(tuple(map(int, input().split())))

people = [(-1, -1)]
d = [(-1, 0), (0, -1), (0, 1), (1, 0)]


def can_go(y, x):
    if 0 < y <= n and 0 < x <= n and field[y][x] != -1:
        return True
    return False


def bfs(s_y, s_x, people_index):
    if not can_go(s_y, s_x):
        return 255
    t_y, t_x = target[people_index]
    visited = [(s_y, s_x)]

    queue = deque([(s_y, s_x, 1)])

    while queue:
        y, x, pos = queue.popleft()

        if y == t_y and x == t_x:
            return pos

        for dy, dx in d:
            if can_go(y + dy, x + dx) and (y + dy, x + dx) not in visited:
                queue.append((y + dy, x + dx, pos + 1))
                visited.append((y + dy, x + dx))


def find_path_and_move(people_index):
    y, x = people[people_index]

    r_y, r_x, value = -1, -1, 225

    for dy, dx in d:  # 최단 경로 방향 탐색
        result = bfs(y + dy, x + dx, people_index)

        if result < value:
            r_y, r_x, value = y + dy, x + dx, result
    people[people_index] = (r_y, r_x)  # 이동


def find_base(start_y, start_x):
    queue = deque([(start_y, start_x)])
    visited = [(start_y, start_x)]

    while queue:
        y, x = queue.popleft()

        if field[y][x] == 1:
            return y, x

        for dy, dx in d:
            if can_go(y + dy, x + dx) and (y + dy, x + dx) not in visited:
                queue.append((y + dy, x + dx))
                visited.append((y + dy, x + dx))


def check_conv():
    for i in range(1, len(people)):
        y, x = target[i]
        if target[i] == people[i] and field[y][x] != -1:
            field[y][x] = -1


t = 0
while True:
    t+=1
    for j in range(1, min(t, m+1)):  # 이동
        if target[j] == people[j]:
            continue
        find_path_and_move(j)
    check_conv() # 도착 확인
    if len(people) != m+1: # 새로운 사람 진입
        y, x = find_base(target[t][0], target[t][1])
        people.append((y, x))
        field[y][x] = -1



    if len(people) != m+1:
        continue
    else:
        end = True
        for i in range(m+1):
            if target[i] != people[i]: end = False
        if end:
            break

print(t)