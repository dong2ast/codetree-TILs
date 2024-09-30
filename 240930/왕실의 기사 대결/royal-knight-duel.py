import sys
input = sys.stdin.readline

L, N, Q = map(int, input().split())
field = [[0 for _ in range(L+1)]]
position = [[0 for _ in range(L+1)] for _ in range(L+1)]
knights = [[0,0,0,0,0,0]]
d = [(-1, 0), (0, 1), (1, 0), (0, -1)]

for _ in range(L): # 맵 정보 저장
    field.append([0]+list(map(int, input().split())))

def fill_position(num, r, c, h, w): # 기사 위치 저장소
    global position
    for y in range(r, r+h):
        for x in range(c, c+w):
            position[y][x] = num

def clean_position():
    global position
    position = [[0 for _ in range(L + 1)] for _ in range(L + 1)]

for i in range(1, N+1): # 기사 정보 저장
    r, c, h, w, k = map(int, input().split())
    fill_position(i, r, c, h, w)
    knights.append([r, c, h, w, k, 0])

def check_boundary(y, x):
    if 0<x<=L and 0<y<=L and field[y][x] != 2:
            return True
    return False

def move_check(num, d):
    result = []
    r, c, h, w = knights[num][0], knights[num][1], knights[num][2], knights[num][3]
    # print(num, r, c, h, w)
    for y in range(r, r + h):
        for x in range(c, c + w):
            if not check_boundary(y+d[0], x+d[1]): # 벽이라면 False
                return False
            if position[y+d[0]][x+d[1]] == num: # 같은 숫자면 패스
                continue
            if position[y+d[0]][x+d[1]] != 0: # 기사라면 move 연쇄
                tmp = move_check(position[y+d[0]][x+d[1]], d)
                if not tmp:
                    return False
                else:
                    result.extend(tmp)
            result.append(num)
    return result

def check_damage(num, d): # 피해 확인
    global field, knights
    r, c, h, w, k, damage = knights[num]
    r, c = r+d[0], c+d[1]
    for y in range(r, r + h): # 함정 탐색
        for x in range(c, c + w):
            if field[y][x] == 1:
                damage += 1
    knights[num][5] = damage # 데미지 업뎃

    if k <= damage: # 죽었으면 return
        return

    knights[num][0] = r # 위치 업뎃
    knights[num][1] = c



for k in range(Q): # 왕의 명령 == main
    i, d_index = map(int, input().split())
    tmp = move_check(i, d[d_index])
    if not tmp:
        continue

    knights[i][0] += d[d_index][0]
    knights[i][1] += d[d_index][1]
    for j in set(tmp):
        if i != j:
            check_damage(j, d[d_index])

    clean_position()

    for j in range(1, N+1):
        if knights[j][4] <= knights[j][5]:
            continue
        fill_position(j, knights[j][0], knights[j][1], knights[j][2], knights[j][3])

summation = 0
for j in range(1, N+1):
    if knights[j][4] <= knights[j][5]:
        continue
    summation += knights[j][5]
print(summation)