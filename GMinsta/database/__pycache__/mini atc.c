#include <stdio.h>
#include <ctype.h>
#include <string.h>

// Function to check if input is a keyword
int isKeyword(char str[]) {
    char *keywords[] = {"if", "while", "for", "int", "return"};
    int n = 5;

    for (int i = 0; i < n; i++) {
        if (strcmp(str, keywords[i]) == 0)
            return 1;
    }
    return 0;
}

// Function to check valid identifier
int isValidIdentifier(char str[]) {

    // Rule 1: First character must be a letter
    if (!isalpha(str[0]))
        return 0;

    // Rule 2: Remaining characters must be letters or digits
    for (int i = 1; str[i] != '\0'; i++) {
        if (!isalnum(str[i]))
            return 0;
    }

    // Rule 3: Should not be a keyword
    if (isKeyword(str))
        return 0;

    return 1;
}

int main() {
    char str[100];

    printf("Enter a string: ");
    scanf("%s", str);

    if (isValidIdentifier(str))
        printf("Valid Identifier\n");
    else
        printf("Invalid Identifier\n");

    return 0;
}