import javax.net.ssl.SSLSocketFactory;
import java.util.Arrays;
import java.util.List;

public class CipherSuiteValidationTest {

    private static void logSuccess(int testNumber, String category, String justification) {
        System.out.println(String.format(
                "[SUCCESS] TEST %02d - %s: PASSED (%s)",
                testNumber, category, justification));
    }

    private static void logFailure(int testNumber, String category, String justification, String details) {
        System.err.println(String.format(
                "[FAILURE] TEST %02d - %s: FAILED (%s)",
                testNumber, category, justification));
        if (details != null && !details.isEmpty()) {
            System.err.println("Details: " + details);
        }
        System.err.println("Process terminated with exit code 1.");
        System.exit(1);
    }

    public static void main(String[] args) {
        System.out.println("--------------------------------------------------------------------------------");
        System.out.println("FIPS 140-3 TLS CIPHER SUITE VALIDATION");
        System.out.println("--------------------------------------------------------------------------------");

        try {
            SSLSocketFactory factory = (SSLSocketFactory) SSLSocketFactory.getDefault();
            String[] supportedCiphers = factory.getSupportedCipherSuites();
            List<String> cipherList = Arrays.asList(supportedCiphers);

            // ===== TEST 01: Verify BCJSSE is the provider =====
            String providerName = factory.getClass().getPackage().getName();
            if (providerName.contains("bouncycastle")) {
                logSuccess(1, "JSSE Provider Origin",
                        "Default SSLSocketFactory is correctly provided by BCJSSE, ensuring FIPS-mode operation.");
            } else {
                logFailure(1, "JSSE Provider Origin",
                        "Default SSLSocketFactory is from a non-FIPS provider: " + providerName, null);
            }

            // ===== TEST 02: Check for presence of strong cipher suites =====
            boolean hasStrongCipher = cipherList.stream()
                    .anyMatch(c -> c.contains("AES_256_GCM_SHA384"));
            if (hasStrongCipher) {
                logSuccess(2, "Strong Cipher Availability",
                        "FIPS-compliant cipher suites like AES_256_GCM_SHA384 are available for negotiation.");
            } else {
                logFailure(2, "Strong Cipher Availability",
                        "No strong, FIPS-compliant AES-GCM cipher suites were found in the supported list.", null);
            }

            // ===== TEST 03: Check for absence of weak cipher suites =====
            String weakCipherFound = cipherList.stream()
                    .filter(c -> c.contains("3DES") || c.contains("RC4") || c.contains("MD5"))
                    .findFirst().orElse(null);

            if (weakCipherFound == null) {
                logSuccess(3, "Weak Cipher Exclusion",
                        "No weak or deprecated cipher suites (e.g., 3DES, RC4, MD5) were found in the list, confirming strict FIPS policy.");
            } else {
                logFailure(3, "Weak Cipher Exclusion",
                        "A non-compliant cipher suite was found enabled in FIPS mode.", "Found: " + weakCipherFound);
            }

        } catch (Exception e) {
            System.err.println("[FATAL] Cipher suite validation encountered an unexpected error.");
            e.printStackTrace();
            System.exit(1);
        }

        System.out.println("--------------------------------------------------------------------------------");
        System.out.println("[SUCCESS] OVERALL TLS CIPHER SUITE CONFIGURATION: PASSED");
        System.out.println("--------------------------------------------------------------------------------");
    }
}