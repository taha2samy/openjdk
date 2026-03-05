import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.Signature;

public class RejectSha1Sign {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA", "BCFIPS");
        kpg.initialize(2048);
        KeyPair kp = kpg.generateKeyPair();

        Signature sig = Signature.getInstance("SHA1withRSA", "BCFIPS");

        // Initialization for SIGNING should fail in FIPS mode
        sig.initSign(kp.getPrivate());
        sig.update("Data".getBytes());
        sig.sign();

        System.out.println("[FAIL] SHA1 Signing was allowed!");
        System.exit(0);
    }
}