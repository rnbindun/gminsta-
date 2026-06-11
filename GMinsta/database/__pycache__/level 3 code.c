#include <stdio.h>
#include <string.h>
#include <ctype.h>
har input[1000];
nt i;
// Skip spaces
void skipSpaces()
{
while(input[i] == ' ' || input[i] == '\n' || input[i] == '\t')
i++;
}
int matchKeyword(char keyword[])
{
skipSpaces();
int len = strlen(keyword);
if(strncmp(&input[i], keyword, len) == 0)
{
i += len;
return 1;
}
return 0;
}
int identifier()
{
skipSpaces();
if(isalpha(input[i]))
{
i++;
while(isalnum(input[i]))
i++;
return 1;
}
return 0;
}
int number()
{
skipSpaces();
if(isdigit(input[i]))
{
i++;
while(isdigit(input[i]))
i++;
return 1;
}
return 0;
}
int match(char ch)
{
skipSpaces();
if(input[i] == ch)
{
i++;
return 1;
}
return 0;
}
int expr()
{
if(identifier() || number())
{
while(1)
{
skipSpaces();
if(input[i] == '+' || input[i] == '-' ||
input[i] == '*' || input[i] == '/')
{
i++;
if(!(identifier() || number()))
return 0;
}
else
{
break;
}
}

return 1;
}

return 0;
}

// Declaration statement
int declStmt()
{
int start = i;

if(matchKeyword("int"))
{
if(identifier())
{
// Optional assignment
if(match('='))
{
if(!expr())
return 0;
}

if(match(';'))
return 1;
}
}

i = start;
return 0;
}

// Assignment statement
int assignStmt()
{
int start = i;

if(identifier())
{
if(match('='))
{
if(expr())
{
if(match(';'))
return 1;
}
}
}

i = start;
return 0;
}
int printStmt()
{
int start = i;

if(matchKeyword("print"))
{
if(match('('))
{
if(identifier())
{
if(match(')'))
{
if(match(';'))
return 1;
}}}}
i = start;
return 0;
}
// Statement list
int stmtList()
{
while(1)
{
if(declStmt() || assignStmt() || printStmt())
{
continue;
}
else
{
break;
}}
return 1;
}
// Program parser
int program()
{
if(matchKeyword("begin"))
{
stmtList();

if(matchKeyword("end"))
{
skipSpaces();

if(input[i] == '\0')
return 1;
}
}
return 0;
}
int main()
{
char choice;

while(1)
{
printf("\nEnter MiniATC Program:\n");

fgets(input, sizeof(input), stdin);

// Remove newline
input[strcspn(input, "\n")] = '\0';

i = 0;

if(program())
printf("\nParsing Successful!\nValid MiniATC Program.\n");
else
printf("\nSyntax Error!\n");

printf("\nDo you want to continue? (y/n): ");
scanf(" %c", &choice);

getchar();

if(choice == 'n' || choice == 'N')
break;
}

return 0;
}
