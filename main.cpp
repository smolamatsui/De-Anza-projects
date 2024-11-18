#include <iostream>
#include <string>
using namespace std;
 
int main() {
    int number;
    cout << "Enter an integer: ";
    cin >> number;
    
    int sum = 0;
    
    for (int i = 1; i <= number; i++) {
        sum += i;
        for (int j = 2; j <= i/2; j++) {
            if (i % j == 0) {
                sum -= i;
                break;
            }
        }
    }
        
        cout << "The sum is " << sum;
        
        return 0;
    }
