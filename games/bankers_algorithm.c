/*
compiled against std=gnu89 to support the LC-3 C toolchain.
*/

#include <stdio.h>

#define N 20 /*Maximum Number of processes*/
#define M 20 /*Number of resources*/

int main()
{
    int allocs[N][M];

    int max[N][M];

    int work[M];

    int need[N][M], finish[N], seq[N];
    int n, m = 0;                /*actual values of n and m, defined by user input.*/
    int i, j, k, y, seq_ind = 0; /*indicies*/
    int safe = 1;

    printf("Enter number of processes, maximum %d: ", N);
    scanf("%d", &n);
    n %= N + 1;
    printf("\n");

    printf("Enter number of resources, maximum %d: ", M);
    scanf("%d", &m);
    m %= M + 1;
    printf("\n");

    printf("Enter allocations, row by row: ");
    for (i = 0; i < n; i++)
        for (j = 0; j < m; j++)
            scanf("%d", &allocs[i][j]);
    printf("\n");

    for (i = 0; i < n; i++)
    {
        for (j = 0; j < m; j++)
            printf("%d ", allocs[i][j]);
        printf("\n");
    }

    printf("Enter max, row by row: ");
    for (i = 0; i < n; i++)
        for (j = 0; j < m; j++)
            scanf("%d", &max[i][j]);
    printf("\n");

    for (i = 0; i < n; i++)
    {
        for (j = 0; j < m; j++)
            printf("%d ", max[i][j]);
        printf("\n");
    }

    printf("Enter available resources: ");
    for (i = 0; i < m; i++)
        scanf("%d", &work[i]); /* initially equals available.*/
    printf("\n");

    for (k = 0; k < n; k++)
        finish[k] = 0;

    /*Need = Max - Allocations*/
    for (i = 0; i < n; i++)
        for (j = 0; j < m; j++)
            need[i][j] = max[i][j] - allocs[i][j];

    for (k = 0; k < n; k++)
    {
        for (i = 0; i < n; i++)
        {
            if (!finish[i])
            {
                int illegal = 0;
                for (j = 0; j < m; j++)
                {
                    if (need[i][j] > work[j])
                    {
                        illegal = 1;
                        break;
                    }
                }

                if (!illegal)
                {
                    seq[seq_ind++] = i;
                    /*Work = Work + Allocations*/
                    for (y = 0; y < m; y++)
                        work[y] += allocs[i][y];
                    finish[i] = 1;
                }
            }
        }
    }

    for (i = 0; i < n; i++)
        safe &= finish[i];

    if (!safe)
    {
        printf("Unsafe state―put on your seatbealts.\n");
        return 0;
    }

    printf("Safe sequence:\n");
    for (i = 0; i < n - 1; i++)
        printf("P%d -> ", seq[i]);
    printf("P%d\n", seq[n - 1]);

    return 0;
}