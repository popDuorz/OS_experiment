#include<stdio.h>
#include<stdlib.h>
int main(int argc, char *argv[])
{
	int m = atoi(argv[1]);
	int n = atoi(argv[2]);
	printf("The max is %d\n", m > n ? m : n);
	exit(0);
}