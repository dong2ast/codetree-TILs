import copy
import sys
input = sys.stdin.readline

N, M, P, C, D = map(int, input().split())
R_Y, R_X = map(int, input().split())
santa = [[0, 0, 0, 0] for _ in range(P+1)]
santa[0][3] = M+1
field = [[0 for _ in range(N+1)] for _ in range(N+1)]
field[R_Y][R_X] = -1



for turn in range(1, P + 1):
    num, y, x = map(int, input().split())
    santa[num][0] = y
    santa[num][1] = x
    field[y][x] = num

def check_boundary(y, x):
    if 0<x<=N and 0<y<=N:
        return True
    return False


def find_santa():
    global R_Y, R_X
    distance = 2501
    santa_y, santa_x = 0, 0
    for y in range(N, 0, -1):
        for x in range(N, 0, -1):
            if field[y][x] > 0:
                tmp = (y-R_Y)**2 + (x-R_X)**2
                if distance > tmp:
                    distance = tmp
                    santa_y = y
                    santa_x = x
    return santa_y, santa_x

def check_direction_ru(target_y, target_x): # 방향 체크
    global R_Y, R_X

    directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
    value, direction_y, direction_x = 2501, 0, 0

    for dy, dx in directions:
        if not check_boundary(R_Y+dy, R_X+dx):
            continue

        tmp = (R_Y + dy - target_y) ** 2 + (R_X + dx - target_x) ** 2
        if value > tmp:
            value = tmp
            direction_y, direction_x = dy, dx

    return direction_y, direction_x


def check_direction_santa(santa_y, santa_x): # 방향 체크
    global R_Y, R_X

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 상, 우, 하, 좌
    value, direction_y, direction_x = ((santa_y-R_Y)**2 + (santa_x-R_X)**2), 0, 0

    for dy, dx in directions:
        if not check_boundary(santa_y+dy, santa_x+dx) or field[santa_y+dy][santa_x+dx] > 0:
            continue
        tmp = (santa_y+dy-R_Y)**2 + (santa_x+dx-R_X)**2

        if value > tmp:
            value = tmp
            direction_y, direction_x = dy, dx

    return direction_y, direction_x

def domino(santa_num, direction_y, direction_x):
    santa_y, santa_x, score, stun = santa[santa_num]
    field[santa_y][santa_x] = 0

    next_y, next_x = santa_y + direction_y, santa_x + direction_x

    if not check_boundary(next_y, next_x): # 장외
        santa[santa_num][3] = M+1
        return

    if field[next_y][next_x] != 0:
        domino(field[next_y][next_x], direction_y, direction_x)

    field[next_y][next_x] = santa_num
    santa[santa_num][0] = next_y
    santa[santa_num][1] = next_x

def conflict(santa_num, target_y, target_x, direction_y, direction_x, point, turn): # 움직일 곳에 산타가 있으면 이거 보내고 루돌프는 움직인 담에 -1 찍자
    field[santa[santa_num][0]][santa[santa_num][1]] = 0
    santa[santa_num][2] += point
    santa[santa_num][3] = turn+1

    next_y, next_x = target_y + direction_y*point, target_x + direction_x*point

    if not check_boundary(next_y, next_x): # 장외
        santa[santa_num][3] = M+1
        return

    if field[next_y][next_x] != 0:
        domino(field[next_y][next_x], direction_y, direction_x)

    field[next_y][next_x] = santa_num
    santa[santa_num][0] = next_y
    santa[santa_num][1] = next_x

for turn in range(1, M + 1):

    # 루돌프 로직
    target_y, target_x = find_santa() # 산타 찾기
    if target_y == 0 and target_x ==0: # 산타가 전부 탈락
        break
    direction_y, direction_x = check_direction_ru(target_y, target_x) # 방향 찾기
    next_y, next_x = R_Y+direction_y, R_X+direction_x

    if field[next_y][next_x] != 0: # 충돌 감지
        conflict(field[next_y][next_x], next_y, next_x, direction_y, direction_x, C, turn)
    field[R_Y][R_X] = 0
    field[next_y][next_x] = -1 # 좌표 이동
    R_Y, R_X = next_y, next_x

    # 산타 로직
    for i in range(1, len(santa)):
        if santa[i][3] >= turn: # 스턴걸린 상태
            continue
        direction_y, direction_x = check_direction_santa(santa[i][0], santa[i][1]) # 방향 찾기
        next_y, next_x = santa[i][0]+direction_y, santa[i][1]+direction_x

        if field[next_y][next_x] == -1:
            conflict(i, next_y, next_x, -1*direction_y, -1*direction_x, D, turn)
        else:
            field[santa[i][0]][santa[i][1]] = 0
            field[next_y][next_x] = i
            santa[i][0] = next_y
            santa[i][1] = next_x

    for s in santa[1:]:
        if s[3]<=M:
            s[2]+=1

result = ''

for i in range(1, P+1):
    result += f"{santa[i][2]} "
print(result.rstrip())