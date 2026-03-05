import java.security.MessageDigest;

public class RejectMd5 {
    public static void main(String[] args) throws Exception {
        MessageDigest.getInstance("MD5", "BCFIPS");
        System.exit(0);
    }
}