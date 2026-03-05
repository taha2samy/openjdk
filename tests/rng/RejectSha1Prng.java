import java.security.SecureRandom;

public class RejectSha1Prng {
    public static void main(String[] args) {
        try {
            // SHA1PRNG is not a NIST-approved DRBG
            SecureRandom sr = SecureRandom.getInstance("SHA1PRNG", "BCFIPS");
            sr.nextBytes(new byte[16]);
            System.out.println("RESULT_DANGER_SHA1PRNG_ALLOWED");
            System.exit(0);
        } catch (Exception e) {
            System.out.println("RESULT_SUCCESS_FIPS_ENFORCED");
            System.exit(1);
        }
    }
}