import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Core FIPS Execution Environment")
class TestCoreFipsEnvironment:

    @allure.story("Approved Mode Enforcement")
    @allure.title("Verify JVM starts strictly in FIPS Approved Mode")
    @allure.description("Ensures the JVM is operating in a strict FIPS-approved state by verifying the 'org.bouncycastle.fips.approved_only' system property. This enforcement guarantees that any attempt to use non-FIPS compliant algorithms will be rejected at runtime.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_approved_mode(self, docker_runner):
        """
        Executes CheckApprovedMode.java to verify that the JVM property 
        'org.bouncycastle.fips.approved_only' is set to true.
        """
        code, stdout, stderr = docker_runner("core/CheckApprovedMode.java", "CheckApprovedMode")
        
        # Test should exit with 0 (Success)
        assert code == 0, f"Approved Mode check failed!\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        assert "[PASS]" in stdout, "Expected [PASS] flag in output."

    @allure.story("Security Providers Priority")
    @allure.title("Verify BouncyCastle FIPS is the primary security provider")
    @allure.description("Checks the security provider chain to confirm that 'BCFIPS' is positioned at the highest priority. This configuration is critical to ensure the JVM uses the FIPS-validated cryptographic module for all operations and prevents accidental fallback to standard, non-certified providers.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_provider_priority(self, docker_runner):
        """
        Executes CheckProviderPriority.java to verify that BCFIPS is at position 1
        and BCJSSE is at position 2 in the JVM Security Providers list.
        """
        code, stdout, stderr = docker_runner("core/CheckProviderPriority.java", "CheckProviderPriority")
        
        # Test should exit with 0 (Success)
        assert code == 0, f"Provider priority check failed!\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        assert "[PASS] Primary Provider is BCFIPS" in stdout, "BCFIPS is not the primary provider."