import sys
input = sys.stdin.readline

N, M, K = map(int, input().split())
field = [[0 for _ in range(M+1)]]

for _ in range(N):
    field.append([0] + list(map(int, input().split())))

history = [[0 for _ in range(M+1)] for _ in range(N+1)]

attacker_y, attacker_x = 0, 0
target_y, target_x = 0, 0

def find_attacker():
    global attacker_y, attacker_x

    damage, turn, y, x = 5001, -1, 0, 0
    for i in range(1, N+1):
        for j in range(1, M+1):
            if field[i][j] <= 0:
                continue
            if field[i][j] < damage: # 공격력이 작으면 갱신
                damage = field[i][j]
                turn = history[i][j]
                y, x = i, j
            elif field[i][j] == damage:
                if history[i][j] > turn: # 가장 최근
                    turn = history[i][j]
                    y, x = i, j
                elif history[i][j] == turn:
                    if (i + j) > (y + x) or ((i + j) == (y + x) and j > x): # 합이 더 큰경우 / 열
                        y, x = i, j
    attacker_y, attacker_x = y, x

def find_target():
    global target_y, target_x

    damage, turn, y, x = 0, K+1, 0, 0

    for i in range(1, N+1):
        for j in range(1, M+1):
            if field[i][j] <= 0 or (i==attacker_y and j==attacker_x):
                continue
            if field[i][j] > damage:
                damage = field[i][j]
                turn = history[i][j]
                y, x = i, j
            elif field[i][j] == damage:
                if history[i][j] < turn:
                    turn = history[i][j]
                    y, x = i, j
                elif history[i][j] == turn:
                    if (i + j) < (y + x) or ((i + j) == (y + x) and j < x):
                        y, x = i, j


    target_y, target_x = y, x

d = [(0, 1), (1, 0), (0, -1), (-1, 0)]
da = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

def lazer(visited, y, x): # 초기에 history에 attacker 넣어서 호출할 것
    global target_y, target_x

    if visited[y][x] or field[y][x] == 0: # 방문했던 곳은 패스, 부서진 포탑은 못지나감
        return False
    if target_y == y and target_x == x: # 목적지 도달
        return [(y, x)]

    visited[y][x] = True  # 메모리

    result = []
    for dy, dx in d:
        tmp = lazer(visited, (y + dy - 1) % N + 1, (x + dx - 1) % M + 1)
        if tmp:
            result.append(tmp+[(y,x)])


    visited[y][x] = False

    if result: # 경로가 있으면
        shortest_path = min(result, key=len)
        return shortest_path
    return False

def bomb():
    global attacker_y, attacker_x, target_y, target_x

    course = [(target_y, target_x)]
    for dy, dx in da:
        ty, tx = (target_y+dy-1)%N+1, (target_x+dx-1)%M+1
        if field[ty][tx] == 0 or (ty == attacker_y and tx == attacker_x): # 벽이거나 공격자라면
            continue
        course.append((ty, tx))
    course.append((attacker_y, attacker_x))

    return course




for k in range(1, K+1):
    find_attacker()
    find_target()
    if target_y == 0 and target_x == 0:
        break
    field[attacker_y][attacker_x] += (N + M)

    visited = [[False for _ in range(M+1)] for _ in range(N+1)]
    course = lazer(visited, attacker_y, attacker_x)

    if not course: # 레이저 공격이 불가능 하다면
        course = bomb()


    for ty, tx in course[1:-1]: # 피해계산
        field[ty][tx] -= field[attacker_y][attacker_x]//2 # 경로 피해
    field[target_y][target_x] -= field[attacker_y][attacker_x] # target 피해
    history[attacker_y][attacker_x] = k # 공격 내역 업뎃

    for y in range(1, N+1):
        for x in range(1, M+1):
            if (y, x) not in course and field[y][x] > 0:
                field[y][x] +=1

ans = 0
for y in range(1, N + 1):
    for x in range(1, M + 1):
        if field[y][x] > ans:
            ans = field[y][x]
print(ans)