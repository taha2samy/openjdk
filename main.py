import json
from datetime import datetime

repo_of_registry="ghcr.io/taha2samy/java"


def loadjson(path):
    with open(f"{path}", "r") as jsonfile: 
        data = json.load(jsonfile)
    return dict(data)

def load_java_version(version):
    config=loadjson("config/context.json")["java"][version]
    jre_std= {"main":loadjson(f"reports/{version}-jre_attestation_details.json"),
    "docker-csi":loadjson(f"reports/{version}-jre-report-docker-cis_full.json"),
    "k8s-nsa":loadjson(f"reports/{version}-jre-report-k8s-nsa_full.json"),
    "k8s-pss-restricted":loadjson(f"reports/{version}-jre-report-k8s-pss-restricted_full.json"),
    "security":loadjson(f"reports/{version}-jre-report-security-full.json"),
    "config":dict(config),
    "tags":[repo_of_registry+f":{version}-jre_standard",repo_of_registry+f":{str(config['full_ver']).replace('-', '_')}-jre_standard"]}
    
    jre_distroless = {"main":loadjson(f"reports/{version}-distroless_attestation_details.json"),
    "docker-csi":loadjson(f"reports/{version}-distroless-report-docker-cis_full.json"),
    "k8s-nsa":loadjson(f"reports/{version}-distroless-report-k8s-nsa_full.json"),
    "k8s-pss-restricted":loadjson(f"reports/{version}-distroless-report-k8s-pss-restricted_full.json"),
    "security":loadjson(f"reports/{version}-distroless-report-security-full.json"),
    "config":dict(config),
    "tags":[repo_of_registry+f":{version}-jre_distroless",repo_of_registry+f":{str(config['full_ver']).replace('-', '_')}-jre_distroless"]}
    
    jdk_std={"main":loadjson(f"reports/{version}-jdk_attestation_details.json"),
    "docker-csi":loadjson(f"reports/{version}-jdk-report-docker-cis_full.json"),
    "k8s-nsa":loadjson(f"reports/{version}-jdk-report-k8s-nsa_full.json"),
    "k8s-pss-restricted":loadjson(f"reports/{version}-jdk-report-k8s-pss-restricted_full.json"),
    "security":loadjson(f"reports/{version}-jdk-report-security-full.json"),
    "config":dict(config),
    "tags":[repo_of_registry+f":{version}-jdk_standard",repo_of_registry+f":{str(config['full_ver']).replace('-', '_')}-jdk_standard"]
    }
    java = {"jdk_standerd":jdk_std,"jre_standerd":jre_std,"jre_distroless":jre_distroless}
    return java


def define_env(env):

    @env.filter
    def to_datetime(date_str):
        try:
            clean_date = date_str.replace('Z', '+00:00').split('.')[0]
            return datetime.fromisoformat(clean_date)
        except:
            return datetime.now()


    env.variables.update({"kics_report":loadjson("reports/kics-report.json")})
    
    env.variables["repo_of_registry"]=repo_of_registry
    env.variables.update({"java_8": load_java_version("8")})
    env.variables.update({"java_11": load_java_version("11")})
    env.variables.update({"java_17": load_java_version("17")})
    env.variables.update({"java_21": load_java_version("21")})
    env.variables.update({"java_25": load_java_version("25")})
    print("------------------------------------")
