# Print a report of successful/failed inserts to the console.

def write_results(rc):
    for r in rc:
        print(r['message'])

def execute(results):
    [write_results(result_case) for result_case in results]