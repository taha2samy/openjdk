import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Positive Cryptography Tests")
class TestCryptoPositive:

    @allure.story("Symmetric Ciphers")
    @allure.title("Verify AES-GCM is allowed by BCFIPS")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_allow_aes_gcm(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowAesGcm.java", "AllowAesGcm")
        assert code == 0

    @allure.story("Hash Algorithms")
    @allure.title("Verify SHA-256 is allowed by BCFIPS")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_allow_sha256(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowSha256.java", "AllowSha256")
        assert code == 0


    @allure.story("Asymmetric Key Generation")
    @allure.title("Verify RSA 2048-bit Key Generation is allowed")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_rsa_2048_gen(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowRsa2048.java", "AllowRsa2048")
        assert code == 0

    @allure.story("Asymmetric Key Generation")
    @allure.title("Verify EC P-256 Key Generation is allowed")
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
    @allure.severity(allure.severity_level.NORMAL)
    def test_pbkdf2(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowPbkdf2.java", "AllowPbkdf2")
        assert code == 0

    @allure.story("Key Agreement")
    @allure.title("Verify ECDH Key Agreement using P-256")
    @allure.description("Validates a full Elliptic Curve Diffie-Hellman (ECDH) key exchange between two parties using the approved BCFIPS provider.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_ecdh_key_agreement(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/TestECDH.java", "TestECDH")
        assert code == 0
        assert "RESULT_SUCCESS_ECDH_MATCH" in stdout

    @allure.story("Symmetric Ciphers")
    @allure.title("Verify AES-CBC with PKCS7 Padding")
    @allure.description("Ensures that standard AES in CBC mode with PKCS7 padding works correctly within the FIPS boundary.")
    def test_allow_aes_cbc(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_positive/AllowAesCbc.java", "AllowAesCbc")
        assert code == 0
        assert "RESULT_SUCCESS_AES_CBC" in stdout