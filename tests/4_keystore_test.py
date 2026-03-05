import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Keystore & PKI Tests")
class TestKeystoreBoundary:

    @allure.story("Keystore Restrictions")
    @allure.title("Verify BCFKS Keystore is allowed and functional")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bcfks_load(self, docker_runner):
        code, stdout, stderr = docker_runner("keystore/TestBcfksLoad.java", "TestBcfksLoad")
        assert code == 0

    @allure.story("Keystore Restrictions")
    @allure.title("Verify JKS Keystore is strictly rejected in FIPS Mode")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_jks_rejection(self, docker_runner):
        code, stdout, stderr = docker_runner("keystore/TestJksRejection.java", "TestJksRejection")
        
        # TestJksRejection returns 1 on PASS (Successful Rejection)
        assert code == 1
        output = stdout + stderr
        assert "not found" in output or "KeyStoreException" in output