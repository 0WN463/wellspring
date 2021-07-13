#include <stdio.h>

int process_withdraw(int previous_withdraw_amt, int requested_amt, int withdraw_limit) {
    if (previous_withdraw_amt + requested_amt < withdraw_limit)
        return requested_amt;
    else
        return 0;
}

int main(int argc, char *argv[])  {
   if(argc != 2) {
   	printf("Wrong number of arguments.\n");
	return 1;
   }
   
   int requested_amt;
   sscanf(argv[1], "%d", &requested_amt);

   int previous_withdraw_amt = 80;
   int WITHDRAW_LIMIT = 100;

   printf("You have previously withdrawn $%d\n", previous_withdraw_amt);
   printf("You have requested to withdraw $%d\n", requested_amt);
   
   int payout = process_withdraw(previous_withdraw_amt, requested_amt, WITHDRAW_LIMIT);
   
   if (payout > 0)
      printf("Here is your $%d. Have a nice day!\n", payout);
   else
      printf("Sorry, the requested amount is beyond the limit\n");
}
