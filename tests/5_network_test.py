import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Network & TLS Tests")
class TestNetworkSecurity:

    @allure.story("TLS Protocol Support")
    @allure.title("Verify TLS 1.3 Handshake using BCFIPS Provider")
    @allure.description("Validates successful TLS 1.3 handshake using the Bouncy Castle JSSE provider. This confirms that modern, secure protocol standards are operational within the FIPS cryptographic boundary and utilize approved cipher suites.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_tls13_connection(self, docker_runner):
        code, stdout, stderr = docker_runner("network/Tls13Connection.java", "Tls13Connection")
        assert code == 0

    @allure.story("TLS Protocol Restrictions")
    @allure.title("Verify TLS 1.0/1.1 are strictly rejected in FIPS Mode")
    @allure.description("Ensures that legacy protocols such as TLS 1.0 and TLS 1.1 are strictly prohibited. These versions are no longer compliant with FIPS 140-3 standards due to known cryptographic weaknesses and vulnerabilities.")
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
    @allure.description("Ensures that anonymous Diffie-Hellman cipher suites are disabled. These suites fail to provide server authentication and are explicitly forbidden in FIPS mode to prevent man-in-the-middle attacks.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_anonymous_cipher(self, docker_runner):
        code, stdout, stderr = docker_runner("network/RejectAnonCipher.java", "RejectAnonCipher")
        assert code == 1
        assert "RESULT_SUCCESS_FIPS_ENFORCED" in stdout

    @allure.story("JSSE Provider Enforcement")
    @allure.title("Verify BCJSSE is the mandated SSLContext provider")
    @allure.description("Validates that the default SSLContext is using the Bouncy Castle JSSE provider. This configuration ensures that all JVM-wide network operations utilize the FIPS-validated cryptographic module.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_default_ssl_context_provider(self, docker_runner):
        code, stdout, stderr = docker_runner("network/CheckSslProvider.java", "CheckSslProvider")
        assert code == 0
        assert "RESULT_SUCCESS_PROVIDER_VERIFIED" in stdout

    @allure.story("TLS Cipher Suite Restrictions")
    @allure.title("Verify RC4 Cipher Suites are strictly rejected")
    @allure.description("Verifies that RC4-based cipher suites are rejected at the JSSE level. RC4 is a broken stream cipher and is strictly prohibited in FIPS environments to maintain data confidentiality.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_rc4_cipher(self, docker_runner):
        code, stdout, stderr = docker_runner("network/RejectRC4Cipher.java", "RejectRC4Cipher")
        assert code == 1
        assert "RESULT_SUCCESS_FIPS_ENFORCED" in stdout

    @allure.story("TLS Cipher Suite Restrictions")
    @allure.title("Verify NULL Encryption Cipher Suites are rejected")
    @allure.description("Confirms the total rejection of NULL cipher suites. Any attempt to establish a network connection without encryption is a severe security violation and is blocked by the FIPS boundary.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_reject_null_cipher(self, docker_runner):
        code, stdout, stderr = docker_runner("network/RejectNullCipher.java", "RejectNullCipher")
        assert code == 1
        assert "RESULT_SUCCESS_FIPS_ENFORCED" in stdout

    @allure.story("JSSE TrustStore Enforcement")
    @allure.title("Verify Default KeyStore type is BCFKS for TLS")
    @allure.description("Ensures that BCFKS is mandated as the default KeyStore type for JSSE operations. This prevents the accidental use of non-compliant storage formats like JKS or PKCS12 for managing trusted certificates.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_enforce_bcfks_default_keystore(self, docker_runner):
        code, stdout, stderr = docker_runner("network/CheckDefaultKeystoreType.java", "CheckDefaultKeystoreType")
        assert code == 0
        assert "RESULT_SUCCESS_BCFKS_ENFORCED" in stdout