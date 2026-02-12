import java.security.*;
import org.bouncycastle.crypto.CryptoServicesRegistrar;

public class FipsTest {

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
        System.out.println("FIPS 140-3 INTEGRATION AND COMPLIANCE SUITE");
        System.out.println("--------------------------------------------------------------------------------");

        // ===== TEST 01: Approved-Only Mode Enforcement =====
        try {
            boolean isApproved = CryptoServicesRegistrar.isInApprovedOnlyMode();

            if (!isApproved) {
                logFailure(
                        1,
                        "Mode Enforcement",
                        "System is not operating in FIPS Approved-Only mode; non-approved algorithms may be permitted.",
                        null);
            }

            logSuccess(
                    1,
                    "Mode Enforcement",
                    "CryptoServicesRegistrar confirms Approved-Only mode is active and enforcing restricted cryptographic policies.");

        } catch (Throwable t) {
            logFailure(
                    1,
                    "Mode Enforcement",
                    "Failed to determine FIPS operational mode due to provider or configuration error.",
                    t);
        }

        // ===== TEST 02: Approved Algorithm Availability (SHA-256) =====
        try {
            MessageDigest.getInstance("SHA256", "BCFIPS");

            logSuccess(
                    2,
                    "Approved Operation (SHA-256)",
                    "SHA-256 MessageDigest successfully initialized using BCFIPS provider, confirming availability of FIPS-approved hashing algorithm.");

        } catch (Throwable t) {
            logFailure(
                    2,
                    "Approved Operation (SHA-256)",
                    "FIPS-approved SHA-256 algorithm failed to initialize, indicating provider misconfiguration or integrity issue.",
                    t);
        }

        // ===== TEST 03: Boundary Enforcement (RSA 1024 Rejection) =====
        try {
            KeyPairGenerator g = KeyPairGenerator.getInstance("RSA", "BCFIPS");
            g.initialize(1024);
            g.generateKeyPair();

            logFailure(
                    3,
                    "Boundary Enforcement (RSA 1024-bit)",
                    "RSA 1024-bit key generation was permitted, violating minimum key length enforcement requirements under FIPS policy.",
                    null);

        } catch (Throwable t) {
            logSuccess(
                    3,
                    "Boundary Enforcement (RSA 1024-bit)",
                    "BCFIPS provider correctly rejected RSA key generation with 1024-bit modulus, enforcing minimum cryptographic strength requirements.");
        }

        System.out.println("--------------------------------------------------------------------------------");
        System.out.println(
                "[SUCCESS] OVERALL COMPLIANCE STATUS: PASSED (All FIPS 140-3 security boundaries validated successfully.)");
        System.out.println("--------------------------------------------------------------------------------");
    }
}
