import json
import traceback
import os
import sys
from os.path import join
from collections import defaultdict
from pl_helper import execute_notebook, extract_grade_cells

"""
The main python entrypoint for the autograder framework.
"""

OUTPUT_FILE = 'output-fname.txt'

if __name__ == '__main__':
    try:
        # TODO: Uncomment this code when try running in a Docker Container
        filenames_dir = os.environ.get("FILENAMES_DIR")
        base_dir = os.environ.get("MERGE_DIR")

        # Read the output filename from a file, and then delete it
        # We could do this via command-line arg but there's a chance of
        # a student picking it up by calling `ps` for example.
        with open(join(filenames_dir, OUTPUT_FILE), 'r') as output_f:
            output_fname = output_f.read()
        os.remove(join(filenames_dir, OUTPUT_FILE))

        # Update the working directory so tests may access local files
        prev_wd = os.getcwd()
        os.chdir(base_dir)

        # TODO: Verify nbformat before running test
        # Run the tests with our custom setup
        grade_cells = extract_grade_cells(execute_notebook(join(filenames_dir, 'ans.ipynb')))
        results = []

        # Extract the results from grade cells
        for cell in grade_cells:
            this_result = {}
            this_result["name"] = cell["metadata"]["nbgrader"]["grade_id"]
            this_result["max_points"] = cell["metadata"]["nbgrader"]["points"]
            try:
                # If outputs empty, test cell passed
                if not cell["outputs"]:
                    this_result["points"] = cell["metadata"]["nbgrader"]["points"]
                    this_result["feedback"] = "Sucessfully passed!"
                else:
                    this_result["points"] = 0
                    this_result["feedback"] = cell["outputs"][0]["traceback"]
                results.append(this_result)
            except:
                print("Failed to access notebook cell")
                continue

        max_points = sum(this_result["max_points"] for this_result in results)
        earned_points = sum(this_result["points"] for this_result in results)

        # Assemble final grading results
        grading_result = {}
        grading_result['tests'] = results
        grading_result['score'] = float(earned_points) / float(max_points)
        grading_result['succeeded'] = True
        grading_result['gradable'] = True
        grading_result['max_points'] = max_points

    except:
        # Last-ditch effort to capture meaningful error information
        grading_result = {}
        grading_result['score'] = 0.0
        grading_result['succeeded'] = False
        grading_result['output'] = traceback.format_exc()
        print("Failed to grade assignment")

    with open(output_fname, mode='w') as out:
        json.dump(grading_result, out)