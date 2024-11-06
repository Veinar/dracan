# Local development, testing and quality checking

To start developing Dracan on your local machine, you can set up a mock service for live debugging. Follow these steps to get started:

1. **Clone the Repository**: First, clone the Dracan repository to your local machine if you haven't done so already.
   ```bash
   git clone https://github.com/Veinar/dracan.git
   cd dracan
   ```
2. Set Up a Virtual Environment: It’s recommended to create a virtual environment for your development work to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\Activate.ps1`
    ```
3. Install Required Dependencies: Install the necessary Python packages using pip. Ensure you have Flask installed, as it is used for the mock service.
    ```bash
    pip install -r requirements.txt
    ```
4. Run the Mock Service: Start the mock service provided in the Dracan package. This service is located in `tests/destination_mock.py` and simulates the application your Dracan middleware will be interfacing with.
    ```bash
    python tests/destination_mock.py
    ```
5. Live Debugging: With the mock service running, you can now run Dracan in your local environment. This allows you to test and debug how Dracan interacts with the mock service in real-time.
6. Modify and Test: Make changes to Dracan's code as needed, and observe the interactions with the mock service. This setup enables you to develop efficiently and troubleshoot any issues in real-time.

## Running Unit Tests

> **This is "must have" to be done before submitting a PR to avoid breaking Dracan itself**

Dracan includes a suite of unit tests to ensure the functionality and reliability of the code. Running these tests is an important step when contributing to the project, especially when adding new features or enhancements.
Please note that these tests were written using ChatGPT due to my lack of experience in this area.

### Prerequisites

Before running the tests, make sure you have **pytest** installed in your environment. You can install it using pip:

```bash
pip install pytest
```

### Running the tests

To run the unit tests for Dracan, execute the following command from the root directory of the project:

```bash
pytest tests/
```

This command will run all the tests located in the `tests` directory and provide you with feedback on the results.

### Expanding Tests

As you work on expanding Dracan with new features or validations, it is essential to also expand the test suite. Ensure that any new validations or limiting functionalities are covered by corresponding tests. This practice not only helps maintain the integrity of the project but also provides assurance that existing functionality remains unaffected by new changes.

We encourage you to contribute by writing additional tests and improving the overall test coverage. Your efforts in this area will help ensure that Dracan remains a reliable and robust middleware solution.

## Running Linter

> **This should be done before submitting a PR to avoid major issues in code**

To maintain code quality and ensure adherence to coding standards, Dracan uses a linter to analyze the codebase. Linting is essential in identifying stylistic errors and enforcing a consistent code format, making it easier to read and maintain.

### Prerequisites

Before running the linter, ensure that **pylint** is installed in your environment. You can install it using pip:

```bash
pip install pylint
```
To run the linter for Dracan, execute the following command from the root directory of the project. This command checks for code issues while disabling the C0301 rule, which restricts line length:

```bash
pylint --disable=C0301 dracan/
```

## Running Security analysis

> **This should be done before submitting a PR to avoid major security issues in code**

Security analysis is a critical step to help identify potential vulnerabilities in the code. Dracan uses Bandit, a security tool designed to detect common security issues in Python code.

### Prerequisites

Before running the security analysis, make sure bandit is installed in your environment. You can install it with the following command:

```bash
pip install bandit
```

To run a security analysis on the Dracan codebase, execute the following command from the root directory of the project:

```bash
bandit -r dracan/
```
This command scans the code recursively and reports any detected security issues.