import java.security.MessageDigest;

public class RejectMd4 {
    public static void main(String[] args) throws Exception {
        // MD4 is totally forbidden
        MessageDigest.getInstance("MD4", "BCFIPS");

        System.out.println("[FAIL] MD4 was allowed!");
        System.exit(0);
    }
}