"""
Unit tests for utility modules to improve code coverage.
Tests for sync_readme_test_results.py and conftest.py utilities.
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from sync_readme_test_results import (
    generate_results_section,
    parse_test_results,
    update_readme,
)


class TestParseTestResults:
    """Tests for parse_test_results function."""

    def test_parse_all_passed(self):
        """Test parsing output with all tests passed."""
        output = """
        tests/test_signup.py::test_one PASSED
        tests/test_signup.py::test_two PASSED
        tests/test_signup.py::test_three PASSED
        =============== 3 passed in 1.23s ===============
        """
        result = parse_test_results(output)

        assert result["passed"] == 3
        assert result["failed"] == 0
        assert result["xfailed"] == 0
        assert result["skipped"] == 0
        assert result["total"] == 3
        assert result["execution_time"] == "1.23"

    def test_parse_mixed_results(self):
        """Test parsing output with mixed test results."""
        output = """
        tests/test_signup.py::test_pass PASSED
        tests/test_signup.py::test_fail FAILED
        tests/test_signup.py::test_xfail XFAIL
        tests/test_signup.py::test_skip SKIPPED
        =============== 1 passed, 1 failed, 1 xfailed, 1 skipped in 2.50s ===============
        """
        result = parse_test_results(output)

        assert result["passed"] == 1
        assert result["failed"] == 1
        assert result["xfailed"] == 1
        assert result["skipped"] == 1
        assert result["total"] == 4
        assert result["execution_time"] == "2.50"

    def test_parse_with_windows_paths(self):
        """Test parsing output with Windows-style paths."""
        output = """
        tests\\test_signup.py::test_one PASSED
        tests\\test_signup.py::test_two PASSED
        tests\\test_signup_verification.py::test_verify PASSED
        =============== 3 passed in 0.85s ===============
        """
        result = parse_test_results(output)

        assert result["passed"] == 3
        assert result["signup_tests"] == 2
        assert result["verification_tests"] == 1

    def test_parse_with_unix_paths(self):
        """Test parsing output with Unix-style paths."""
        output = """
        tests/test_signup.py::test_one PASSED
        tests/test_signup.py::test_two PASSED
        tests/test_signup_verification.py::test_verify PASSED
        =============== 3 passed in 0.85s ===============
        """
        result = parse_test_results(output)

        assert result["passed"] == 3
        assert result["signup_tests"] == 2
        assert result["verification_tests"] == 1

    def test_parse_no_time_match(self):
        """Test parsing when execution time is not found."""
        output = "tests/test_signup.py::test_one PASSED"
        result = parse_test_results(output)

        assert result["execution_time"] == "N/A"

    def test_parse_empty_output(self):
        """Test parsing empty output."""
        result = parse_test_results("")

        assert result["total"] == 0
        assert result["passed"] == 0
        assert result["failed"] == 0

    def test_timestamp_format(self):
        """Test that timestamp is in correct format."""
        output = "tests/test_signup.py::test_one PASSED"
        result = parse_test_results(output)

        # Check timestamp format: YYYY-MM-DD HH:MM:SS
        assert len(result["timestamp"]) == 19
        assert result["timestamp"][4] == "-"
        assert result["timestamp"][7] == "-"
        assert result["timestamp"][10] == " "


class TestGenerateResultsSection:
    """Tests for generate_results_section function."""

    def test_generate_section_all_passed(self):
        """Test generating section when all tests pass."""
        stats = {
            "total": 29,
            "passed": 29,
            "failed": 0,
            "xfailed": 0,
            "skipped": 0,
            "execution_time": "1.50",
            "signup_tests": 19,
            "verification_tests": 10,
            "timestamp": "2026-01-06 14:30:00",
        }
        result = generate_results_section(stats)

        assert "## 📈 Test Execution Results ✅" in result
        assert "29 passed" in result
        assert "1.50s" in result
        assert "2026-01-06 14:30:00" in result

    def test_generate_section_with_failures(self):
        """Test generating section when tests fail."""
        stats = {
            "total": 29,
            "passed": 25,
            "failed": 4,
            "xfailed": 0,
            "skipped": 0,
            "execution_time": "2.00",
            "signup_tests": 19,
            "verification_tests": 10,
            "timestamp": "2026-01-06 14:30:00",
        }
        result = generate_results_section(stats)

        assert "## 📈 Test Execution Results ❌" in result
        assert "25 passed" in result

    def test_generate_section_with_xfailed(self):
        """Test generating section with xfailed tests."""
        stats = {
            "total": 29,
            "passed": 24,
            "failed": 0,
            "xfailed": 5,
            "skipped": 0,
            "execution_time": "1.75",
            "signup_tests": 19,
            "verification_tests": 10,
            "timestamp": "2026-01-06 14:30:00",
        }
        result = generate_results_section(stats)

        assert "## 📈 Test Execution Results ✅" in result  # No failures = success
        assert "5 xfailed" in result
        assert "security issues documented" in result


class TestUpdateReadme:
    """Tests for update_readme function."""

    def test_update_existing_section(self):
        """Test updating an existing results section."""
        with tempfile.TemporaryDirectory() as tmpdir:
            readme_path = os.path.join(tmpdir, "README.md")

            # Create initial README with results section
            initial_content = """# Project Title

