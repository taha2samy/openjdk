import pytest
import allure

@allure.epic("FIPS 140-3 Boundary Validation")
@allure.feature("Random Number Generator Tests")
class TestRNGSecurity:

    @allure.story("Approved RNG Algorithms")
    @allure.title("Verify SecureRandom uses FIPS-Approved DRBG")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_approved_drbg(self, docker_runner):
        code, stdout, stderr = docker_runner("rng/CheckSecureRandom.java", "CheckSecureRandom")
        assert code == 0
        assert "Algorithm: DEFAULT" in stdout
        assert "Provider: BCFIPS" in stdout



    @allure.story("Non-Approved RNG Rejection")
    @allure.title("Verify SHA1PRNG is rejected by BCFIPS")
    @allure.description("Ensures that the legacy SHA1PRNG algorithm is inaccessible through the BCFIPS provider, as FIPS 140-3 requires NIST SP 800-90A DRBGs.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_reject_sha1prng(self, docker_runner):
        code, stdout, stderr = docker_runner("rng/RejectSha1Prng.java", "RejectSha1Prng")
        assert code == 1
        assert "RESULT_SUCCESS_FIPS_ENFORCED" in stdout