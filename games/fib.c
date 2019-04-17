#include <stdio.h>

#define MAX_N 100

int known_fibs[MAX_N];

int fib(int n);

int main(void)
{
    known_fibs[1] = 1;
    printf("I calculate Fibonacci.\n");
    while (1)
    {
        int n, i;
        printf("Enter a number (maximum is %d): ", MAX_N);
        scanf("%d", &n);
        n %= MAX_N;

        printf("First %d components of Fibonacci series is:\n", n);
        for (i = 0; i <= n; i++)
        {
            int res = fib(i);
            known_fibs[i] = res;
            printf("%d ", res);
        }
        printf("\n");
    }
    return 0;
}

int fib(int n)
{
    if (known_fibs[n])
        return known_fibs[n];
    else if (n <= 0)
        return 0;
    else
        return fib(n - 1) + fib(n - 2);
}