import nbformat
from nbformat import NotebookNode
from nbconvert.preprocessors import ExecutePreprocessor


def execute_notebook(input_filedir: str, nb_version=4):
    """
    execute_notebook(input_filedir)

    Helper function for running student's notebook.

    - input_filedir: File directory for the student's answer code.

    Returns:
    - nb: Executed NotebookNode object
    """
    # Load the input notebook, and excecute it
    with open(input_filedir) as f:
        nb = nbformat.read(f, as_version=nb_version)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3', allow_errors=True)
        ep.preprocess(nb)

    return nb


def extract_grade_cells(nb: NotebookNode):
    """
    extract_grade_cells(nb)

    Helper function for extracting grade cells from an excecuted notebook.

    - nb: Executed NotebookNode object.

    Returns:
    - grade_cells: A list of grade cells 
    """
    grade_cells = []

    for cell in nb.cells:
        # FIXME: Check for code cell only (for now)
        if not cell["cell_type"] == "code":
            continue
        try:
            nbgrader_metadata = cell["metadata"]["nbgrader"]
            if (nbgrader_metadata["grade"] == True):
                grade_cells.append(cell)
        except:
            continue

    return grade_cells


def write_notebook(output_filedir: str, nb: NotebookNode):
    """
    write_notebook(output_filedir: str, nb: NotebookNode)

    Helper function to write a notebook object to an output file
    """
    with open(output_filedir, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)