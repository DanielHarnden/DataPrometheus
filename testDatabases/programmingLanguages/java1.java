public class ExampleFunctions {
    
    // Function to add two integers
    public static int add(int a, int b) {
        return a + b;
    }
    
    // Function to calculate the area of a rectangle
    public static int calculateRectangleArea(int length, int width) {
        return length * width;
    }
    
    // Function to check if a given number is even
    public static boolean isEven(int num) {
        return (num % 2 == 0);
    }
    
    // Function to convert Celsius to Fahrenheit
    public static double celsiusToFahrenheit(double celsius) {
        return (celsius * 9/5) + 32;
    }
    
    // Function to print a message a specified number of times
    public static void printMessage(String message, int numTimes) {
        for (int i = 0; i < numTimes; i++) {
            System.out.println(message);
        }
    }
    
    // Main method to test the functions
    public static void main(String[] args) {
        int sum = add(3, 5);
        System.out.println("3 + 5 = " + sum);
        
        int area = calculateRectangleArea(4, 5);
        System.out.println("Area of rectangle with length 4 and width 5 is " + area);
        
        int num = 6;
        if (isEven(num)) {
            System.out.println(num + " is even");
        } else {
            System.out.println(num + " is odd");
        }
        
        double celsius = 25;
        double fahrenheit = celsiusToFahrenheit(celsius);
        System.out.println(celsius + " degrees Celsius is equal to " + fahrenheit + " degrees Fahrenheit");
        
        printMessage("Hello, world!", 3);
    }
}