Some description here.

## 📈 Test Execution Results ✅

### Old Results
- Old data

## Another Section

More content here.
"""
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(initial_content)

            # Change to temp directory for the test
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                new_section = """## 📈 Test Execution Results ✅

### New Results
- New data"""
                result = update_readme(new_section)

                assert result is True

                with open(readme_path, encoding="utf-8") as f:
                    updated_content = f.read()

                assert "### New Results" in updated_content
                assert "### Old Results" not in updated_content
                assert "## Another Section" in updated_content
            finally:
                os.chdir(original_cwd)

    def test_append_section_when_missing(self):
        """Test appending section when it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            readme_path = os.path.join(tmpdir, "README.md")

            # Create README without results section
            initial_content = """# Project Title

Some description here.
"""
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(initial_content)

            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                new_section = """## 📈 Test Execution Results ✅

### Test Results
- Data here"""
                result = update_readme(new_section)

                assert result is True

                with open(readme_path, encoding="utf-8") as f:
                    updated_content = f.read()

                assert "## 📈 Test Execution Results" in updated_content
                assert "### Test Results" in updated_content
            finally:
                os.chdir(original_cwd)

    def test_update_readme_file_not_found(self):
        """Test handling when README doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                result = update_readme("## Test Section")
                assert result is False
            finally:
                os.chdir(original_cwd)

    def test_update_section_at_end_of_file(self):
        """Test updating section when it's at the end (no next section)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            readme_path = os.path.join(tmpdir, "README.md")

            # Create README with results section at the end
            initial_content = """# Project Title

Some description.

## 📈 Test Execution Results ✅

Old content at end of file."""
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(initial_content)

            original_cwd = os.getcwd()
            os.chdir(tmpdir)

            try:
                new_section = """## 📈 Test Execution Results ✅

New content at end."""
                result = update_readme(new_section)

                assert result is True

                with open(readme_path, encoding="utf-8") as f:
                    updated_content = f.read()

                assert "New content at end" in updated_content
                assert "Old content at end" not in updated_content
            finally:
                os.chdir(original_cwd)


