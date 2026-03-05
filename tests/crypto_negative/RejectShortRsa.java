import java.security.KeyPairGenerator;

public class RejectShortRsa {
    public static void main(String[] args) throws Exception {
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA", "BCFIPS");
        kpg.initialize(1024);
        kpg.generateKeyPair();
        System.exit(0);
    }
}