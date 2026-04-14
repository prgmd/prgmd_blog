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
### [1629번 - 곱셈](https://www.acmicpc.net/problem/1629)
> 자연수 A를 B번 곱한 수를 알고 싶다. 단 구하려는 수가 매우 커질 수 있으므로 이를 C로 나눈 나머지를 구하는 프로그램을 작성하시오. 첫째 줄에 A, B, C가 빈 칸을 사이에 두고 순서대로 주어진다. A, B, C는 모두 2,147,483,647 이하의 자연수이다.

이 유형을 정의하는 문제. 이를 응용해서 푸는 식이다. 이 코드가 정석이니 이를 외워두는 것이 좋다.

``` python
a, b, c = map(int, input().split())

def mul(n1, n2):
    return (n1*n2)%c

def square(exp):
    if exp == 1:
        return a
    
    half = square(exp//2)
    
    if exp % 2 == 0:
        return mul(half, half)
    else:
        return mul(mul(half, half), a)
        
print(square(b)%c)
```

### [10830번 - 행렬 제곱](https://www.acmicpc.net/problem/10830)

> 크기가 N*N인 행렬 A가 주어진다. 이때, A의 B제곱을 구하는 프로그램을 작성하시오. A^B의 각 원소를 1,000으로 나눈 나머지를 출력하라.
 조건: (2 ≤ N ≤ 5, 1 ≤ B ≤ 100,000,000,000)

이 문제의 경우 1629번에서 구한 식에 '행렬 제곱'을 응용.

``` python
import sys
input = sys.stdin.readline

n, b = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(n)]

# 두 행렬 mat1과 mat2를 곱하는 함수 (표준 행렬 곱셈 알고리즘)
def multi(mat1, mat2):
    temp = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n): # 공통 차원 순회 (곱하고 더하기)
                # += 를 통해 값을 누적함
                temp[i][j] += mat1[i][k] * mat2[k][j]
            temp[i][j] %= 1000
    return temp

def power(mat, exp):
    if exp == 1:
        # A^1이라도 원소가 1000인 경우 결과는 0이 되어야 하므로 나머지 연산 수행
        for i in range(n):
            for j in range(n):
                mat[i][j] %= 1000
        return mat

    half = power(mat, exp // 2)

    if exp % 2 == 0:
        return multi(half, half)
    else:
        return multi(multi(half, half), mat)

result = power(a, b)

for row in result:
    print(*row)
```

### [2749번 - 피보나치 수3]
> n이 주어졌을 때, n번째 피보나치 수를 구하는 프로그램을 작성하시오. n은 1,000,000,000,000,000,000보다 작거나 같은 자연수이다.

이 문제의 경우 일반적인 '분할정복'으로는 풀이가 불가능. 피보나치 수의 경우 어떤 수 K로 나눌 때 나머지가 항상 주기를 가진다는 '피사노 주기' 정리가 있다. 이를 사용해야만 풀 수 있는 문제. 다만, 이런 문제를 풀기 위해 피사노 주기를 굳이 공부할 필요는 없어보인다... (백준에도 피사노 주기를 활용한 문제는 10문제 밖에 되지 않는다)
