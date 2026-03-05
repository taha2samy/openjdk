import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Negative Cryptography Tests")
class TestCryptoNegative:

    @allure.story("Hash Algorithms Restrictions")
    @allure.title("Verify MD5 is strictly rejected")
    @allure.description("Verifies that the MD5 message digest algorithm is strictly prohibited. As a non-approved hash function in FIPS 140-3, any attempt to instantiate MD5 must result in a security exception.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_md5(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectMd5.java", "RejectMd5")
        assert code != 0
        assert "NoSuchAlgorithmException" in stdout + stderr

    @allure.story("Symmetric Ciphers Restrictions")
    @allure.title("Verify DES is strictly rejected")
    @allure.description("Ensures that the legacy DES (Data Encryption Standard) algorithm is rejected. FIPS mode prohibits weak block ciphers with 56-bit keys to prevent brute-force vulnerabilities.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_des(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectDes.java", "RejectDes")
        assert code != 0
        assert "NoSuchAlgorithmException" in stdout + stderr

    @allure.story("Asymmetric Key Size Restrictions")
    @allure.title("Verify 1024-bit RSA is rejected")
    @allure.description("Validates the enforcement of minimum key lengths for RSA. FIPS 140-3 requires a minimum of 2048 bits; attempts to use 1024-bit or smaller keys must be blocked.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_short_rsa(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectShortRsa.java", "RejectShortRsa")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["FipsUnapprovedOperationError", "unapproved factory", "NoSuchAlgorithmException"])

    @allure.story("Signature Algorithm Restrictions")
    @allure.title("Verify SHA-1 Signature Generation is rejected")
    @allure.description("Confirms that SHA-1 based digital signatures are rejected for creation. FIPS policy prohibits SHA-1 for digital signature generation due to collision risks.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_sha1_signing(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectSha1Sign.java", "RejectSha1Sign")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["FipsUnapprovedOperationError", "NoSuchAlgorithmException", "Unapproved"])

    @allure.story("Legacy Key Generation Restrictions")
    @allure.title("Verify 1024-bit DSA Key Generation is rejected")
    @allure.description("Ensures that 1024-bit DSA keys are rejected. FIPS compliance mandates higher security strengths, effectively blocking legacy DSA parameters that do not meet the 112-bit security threshold.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_reject_dsa_1024(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectDsa1024Gen.java", "RejectDsa1024Gen")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["FipsUnapprovedOperationError", "InvalidParameterException", "NoSuchAlgorithmException"])

    @allure.story("RSA Encryption Restrictions")
    @allure.title("Verify RSA PKCS#1 v1.5 Encryption is rejected")
    @allure.description("Verifies rejection of RSA PKCS#1 v1.5 padding for encryption. Under strict FIPS enforcement, modern and secure padding schemes like OAEP are required, and legacy schemes are disabled.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_rsa_pkcs1_encryption(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectRsaPkcs1.java", "RejectRsaPkcs1")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["InvalidParameterException", "WRAP_MODE and UNWRAP_MODE only", "FipsUnapprovedOperationError"])

    @allure.story("PBKDF2 Salt Length Restrictions")
    @allure.title("Verify PBKDF2 with short salt (<128 bits) is rejected")
    @allure.description("Validates that PBKDF2 operations require a minimum salt length. FIPS standards enforce sufficient entropy in key derivation to protect against pre-computed dictionary attacks.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_reject_short_salt_pbkdf2(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectShortSaltPbkdf2.java", "RejectShortSaltPbkdf2")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["InvalidAlgorithmParameterException", "FipsUnapprovedOperationError", "salt must be at least"])

    @allure.story("Hash Algorithms Restrictions")
    @allure.title("Verify MD4 is strictly rejected")
    @allure.description("Confirms that the MD4 hash algorithm is completely disabled. MD4 is cryptographically broken and strictly forbidden in any FIPS-validated environment.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_md4(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectMd4.java", "RejectMd4")
        assert code != 0
        assert "NoSuchAlgorithmException" in stdout + stderr

    @allure.story("Elliptic Curve Restrictions")
    @allure.title("Verify Non-NIST Curve (secp160r1) is rejected")
    @allure.description("Ensures that only NIST-approved Elliptic Curves (e.g., P-256, P-384) are allowed. Attempts to use non-standard or custom curves must be rejected by the provider.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_non_nist_curve(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectNonNistCurve.java", "RejectNonNistCurve")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["FipsUnapprovedOperationError", "NoSuchAlgorithmException", "InvalidAlgorithmParameterException"])

    @allure.story("MAC Key Length Restrictions")
    @allure.title("Verify Short HMAC Key is rejected")
    @allure.description("Checks that HMAC operations reject keys that are shorter than the minimum required length. This ensures the integrity of the message authentication code meets FIPS security strength requirements.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_short_hmac_key(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectShortHmacKey.java", "RejectShortHmacKey")
        # Logic Fix: Check for successful FIPS rejection via explicit token and exit code
        assert code == 1, "Security Failure: Short HMAC key was NOT rejected!"
        assert "RESULT_SUCCESS_FIPS_ENFORCED" in stdout

    @allure.story("Symmetric Encryption Restrictions")
    @allure.title("Verify Triple-DES Encryption is rejected")
    @allure.description("Verifies that Triple-DES (TDEA) encryption is prohibited. Following recent NIST guidance, 3DES is no longer an approved encryption algorithm due to its vulnerability to Sweet32 attacks.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_triple_des_encryption(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectTripleDes.java", "RejectTripleDes")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["FipsUnapprovedOperationError", "NoSuchAlgorithmException"])