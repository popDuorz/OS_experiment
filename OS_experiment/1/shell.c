#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

void max(int m, int n);
int analyze(char *input,char *analyzed[])
{
    char *tmp = input;
    int start =0;
    int finish =0;
    int count = 0;
    //putchar(*tmp);
    while(1)
    {
        //putchar(*tmp);
        if(*tmp=='(')
        {
            int pp =0;
            for(int i =start;i<finish;i++)
            {
                (analyzed[count])[pp++] = input[i];
            }
            // (analyzed[count])[pp++]="\0";
            count++;
            start = finish+1;
        }
        else if(*tmp==',')
        {
            int pp =0;
            for(int i =start;i<finish;i++)
            {
                (analyzed[count])[pp++]=input[i];
            }
            // (analyzed[count])[pp++]="\0";
            count++;
            start = finish+1;
        }
        else if(*tmp=='\n')
        {
            int pp =0;
            for(int i = start;i < finish - 1;i++)
            {
                (analyzed[count])[pp++] = input[i];
            }
            // (analyzed[count])[pp++]="\0";
            count++;
            start = finish + 1;
            break;
        }
        finish++;
        tmp++;
    }
    return count;
}

int third(void) {
    
    char maxf[] = "max";
    char minf[] = "min";
    char exitf[] = "q";
    char averagef[] = "average";
    int len = 0;
    char input[100];
    char * analyzed[10];
    pid_t pid = -1;
    for(int i = 0; i < 10; i++)
        analyzed[i] = (char*)malloc(100 * sizeof(char));
    while(1) {
        for(int i = 0; i < 10; i++)
            memset(analyzed[i], 0, 100 * sizeof(char));
        len = 0;
        printf("Please enter the command(enter q to quit)\n>>");
        int count = 0;
        char ch = getchar();
        while(len < 100 && ch != '\n') {
            input[len++] = ch;
            ch = getchar();
        }
//        input[len] = '\n';
//        len++;
        input[len] = 0;
        if(!strcmp(input, exitf))
            exit(0);
        pid = fork();
        if (pid == -1) {
            printf("Fail to create a new process!");
        }
        else if (pid > 0) {
            wait(NULL);
        }
        else if (pid == 0) {
            count = analyze(input,analyzed);
            if(!strcmp(analyzed[0],maxf)) {
                char * argv[]={"max",analyzed[1],analyzed[2],NULL};
                execve("./max",argv,NULL);
            }
            if(!strcmp(analyzed[0],minf)) {
                char * argv[]={"min",analyzed[1],analyzed[2],NULL};
                execve("./min",argv,NULL);
            }
            if(!strcmp(analyzed[0],averagef)) {
                char * argv[]={"average",analyzed[1],analyzed[2],analyzed[3],NULL};
                execve("./average",argv,NULL);
            }
            exit(0);
        }
    }
    printf("\n");
    return 0;
}

int second(void)
{
    pid_t cpid1 = -1;
    pid_t cpid2 = -1;
    cpid1 = fork();
    if(cpid1 != 0) {
        cpid2 = fork();
    }
    if (cpid1 == 0) {
        printf("I'm the child1 process, my process id is %d\n", getpid());
        exit(0);
    }
    if (cpid2 == 0) {
        printf("I'm the child2 process, my process id is %d\n", getpid());
        exit(0);
    }
    if(cpid1 > 0 && cpid2 > 0) {
        printf("I'm the father process, my process id is %d\n",getpid());
        printf("my child1 id is %d, ",cpid1);
        printf("and my child2 id is %d\n",cpid2);
        wait(NULL);
    }
    if(cpid1 <= 0) {
        exit(0);
    }
    if(cpid2 <= 0)
        exit(0);
    printf("\n");
    return 0;
}
int first(void)
{
    pid_t cpid1;
    pid_t cpid2=-1;
    cpid1 = fork();
    if (cpid1 == -1) {
        printf("failed to create a new process!\n");
        return 0;
    }
    if (cpid1 == 0) {
        cpid2 = fork();
        if (cpid2 == -1) {
            printf("failed to create a new process!\n");
            return 0;
        }
        if (cpid2 == 0) {
            printf("I'm the child2 process, my process id is %d\n",getpid());
            exit(0);
        }
        if (cpid2 > 0) {
            printf("I'm the child1 process, my process id is %d, child2's pid is %d\n", getpid(), cpid2);
            wait(NULL);
            exit(0);
        }
    }
    if (cpid1 > 0) {
        printf("I'm the father process, my process id is %d, child1's pid is %d\n", getpid(), cpid1);
        wait(NULL);
    }
    return 0;
}

int main(void)
{
    char id;
    while(1)
    {
        fflush(stdin);
        printf("please enter the number of tasks(input q to exit)\n");
        scanf("%c",&id);
        getchar();
        switch(id)
        {
            case '1':
                first();
                break;
            case '2':
                second();
                break;
            case '3':
                third();
                break;
            default:
                return 0;
        }
    }
    return 0;
}

