"""
Test runner script for executing all tests and generating coverage reports.
"""

import pytest
import coverage
import os
import sys
from datetime import datetime

def run_tests():
    """Run all tests and generate coverage report."""
    # Start coverage
    cov = coverage.Coverage(
        branch=True,
        source=['features'],
        omit=['*/tests/*', '*/__init__.py']
    )
    cov.start()

    # Run tests
    test_result = pytest.main([
        'tests/',
        '-v',
        '--junitxml=test-results.xml'
    ])

    # Stop coverage and save report
    cov.stop()
    cov.save()

    # Generate coverage reports
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_dir = f'coverage_reports/{timestamp}'
    os.makedirs(report_dir, exist_ok=True)

    # Generate HTML report
    cov.html_report(directory=f'{report_dir}/html')
    
    # Generate console report
    print('\nCoverage Report:')
    cov.report()

    # Save coverage data
    cov.save()

    return test_result

if __name__ == '__main__':
    sys.exit(run_tests()) 