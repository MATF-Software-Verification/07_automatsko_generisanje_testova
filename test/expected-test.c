#include <stdio.h>

unsigned c = 0;

int main(){
	int i, j, k;
	scanf("%d %d %d", &i, &j, &k);

	if(i < j){
        printf("%u. i<j: %d < %d : %d\n", c++, i, j, i<j);
        
		if(j < k){
            printf("%u. j<k: %d < %d : %d\n", c++, j, k, j<k);
			i = k;
		}else {
            printf("%u. j<k: %d < %d : %d\n", c++, j, k, j<k);
			k = i;
		}
	}
    printf("%u. i<j: %d < %d : %d\n", c++, i, j, i<j);
	printf("%d %d %d", i, j, k);
	return 0;
}
