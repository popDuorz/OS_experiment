#include<stdio.h>
#include<stdlib.h>
int main(int argc, char *argv[])
{
	//int p = atoi(argv[1]);
	int num[100];
	int sum = 0;
	for(int i = 0; i < 3; i++)
	{
		num[i]=atoi(argv[i+1]);
		sum += num[i];
	}
	printf("The average of the numbers you gave is %f\n",((float)sum/3));
	exit(0);
}