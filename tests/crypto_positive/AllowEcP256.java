import java.security.KeyPairGenerator;
import java.security.spec.ECGenParameterSpec;

public class AllowEcP256 {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC", "BCFIPS");
        kpg.initialize(new ECGenParameterSpec("secp256r1")); // NIST P-256
        kpg.generateKeyPair();
        System.out.println("[PASS] EC P-256 Generated Successfully");
        System.exit(0);
    }
}