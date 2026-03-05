import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import java.security.SecureRandom;

public class AllowPbkdf2 {
    public static void main(String[] args) throws Exception {
        // FIPS requires Salt >= 128 bits (16 bytes) and Password >= 112 bits (14 chars)
        char[] password = "StrongFipsPassword123!".toCharArray();
        byte[] salt = new byte[16];
        new SecureRandom().nextBytes(salt);

        PBEKeySpec spec = new PBEKeySpec(password, salt, 10000, 256);
        SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256", "BCFIPS");
        skf.generateSecret(spec);

        System.out.println("[PASS] PBKDF2 Derived Key Successfully");
        System.exit(0);
    }
}