class TestRunTestsAndCaptureOutput:
    """Tests for run_tests_and_capture_output function."""

    @patch("sync_readme_test_results.subprocess.run")
    def test_successful_test_run(self, mock_run):
        """Test successful pytest execution."""
        from sync_readme_test_results import run_tests_and_capture_output

        mock_run.return_value = MagicMock(
            stdout="3 passed in 1.0s",
            stderr="",
            returncode=0,
        )

        output, returncode = run_tests_and_capture_output()

        assert output == "3 passed in 1.0s"
        assert returncode == 0
        mock_run.assert_called_once()

    @patch("sync_readme_test_results.subprocess.run")
    def test_test_run_with_failures(self, mock_run):
        """Test pytest execution with failures."""
        from sync_readme_test_results import run_tests_and_capture_output

        mock_run.return_value = MagicMock(
            stdout="1 passed, 2 failed in 1.5s",
            stderr="",
            returncode=1,
        )

        output, returncode = run_tests_and_capture_output()

        assert "2 failed" in output
        assert returncode == 1

    @patch("sync_readme_test_results.subprocess.run")
    def test_test_run_timeout(self, mock_run):
        """Test handling of timeout during test execution."""
        import subprocess

        from sync_readme_test_results import run_tests_and_capture_output

        mock_run.side_effect = subprocess.TimeoutExpired(cmd="pytest", timeout=300)

        output, returncode = run_tests_and_capture_output()

        assert output is None
        assert returncode == -1

    @patch("sync_readme_test_results.subprocess.run")
    def test_test_run_exception(self, mock_run):
        """Test handling of general exception during test execution."""
        from sync_readme_test_results import run_tests_and_capture_output

        mock_run.side_effect = Exception("Unexpected error")

        output, returncode = run_tests_and_capture_output()

        assert output is None
        assert returncode == -1


class TestConftestUtilities:
    """Tests for conftest.py utility functions."""

    def test_pytest_configure_sets_update_readme_env(self):
        """Test that pytest_configure sets UPDATE_README env variable."""
        # Clear any existing value
        if "UPDATE_README" in os.environ:
            del os.environ["UPDATE_README"]

        # Create a mock config object
        mock_config = MagicMock()
        mock_config.getoption.return_value = True
        mock_config.addinivalue_line = MagicMock()

        # Import and call pytest_configure
        from conftest import pytest_configure

        pytest_configure(mock_config)

        assert os.environ.get("UPDATE_README") == "true"

        # Cleanup
        del os.environ["UPDATE_README"]

    def test_pytest_configure_without_update_readme_flag(self):
        """Test pytest_configure when --update-readme is not set."""
        # Clear any existing value
        if "UPDATE_README" in os.environ:
            del os.environ["UPDATE_README"]

        mock_config = MagicMock()
        mock_config.getoption.return_value = False
        mock_config.addinivalue_line = MagicMock()

        from conftest import pytest_configure

        pytest_configure(mock_config)

        # UPDATE_README should not be set
        assert os.environ.get("UPDATE_README") != "true"


class TestDataFactory:
    """Tests for data_factory.py utilities."""

    def test_create_signup_payload_structure(self):
        """Test that signup payload has required fields."""
        from data_factory import UserDataFactory

        payload = UserDataFactory.create_signup_payload()

        assert "name" in payload
        assert "email" in payload
        assert "password" in payload
        assert len(payload) == 3

    def test_create_signup_payload_unique_emails(self):
        """Test that each call generates unique email."""
        from data_factory import UserDataFactory

        payload1 = UserDataFactory.create_signup_payload()
        payload2 = UserDataFactory.create_signup_payload()

        assert payload1["email"] != payload2["email"]

    def test_generate_unique_email_format(self):
        """Test unique email generation with custom parameters."""
        from data_factory import UserDataFactory

        email = UserDataFactory.generate_unique_email(prefix="test", domain="example.com")

        assert email.startswith("test")
        assert email.endswith("@example.com")
        assert "@" in email

    def test_generate_unique_email_default_domain(self):
        """Test unique email generation with default domain."""
        from data_factory import UserDataFactory

        email = UserDataFactory.generate_unique_email()

        assert "@" in email
        # Check it ends with a valid domain
        assert "." in email.split("@")[1]


