import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Network & TLS Tests")
class TestNetworkSecurity:

    @allure.story("TLS Protocol Support")
    @allure.title("Verify TLS 1.3 Handshake using BCFIPS Provider")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tls13_connection(self, docker_runner):
        code, stdout, stderr = docker_runner("network/Tls13Connection.java", "Tls13Connection")
        assert code == 0

    @allure.story("TLS Protocol Restrictions")
    @allure.title("Verify TLS 1.0/1.1 are strictly rejected in FIPS Mode")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_weak_tls(self, docker_runner):
        code, stdout, stderr = docker_runner("network/RejectWeakTls.java", "RejectWeakTls")
        assert code == 1
        output = stdout + stderr
        assert "SSLHandshakeException" in output or \
               "protocol not enabled" in output or \
               "No appropriate protocol" in output or \
               "No usable protocols enabled" in output


    @allure.story("TLS Cipher Suite Restrictions")
    @allure.title("Verify Anonymous Cipher Suites (DH_anon) are rejected")
    @allure.description("Ensures that anonymous Diffie-Hellman cipher suites are disabled, as they provide no authentication and are forbidden in FIPS mode.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_anonymous_cipher(self, docker_runner):
        code, stdout, stderr = docker_runner("network/RejectAnonCipher.java", "RejectAnonCipher")
        assert code == 1
        assert "RESULT_SUCCESS_FIPS_ENFORCED" in stdout

    @allure.story("JSSE Provider Enforcement")
    @allure.title("Verify BCJSSE is the mandated SSLContext provider")
    @allure.description("Validates that the default SSLContext is using the Bouncy Castle JSSE provider, ensuring all network operations are FIPS-compliant.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_default_ssl_context_provider(self, docker_runner):
        code, stdout, stderr = docker_runner("network/CheckSslProvider.java", "CheckSslProvider")
        assert code == 0
        assert "RESULT_SUCCESS_PROVIDER_VERIFIED" in stdout


    @allure.story("TLS Cipher Suite Restrictions")
    @allure.title("Verify RC4 Cipher Suites are strictly rejected")
    @allure.description("Ensures that RC4-based cipher suites are disabled, as they are cryptographically broken and forbidden in FIPS mode.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_rc4_cipher(self, docker_runner):
        code, stdout, stderr = docker_runner("network/RejectRC4Cipher.java", "RejectRC4Cipher")
        assert code == 1
        assert "RESULT_SUCCESS_FIPS_ENFORCED" in stdout

    @allure.story("TLS Cipher Suite Restrictions")
    @allure.title("Verify NULL Encryption Cipher Suites are rejected")
    @allure.description("Validates that cipher suites with no encryption (NULL) are strictly prohibited by the FIPS boundary.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_reject_null_cipher(self, docker_runner):
        code, stdout, stderr = docker_runner("network/RejectNullCipher.java", "RejectNullCipher")
        assert code == 1
        assert "RESULT_SUCCESS_FIPS_ENFORCED" in stdout

    @allure.story("JSSE TrustStore Enforcement")
    @allure.title("Verify Default KeyStore type is BCFKS for TLS")
    @allure.description("Confirms that the JVM is locked to BCFKS as the default KeyStore type, preventing fallback to insecure JKS/PKCS12 during TLS setup.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_enforce_bcfks_default_keystore(self, docker_runner):
        code, stdout, stderr = docker_runner("network/CheckDefaultKeystoreType.java", "CheckDefaultKeystoreType")
        assert code == 0
        assert "RESULT_SUCCESS_BCFKS_ENFORCED" in stdout