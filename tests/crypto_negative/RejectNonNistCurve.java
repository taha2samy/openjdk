import java.security.KeyPairGenerator;
import java.security.spec.ECGenParameterSpec;

public class RejectNonNistCurve {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC", "BCFIPS");
        kpg.initialize(new ECGenParameterSpec("secp160r1"));
        kpg.generateKeyPair();
        System.out.println("[FAIL] Non-NIST curve allowed!");
        System.exit(0);
    }
}