class TestSchemas:
    """Tests for schemas.py validation utilities."""

    def test_signup_success_schema_valid(self):
        """Test valid signup success response."""
        from schemas import SignupSuccessResponseSchema, assert_response_schema

        valid_response = {
            "message": "User created successfully",
            "error": False,
            "code": "SUCCESS",
            "data": {"user_id": "123", "email": "test@example.com"},
        }

        # Should not raise
        assert_response_schema(valid_response, SignupSuccessResponseSchema)

    def test_signup_error_schema_valid(self):
        """Test valid signup error response."""
        from schemas import SignupErrorResponseSchema, assert_response_schema

        valid_response = {
            "error": "Validation failed",
            "message": "Email already exists",
            "errors": [{"field": "email", "message": "This email is already registered", "code": "DUPLICATE"}],
        }

        # Should not raise
        assert_response_schema(valid_response, SignupErrorResponseSchema)

    def test_validate_response_schema_success(self):
        """Test validate_response_schema returns True for valid data."""
        from schemas import SignupSuccessResponseSchema, validate_response_schema

        valid_response = {
            "message": "Success",
            "error": False,
            "code": "OK",
        }

        is_valid, error = validate_response_schema(valid_response, SignupSuccessResponseSchema)
        assert is_valid is True
        assert error is None

    def test_validate_response_schema_failure(self):
        """Test validate_response_schema returns False for invalid data."""
        from schemas import SignupSuccessResponseSchema, validate_response_schema

        invalid_response = {
            "wrong_field": "value",
        }

        is_valid, error = validate_response_schema(invalid_response, SignupSuccessResponseSchema)
        assert is_valid is False
        assert error is not None

    def test_performance_assertion_pass(self):
        """Test PerformanceAssertion passes for acceptable time."""
        from schemas import PerformanceAssertion

        # Should not raise
        PerformanceAssertion.assert_response_time(100.0, 500.0, "/api/test")

    def test_performance_assertion_fail(self):
        """Test PerformanceAssertion fails for exceeded time."""
        from schemas import PerformanceAssertion

        with pytest.raises(AssertionError):
            PerformanceAssertion.assert_response_time(600.0, 500.0, "/api/test")


