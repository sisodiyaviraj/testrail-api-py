from flask import Flask, render_template, request
from testrail_client import TestRailClient
import re

app = Flask(__name__)
client = TestRailClient()

@app.route("/", methods=["GET", "POST"])
def index():
    total = executed = not_executed = None
    error = None

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

                    # DEBUG: Print status of first 5 tests
                    for test in tests[:5]:
                        print(f"Test ID: {test.get('id')}, Status ID: {test.get('status_id')}")

                    total = len(tests)
                    executed = sum(1 for test in tests if test.get("status_id", 3) != 3)
                    not_executed = total - executed
                except Exception as e:
                    error = f"Error fetching data: {str(e)}"
            else:
                error = "Invalid TestRail URL. Please include `/runs/view/<id>`."
        else:
            error = "No URL input received."

    return render_template("index.html", total=total, executed=executed, not_executed=not_executed, error=error)

if __name__ == "__main__":
    app.run(debug=True)
