import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

public class RejectTripleDes {
    public static void main(String[] args) throws Exception {
        KeyGenerator kg = KeyGenerator.getInstance("DESede", "BCFIPS");
        kg.init(168);
        SecretKey key = kg.generateKey();
        Cipher cipher = Cipher.getInstance("DESede/CBC/PKCS5Padding", "BCFIPS");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        System.out.println("[FAIL] Triple-DES encryption allowed!");
        System.exit(0);
    }
}