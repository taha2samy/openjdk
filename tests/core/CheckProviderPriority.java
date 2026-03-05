import java.security.Provider;
import java.security.Security;

public class CheckProviderPriority {
    public static void main(String[] args) {
        Provider[] p = Security.getProviders();

        if (p.length < 2) {
            System.err.println("[FAIL] Not enough providers loaded.");
            System.exit(1);
        }

        boolean bcfipsFirst = p[0].getName().equals("BCFIPS");
        boolean bcjsseSecond = p[1].getName().equals("BCJSSE");

        if (bcfipsFirst && bcjsseSecond) {
            System.out.println("[PASS] Primary Provider is BCFIPS.");
            System.out.println("[PASS] Secondary Provider is BCJSSE.");
            System.exit(0);
        } else {
            System.err.println("[FAIL] Provider priority is WRONG!");
            System.err.println("1st Provider: " + p[0].getName());
            System.err.println("2nd Provider: " + p[1].getName());
            System.exit(1);
        }
    }
}