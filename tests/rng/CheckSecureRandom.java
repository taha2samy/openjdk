import java.security.SecureRandom;

public class CheckSecureRandom {
    public static void main(String[] args) throws Exception {
        SecureRandom sr = new SecureRandom();

        System.out.println("Algorithm: " + sr.getAlgorithm());
        System.out.println("Provider: " + sr.getProvider().getName());
        if (sr.getProvider().getName().equals("BCFIPS")) {
            System.out.println("[PASS] SecureRandom is using BCFIPS Provider.");
            System.exit(0);
        } else {
            System.err.println("[FAIL] SecureRandom is NOT using BCFIPS! Found: " + sr.getProvider().getName());
            System.exit(1);
        }
    }
}