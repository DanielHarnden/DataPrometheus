#include <iostream>
#include <cmath>

// Function to calculate the area of a circle given its radius
double calculateCircleArea(double radius) {
    return M_PI * pow(radius, 2);
}

// Function to convert Celsius to Fahrenheit
double celsiusToFahrenheit(double celsius) {
    return (celsius * 9 / 5) + 32;
}

// Function to calculate the factorial of a number
int factorial(int n) {
    if (n == 0) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

// Function to check if a number is prime
bool isPrime(int number) {
    if (number <= 1) {
        return false;
    }

    for (int i = 2; i <= sqrt(number); i++) {
        if (number % i == 0) {
            return false;
        }
    }

    return true;
}

// Function to print a message to the console
void printMessage(std::string message) {
    std::cout << message << std::endl;
}

int main() {
    double circleRadius = 5.0;
    double circleArea = calculateCircleArea(circleRadius);
    std::cout << "The area of a circle with radius " << circleRadius << " is " << circleArea << std::endl;

    double celsius = 25.0;
    double fahrenheit = celsiusToFahrenheit(celsius);
    std::cout << celsius << " degrees Celsius is " << fahrenheit << " degrees Fahrenheit" << std::endl;

    int n = 5;
    int nFactorial = factorial(n);
    std::cout << "The factorial of " << n << " is " << nFactorial << std::endl;

    int primeNumber = 17;
    bool isPrimeNumber = isPrime(primeNumber);
    std::cout << primeNumber << " is " << (isPrimeNumber ? "prime" : "not prime") << std::endl;

    std::string message = "Hello, world!";
    printMessage(message);

    return 0;
}