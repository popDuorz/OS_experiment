#include<stdio.h>
#include<stdlib.h>
int main(int argc, char *argv[]) {
	int num[3];
	int sum = 0;
	for(int i = 0; i < 3; i++) {
		num[i]=atoi(argv[i+1]);
		sum += num[i];
	}
	printf("The average value is \033[;32;0m%.2f\033[0m\n",((float)sum/3));
	exit(0);
}