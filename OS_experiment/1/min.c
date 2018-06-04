#include<stdio.h>
#include<stdlib.h>
int main(int argc, char *argv[]) {

	int m = atoi(argv[1]);
	int n = atoi(argv[2]);
	printf("The min num is \033[;32;0m%d\033[0m\n", m < n ? m : n);
	exit(0);
}