import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Random Number Generator Tests")
class TestRNGSecurity:

    @allure.story("Approved RNG Algorithms")
    @allure.title("Verify SecureRandom uses FIPS-Approved DRBG")
    @allure.description("Confirms that the default SecureRandom implementation utilizes the Bouncy Castle FIPS-approved DRBG (Deterministic Random Bit Generator). This ensures all entropy and random value generation within the JVM meets the strict NIST SP 800-90A security requirements.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_approved_drbg(self, docker_runner):
        code, stdout, stderr = docker_runner("rng/CheckSecureRandom.java", "CheckSecureRandom")
        assert code == 0
        assert "Algorithm: DEFAULT" in stdout
        assert "Provider: BCFIPS" in stdout

    @allure.story("Non-Approved RNG Rejection")
    @allure.title("Verify SHA1PRNG is rejected by BCFIPS")
    @allure.description("Ensures that the legacy SHA1PRNG algorithm is strictly prohibited and inaccessible through the BCFIPS provider. FIPS 140-3 standards mandate the use of stronger, approved DRBG mechanisms and forbid the use of non-compliant RNG algorithms.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_sha1prng(self, docker_runner):
        code, stdout, stderr = docker_runner("rng/RejectSha1Prng.java", "RejectSha1Prng")
        assert code == 1
        assert "RESULT_SUCCESS_FIPS_ENFORCED" in stdout