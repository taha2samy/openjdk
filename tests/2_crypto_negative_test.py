import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Negative Cryptography Tests")
class TestCryptoNegative:

    @allure.story("Hash Algorithms Restrictions")
    @allure.title("Verify MD5 is strictly rejected")
    @allure.description("Ensures that BCFIPS refuses to instantiate MD5, as it is a non-approved algorithm in FIPS 140-3.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_md5(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectMd5.java", "RejectMd5")
        assert code != 0
        assert "NoSuchAlgorithmException" in stdout + stderr

    @allure.story("Symmetric Ciphers Restrictions")
    @allure.title("Verify DES is strictly rejected")
    @allure.description("Validates that legacy DES encryption is inaccessible through the BCFIPS provider.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_des(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectDes.java", "RejectDes")
        assert code != 0
        assert "NoSuchAlgorithmException" in stdout + stderr

    @allure.story("Asymmetric Key Size Restrictions")
    @allure.title("Verify 1024-bit RSA is rejected")
    @allure.description("Checks that RSA key generation with sizes below 2048 bits is blocked by the FIPS boundary.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_short_rsa(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectShortRsa.java", "RejectShortRsa")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["FipsUnapprovedOperationError", "unapproved factory", "NoSuchAlgorithmException"])

    @allure.story("Signature Algorithm Restrictions")
    @allure.title("Verify SHA-1 Signature Generation is rejected")
    @allure.description("Verifies that SHA-1 is prohibited for generating new digital signatures in approved mode.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_sha1_signing(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectSha1Sign.java", "RejectSha1Sign")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["FipsUnapprovedOperationError", "NoSuchAlgorithmException", "Unapproved"])

    @allure.story("Legacy Key Generation Restrictions")
    @allure.title("Verify 1024-bit DSA Key Generation is rejected")
    @allure.description("Ensures that the BCFIPS provider blocks the creation of legacy 1024-bit DSA keys.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_reject_dsa_1024(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectDsa1024Gen.java", "RejectDsa1024Gen")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["FipsUnapprovedOperationError", "InvalidParameterException", "NoSuchAlgorithmException"])

    @allure.story("RSA Encryption Restrictions")
    @allure.title("Verify RSA PKCS#1 v1.5 Encryption is rejected")
    @allure.description("Confirms that RSA encryption using PKCS#1 v1.5 padding is disabled, as FIPS only allows it for Key Wrapping.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_rsa_pkcs1_encryption(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectRsaPkcs1.java", "RejectRsaPkcs1")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["InvalidParameterException", "WRAP_MODE and UNWRAP_MODE only", "FipsUnapprovedOperationError"])

    @allure.story("PBKDF2 Salt Length Restrictions")
    @allure.title("Verify PBKDF2 with short salt (<128 bits) is rejected")
    @allure.description("Ensures compliance with SP 800-132 by requiring a minimum salt length of 128 bits for PBKDF2.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_reject_short_salt_pbkdf2(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectShortSaltPbkdf2.java", "RejectShortSaltPbkdf2")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["InvalidAlgorithmParameterException", "FipsUnapprovedOperationError", "salt must be at least"])

    @allure.story("Hash Algorithms Restrictions")
    @allure.title("Verify MD4 is strictly rejected")
    @allure.description("Validates that MD4 is completely unavailable in the FIPS-validated module.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_md4(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectMd4.java", "RejectMd4")
        assert code != 0
        assert "NoSuchAlgorithmException" in stdout + stderr

    @allure.story("Elliptic Curve Restrictions")
    @allure.title("Verify Non-NIST Curve (secp160r1) is rejected")
    @allure.description("Ensures that only NIST-approved curves are allowed for Elliptic Curve Cryptography.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_non_nist_curve(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectNonNistCurve.java", "RejectNonNistCurve")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["FipsUnapprovedOperationError", "NoSuchAlgorithmException", "InvalidAlgorithmParameterException"])

    @allure.story("MAC Key Length Restrictions")
    @allure.title("Verify Short HMAC Key is rejected")
    @allure.description("Ensures that HMAC keys shorter than the FIPS-required 112 bits are strictly rejected.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_short_hmac_key(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectShortHmacKey.java", "RejectShortHmacKey")
        # Logic Fix: Check for successful FIPS rejection via explicit token and exit code
        assert code == 1, "Security Failure: Short HMAC key was NOT rejected!"
        assert "RESULT_SUCCESS_FIPS_ENFORCED" in stdout

    @allure.story("Symmetric Encryption Restrictions")
    @allure.title("Verify Triple-DES Encryption is rejected")
    @allure.description("Validates that Triple-DES encryption is disabled in strict mode per FIPS 140-3 guidance.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_triple_des_encryption(self, docker_runner):
        code, stdout, stderr = docker_runner("crypto_negative/RejectTripleDes.java", "RejectTripleDes")
        assert code != 0
        assert any(msg in stdout + stderr for msg in ["FipsUnapprovedOperationError", "NoSuchAlgorithmException"])