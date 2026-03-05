import pytest
import subprocess
import tempfile
import allure
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("FIPS_TESTER")

def pytest_addoption(parser):
    parser.addoption("--jdk-img", action="store", required=True)
    parser.addoption("--jre-img", action="store", required=True)

@pytest.fixture(scope="session")
def jdk_img(request):
    return request.config.getoption("--jdk-img")

@pytest.fixture(scope="session")
def jre_img(request):
    return request.config.getoption("--jre-img")

@pytest.fixture(scope="session")
def docker_runner(jdk_img, jre_img):
    def run_java_test(java_file_path, class_name):
        base_dir = Path(__file__).parent.resolve()
        full_java_path = base_dir / java_file_path
        
        if not full_java_path.exists():
            pytest.fail(f"Test File Not Found: {full_java_path}")
            
        local_tmp_dir = base_dir / ".pytest_tmp"
        local_tmp_dir.mkdir(exist_ok=True)
        
        with tempfile.TemporaryDirectory(dir=local_tmp_dir) as temp_out:
            os.chmod(temp_out, 0o777)
            src_dir = str(full_java_path.parent.absolute())
            
            with allure.step(f"Compile {class_name}"):
                compile_cmd = [
                    "docker", "run", "--rm",
                    "-v", f"{src_dir}:/src:ro",
                    "-v", f"{temp_out}:/out",
                    jdk_img,
                    "/opt/java/bin/javac", "-d", "/out", f"/src/{full_java_path.name}"
                ]
                comp_res = subprocess.run(compile_cmd, capture_output=True, text=True)
                if comp_res.returncode != 0:
                    pytest.fail(f"Javac Failed: {comp_res.stderr}")

            subprocess.run(["sync"])

            with allure.step(f"Run {class_name}"):
                run_cmd = [
                    "docker", "run", "--rm",
                    "--entrypoint", "/opt/java/bin/java",
                    "-v", f"{temp_out}:/app:ro",
                    "-w", "/app",
                    jre_img,
                    "-Dorg.bouncycastle.fips.approved_only=true",
                    "-cp", "/app", 
                    class_name
                ]
                
                run_res = subprocess.run(run_cmd, capture_output=True, text=True)
                
                allure.attach(run_res.stdout or "No Stdout", name="Stdout")
                allure.attach(run_res.stderr or "No Stderr", name="Stderr")

                return run_res.returncode, run_res.stdout, run_res.stderr
                
    return run_java_test