import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchProviderException;

public class TestJksRejection {
    public static void main(String[] args) {
        try {
            KeyStore.getInstance("JKS", "BCFIPS");
            System.out.println("[FAIL] Vulnerability! BCFIPS allowed JKS instantiation.");
            System.exit(0);
        } catch (KeyStoreException | NoSuchProviderException e) {
            System.out.println("[PASS] BCFIPS correctly rejected JKS request.");
            System.err.println("Exception: " + e.getMessage());
            System.exit(1);
        } catch (Exception e) {
            System.out.println("[PASS] Request failed as expected.");
            System.err.println("Exception: " + e.getMessage());
            System.exit(1);
        }
    }
}