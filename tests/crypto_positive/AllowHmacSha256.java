import javax.crypto.KeyGenerator;
import javax.crypto.Mac;
import javax.crypto.SecretKey;

public class AllowHmacSha256 {
    public static void main(String[] args) throws Exception {
        KeyGenerator kg = KeyGenerator.getInstance("HmacSHA256", "BCFIPS");
        SecretKey key = kg.generateKey();

        Mac mac = Mac.getInstance("HmacSHA256", "BCFIPS");
        mac.init(key);
        byte[] result = mac.doFinal("FIPS-TEST-DATA".getBytes());

        System.out.println("[PASS] HMAC-SHA256 Computed Successfully");
        System.exit(0);
    }
}