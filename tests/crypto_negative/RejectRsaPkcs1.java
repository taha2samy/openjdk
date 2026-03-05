import javax.crypto.Cipher;
import java.security.KeyPair;
import java.security.KeyPairGenerator;

public class RejectRsaPkcs1 {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA", "BCFIPS");
        kpg.initialize(2048);
        KeyPair kp = kpg.generateKeyPair();

        // PKCS1 v1.5 padding is typically restricted for encryption in strict FIPS
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding", "BCFIPS");
        cipher.init(Cipher.ENCRYPT_MODE, kp.getPublic());

        System.out.println("[FAIL] RSA PKCS#1 v1.5 encryption allowed!");
        System.exit(0);
    }
}