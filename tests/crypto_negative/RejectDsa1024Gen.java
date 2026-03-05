import java.security.KeyPairGenerator;

public class RejectDsa1024Gen {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("DSA", "BCFIPS");

        // FIPS 140-3 allows 1024 for verification ONLY, but rejects generation
        kpg.initialize(1024);
        kpg.generateKeyPair();

        System.out.println("[FAIL] DSA 1024-bit Generation was allowed!");
        System.exit(0);
    }
}