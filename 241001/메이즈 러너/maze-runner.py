import copy
import sys

input = sys.stdin.readline

N, M, K = map(int, input().split())

field = [[0 for _ in range(N + 1)]]  # 미로
for _ in range(N):
    field.append([0] + list(map(int, input().split())))

player = [list(map(int, input().split())) for _ in range(M)]  # 참가자 상태

exit_y, exit_x = map(int, input().split())  # 탈출구 좌표

answer = 0


def can_move(y, x):
    if 0 < y <= N and 0 < x <= N and field[y][x] < 1:  # 벽과 장외가 아닌 경우
        return True
    return False


def rotate(y, x, length):  # 미로 회전
    global field, exit_y, exit_x
    tmp = copy.deepcopy(field)
    for r in range(y, y + length):
        for c in range(x, x + length):
            # 좌표를 0, 0 으로 변환
            oy, ox = r-y, c-x
            # 90도 회전시의 좌표를 구함
            ry, rx = ox, length - oy -1
            # 다시 좌표 원복

            if field[r][c] > 0:  # 벽 체력 감소
                tmp[y+ry][x+rx] = field[r][c] - 1
            else:
                tmp[y + ry][x + rx] = field[r][c]
    field = tmp  # field 반영

def rotate_player_exit(r, c, distance):
    global exit_y, exit_x

    for p in player:
        py, px = p[0], p[1] # 1, 3
        if r<=py<r+distance and c<=px<c+distance: # 정사각형 안에 포함되어 있는 경우만
            # 0, 0 으로 이동
            oy, ox = py - r, px - c # 0, 2
            # 90도 회전시의 좌표를 구함
            ry, rx = ox, distance - oy - 1 # 2, 2
            p[0] = ry + r
            p[1] = rx + c

    if r<=exit_y<r+distance and c<=exit_x<c+distance: # 정사각형 안에 포함되어 있는 경우만
        # 0, 0 으로 이동
        oy, ox = exit_y - r, exit_x - c
        # 90도 회전시의 좌표를 구함
        ry, rx = ox, distance - oy - 1
        exit_y = ry + r
        exit_x = rx + c


def move_all():
    global exit_y, exit_x, answer

    for p in player:
        if p[0] == exit_y and p[1] == exit_x: # 이미 출구에 있는 경우
            continue

        py, px = p[0], p[1]

        if py != exit_y: # 행이 다른 경우
            ny = py
            if exit_y > ny:
                ny += 1
            else:
                ny -=1

            if not field[ny][px]:
                p[0] = ny
                answer += 1
                continue

        if px != exit_x: # 열이 다른 경우
            nx = px
            if exit_x > nx:
                nx += 1
            else:
                nx -= 1

            if not field[py][nx]:
                p[1] = nx
                answer += 1
                continue


def find_square():
    global exit_y, exit_x
    for distance in range(2, N+1): # distance
        for r in range(1, N+2-distance): # 가장 위의 행부터
            for c in range(1, N+2-distance): # 가장 왼쪽 열부터
                y2, x2 = r+distance-1, c+distance-1

                # 만약 출구가 해당 정사각형 안에 없다면 스킵합니다.
                if not (c <= exit_x <= x2 and r <= exit_y <= y2):
                    continue

                # 한 명 이상의 참가자가 해당 정사각형 안에 있는지 판단
                is_player_in = False
                for p in player:
                    py, px = p[0], p[1]
                    if c <= px <= x2 and r <= py <= y2:
                        if not (px==exit_x and py==exit_y):
                            is_player_in = True

                if is_player_in:
                    return r, c, distance

for _ in range(K):
    move_all() # 참가자 이동

    is_all_escaped = True
    for p in player:
        if p[0] != exit_y or p[1] != exit_x:
            is_all_escaped = False

    # 만약 모든 사람이 출구로 탈출했으면 바로 종료합니다.
    if is_all_escaped:
        break

    result_y, result_x, distance = find_square() # 젤 작은 사각형 찾기 | position 이용
    rotate(result_y, result_x, distance) # 필드 돌리기
    rotate_player_exit(result_y, result_x, distance) # 참가자 및 출구 돌리기
print(answer)
print(exit_y, exit_x)