#include <stdio.h>

void change_value(char index, char value) {
	char arr[10];
	int b = 100;
	printf("The value of b is %d\n", b);	
	printf("The return address is %p\n", __builtin_return_address(0));
	
	printf("\nChanging index %d of a to %d\n\n", index, value);

	arr[index] = value;
	
	printf("The value of b is %d\n", b);	
	printf("The return address is %p\n", __builtin_return_address(0));
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
