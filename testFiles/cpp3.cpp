// File name: pemutations.cpp
// Author: Daniel Harnden
// Date: October 28th, 2021
// Purpose: Create a Johnson-Trotter and Lexicographic Sorting algorithm
#include <iostream>
using namespace std;

// A simple swapping algorithm. Swaps the values k and l of the input array and the left array. I thought I'd try function overloading, it was way simpler than I thought it would be.
void Swap(int* input, bool* left, int k, int l)
{
    int temp = input[k];
    input[k] = input[l];
    input[l] = temp;
    bool tempLeft = left[k];
    left[k] = left[l];
    left[l] = tempLeft;
}

void Swap(int* input, int k, int l)
{
    int temp = input[k];
    input[k] = input[l];
    input[l] = temp;
}

// This just prints the values. It's cleaner than having it in the middle of the code. It also keeps track of a counting variable by returning count + 1.
int Print(int* input, bool* left, int length, int count)
{
    cout << count << ":\t";

    for (int i = 0; i < length; i ++)
    {
        if (left[i])
        {
            cout << "<- ";
        } else {
            cout << "-> ";
        }
    }

    cout << endl << count << ":\t";

    for (int i = 0; i < length; i ++)
    {
        char temp = input[i];
        cout << temp << "  ";
    }

    cout << endl << endl;

    return count += 1;
}

int Print(int* input, int length, int count, int i, int j)
{
    cout << count << ":\t";

    for (int i = 0; i < length; i ++)
    {
        char temp = input[i];
        cout << temp << " ";
    }

    cout << "  i = " << i << "   j = " << j << endl << endl;

    return count += 1;
}

void Print(int* input, int length, int count)
{
    cout << count << ":\t";

    for (int i = 0; i < length; i++)
    {
        char temp = input[i];
        cout << temp << " ";
    }

    cout << endl << endl;
}

// The JohnsonTrotter sorting algorithm.
void JohnsonTrotter(int* input, int length)
{
    // Keeps track of the highest movable value.
    int value = 0;
    int valueIndex = 0;
    // Keeps track of the current iteration for the printing function.
    int count = 1;
    // Keeps track of if there was a swap. If there wasn't, the function ends.
    bool swapped;
    // Creates and initializes an "arrow" array using bools to determine which way the numbers are facing. Since it's called left, and the arrows start facing left, all values are true.
    bool left[length];
    for (int i = 0; i < length; i++)
    {
        left[i] = true;
    }

    // Prints the first iteration before entering the loop.
    count = Print(input, left, length, count);

    // Loops until a switch does not happen.
    while (valueIndex != -1)
    {
        // Sets up three variables used in the loop.
        value = -1;
        valueIndex = 0;
        swapped = false;

        // Checks every value of the array.
        for (int i = 0; i < length; i++)
        {
            // Checks if the arrow is facing left and there is a value to the left (not i = 0).
            if (left[i] && i != 0)
            {
                // If the number at i is greater than the number to the left AND the number at i is greater than the current highest number, then a swap will take place and i is now the index value.
                if (input[i] > input[i - 1] && input[i] > value)
                {
                    value = input[i];
                    valueIndex = i;
                    swapped = true;
                }
            }
            // If the arrow is facing right OR i = 0.
            else 
            {
                // Double checks the the arrow is facing right and that there is a value to the right.
                if (!left[i] && i + 1 < length) 
                {
                    // If the number at i is greater than the number to the right AND the number at i is greater than the current highest number, then a swap will take palce and i is now the index value.
                    if (input[i + 1] < input[i] && input[i] > value)
                    {
                        value = input[i];
                        valueIndex = i;
                        swapped = true;
                    }
                }
            }
        }
        
        //If a swap has been determined to take place...
        if (swapped)
        {
            // Changes the direction of the arrows of the values greater than the highest swapped value.
            for (int i = 0; i < length; i++)
            {
                if (input[i] > input[valueIndex])
                {
                    left[i] = !left[i];
                }
            }

            // Swaps the values.
            if (left[valueIndex])
            {
                Swap(input, left, valueIndex, valueIndex - 1);
            } else {
                Swap(input, left, valueIndex, valueIndex + 1);
            }

            // Prints teh subsequent arrays.
            count = Print(input, left, length, count);
            
        // If no swap has been determined to take place, the loop exits.
        } else {
            valueIndex = -1;
            cout << "Johnson-Trotter Algorithm complete!" << endl << endl;
        }
    }
}

void LexicographicSort(int* input, int length)
{
    // Same as in the JohnsonTrotter algorithm.
    int count = 1;
    // This i is used exactly the same as in the pseudocode, but it's initialized outside the while loop so it can act as the loop breaker.
    int i = 0;

    // Loops until a switch does not happen.
    while (i != -1)
    {
        // Same as in pseudocode. If i is not changed, the break condition is met.
        i = -1;
        int j = -1;

        // Checks the array for an i such that i < i + 1.
        for (int a = 0; a < length - 1; a++)
        {
            if (input[a] < input[a + 1])
            {
                i = a;
            }
        }

        // Checks the array for a j such that j > i.
        for (int b = 0; b < length; b++)
        {
            if (input[b] > input[i])
            {
                j = b;
            }
        }

        // If there has been a swap...
        if (i != -1)
        {
            // Prints the information.
            count = Print(input, length, count, i, j);
            // Swaps the variables.
            Swap(input, i, j);
            // Does so math mumbo jumbo to reverse everything past i + 1. Defnitely a way to make this better but it works and I'm lazy.
            if (i + 1 < length - 1)
            {
                int z = 0;
                int y = 0;
                if ((length) % 2 == 0)
                {
                    y =  length / 2;
                } else {
                    y = (length / 2) + 1;
                }

                for (int c = i + 1; c <= y; c++)
                {
                    if (c + z < length - 1)
                    {
                        Swap(input, c, length - 1 - z);
                        z += 1;
                    }
                }
            }
        } else {
            // If there has not been a swap, then the final print statement is printed and the program exits.
            Print(input, length, count);
            cout << "Lexicographic Algorithm complete!" << endl << "All done!" << endl << endl;
        }
    }
}

int main()
{
    // Prompts the user for the raw input
    cout << "Enter a string to find its permutations: ";
    string rawInput;
    cin >> rawInput;

    // So I think this is cool but I store each character of the raw input into an int array by converting each character into an int. When it's printed, the ints are converted into chars, and each char is printed.
    int inputArray[rawInput.length()];
    for (int i = 0; i < rawInput.length(); i++)
    {
        inputArray[i] = int(rawInput[i]);
    }

    // Goes to the JohnsonTrotter function.
    JohnsonTrotter(inputArray, rawInput.length());

    // Resets the array and goes to the LexicographicSort function.
    for (int i = 0; i < rawInput.length(); i++)
    {
        inputArray[i] = int(rawInput[i]);
    }
    LexicographicSort(inputArray, rawInput.length());

    // End of program. This input buffer is here because if I didn't have it, the Windows terminal would just close.
    cin >> rawInput;
}

