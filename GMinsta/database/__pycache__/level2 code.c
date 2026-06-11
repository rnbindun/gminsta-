#include <stdio.h>
#include <string.h>
#include <ctype.h>
char keywords[][10] = {"begin", "end", "int", "print"};
int isKeyword(char str[])
{
for(int i = 0; i < 4; i++)
{
if(strcmp(str, keywords[i]) == 0)
return 1;
}
return 0;
}
int isIdentifier(char str[])
{
if(!isalpha(str[0]))
return 0;
for(int i = 1; str[i] != '\0'; i++)
{
if(!isalnum(str[i]))
return 0;
}
return 1;
}
int isNumber(char str[])
{
for(int i = 0; str[i] != '\0'; i++)
{
if(!isdigit(str[i]))
return 0;
}
return 1;
}
int isOperator(char ch)
{
return (ch == '+' || ch == '-' || ch == '*' ||
ch == '/' || ch == '=');
}
int isDelimiter(char ch)
{
return (ch == ';' || ch == '(' || ch == ')');
}
int main()
{
char input[1000];
char choice;
while(1)
{
printf("\nEnter MiniATC Program:\n");
fgets(input, sizeof(input), stdin);
char token[100];
int i = 0, j = 0;
while(input[i] != '\0')
{
if(isalnum(input[i]))
{
j = 0;

while(isalnum(input[i]))
{
token[j++] = input[i++];
}
token[j] = '\0';
if(isKeyword(token))
printf("%s -> Keyword\n", token);
else if(isNumber(token))
printf("%s -> Number\n", token);
else if(isIdentifier(token))
printf("%s -> Identifier\n", token);
}
else if(isOperator(input[i]))
{
printf("%c -> Operator\n", input[i]);
i++;
}
else if(isDelimiter(input[i]))
{
printf("%c -> Delimiter\n", input[i]);
i++;
}
else
{
i++;}}
printf("\nDo you want to continue? (y/n): ");
scanf(" %c", &choice);
getchar();
if(choice == 'n' || choice == 'N')
break;
}

return 0;
}
