import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Keystore & PKI Tests")
class TestKeystoreBoundary:

    @allure.story("Keystore Restrictions")
    @allure.title("Verify BCFKS Keystore is allowed and functional")
    @allure.description("Verifies that the Bouncy Castle FIPS KeyStore (BCFKS) is fully supported and operational. BCFKS is the mandated storage format for keys and certificates within a FIPS 140-3 environment to ensure the protection of sensitive security parameters using approved algorithms.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bcfks_load(self, docker_runner):
        code, stdout, stderr = docker_runner("keystore/TestBcfksLoad.java", "TestBcfksLoad")
        assert code == 0

    @allure.story("Keystore Restrictions")
    @allure.title("Verify JKS Keystore is strictly rejected in FIPS Mode")
    @allure.description("Ensures that legacy Java KeyStore (JKS) files are strictly rejected at runtime. Blocking non-compliant keystore formats is a mandatory security control to prevent the accidental use of weak integrity checks and non-approved cryptographic primitives.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_jks_rejection(self, docker_runner):
        code, stdout, stderr = docker_runner("keystore/TestJksRejection.java", "TestJksRejection")
        assert code == 1
        output = stdout + stderr
        assert "not found" in output or "KeyStoreException" in output