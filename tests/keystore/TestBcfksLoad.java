import java.security.KeyStore;

public class TestBcfksLoad {
    public static void main(String[] args) throws Exception {
        KeyStore ks = KeyStore.getInstance("BCFKS", "BCFIPS");
        ks.load(null, "password".toCharArray());
        System.out.println("BCFKS Loaded Successfully");
        System.exit(0);
    }
}