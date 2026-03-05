import java.security.MessageDigest;

public class AllowSha256 {
    public static void main(String[] args) throws Exception {
        MessageDigest md = MessageDigest.getInstance("SHA-256", "BCFIPS");
        md.update("FIPS-140-3-TEST".getBytes());
        byte[] digest = md.digest();

        System.out.println("SHA-256 SUCCESS");
        System.exit(0);
    }
}