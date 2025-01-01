import unittest
import sys
from pathlib import Path
import coverage
import datetime
import json
from typing import Dict, List

# Add the project root directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

class TestReport:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = []
        self.errors = []
        self.coverage_data = {}
        self.start_time = None
        self.end_time = None

    def generate_html_report(self, output_path: Path) -> None:
        """Generate an HTML report of test results"""
        duration = (self.end_time - self.start_time).total_seconds()
        pass_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0

        html_content = f"""
        <html>
        <head>
            <title>Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .summary {{ background-color: #f5f5f5; padding: 20px; border-radius: 5px; }}
                .failed {{ color: red; }}
                .passed {{ color: green; }}
                .coverage {{ margin-top: 20px; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .header {{ background: linear-gradient(45deg, #1976d2 30%, #2196f3 90%);
                          color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Test Report</h1>
                <p>Generated on: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="summary">
                <h2>Summary</h2>
                <p>Duration: {duration:.2f} seconds</p>
                <p>Total Tests: {self.total_tests}</p>
                <p>Passed Tests: <span class="passed">{self.passed_tests}</span></p>
                <p>Failed Tests: <span class="failed">{len(self.failed_tests)}</span></p>
                <p>Pass Rate: {pass_rate:.2f}%</p>
            </div>
            
            <div class="coverage">
                <h2>Coverage Report</h2>
                <table>
                    <tr>
                        <th>Module</th>
                        <th>Coverage %</th>
                        <th>Missing Lines</th>
                    </tr>
        """

        for module, data in self.coverage_data.items():
            html_content += f"""
                    <tr>
                        <td>{module}</td>
                        <td>{data['coverage']:.2f}%</td>
                        <td>{', '.join(map(str, data['missing_lines']))}</td>
                    </tr>
            """

        html_content += "</table>"

        if self.failed_tests:
            html_content += """
                <h2>Failed Tests</h2>
                <ul>
            """
            for test in self.failed_tests:
                html_content += f"<li class='failed'>{test}</li>"
            html_content += "</ul>"

        if self.errors:
            html_content += """
                <h2>Errors</h2>
                <ul>
            """
            for error in self.errors:
                html_content += f"<li class='failed'>{error}</li>"
            html_content += "</ul>"

        html_content += """
            </div>
        </body>
        </html>
        """

        output_path.write_text(html_content)

def run_tests_with_coverage():
    # Initialize coverage
    cov = coverage.Coverage(
        source=['src'],
        omit=['src/__init__.py', 'src/run_server.py']
    )
    cov.start()

    # Initialize test report
    report = TestReport()
    report.start_time = datetime.datetime.now()

    # Find and run tests
    loader = unittest.TestLoader()
    test_dir = Path(__file__).parent
    suite = loader.discover(str(test_dir), pattern='test_*.py')
    
    # Run tests and capture results
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Stop coverage
    cov.stop()
    cov.save()

    # Gather test results
    report.total_tests = result.testsRun
    report.passed_tests = result.testsRun - len(result.failures) - len(result.errors)
    report.failed_tests = [f"{test[0]}: {test[1]}" for test in result.failures]
    report.errors = [f"{test[0]}: {test[1]}" for test in result.errors]

    # Get coverage data
    for filename in cov.get_data().measured_files():
        analysis = cov.analysis2(filename)
        module_name = Path(filename).name
        report.coverage_data[module_name] = {
            'coverage': cov.report(include=filename, show_missing=True),
            'missing_lines': analysis[3]  # Missing lines
        }

    report.end_time = datetime.datetime.now()
    return report, result.wasSuccessful()

if __name__ == '__main__':
    # Create test_reports directory if it doesn't exist
    reports_dir = Path(__file__).parent.parent / 'test_reports'
    reports_dir.mkdir(exist_ok=True)

    # Run tests with coverage
    print("\nRunning tests with coverage...\n")
    report, success = run_tests_with_coverage()

    # Generate HTML report
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = reports_dir / f'test_report_{timestamp}.html'
    report.generate_html_report(report_path)

    print(f"\nTest report generated: {report_path}")
    sys.exit(not success) 