#!/usr/bin/env python3
"""Test runner script for art_tactile_transform project."""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and print the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode != 0:
        print(f"\n❌ {description} failed with exit code {result.returncode}")
        return False
    else:
        print(f"\n✅ {description} completed successfully")
        return True


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description='Run tests for art_tactile_transform')

    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--api', action='store_true', help='Run API tests only')
    parser.add_argument('--slow', action='store_true', help='Include slow tests')
    parser.add_argument('--coverage', action='store_true', help='Run with coverage report')
    parser.add_argument('--parallel', '-n', type=int, help='Run tests in parallel (number of workers)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--file', '-f', help='Run specific test file')
    parser.add_argument('--function', '-k', help='Run tests matching pattern')
    parser.add_argument('--html-coverage', action='store_true', help='Generate HTML coverage report')

    args = parser.parse_args()

    # Build pytest command
    cmd = ['python', '-m', 'pytest']

    # Add verbosity
    if args.verbose:
        cmd.append('-v')

    # Add coverage if requested
    if args.coverage or args.html_coverage:
        cmd.extend(['--cov=src/art_tactile_transform', '--cov-report=term-missing'])
        if args.html_coverage:
            cmd.append('--cov-report=html')

    # Add parallel execution
    if args.parallel:
        cmd.extend(['-n', str(args.parallel)])

    # Add test selection
    if args.unit:
        cmd.extend(['-m', 'unit'])
    elif args.integration:
        cmd.extend(['-m', 'integration'])
    elif args.api:
        cmd.extend(['-m', 'api'])

    # Include or exclude slow tests
    if not args.slow:
        cmd.extend(['-m', 'not slow'])

    # Run specific file
    if args.file:
        cmd.append(f'tests/{args.file}')

    # Run tests matching pattern
    if args.function:
        cmd.extend(['-k', args.function])

    # Show test configuration
    print("🧪 Art Tactile Transform Test Runner")
    print(f"Command to execute: {' '.join(cmd)}")

    # Run the tests
    success = run_command(cmd, "pytest test suite")

    if success:
        print("\n🎉 All tests completed successfully!")

        if args.html_coverage:
            print("\n📊 HTML coverage report generated in htmlcov/")
            print("Open htmlcov/index.html in your browser to view the report")
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()