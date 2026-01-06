"""
Setup script for API Testing Framework
Handles installation, configuration, and verification
"""

import shutil
import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"


def print_header(text):
    """Print formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def run_command(command, description, check=True):
    """
    Run a shell command and handle errors.

    Args:
        command: Command to run (string or list)
        description: Description of what the command does
        check: Whether to check for errors

    Returns:
        CompletedProcess object
    """
    print_info(f"Running: {description}...")

    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, capture_output=True, text=True)

        if result.returncode == 0:
            print_success(f"{description} - Completed")
        else:
            print_error(f"{description} - Failed")
            if result.stderr:
                print(f"  Error: {result.stderr}")

        return result

    except subprocess.CalledProcessError as e:
        print_error(f"{description} - Failed with error")
        print(f"  Error: {e.stderr}")
        if check:
            sys.exit(1)
        return e
    except Exception as e:
        print_error(f"{description} - Unexpected error: {str(e)}")
        if check:
            sys.exit(1)
        return None


def check_python_version():
    """Check if Python version is 3.8+"""
    print_header("Checking Python Version")

    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required. Current version: {version.major}.{version.minor}")
        sys.exit(1)

    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")


def check_pip():
    """Check if pip is available."""
    print_header("Checking pip")

    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
        print_success("pip is available")
    except subprocess.CalledProcessError:
        print_error("pip is not available")
        sys.exit(1)


def install_dependencies():
    """Install all dependencies from requirements.txt"""
    print_header("Installing Dependencies")

    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], "Upgrading pip")

    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], "Installing project dependencies")


def install_playwright():
    """Install Playwright browsers."""
    print_header("Installing Playwright Browsers")

    run_command([sys.executable, "-m", "playwright", "install", "chromium"], "Installing Chromium browser")


def setup_environment():
    """Setup environment configuration."""
    print_header("Setting up Environment Configuration")

    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        print_warning(".env file already exists")
        response = input("  Do you want to overwrite it? (y/N): ").strip().lower()
        if response != "y":
            print_info("Keeping existing .env file")
            return

    if env_example.exists():
        shutil.copy(env_example, env_file)
        print_success("Created .env file from .env.example")
        print_info("Please edit .env file with your configuration")
    else:
        print_error(".env.example not found")


def create_directories():
    """Create necessary directories."""
    print_header("Creating Directories")

    directories = ["allure-results", "test-results", "screenshots", "logs"]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print_success(f"Created directory: {directory}")


def verify_installation():
    """Verify that everything is installed correctly."""
    print_header("Verifying Installation")

    # Check pytest
    result = run_command([sys.executable, "-m", "pytest", "--version"], "Checking pytest", check=False)

    # Check playwright
    result = run_command([sys.executable, "-m", "playwright", "--version"], "Checking playwright", check=False)

    # Check allure (optional)
    result = subprocess.run(["allure", "--version"], capture_output=True, text=True)

    if result.returncode == 0:
        print_success("Allure CLI is installed")
    else:
        print_warning("Allure CLI is not installed (optional)")
        print_info("  Install from: https://github.com/allure-framework/allure2/releases")


def print_next_steps():
    """Print next steps after installation."""
    print_header("Installation Complete!")

    print(f"{Colors.OKGREEN}Next Steps:{Colors.ENDC}")
    print()
    print("1. Configure your environment:")
    print("   - Edit .env file with your settings")
    print("   - Set BASE_URL, RP_UUID, etc.")
    print()
    print("2. Run tests:")
    print(f"   {Colors.OKCYAN}pytest{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}pytest -n auto{Colors.ENDC}  (parallel execution)")
    print()
    print("3. Generate reports:")
    print(f"   {Colors.OKCYAN}pytest --alluredir=./allure-results{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}allure serve ./allure-results{Colors.ENDC}")
    print()
    print("4. Setup ReportPortal (optional):")
    print("   - Read REPORTPORTAL_SETUP.md for instructions")
    print()
    print(f"{Colors.OKGREEN}Documentation:{Colors.ENDC}")
    print("   - README.md - Full documentation")
    print("   - TEST_COVERAGE.md - Test coverage matrix")
    print("   - QUICK_REFERENCE.md - Quick commands reference")
    print("   - REPORTPORTAL_SETUP.md - ReportPortal setup guide")
    print()


def main():
    """Main setup function."""
    print(f"{Colors.BOLD}")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║   API Test Automation Framework - Setup Script           ║")
    print("║   Python + Playwright + Allure + ReportPortal            ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

    try:
        check_python_version()
        check_pip()
        install_dependencies()
        install_playwright()
        setup_environment()
        create_directories()
        verify_installation()
        print_next_steps()

    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Setup interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error during setup: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
