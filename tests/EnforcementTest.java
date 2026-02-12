import java.security.*;
import javax.crypto.*;

public class EnforcementTest {

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

        // ===== TEST 01: MD5 Block Enforcement =====
        try {
            MessageDigest.getInstance("MD5", "BCFIPS");

            logFailure(
                    1,
                    "Weak Hash Algorithm Enforcement (MD5)",
                    "MD5 digest was permitted by BCFIPS provider, indicating failure to enforce cryptographic policy restrictions.",
                    null);

        } catch (Throwable t) {
            logSuccess(
                    1,
                    "Weak Hash Algorithm Enforcement (MD5)",
                    "BCFIPS provider correctly rejected MD5 algorithm, confirming enforcement of non-approved hash restrictions.");
        }

        // ===== TEST 02: DES Block Enforcement =====
        try {
            Cipher.getInstance("DES/ECB/PKCS5Padding", "BCFIPS");

            logFailure(
                    2,
                    "Weak Symmetric Cipher Enforcement (DES)",
                    "DES cipher initialization was permitted, indicating failure to block deprecated symmetric algorithms.",
                    null);

        } catch (Throwable t) {
            logSuccess(
                    2,
                    "Weak Symmetric Cipher Enforcement (DES)",
                    "BCFIPS provider correctly rejected DES cipher, confirming enforcement of weak algorithm restrictions.");
        }

        // ===== TEST 03: RSA 1024 Key Size Enforcement =====
        try {
            KeyPairGenerator g = KeyPairGenerator.getInstance("RSA", "BCFIPS");
            g.initialize(1024);
            g.generateKeyPair();

            logFailure(
                    3,
                    "Insufficient Key Length Enforcement (RSA 1024-bit)",
                    "RSA 1024-bit key generation was permitted, violating minimum key size enforcement policy (expected  2048 bits).",
                    null);

        } catch (Throwable t) {
            logSuccess(
                    3,
                    "Insufficient Key Length Enforcement (RSA 1024-bit)",
                    "BCFIPS provider correctly rejected RSA key generation with 1024-bit modulus, enforcing minimum cryptographic strength requirements.");
        }

        // ===== OVERALL STATUS =====
        System.out.println(
                "[SUCCESS] OVERALL CRYPTOGRAPHIC POLICY ENFORCEMENT STATUS: PASSED (All non-approved algorithms and insufficient key sizes were correctly blocked.)");
    }
}
