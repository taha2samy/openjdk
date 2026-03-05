import json
import os
import glob
from datetime import datetime

repo_of_registry = "ghcr.io/taha2samy/java"

def loadjson(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def parse_allure_results(results_dir):
    report = {
        "summary": {"passed": 0, "failed": 0, "total": 0, "duration": 0.0},
        "tests": []
    }
    
    if not os.path.exists(results_dir):
        return report

    result_files = glob.glob(os.path.join(results_dir, "*-result.json"))
    total_duration_ms = 0

    for file_path in result_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                status = data.get("status", "failed")
                start = data.get("start", 0)
                stop = data.get("stop", 0)
                duration = (stop - start) / 1000.0
                
                # تنظيف الوصف لمنع كسر جداول Markdown
                raw_desc = data.get("description", "No description provided")
                clean_desc = raw_desc.replace('\n', ' ').replace('\r', ' ').strip()

                report["tests"].append({
                    "name": data.get("name", "Unknown"),
                    "description": clean_desc,
                    "outcome": "passed" if status == "passed" else "failed",
                    "duration": duration,
                    "nodeid": data.get("fullName", "")
                })
                
                report["summary"]["total"] += 1
                total_duration_ms += duration
                if status == "passed":
                    report["summary"]["passed"] += 1
                else:
                    report["summary"]["failed"] += 1
        except:
            continue

    report["summary"]["duration"] = round(total_duration_ms, 2)
    return report

def load_java_version(version):
    # تحميل بيانات النسخة من الـ context
    context = loadjson("config/context.json")
    if not context or "java" not in context or version not in context["java"]:
        return {}
        
    config = context["java"][version]
    v_full = str(config.get('full_ver', version)).replace('-', '_')
    
    def build_entry(flavor_key, report_suffix):
        return {
            "main": loadjson(f"reports/{version}-{report_suffix}_attestation_details.json"),
            "docker-csi": loadjson(f"reports/{version}-{report_suffix}-report-docker-cis_full.json"),
            "k8s-nsa": loadjson(f"reports/{version}-{report_suffix}-report-k8s-nsa_full.json"),
            "k8s-pss-restricted": loadjson(f"reports/{version}-{report_suffix}-report-k8s-pss-restricted_full.json"),
            "security": loadjson(f"reports/{version}-{report_suffix}-report-security-full.json"),
            "config": config,
            "tags": [
                f"{repo_of_registry}:{version}-{flavor_key}", 
                f"{repo_of_registry}:{v_full}-{flavor_key}"
            ]
        }

    return {
        "jdk_standerd": build_entry("jdk_standard", "jdk"),
        "jre_standerd": build_entry("jre_standard", "jre"),
        "jre_distroless": build_entry("jre_distroless", "distroless"),
        "fips_tests": parse_allure_results(f"reports/{version}-fips/allure-results")
    }

def define_env(env):
    @env.filter
    def to_datetime(date_str):
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00').split('.')[0])
        except:
            return datetime.now()

    # تحميل التقارير العامة
    env.variables.update({
        "kics_report": loadjson("reports/kics-report.json"),
        "repo_of_registry": repo_of_registry
    })

    # تحميل كل إصدارات Java المدعومة
    supported_versions = ["8", "11", "17", "21", "25"]
    for v in supported_versions:
        env.variables.update({f"java_{v}": load_java_version(v)})