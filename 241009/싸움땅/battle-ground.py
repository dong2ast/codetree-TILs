import sys

input = sys.stdin.readline

n, m, k = map(int, input().split())

field = [[-1 for _ in range(n + 1)]] # 필드 정보
for _ in range(n):
    tmp = [-1]
    for f in list(map(int, input().split())):
        tmp.append([f])
    field.append(tmp)

player = [[-1, -1, -1, -1, -1]] # 플레이어 상태
pos = [[0 for _ in range(n + 1)] for _ in range(n + 1)] # 플레이어 위치
point = [0 for _ in range(m + 1)] # 플레이어 점수
d = [(-1, 0), (0, 1), (1, 0), (0, -1)]

for i in range(1, m + 1):
    y, x, dist, s = map(int, input().split())
    player.append([y, x, dist, s, 0]) # 좌표, 방향, 초기능력치, 총
    pos[y][x] = i


def check_boundary(y, x, dist):
    dy, dx = d[dist]
    if 0 < x+dx <= n and 0 < y+dy <= n:
        return y+dy, x+dx, dist

    dist = (dist + 2) % 4
    dy, dx = d[dist]
    return y+dy, x+dx, dist

def compare_gun(y, x, gun):
    global field

    tmp = gun
    for g in field[y][x]:
        if g > tmp:
            tmp = g
    if tmp != gun:
        field[y][x].append(gun)
        field[y][x].remove(tmp)
    return tmp

def win(y, x, index, earn):
    global point, player
    point[index] += earn

    p_y, p_x, dist, s, gun = player[index]

    gun = compare_gun(y, x, gun)
    pos[y][x] = index
    player[index] = [y, x, dist, s, gun]


def lose(y, x, index):
    global player, field

    p_y, p_x, dist, s, gun = player[index]
    if gun != 0:
        field[y][x].append(gun)
    gun = 0

    for i in range(4):
        i = (dist+i)%4
        dy, dx = d[i]
        if 0<y+dy<=n and 0<x+dx<=n and pos[y+dy][x+dx]==0:
            p_y, p_x = y+dy, x+dx
            dist = i
            break
    pos[p_y][p_x] = index
    gun = compare_gun(p_y, p_x, gun)
    player[index] = [p_y, p_x, dist, s, gun]



def battle(y, x, contender):
    global player, pos

    c_s, c_g = player[contender][3], player[contender][4]
    c_power = c_s + c_g

    remainder = pos[y][x]
    r_s, r_g = player[remainder][3], player[remainder][4]
    r_power = r_s + r_g

    winner, loser, earn = -1, -1, 0
    if c_power == r_power:
        if c_s > r_s:
            winner, loser= contender, remainder
        else:
            winner, loser= remainder, contender
    elif c_power > r_power:
        winner, loser, earn = contender, remainder, c_power-r_power
    else:
        winner, loser, earn = remainder, contender, r_power-c_power

    lose(y, x, loser)
    win(y, x, winner, earn)






def move(player_index):
    global player, pos
    y, x, dist, s, gun = player[player_index]
    pos[y][x] = 0

    y, x, dist = check_boundary(y, x, dist) # 한칸 이동

    if pos[y][x] > 0: # 플레이어와 배틀
        battle(y, x, player_index)
    else: # 총기비교 및 교체 (플레이어가 없는경우)
        gun = compare_gun(y, x, gun)
        pos[y][x] = player_index
        player[player_index] = [y, x, dist, s, gun] # 이동완료



# 라운드
for _ in range(k):
    for i in range(1, m + 1):
        move(i)

result = ''
for i in point[1:]:
    result += f'{i} '
print(result.rstrip())