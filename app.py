from flask import Flask, render_template, request
from testrail_client import TestRailClient
import re

app = Flask(__name__)
client = TestRailClient()

@app.route("/", methods=["GET", "POST"])
def index():
    total = executed = not_executed = None
    error = None
    priority_counts = {}

    if request.method == "POST":
        url_input = request.form.get("testrail_url", "").strip()
        print("Received URL input:", url_input)

        if url_input:
            match = re.search(r"/runs/view/(\d+)", url_input)
            if match:
                run_id = match.group(1)
                print("Extracted Run ID:", run_id)

                try:
                    tests = client.get_tests(run_id)
                    print(f"Total tests fetched: {len(tests)}")

                    total = len(tests)
                    executed = sum(1 for test in tests if test.get("status_id") not in (None, 3))
                    not_executed = total - executed

                    # Priority breakdown
                    priority_counts = {"High": 0, "Medium": 0, "Low": 0}
                    priority_map = {
                        4: "High",   # Example: Replace with your real priority IDs
                        2: "Medium",
                        1: "Low"
                    }

                    for test in tests:
                        pid = test.get("priority_id")
                        pname = priority_map.get(pid)
                        if pname:
                            priority_counts[pname] += 1

                except Exception as e:
                    error = f"Error fetching data: {str(e)}"
            else:
                error = "Invalid TestRail URL. Please include `/runs/view/<id>`."
        else:
            error = "No URL input received."

    return render_template(
        "index.html",
        total=total,
        executed=executed,
        not_executed=not_executed,
        priority_counts=priority_counts,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
