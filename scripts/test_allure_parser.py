import json
import glob
import os

def parse_allure_results(results_dir):
    if not os.path.exists(results_dir):
        print(f"Error: Path {results_dir} not found!")
        return None

    report = {
        "summary": {"passed": 0, "failed": 0, "total": 0, "duration": 0.0},
        "tests": []
    }

    result_files = glob.glob(os.path.join(results_dir, "*-result.json"))
    print(f"Found {len(result_files)} result files. Processing...")

    total_duration_ms = 0

    for file_path in result_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                status = data.get("status", "failed")
                start_time = data.get("start", 0)
                stop_time = data.get("stop", 0)
                duration = (stop_time - start_time) / 1000.0
                
                description = data.get("description", "No description provided in @allure.description")
                
                params = {p.get("name"): p.get("value") for p in data.get("parameters", [])}

                test_entry = {
                    "name": data.get("name", "Unknown Test"),
                    "description": description,
                    "outcome": "passed" if status == "passed" else "failed",
                    "duration": duration,
                    "full_name": data.get("fullName", ""),
                    "params": params
                }

                report["tests"].append(test_entry)
                
                report["summary"]["total"] += 1
                total_duration_ms += duration
                if status == "passed":
                    report["summary"]["passed"] += 1
                else:
                    report["summary"]["failed"] += 1

        except Exception as e:
            print(f"Error parsing {file_path}: {e}")

    report["summary"]["duration"] = round(total_duration_ms, 2)
    return report

if __name__ == "__main__":
    MY_PATH = "reports/8-fips/allure-results" 
    
    final_data = parse_allure_results(MY_PATH)
    
    if final_data:
        print("\nParsing Complete!")
        print(f"Summary: {final_data['summary']}")
        print(f"Samples (First 2 tests):")
        for t in final_data['tests'][:2]:
            print(f"   - Name: {t['name']}")
            print(f"     Status: {t['outcome']}")
            print(f"     Desc: {t['description']}")
            print("-" * 30)