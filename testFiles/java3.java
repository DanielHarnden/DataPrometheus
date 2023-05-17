public class File1 {
    public static void main(String[] args) {
        functionA();
    }
    
    public static void functionA() {
        System.out.println("This is function A");
        functionB();
    }
    
    public static void functionB() {
        System.out.println("This is function B");
        functionC();
    }
    
    public static void functionC() {
        System.out.println("This is function C");
        functionD();
    }
    
    public static void functionD() {
        System.out.println("This is function D");
        functionE();
    }
    
    public static void functionE() {
        System.out.println("This is function E");
    }
}