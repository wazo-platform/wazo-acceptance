#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <time.h>

int main()
{
    printf("PID: %i\n", getpid());
    printf("Epoch time: %i\n", time(NULL));
    fflush(stdout);
    int **a = NULL;
    *a = 4;
}
