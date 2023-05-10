#include <iostream>
using namespace std;

int main(int argc, char* argv[])
{
    // Enters the FIRST TWO integers entered into the command line into the ints m and n respectively
    int m = atoi(argv[1]);
    int n = atoi(argv[2]);
    int temp = 0;

    // First, the program checks if m and n are non-negative and non-zero. If either of the ints entered are 0 or below, the program exits with an error message. If not, then the values of m and n are compared. If n is larger than m, their valeus are swapped.
    if (m < 1 || n < 1)
    {
        cout << "Please start the program with the following command:\n\tdpharnden42_A.exe m n\nWhere m and n are non-zero, non-negative integers.\n";
        return 0;
    } else {
        if (n > m)
        {
            temp = m;
            m = n;
            n = temp;
        }
    }

    // I print this part of the output first since I didn't want to create 2 other variables to store m and n for an output after the algorithm. I only now realized that I could have used argv, but it's too late now.
    cout << "gcd(" << m << ", " << n << ") is ";

    // Finds the remainder of m and n using the modulo operator. When the smaller number equals zero, the larger number is the found denominator.
    while (n != 0)
    {
        temp = m % n;
        m = n;
        n = temp;
    }

    // Finishes the earlier output with the calculated GCD.
    cout << m;

    return 0;
}