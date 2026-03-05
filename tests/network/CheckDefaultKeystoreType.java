import java.security.KeyStore;

public class CheckDefaultKeystoreType {
    public static void main(String[] args) {
        String defaultType = KeyStore.getDefaultType();
        System.out.println("Default Keystore Type: " + defaultType);

        if ("BCFKS".equalsIgnoreCase(defaultType)) {
            System.out.println("RESULT_SUCCESS_BCFKS_ENFORCED");
            System.exit(0);
        } else {
            System.out.println("RESULT_FAIL_INSECURE_DEFAULT: " + defaultType);
            System.exit(1);
        }
    }
}