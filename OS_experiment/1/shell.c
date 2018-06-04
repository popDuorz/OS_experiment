#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

void max(int m, int n);
void getCmd(char *input, char *parameterlist[]) {
    char *tmp = input;
    int count = 0;
    int i = 0;
    for (i = 0; *tmp != '(' && i < 20; tmp++, i++) {
        parameterlist[count][i] = *tmp;
    }
    tmp ++;
    count ++;
    while (*tmp) {
        i = 0;
        while (*tmp > 48 && *tmp < 58) {
            parameterlist[count][i] = *tmp;
            tmp ++;
            i++;
        }
        count ++;
        tmp ++;
    }
}

int fork_test1(void) {
    pid_t childPid1;
    pid_t childPid2=-1;
    childPid1 = fork();
    if (childPid1 == -1) {
        printf("failed to create a new process!\n");
        return 0;
    }
    if (childPid1 == 0) {
        childPid2 = fork();
        if (childPid2 == -1) {
            printf("failed to create a new process!\n");
            return 0;
        }
        if (childPid2 == 0) {
            printf("I'm the child2 process, my process id is \033[;32;0m%d\033[0m\n", getpid());
            exit(0);
        }
        if (childPid2 > 0) {
            printf("I'm the child1 process, my process id is \033[;32;0m%d\033[0m, child2's pid is \033[;32;0m%d\033[0m\n",  getpid(),  childPid2);
            wait(NULL);
            exit(0);
        }
    }
    if (childPid1 > 0) {
        printf("I'm the father process, my process id is \033[;32;0m%d\033[0m, child1's pid is \033[;32;0m%d\033[0m\n",  getpid(),  childPid1);
        wait(NULL);
    }
    return 0;
}

int fork_test2(void) {
    pid_t childPid1=-1;
    pid_t childPid2=-1;
    childPid1 = fork();
    if(childPid1 !=0) {
        childPid2 = fork();
    }
    if (childPid1 == 0) {
        printf("I'm the child1 process, my process id is \033[;32;0m%d\033[0m\n",  getpid());
        exit(0);
    }
    if (childPid2 == 0) {
        printf("I'm the child2 process, my process id is \033[;32;0m%d\033[0m\n",  getpid());
        exit(0);
    }
    if(childPid1 > 0 && childPid2 > 0) {
        printf("I'm the father process, my process id is \033[;32;0m%d\033[0m\n", getpid());
        printf("my child1 id is \033[;32;0m%d\033[0m", childPid1);
        printf("and my child2 id is \033[;32;0m%d\033[0m\n", childPid2);
        wait(NULL);
    }
    if(childPid1 <=0) {
        exit(0);
    }
    if(childPid2 <=0)
        exit(0);
    printf("\n");
    return 0;
}

int threeCommand(void) {
    char input[20];
    char *parameterlist[10];
    pid_t pid = -1;
    for(int i = 0; i < 10; i++)
        parameterlist[i] = (char*)malloc(100 * sizeof(char));
    
    while(1) {
        for(int i = 0; i < 10; i++)
            memset(parameterlist[i],  0, 100 * sizeof(char));
        for (int i = 0; i < 20; ++i)
            input[i] = 0;
        
        printf(">");
        scanf("%s", input);
        if(!strcmp(input, "q"))
            exit(0);
        
        pid = fork();
        if (pid == -1) {
            printf("Fail to create a new process!");
        }
        else if (pid > 0) {
            wait(NULL);
        }
        else if (pid == 0) {
            getCmd(input, parameterlist);
            if(!strcmp(parameterlist[0], "max")) {
                char *argv[] = {"max", parameterlist[1], parameterlist[2], NULL};
                execve("./max", argv, NULL);
            }
            else if(!strcmp(parameterlist[0], "min")) {
                char *argv[] = {"min", parameterlist[1], parameterlist[2], NULL};
                execve("./min", argv, NULL);
            }
            else if(!strcmp(parameterlist[0], "average")) {
                char *argv[] = {"average", parameterlist[1], parameterlist[2], parameterlist[3], NULL};
                execve("./average", argv, NULL);
            }
            exit(0);
        }
    }
    return 0;
}

int main(void) {
    char choice;
    while(1) {
        fflush(stdin);
        printf("Please enter the number of tasks(input q to exit)\n");
        scanf("%c", &choice);
        getchar();
        if (choice == '1') {
            fork_test1();
        }
        else if (choice == '2') {
            fork_test2();
        }
        else if (choice == '3') {
            threeCommand();
        }
        else{
            return 0;
        }
    }
    return 0;
}