class TestDecorators:
    """Tests for decorators.py utilities."""

    def test_api_smoke_decorator(self):
        """Test api_smoke decorator applies correctly."""
        from decorators import api_smoke

        @api_smoke(method="POST", endpoint="/api/test")
        def sample_test():
            """Empty test function to verify decorator application."""

        # Check that pytest marks are applied
        assert hasattr(sample_test, "pytestmark")

    def test_validation_test_decorator(self):
        """Test validation_test decorator applies correctly."""
        from decorators import validation_test

        @validation_test(field="email", validation_type="format")
        def sample_test():
            """Empty test function to verify decorator application."""

        assert hasattr(sample_test, "pytestmark")

    def test_feature_story_decorator(self):
        """Test feature_story decorator for classes."""
        from decorators import feature_story

        @feature_story(feature="Auth", story="Login")
        class TestClass:
            """Empty test class to verify decorator application."""

        # Decorator should return the class with pytestmark
        assert hasattr(TestClass, "pytestmark")

    def test_known_bug_decorator(self):
        """Test known_bug decorator marks test as xfail."""
        from decorators import known_bug

        @known_bug(bug_id="BUG-001", reason="Known issue")
        def sample_test():
            """Empty test function to verify decorator application."""

        assert hasattr(sample_test, "pytestmark")
        # Check it's marked as xfail
        marks = [m.name for m in sample_test.pytestmark]
        assert "xfail" in marks

    def test_smoke_test_decorator_with_title(self):
        """Test smoke_test decorator with title and description."""
        from decorators import smoke_test

        @smoke_test(title="Test Title", description="Test Description")
        def sample_test():
            """Empty test function to verify decorator application."""

        assert hasattr(sample_test, "pytestmark")
        marks = [m.name for m in sample_test.pytestmark]
        assert "smoke" in marks

    def test_smoke_test_decorator_without_args(self):
        """Test smoke_test decorator without arguments."""
        from decorators import smoke_test

        @smoke_test()
        def sample_test():
            """Empty test function to verify decorator application."""

        assert hasattr(sample_test, "pytestmark")

    def test_regression_test_decorator(self):
        """Test regression_test decorator."""
        from decorators import regression_test

        @regression_test(title="Regression", description="Test", severity="CRITICAL")
        def sample_test():
            """Empty test function to verify decorator application."""

        assert hasattr(sample_test, "pytestmark")
        marks = [m.name for m in sample_test.pytestmark]
        assert "regression" in marks

    def test_regression_test_decorator_all_severities(self):
        """Test regression_test with all severity levels."""
        from decorators import regression_test

        severities = ["BLOCKER", "CRITICAL", "NORMAL", "MINOR", "TRIVIAL", "UNKNOWN"]
        for severity in severities:

            @regression_test(severity=severity)
            def sample_test():
                """Empty test function to verify decorator application."""

            assert hasattr(sample_test, "pytestmark")

    def test_api_test_decorator(self):
        """Test api_test decorator."""
        from decorators import api_test

        @api_test(method="GET", endpoint="/api/users")
        def sample_test():
            return "success"

        # Call the decorated function
        result = sample_test()
        assert result == "success"

    def test_api_test_decorator_with_title(self):
        """Test api_test decorator with custom title."""
        from decorators import api_test

        @api_test(method="POST", endpoint="/api/create", title="Custom Title")
        def sample_test():
            return "created"

        result = sample_test()
        assert result == "created"

    def test_flaky_test_decorator(self):
        """Test flaky_test decorator."""
        from decorators import flaky_test

        @flaky_test(reruns=3, reruns_delay=2)
        def sample_test():
            """Empty test function to verify decorator application."""

        assert hasattr(sample_test, "pytestmark")
        marks = [m.name for m in sample_test.pytestmark]
        assert "flaky" in marks

    def test_performance_test_decorator_pass(self):
        """Test performance_test decorator with fast function."""
        from decorators import performance_test

        @performance_test(max_duration=5)
        def fast_function():
            return "fast"

        result = fast_function()
        assert result == "fast"

    def test_with_test_data_decorator(self):
        """Test with_test_data decorator."""
        from decorators import with_test_data

        @with_test_data(username="test_user", role="admin")
        def sample_test():
            return "data attached"

        result = sample_test()
        assert result == "data attached"

    def test_critical_smoke_decorator(self):
        """Test critical_smoke convenience decorator."""
        from decorators import critical_smoke

        @critical_smoke(title="Critical Test", description="Important test")
        def sample_test():
            """Empty test function to verify decorator application."""

        assert hasattr(sample_test, "pytestmark")

    def test_known_bug_without_reason(self):
        """Test known_bug decorator without reason."""
        from decorators import known_bug

        @known_bug(bug_id="BUG-002")
        def sample_test():
            """Empty test function to verify decorator application."""

        assert hasattr(sample_test, "pytestmark")


