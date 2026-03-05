import java.security.KeyPairGenerator;

public class AllowRsa2048 {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA", "BCFIPS");
        kpg.initialize(2048);
        kpg.generateKeyPair();
        System.out.println("[PASS] RSA 2048 Generated Successfully");
        System.exit(0);
    }
}