---
id: 20260413-algorithm-exponentiationbysquaring
title: 분할정복을 이용한 거듭제곱
date: 2026-04-13
category: algorithm
subCategory:
  - Python
---
## 개요
분할정복 유형 중 하나. 거듭제곱 연산에 쓰이는 B의 숫자가 기하급수적으로 높을 때 지수를 절반씩 나눠 계산해 연산 횟수를 획기적으로 줄이는 알고리즘이다. 일반적으로 $A^B$를 구할 때 시간 복잡도는 $O(logB)$. 하지만 분할정복을 이용하면 10억 번 계산을 단 30번 내외로 끝낼 수 있다.

## 핵심 원리
$$A^B = 
\begin{cases} 
1 & \text{if } B = 0 \\
(A^{B/2})^2 & \text{if } B \text{ is even} \\
A \times (A^{(B-1)/2})^2 & \text{if } B \text{ is odd} 
\end{cases}$$

지수를 짝수와 홀수로 나눠 생각. 만약 2로 나눠진다면 `half`를 곱(`multi` 함수)하고, 아니라면 원래 값을 한 번 더 곱해줌.

## 대표 문제
### [행렬 제곱](https://www.acmicpc.net/problem/10830)

> 크기가 N*N인 행렬 A가 주어진다. 이때, A의 B제곱을 구하는 프로그램을 작성하시오. A^B의 각 원소를 1,000으로 나눈 나머지를 출력하라.
 조건: (2 ≤ N ≤ 5, 1 ≤ B ≤ 100,000,000,000)

``` python
import sys
input = sys.stdin.readline

# N: 행렬의 크기, B: 제곱 횟수 입력
n, b = map(int, input().split())
# 행렬 A 입력 (N x N 크기)
a = [list(map(int, input().split())) for _ in range(n)]

# 두 행렬 mat1과 mat2를 곱하는 함수 (표준 행렬 곱셈 알고리즘)
def multi(mat1, mat2):
    # 곱셈 결과를 저장할 N x N 행렬 초기화
    temp = [[0] * n for _ in range(n)]
    for i in range(n):      # 첫 번째 행렬의 행
        for j in range(n):  # 두 번째 행렬의 열
            for k in range(n): # 공통 차원 순회 (곱하고 더하기)
                # 이전 질문에서 수정된 부분: += 를 통해 값을 누적함
                temp[i][j] += mat1[i][k] * mat2[k][j]
            # 문제 조건에 따라 각 원소를 1000으로 나눈 나머지 저장
            temp[i][j] %= 1000
    return temp

# 분할 정복을 이용해 행렬을 거듭제곱하는 함수
def power(mat, exp):
    # 기저 사례(Base Case): 제곱 횟수가 1인 경우
    if exp == 1:
        # A^1이라도 원소가 1000인 경우 결과는 0이 되어야 하므로 나머지 연산 수행
        for i in range(n):
            for j in range(n):
                mat[i][j] %= 1000
        return mat

    # 지수를 절반으로 나누어 재귀적으로 계산 (log B의 시간 복잡도 핵심)
    # 예: A^10을 구하기 위해 A^5를 먼저 계산함
    half = power(mat, exp // 2)

    # 지수가 홀수인 경우: A^exp = (A^(exp//2))^2 * A
    if exp % 2:
        # half * half를 먼저 수행한 후 원래 행렬(mat)을 한 번 더 곱함
        return multi(multi(half, half), mat)
    # 지수가 짝수인 경우: A^exp = (A^(exp//2))^2
    else:
        # 구한 절반값(half)을 서로 곱함
        return multi(half, half)

# 최종 결과 계산 시작
result = power(a, b)

# 결과 행렬 출력 (각 행의 원소를 공백으로 구분)
for row in result:
    print(*row)
```
