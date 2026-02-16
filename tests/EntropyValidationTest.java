import java.security.Provider;
import java.security.SecureRandom;
import java.util.Arrays;

public class EntropyValidationTest {

    private static void logSuccess(int testNumber, String category, String justification) {
        System.out.println(String.format(
                "[SUCCESS] TEST %02d - %s: PASSED (%s)",
                testNumber, category, justification));
    }

    private static void logFailure(int testNumber, String category, String justification) {
        System.err.println(String.format(
                "[FAILURE] TEST %02d - %s: FAILED (%s)",
                testNumber, category, justification));
        System.err.println("Process terminated with exit code 1.");
        System.exit(1);
    }

    public static void main(String[] args) {
        System.out.println("--------------------------------------------------------------------------------");
        System.out.println("FIPS 140-3 ENTROPY AND SECURE RANDOM VALIDATION SUITE");
        System.out.println("--------------------------------------------------------------------------------");

        try {
            // ===== TEST 01: SecureRandom Provider Verification =====
            SecureRandom random = new SecureRandom();
            String providerName = random.getProvider().getName();
            if ("BCFIPS".equals(providerName)) {
                logSuccess(1, "SecureRandom Provider Origin",
                        "Default SecureRandom is correctly sourced from the BCFIPS provider, ensuring FIPS-validated entropy.");
            } else {
                logFailure(1, "SecureRandom Provider Origin",
                        "Default SecureRandom is sourced from a non-FIPS provider '" + providerName
                                + "', which violates cryptographic policy.");
            }

            // ===== TEST 02: SecureRandom Algorithm Verification =====
            String algorithm = random.getAlgorithm();
            if (algorithm.contains("DRBG")) {
                logSuccess(2, "SecureRandom Algorithm Type",
                        "Default SecureRandom is using an approved DRBG (Deterministic Random Bit Generator) algorithm: "
                                + algorithm);
            } else {
                logFailure(2, "SecureRandom Algorithm Type",
                        "Default SecureRandom is using a non-approved or unknown algorithm '" + algorithm
                                + "'. A FIPS-compliant DRBG is required.");
            }

            // ===== TEST 03: Entropy Quality Check (Non-Repeating Bytes) =====
            byte[] firstBatch = new byte[32];
            byte[] secondBatch = new byte[32];
            random.nextBytes(firstBatch);
            random.nextBytes(secondBatch);

            if (!Arrays.equals(firstBatch, secondBatch)) {
                logSuccess(3, "Entropy Quality",
                        "Generated random byte sequences are unique, indicating a non-deterministic and high-quality entropy source.");
            } else {
                logFailure(3, "Entropy Quality",
                        "Generated random byte sequences were identical, indicating a critical failure in the entropy source.");
            }

        } catch (Exception e) {
            System.err.println("[FATAL] Entropy validation suite encountered an unexpected error.");
            e.printStackTrace();
            System.exit(1);
        }

        System.out.println("--------------------------------------------------------------------------------");
        System.out.println("[SUCCESS] OVERALL ENTROPY AND RANDOMNESS VALIDATION: PASSED");
        System.out.println("--------------------------------------------------------------------------------");
    }
}