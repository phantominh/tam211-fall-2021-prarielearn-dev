# Python "nbgrader" Autograder

This file documents the Python "nbgrader" autograder included in the `prairielearn/grader-python-nbgrader` Docker image. For general information on how to set up an external grader, visit the [external grading](../externalGrading.md) page.

## Setting up

### `info.json`

The question should be first set up to enable [external grading](../externalGrading.md), with `"gradingMethod": "External"` set in the `info.json` settings. To use the specific Python autograder detailed in this document, `"image"` should be set to `"prairielearn/grader-python-nbgrader"` and `"entrypoint"` should point to `"/python_autograder/run.sh"` in the `"externalGradingOptions"` dictionary.

A full `info.json` file should look something like:

```javascript
{
    "uuid": "...",
    "title": "...",
    "topic": "...",
    "tags": [...],
    "type": "v3",
    "singleVariant": true,
    "gradingMethod": "External",
    "externalGradingOptions": {
        "enabled": true,
        "image": "prairielearn/grader-python-nbgrader",
        "entrypoint": "/python_autograder/run.sh",
    }
}
```

### `server.py`

The server code in the `generate()` function must define the list of variables or functions that will be passed to the autograded student code as `names_for_user`, and also those that will be passed from the student code to the test code as `names_from_user`. Only variables or functions listed in `names_for_user` will be accessible by the user from the setup code; only names listed in `names_from_user` will be accessible by the test cases from the user code.

These are stored as a list of dictionary objects in the `data["params"]` dict. The above `names_for_user` and `names_from_user` lists are stored as separate keys in `params`. For example:

```python
def generate(data):
    data["params"]["names_for_user"] = [
        {"name": "x", "description": "Description of the variable", "type": "float"},
    ]
    data["params"]["names_from_user"] = [
        {"name": "x_sq", "description": "The square of $x$", "type": "float"},
    ]
```

Each variable dictionary has entries `name` (the Python variable name in the code), `description` (human readable), and `type` (human readable). These variable lists are used for two purposes: (1) showing students which variables are used, and (2) making variables available to the student code and autograder code.

### `question.html`

At a minimum, the question markup should contain a `pl-file-editor` element (or `pl-file-upload`) and a `pl-external-grading-results` to show the status of grading jobs. These are placed in the question panel and submission panel, respectively. It is also recommended to place a `pl-file-preview` element in the submission panel so that students may see their previous code submissions. An example question markup is given below:

```html
<pl-question-panel>
  <pl-file-editor file-name="ans.ipynb"></pl-file-editor>
</pl-question-panel>

<pl-submission-panel>
  <pl-external-grading-results></pl-external-grading-results>
  <pl-file-preview></pl-file-preview>
</pl-submission-panel>
```

By default, the grader will look for a gradable file named `ans.ipynb`.
Expected variables can also be displayed to the user with the `<pl-external-grader-variables>` element. By setting the `variables-name` attribute to either `names_for_user` or `names_from_user`, both sets of variables can be shown.

Full example:

```html
<pl-question-panel>
  <p>... Question prompt ...</p>

  <p>The setup code gives the following variables:</p>
  <p>
    <pl-external-grader-variables
      variables-category="names_for_user"
    ></pl-external-grader-variables>
  </p>

  <p>Your code snippet should define the following variables:</p>
  <pl-external-grader-variables variables-category="names_from_user"></pl-external-grader-variables>
  <pl-file-editor
    file_name="ans.ipynb"
    ace_mode="ace/mode/python"
  ></pl-file-editor>
</pl-question-panel>

<pl-submission-panel>
  <pl-external-grader-results />
</pl-submission-panel>
```

Note that the `<pl-external-grader-variables>` element is for purely decorative purposes only, `names_for_user` or `names_from_user` or both can be omitted without any negative results.


### Writing questions and test cases for assignments
Questions and test cases for an assignment will be written directly inside the initial code provided to student (`ans.ipynb`).

Each cell that contains student's code answer should have the following nbgrader metadata:
```json
   "metadata": {
    "nbgrader": {
     "grade": false,
     "grade_id": <INSERT THE QUESTION ID>,
     "locked": false,
     "schema_version": 3,
     "solution": true
    }
   }
```

We will be using python `assert`function to write tests. Each question can have multiple tests, however, each test cell should be understood as an Unit Test, because if one line of code fails in a testing cell, that cell would reward 0 point to the students.

Below is an example of 2 cells of test for one function
```json
   "metadata": {
    "nbgrader": {
     "grade": true,
     "grade_id": "correct_squares",
     "locked": false,
     "points": 1,
     "schema_version": 3,
     "solution": false
    }
   }
    ========================
   "metadata": {
    "nbgrader": {
     "grade": true,
     "grade_id": "squares_invalid_input",
     "locked": false,
     "points": 1,
     "schema_version": 3,
     "solution": false
    }
   }

```

Note that each test cell can have multiple assertion, but if one fails the whole cells will result in 0 point.