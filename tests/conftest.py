import pytest
import subprocess
import tempfile
import allure
import logging
import os
from pathlib import Path

# إعداد الـ Logger ليطبع التفاصيل بوضوح
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
logger = logging.getLogger("FIPS_TESTER")

def pytest_addoption(parser):
    parser.addoption("--jdk-img", action="store", required=True, help="Docker image for JDK")
    parser.addoption("--jre-img", action="store", required=True, help="Docker image for JRE Distroless")

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
            logger.error(f"Java test file not found at: {full_java_path}")
            pytest.fail(f"Test File Not Found: {full_java_path}")
            
        # حل مشكلة الـ Mounts Denied: إنشاء المجلد المؤقت داخل مجلد المشروع نفسه
        local_tmp_dir = base_dir / ".pytest_tmp"
        local_tmp_dir.mkdir(exist_ok=True)
        
        with tempfile.TemporaryDirectory(dir=local_tmp_dir) as temp_out:
            # إعطاء صلاحيات 777 للمجلد المؤقت حتى يتمكن الـ Docker Container من الكتابة والقراءة
            os.chmod(temp_out, 0o777)
            
            src_dir = str(full_java_path.parent.absolute())
            file_name = full_java_path.name
            
            # ==========================================
            # 1. Compile Phase (Using JDK Image)
            # ==========================================
            with allure.step(f"Compile Java File: {class_name}.java using JDK"):
                compile_cmd = [
                    "docker", "run", "--rm",
                    "-v", f"{src_dir}:/src:ro",
                    "-v", f"{temp_out}:/out",
                    jdk_img,
                    # الـ JDK ليس له Entrypoint صارم، لذلك نمرر مسار المترجم بالكامل
                    "/opt/java/bin/javac", "-d", "/out", f"/src/{file_name}"
                ]
                
                cmd_str = " ".join(compile_cmd)
                logger.info(f"🏃 RUNNING JAVAC: {cmd_str}")
                
                comp_res = subprocess.run(compile_cmd, capture_output=True, text=True)
                
                if comp_res.stdout:
                    logger.info(f"💬 JAVAC STDOUT:\n{comp_res.stdout.strip()}")
                    allure.attach(comp_res.stdout, name="Javac Stdout", attachment_type=allure.attachment_type.TEXT)
                if comp_res.stderr:
                    logger.error(f"❌ JAVAC STDERR:\n{comp_res.stderr.strip()}")
                    allure.attach(comp_res.stderr, name="Javac Stderr", attachment_type=allure.attachment_type.TEXT)
                    
                if comp_res.returncode != 0:
                    pytest.fail(f"Compilation Failed!\nCommand: {cmd_str}\nError: {comp_res.stderr}")

            # ==========================================
            # 2. Execution Phase (Using JRE Distroless Image)
            # ==========================================
            with allure.step(f"Execute Java Class: {class_name} in JRE Distroless"):
                run_cmd = [
                    "docker", "run", "--rm",
                    "-v", f"{temp_out}:/app:ro",
                    "-w", "/app",
                    jre_img,
                    # حل مشكلة الـ ENTRYPOINT: نمرر المتغيرات مباشرة لأن الـ Distroless ينفذ java تلقائياً
                    "-Dorg.bouncycastle.fips.approved_only=true",
                    "-cp", ".",
                    class_name
                ]
                
                cmd_str = " ".join(run_cmd)
                logger.info(f"🚀 RUNNING JAVA: {cmd_str}")
                
                run_res = subprocess.run(run_cmd, capture_output=True, text=True)
                
                if run_res.stdout:
                    logger.info(f"💬 JAVA STDOUT:\n{run_res.stdout.strip()}")
                    allure.attach(run_res.stdout, name="Execution Stdout", attachment_type=allure.attachment_type.TEXT)
                if run_res.stderr:
                    logger.warning(f"⚠️ JAVA STDERR:\n{run_res.stderr.strip()}")
                    allure.attach(run_res.stderr, name="Execution Stderr", attachment_type=allure.attachment_type.TEXT)

                logger.info(f"🏁 EXIT CODE: {run_res.returncode}")
                return run_res.returncode, run_res.stdout, run_res.stderr
                
    return run_java_test