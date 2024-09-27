import sys, copy
input = sys.stdin.readline

K, M = map(int, input().split())

field = [[0, 0, 0, 0, 0, 0]]
for _ in range(5):
    field.append([0]+list(map(int, input().split())))
M = list(map(int, input().split()))

def in_boundary(x, y):
    return (0<x<6 and 0<y<6)

def dfs(x, y, field, target):
    if not in_boundary(x, y) or field[y][x] != target :
        return 0

    field[y][x] = 0
    return dfs(x-1, y, field, target) + dfs(x+1, y, field, target) + dfs(x, y+1, field, target) + 1
    
def recover(x, y, check_field, field):
    check_field[y][x] = field[y][x]
    if x > 1 :
        check_field[y][x-1] = field[y][x-1]
    if x < 5 :
        check_field[y][x+1] = field[y][x+1]
    if y < 5 :
        check_field[y+1][x] = field[y+1][x]


def check_relics(field):
    result = 0
    check_field = copy.deepcopy(field)
    for i in range(1, 6):
        for j in range(1, 6):
            if check_field[i][j] == 0:
                continue
            value = dfs(i, j, check_field, field[i][j])
            if value > 2:
                result += value
            else:
                recover(x, y, check_field, field)
    return result, check_field

def turn(x, y, field, degree):
    new_field = copy.deepcopy(field)
    if degree == 90:
        for i in range(-1, 2): # 한개의 라인
            for j in range (-1, 2): # 한개의 요소
                new_field[y+j][x-i] = field[y+i][x+j] 
        return new_field
    elif degree == 180:
        for i in range(-1, 2): # 한개의 라인
            for j in range (-1, 2): # 한개의 요소
                new_field[y-i][x-j] = field[y+i][x+j] 
        return new_field
    elif degree == 270:
        for i in range(-1, 2): # 한개의 라인
            for j in range (-1, 2): # 한개의 요소
                new_field[y-j][x+i] = field[y+i][x+j] 
        return new_field


def main():
    value = 0
    change_field = []
    for degree in [90, 180, 270]:
        for x in range(2, 5):
            for j in range(2, 5):
                turn_field = turn(field)
                result, result_field = check_relics(turn_field)
                if result > value:
                    value = result
                    change_field = result_field


main()