#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>

int check_key()
{
    fd_set writefds;
    FD_ZERO(&writefds);
    FD_SET(STDIN_FILENO, &writefds);

    struct timeval timeout;
    timeout.tv_sec = 0;
    timeout.tv_usec = 0;
    return select(1, NULL, &writefds, NULL, &timeout) != 0;
}