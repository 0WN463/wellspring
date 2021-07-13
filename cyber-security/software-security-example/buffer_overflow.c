#include <stdio.h>

void change_value(char index, char value) {
	char arr[10];
	int b = 100;

	printf("The value of b is %d\n", b);	
	printf("Changing index %d of a to %d\n", index, value);
	
	arr[index] = value;
	printf("The value of b is %d\n", b);	
	printf("Changing index %d of a to %d\n", index, value);
}

int main(int argc, char *argv[])  {
	if(argc != 3) {
   		printf("Wrong number of arguments.\n");
		return 1;
   	}

	int index, value;
	sscanf(argv[1], "%d", &index);
	sscanf(argv[2], "%d", &value);

	change_value(index, value);	
}
