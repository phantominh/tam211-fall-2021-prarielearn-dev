# Add nb-grader extension support for Prairelearn Fall 2021

## Steps to setup and run grader-python-nbgrader from a local version of Prairielearn

1. Copy the python-nbgrader folder into Prarielearn's graders directory
2. Build a local Docker image for the grader (or upload an image on Docker Cloud):

    ```bash
    ### Go to the python-nbgrader directory
    sudo docker build . -t prairielearn/grader-python-nbgrader
    ```
3. In order to test the grader, you can run local Prarielearn with the example course in this folder with the following command:
    ```bash
    ### NOTE: Make sure the directory to example course is correct for your local machine 
    sudo docker run -it --rm -p 3000:3000 \
    -v ./exampleCourse:/course `# Map your current directory in as course content` \
    -v "$HOME/pl_ag_jobs:/jobs" `# Map jobs directory into /jobs` \
    -e HOST_JOBS_DIR="$HOME/pl_ag_jobs" \
    -v /var/run/docker.sock:/var/run/docker.sock `# Mount docker into itself so container can spawn others` \
    --add-host=host.docker.internal:172.17.0.1 `# this line is new vs MacOS` \
    prairielearn/prairielearn:local
    ```
4. Do "Load course" on Prairelearn interface, and access course XC 102. You can test the grader using the Question Workspace:JupyterLab, which will grader the ans.ipynb file, or inside Prarielearn Python Autograder demo question, the file upload question, upload a properly setup .ipynb file and the grader should work.
## Things that I have not been able to do
1. Set up nb-grader for jupyter workspace
2. Make an exclusive test course for this grader