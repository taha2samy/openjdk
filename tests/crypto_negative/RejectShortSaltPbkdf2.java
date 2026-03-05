import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public class RejectShortSaltPbkdf2 {
    public static void main(String[] args) throws Exception {
        char[] password = "FipsPassword123!".toCharArray();
        // Salt only 4 bytes (32 bits) - Should be rejected (FIPS requires >= 128 bits)
        byte[] shortSalt = new byte[4];

        PBEKeySpec spec = new PBEKeySpec(password, shortSalt, 1000, 256);
        SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256", "BCFIPS");

        skf.generateSecret(spec);

        System.out.println("[FAIL] PBKDF2 with short salt was allowed!");
        System.exit(0);
    }
}