class TestDataFactoryExtended:
    """Extended tests for data_factory.py utilities."""

    def test_random_name(self):
        """Test random_name generation."""
        from data_factory import UserDataFactory

        name = UserDataFactory.random_name()
        assert isinstance(name, str)
        assert len(name) > 0

    def test_random_name_with_locale(self):
        """Test random_name with different locale."""
        from data_factory import UserDataFactory

        name = UserDataFactory.random_name(locale="en_GB")
        assert isinstance(name, str)
        assert len(name) > 0

    def test_random_first_name(self):
        """Test random_first_name generation."""
        from data_factory import UserDataFactory

        first_name = UserDataFactory.random_first_name()
        assert isinstance(first_name, str)
        assert len(first_name) > 0

    def test_random_last_name(self):
        """Test random_last_name generation."""
        from data_factory import UserDataFactory

        last_name = UserDataFactory.random_last_name()
        assert isinstance(last_name, str)
        assert len(last_name) > 0

    def test_random_email_with_domain(self):
        """Test random_email with custom domain."""
        from data_factory import UserDataFactory

        email = UserDataFactory.random_email(domain="company.com")
        assert email.endswith("@company.com")

    def test_random_email_without_domain(self):
        """Test random_email without domain (random)."""
        from data_factory import UserDataFactory

        email = UserDataFactory.random_email()
        assert "@" in email

    def test_random_password_default(self):
        """Test random_password with defaults."""
        from data_factory import UserDataFactory

        password = UserDataFactory.random_password()
        assert len(password) == 12
        # Check complexity
        assert any(c.isupper() for c in password)
        assert any(c.islower() for c in password)
        assert any(c.isdigit() for c in password)

    def test_random_password_custom_length(self):
        """Test random_password with custom length."""
        from data_factory import UserDataFactory

        password = UserDataFactory.random_password(length=20)
        assert len(password) == 20

    def test_random_password_no_special(self):
        """Test random_password without special characters."""
        from data_factory import UserDataFactory

        password = UserDataFactory.random_password(include_special=False)
        special_chars = "!@#$%^&*"
        assert not any(c in special_chars for c in password)

    def test_random_phone_number(self):
        """Test random_phone_number generation."""
        from data_factory import UserDataFactory

        phone = UserDataFactory.random_phone_number()
        assert phone.startswith("+1")

    def test_random_phone_number_custom_code(self):
        """Test random_phone_number with custom country code."""
        from data_factory import UserDataFactory

        phone = UserDataFactory.random_phone_number(country_code="+44")
        assert phone.startswith("+44")

    def test_random_address(self):
        """Test random_address generation."""
        from data_factory import UserDataFactory

        address = UserDataFactory.random_address()
        assert "street" in address
        assert "city" in address
        assert "state" in address
        assert "zip_code" in address
        assert "country" in address

    def test_create_signup_payload_with_custom_values(self):
        """Test create_signup_payload with custom values."""
        from data_factory import UserDataFactory

        payload = UserDataFactory.create_signup_payload(
            name="Custom Name", email="custom@test.com", password="CustomPass123!"  # NOSONAR - Test data
        )
        assert payload["name"] == "Custom Name"
        assert payload["email"] == "custom@test.com"
        assert payload["password"] == "CustomPass123!"  # NOSONAR - Test data

    def test_create_signup_payload_with_kwargs(self):
        """Test create_signup_payload with extra kwargs."""
        from data_factory import UserDataFactory

        payload = UserDataFactory.create_signup_payload(phone="+1234567890", role="admin")
        assert "phone" in payload
        assert "role" in payload
        assert payload["phone"] == "+1234567890"
        assert payload["role"] == "admin"

    def test_create_invalid_payload_email(self):
        """Test create_invalid_payload for email field."""
        from data_factory import UserDataFactory

        payload = UserDataFactory.create_invalid_payload("email")
        assert payload["email"] == "invalid-email-format"

    def test_create_invalid_payload_name(self):
        """Test create_invalid_payload for name field."""
        from data_factory import UserDataFactory

        payload = UserDataFactory.create_invalid_payload("name")
        assert payload["name"] == "User@123!"

    def test_create_invalid_payload_password(self):
        """Test create_invalid_payload for password field."""
        from data_factory import UserDataFactory

        payload = UserDataFactory.create_invalid_payload("password")
        assert payload["password"] == "weak"

    def test_create_invalid_payload_custom_value(self):
        """Test create_invalid_payload with custom invalid value."""
        from data_factory import UserDataFactory

        payload = UserDataFactory.create_invalid_payload("email", invalid_value="completely_broken")
        assert payload["email"] == "completely_broken"

    def test_create_invalid_payload_unknown_field(self):
        """Test create_invalid_payload for unknown field."""
        from data_factory import UserDataFactory

        payload = UserDataFactory.create_invalid_payload("unknown_field")
        assert payload["unknown_field"] == ""


