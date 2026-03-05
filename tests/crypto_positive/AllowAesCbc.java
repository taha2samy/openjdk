import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;

public class AllowAesCbc {
    public static void main(String[] args) throws Exception {
        KeyGenerator kg = KeyGenerator.getInstance("AES", "BCFIPS");
        kg.init(256);
        SecretKey key = kg.generateKey();
        byte[] iv = new byte[16];
        new java.security.SecureRandom().nextBytes(iv);

        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS7Padding", "BCFIPS");
        cipher.init(Cipher.ENCRYPT_MODE, key, new IvParameterSpec(iv));
        byte[] ct = cipher.doFinal("FIPS_STRICT_TEST".getBytes());

        cipher.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(iv));
        byte[] pt = cipher.doFinal(ct);

        if (new String(pt).equals("FIPS_STRICT_TEST")) {
            System.out.println("RESULT_SUCCESS_AES_CBC");
            System.exit(0);
        } else {
            System.exit(1);
        }
    }
}