import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

public class RejectShortHmacKey {
    public static void main(String[] args) {
        try {
            // FIPS Minimum key strength is 112 bits. 8 bytes = 64 bits (Illegal)
            byte[] shortKey = new byte[8];
            SecretKeySpec keySpec = new SecretKeySpec(shortKey, "HmacSHA256");
            Mac mac = Mac.getInstance("HmacSHA256", "BCFIPS");

            mac.init(keySpec);

            // If we reach here, FIPS failed to block the short key
            System.out.println("RESULT_DANGER_KEY_ALLOWED");
            System.exit(0);

        } catch (Exception e) {
            // This is the expected behavior in a hardened FIPS environment
            System.out.println("RESULT_SUCCESS_FIPS_ENFORCED");
            System.exit(1);
        }
    }
}