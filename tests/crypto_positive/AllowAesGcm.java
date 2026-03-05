import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

public class AllowAesGcm {
    public static void main(String[] args) throws Exception {
        KeyGenerator keyGen = KeyGenerator.getInstance("AES", "BCFIPS");
        keyGen.init(256);
        SecretKey aesKey = keyGen.generateKey();

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding", "BCFIPS");
        cipher.init(Cipher.ENCRYPT_MODE, aesKey);

        byte[] cipherText = cipher.doFinal("FIPS-140-3-TEST".getBytes());
        System.out.println("AES-GCM SUCCESS");
        System.exit(0);
    }
}