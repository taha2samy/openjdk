import javax.crypto.Cipher;

public class RejectDes {
    public static void main(String[] args) throws Exception {
        Cipher.getInstance("DES/ECB/PKCS5Padding", "BCFIPS");
        System.exit(0);
    }
}