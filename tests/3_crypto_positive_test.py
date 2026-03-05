import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Positive Cryptography Tests")
class TestCryptoPositive:

    @allure.story("Symmetric Ciphers")
    @allure.title("Verify AES-GCM is allowed by BCFIPS")
    @allure.description("Verifies that AES in Galois/Counter Mode (GCM) is available and operational. AES-GCM is a FIPS-approved authenticated encryption algorithm that provides both confidentiality and data integrity.")

    @allure.severity(allure.severity_level.CRITICAL)
    def test_allow_aes_gcm(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowAesGcm.java", "AllowAesGcm")
        assert code == 0

    @allure.story("Hash Algorithms")
    @allure.title("Verify SHA-256 is allowed by BCFIPS")
    @allure.description("Ensures the SHA-256 hash algorithm is functioning correctly. SHA-256 is a core FIPS-approved primitive used for secure message digesting and integrity verification.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_allow_sha256(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowSha256.java", "AllowSha256")
        assert code == 0


    @allure.story("Asymmetric Key Generation")
    @allure.title("Verify RSA 2048-bit Key Generation is allowed")
    @allure.description("Validates the generation of 2048-bit RSA key pairs. This confirms the provider can create asymmetric keys that meet the minimum security strength requirements defined by FIPS 140-3.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_rsa_2048_gen(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowRsa2048.java", "AllowRsa2048")
        assert code == 0

    @allure.story("Asymmetric Key Generation")
    @allure.title("Verify EC P-256 Key Generation is allowed")
    @allure.description("Confirms successful generation of Elliptic Curve keys using the NIST P-256 curve. This curve is an approved standard for secure and efficient asymmetric cryptography in FIPS environments.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_ec_p256_gen(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowEcP256.java", "AllowEcP256")
        assert code == 0

    @allure.story("Message Authentication Code")
    @allure.title("Verify HMAC-SHA256 is allowed")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_hmac_sha256(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowHmacSha256.java", "AllowHmacSha256")
        assert code == 0

    @allure.story("Key Derivation")
    @allure.title("Verify PBKDF2WithHmacSHA256 is allowed")
    @allure.description("Ensures that PBKDF2 (Password-Based Key Derivation Function 2) is available. It verifies that secure cryptographic keys can be derived from passwords using FIPS-approved iteration and hashing methods.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_pbkdf2(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowPbkdf2.java", "AllowPbkdf2")
        assert code == 0

    @allure.story("Key Agreement")
    @allure.title("Verify ECDH Key Agreement using P-256")
    @allure.description("Validates the Elliptic Curve Diffie-Hellman (ECDH) key agreement protocol. This confirms that the environment can securely establish shared secrets using approved elliptic curve primitives.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_ecdh_key_agreement(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/TestECDH.java", "TestECDH")
        assert code == 0
        assert "RESULT_SUCCESS_ECDH_MATCH" in stdout

    @allure.story("Symmetric Ciphers")
    @allure.title("Verify AES-CBC with PKCS7 Padding")
    @allure.description("Verifies that AES in Cipher Block Chaining (CBC) mode is available. CBC remains a FIPS-approved encryption mode for various legacy and standard interoperability requirements.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_allow_aes_cbc(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowAesCbc.java", "AllowAesCbc")
        assert code == 0
        assert "RESULT_SUCCESS_AES_CBC" in stdout