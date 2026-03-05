import javax.crypto.KeyAgreement;
import java.security.*;
import java.security.spec.ECGenParameterSpec;

public class TestECDH {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("EC", "BCFIPS");
        kpg.initialize(new ECGenParameterSpec("secp256r1"));

        KeyPair aliceKP = kpg.generateKeyPair();
        KeyPair bobKP = kpg.generateKeyPair();

        KeyAgreement aliceAgree = KeyAgreement.getInstance("ECDH", "BCFIPS");
        aliceAgree.init(aliceKP.getPrivate());
        aliceAgree.doPhase(bobKP.getPublic(), true);
        byte[] aliceSecret = aliceAgree.generateSecret();

        KeyAgreement bobAgree = KeyAgreement.getInstance("ECDH", "BCFIPS");
        bobAgree.init(bobKP.getPrivate());
        bobAgree.doPhase(aliceKP.getPublic(), true);
        byte[] bobSecret = bobAgree.generateSecret();

        if (java.util.Arrays.equals(aliceSecret, bobSecret)) {
            System.out.println("RESULT_SUCCESS_ECDH_MATCH");
            System.exit(0);
        } else {
            System.exit(1);
        }
    }
}