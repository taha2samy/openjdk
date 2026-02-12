import java.security.*;
import org.bouncycastle.crypto.CryptoServicesRegistrar;

public class KeystoreRandomTest {

    private static void logSuccess(int testNumber, String category, String justification) {
        System.out.println(String.format(
                "[SUCCESS] TEST %02d - %s: PASSED (%s)",
                testNumber, category, justification));
    }

    private static void logFailure(int testNumber, String category, String justification, Throwable t) {
        System.err.println(String.format(
                "[FAILURE] TEST %02d - %s: FAILED (%s)",
                testNumber, category, justification));
        if (t != null) {
            System.err.println("Root Cause: " + t.getClass().getName() + ": " + t.getMessage());
        }
        System.err.println("Process terminated with exit code 1.");
        System.exit(1);
    }

    public static void main(String[] args) {

        System.out.println("--------------------------------------------------------------------------------");
        System.out.println("KEYSTORE & RANDOM PROVIDER COMPLIANCE VALIDATION SUITE");
        System.out.println("--------------------------------------------------------------------------------");

        // ===== TEST 01: Default KeyStore Type Enforcement =====
        try {
            String ksType = KeyStore.getDefaultType();

            if (!ksType.equalsIgnoreCase("BCFKS")) {
                logFailure(
                        1,
                        "Default KeyStore Type Enforcement",
                        "java.security configuration does not enforce BCFKS as the default keystore type.",
                        null);
            }

            logSuccess(
                    1,
                    "Default KeyStore Type Enforcement",
                    "Default keystore type is BCFKS, aligning with FIPS-compliant keystore requirements.");

        } catch (Throwable t) {
            logFailure(
                    1,
                    "Default KeyStore Type Enforcement",
                    "Unable to determine or validate default keystore configuration.",
                    t);
        }

        // ===== TEST 02: BCFKS Provider Availability =====
        try {
            KeyStore.getInstance("BCFKS", "BCFIPS");

            logSuccess(
                    2,
                    "BCFKS Provider Availability",
                    "BCFKS keystore successfully instantiated via BCFIPS provider, confirming FIPS keystore support.");

        } catch (Throwable t) {
            logFailure(
                    2,
                    "BCFKS Provider Availability",
                    "BCFKS keystore type is unavailable under BCFIPS provider, indicating incomplete FIPS configuration.",
                    t);
        }

        // ===== TEST 03: SecureRandom Provider Enforcement =====
        try {
            SecureRandom random = new SecureRandom();
            String providerName = random.getProvider().getName();

            if (!"BCFIPS".equals(providerName)) {
                logFailure(
                        3,
                        "SecureRandom Provider Enforcement",
                        "Default SecureRandom provider is not BCFIPS, indicating non-compliant randomness source.",
                        null);
            }

            logSuccess(
                    3,
                    "SecureRandom Provider Enforcement",
                    "SecureRandom is backed by BCFIPS provider, ensuring FIPS-approved entropy source.");

        } catch (Throwable t) {
            logFailure(
                    3,
                    "SecureRandom Provider Enforcement",
                    "Failed to validate SecureRandom provider configuration.",
                    t);
        }

        // ===== TEST 04: Approved-Only Mode Status =====
        try {
            boolean approved = CryptoServicesRegistrar.isInApprovedOnlyMode();

            if (!approved) {
                logFailure(
                        4,
                        "Approved-Only Mode Verification",
                        "System is not operating in FIPS Approved-Only mode; non-approved algorithms may be permitted.",
                        null);
            }

            logSuccess(
                    4,
                    "Approved-Only Mode Verification",
                    "CryptoServicesRegistrar confirms Approved-Only mode is active and enforcing restricted cryptographic policies.");

        } catch (Throwable t) {
            logFailure(
                    4,
                    "Approved-Only Mode Verification",
                    "Unable to determine FIPS Approved-Only mode status due to provider configuration issue.",
                    t);
        }

        System.out.println("--------------------------------------------------------------------------------");
        System.out.println(
                "[SUCCESS] OVERALL KEYSTORE & RANDOM COMPLIANCE STATUS: PASSED (All keystore, randomness, and FIPS mode requirements validated successfully.)");
        System.out.println("--------------------------------------------------------------------------------");
    }
}