class TestAttackVectorFactory:
    """Tests for AttackVectorFactory security test utilities."""

    def test_sql_injection_payloads(self):
        """Test SQL injection payloads."""
        from data_factory import AttackVectorFactory

        payloads = AttackVectorFactory.sql_injection_payloads()
        assert isinstance(payloads, list)
        assert len(payloads) > 0
        assert "' OR '1'='1" in payloads

    def test_xss_payloads(self):
        """Test XSS payloads."""
        from data_factory import AttackVectorFactory

        payloads = AttackVectorFactory.xss_payloads()
        assert isinstance(payloads, list)
        assert len(payloads) > 0
        assert "<script>alert('XSS')</script>" in payloads

    def test_boundary_test_strings(self):
        """Test boundary test strings."""
        from data_factory import AttackVectorFactory

        strings = AttackVectorFactory.boundary_test_strings()
        assert isinstance(strings, list)
        assert len(strings) > 0
        assert "" in strings  # Empty string
        assert "🔥💯🎉" in strings  # Emoji


class TestSchemasExtended:
    """Extended tests for schemas.py."""

    def test_signup_request_schema_valid(self):
        """Test SignupRequestSchema with valid data."""
        from schemas import SignupRequestSchema

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123!",  # NOSONAR - Test data
            "confirm_password": "SecurePass123!",  # NOSONAR - Test data
        }
        schema = SignupRequestSchema(**data)
        assert schema.name == "John Doe"
        assert schema.email == "john@example.com"

    def test_signup_request_schema_name_with_numbers(self):
        """Test SignupRequestSchema rejects name with numbers."""
        from pydantic import ValidationError

        from schemas import SignupRequestSchema

        with pytest.raises(ValidationError):
            SignupRequestSchema(
                name="John123",
                email="john@example.com",
                password="SecurePass123!",  # NOSONAR - Test data
                confirm_password="SecurePass123!",  # NOSONAR - Test data
            )

    def test_signup_request_schema_password_mismatch(self):
        """Test SignupRequestSchema rejects password mismatch."""
        from pydantic import ValidationError

        from schemas import SignupRequestSchema

        with pytest.raises(ValidationError):
            SignupRequestSchema(
                name="John Doe",
                email="john@example.com",
                password="SecurePass123!",  # NOSONAR - Test data
                confirm_password="DifferentPass456!",  # NOSONAR - Test data
            )

    def test_login_request_schema(self):
        """Test LoginRequestSchema with valid data."""
        from schemas import LoginRequestSchema

        data = {"email": "user@example.com", "password": "Password123!"}  # NOSONAR - Test data
        schema = LoginRequestSchema(**data)
        assert schema.email == "user@example.com"

    def test_login_success_response_schema(self):
        """Test LoginSuccessResponseSchema."""
        from schemas import LoginSuccessResponseSchema

        data = {
            "access_token": "jwt_token_here",
            "refresh_token": "refresh_token_here",
            "token_type": "Bearer",
            "expires_in": 3600,
        }
        schema = LoginSuccessResponseSchema(**data)
        assert schema.access_token == "jwt_token_here"

    def test_user_profile_schema(self):
        """Test UserProfileSchema."""
        from schemas import UserProfileSchema

        data = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "is_active": True,
        }
        schema = UserProfileSchema(**data)
        assert schema.id == 1
        assert schema.is_active is True

    def test_performance_assertion_get_response_time(self):
        """Test PerformanceAssertion.get_response_time_ms placeholder."""
        from schemas import PerformanceAssertion

        # This is a placeholder that returns 0.0
        result = PerformanceAssertion.get_response_time_ms(None)
        assert abs(result - 0.0) < 1e-9  # Use epsilon comparison for floats
