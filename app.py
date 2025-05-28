from testrail_client import TestRailClient

def main():
    client = TestRailClient()

    # Example: Get projects
    print("Fetching projects...")
    projects = client.get_projects()
    for project in projects:
        print(f"Project ID: {project['id']}, Name: {project['name']}")

    # Example: Create a test run in a project (replace IDs accordingly)
    project_id = 1   # replace with your project ID
    suite_id = 1     # replace with your suite ID
    test_run_name = "Automated Test Run"
    description = "Created via API"

    print(f"\nCreating test run '{test_run_name}' in project ID {project_id}...")
    test_run = client.add_test_run(project_id, suite_id, test_run_name, description)
    print(f"Test Run created with ID: {test_run['id']}")

    # Example: Add test result (replace test_id and status_id accordingly)
    test_id = 1      # replace with your test ID
    status_id = 1    # 1=Passed, 2=Blocked, 3=Untested, 4=Retest, 5=Failed
    comment = "Test passed successfully."

    print(f"\nAdding test result for test ID {test_id}...")
    result = client.add_test_result(test_id, status_id, comment)
    print("Test result added:", result)

if __name__ == "__main__":
    main()
