import java.security.*;
import javax.crypto.*;
import javax.crypto.spec.*;
import org.bouncycastle.crypto.CryptoServicesRegistrar;

public class CryptoOpsTest {

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
        System.out.println("CRYPTOGRAPHIC APPROVED OPERATIONS VALIDATION SUITE (WITH AES-256 TEST)");
        System.out.println("--------------------------------------------------------------------------------");

        // ===== TEST 01: Approved-Only Mode Verification =====
        try {
            boolean approved = CryptoServicesRegistrar.isInApprovedOnlyMode();
            if (!approved) {
                logFailure(1, "Approved-Only Mode Verification",
                        "System is not operating in FIPS Approved-Only mode; approved cryptographic guarantees cannot be enforced.",
                        null);
            }
            logSuccess(1, "Approved-Only Mode Verification",
                    "CryptoServicesRegistrar confirms Approved-Only mode is active and enforcing restricted cryptographic policies.");
        } catch (Throwable t) {
            logFailure(1, "Approved-Only Mode Verification",
                    "Unable to determine FIPS operational mode due to provider or configuration error.", t);
        }

        // ===== TEST 02: AES Encryption (128-bit) =====
        try {
            byte[] keyBytes = new byte[16];
            SecureRandom.getInstance("DEFAULT", "BCFIPS").nextBytes(keyBytes);
            SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding", "BCFIPS");
            cipher.init(Cipher.ENCRYPT_MODE, key);
            cipher.doFinal("FIPS_IS_ACTIVE".getBytes());
            logSuccess(2, "Symmetric Encryption (AES-128 CBC)",
                    "Cipher successfully initialized using BCFIPS provider with 128-bit AES key generated via FIPS-approved SecureRandom.");
        } catch (Throwable t) {
            logFailure(2, "Symmetric Encryption (AES-128 CBC)",
                    "AES encryption failed under BCFIPS provider, indicating improper provider configuration or non-approved operational mode.",
                    t);
        }

        // ===== TEST 03: SHA-256 Digest =====
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA256", "BCFIPS");
            digest.update("test".getBytes());
            digest.digest();
            logSuccess(3, "Cryptographic Hash Function (SHA-256)",
                    "SHA-256 MessageDigest successfully instantiated from BCFIPS provider, confirming availability of FIPS-approved hashing algorithm.");
        } catch (Throwable t) {
            logFailure(3, "Cryptographic Hash Function (SHA-256)",
                    "SHA-256 digest operation failed under BCFIPS provider, indicating provider misconfiguration or missing FIPS enforcement.",
                    t);
        }

        // ===== TEST 04: RSA 2048 Key Generation =====
        try {
            KeyPairGenerator g = KeyPairGenerator.getInstance("RSA", "BCFIPS");
            g.initialize(2048);
            g.generateKeyPair();
            logSuccess(4, "Asymmetric Key Generation (RSA 2048-bit)",
                    "RSA KeyPairGenerator initialized with 2048-bit modulus under BCFIPS provider, satisfying minimum cryptographic strength requirements.");
        } catch (Throwable t) {
            logFailure(4, "Asymmetric Key Generation (RSA 2048-bit)",
                    "RSA 2048-bit key generation failed under BCFIPS provider, indicating improper security policy enforcement or provider misconfiguration.",
                    t);
        }

        // ===== TEST 05: AES Encryption (256-bit) =====
        try {
            byte[] keyBytes256 = new byte[32]; // 256-bit key
            SecureRandom.getInstance("DEFAULT", "BCFIPS").nextBytes(keyBytes256);
            SecretKeySpec key256 = new SecretKeySpec(keyBytes256, "AES");
            Cipher cipher256 = Cipher.getInstance("AES/CBC/PKCS5Padding", "BCFIPS");
            cipher256.init(Cipher.ENCRYPT_MODE, key256);
            cipher256.doFinal("FIPS_256_TEST".getBytes());
            logSuccess(5, "Symmetric Encryption (AES-256 CBC)",
                    "Cipher successfully initialized using BCFIPS provider with 256-bit AES key, confirming support for strong FIPS-approved encryption.");
        } catch (Throwable t) {
            logFailure(5, "Symmetric Encryption (AES-256 CBC)",
                    "AES 256-bit encryption failed under BCFIPS provider, indicating incomplete FIPS-approved key size support.",
                    t);
        }

        System.out.println("--------------------------------------------------------------------------------");
        System.out.println(
                "[SUCCESS] OVERALL CRYPTOGRAPHIC APPROVED OPERATIONS STATUS: PASSED (All approved cryptographic primitives including AES-256 executed successfully under enforced policy.)");
        System.out.println("--------------------------------------------------------------------------------");
    }
}
