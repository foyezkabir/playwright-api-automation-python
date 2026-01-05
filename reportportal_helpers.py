"""
ReportPortal Integration Utilities
Provides helper functions for enhanced ReportPortal reporting with AI-powered analytics.
"""
import os
import json
from typing import Dict, Any, Optional
from datetime import datetime


class ReportPortalHelper:
    """Helper class for ReportPortal integration."""
    
    @staticmethod
    def is_enabled() -> bool:
        """Check if ReportPortal is enabled."""
        return os.getenv("REPORT_PORTAL_ENABLED", "false").lower() == "true"
    
    @staticmethod
    def log_request(test_name: str, method: str, url: str, payload: Dict = None, headers: Dict = None):
        """
        Logs API request details to ReportPortal.
        
        Args:
            test_name: Name of the test
            method: HTTP method
            url: Request URL
            payload: Request payload
            headers: Request headers
        """
        if not ReportPortalHelper.is_enabled():
            return
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            request_info = {
                "test": test_name,
                "method": method,
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
            
            if payload:
                request_info["payload"] = payload
            
            if headers:
                # Mask sensitive headers
                masked_headers = {k: "***" if k.lower() in ["authorization", "api-key"] else v 
                                 for k, v in headers.items()}
                request_info["headers"] = masked_headers
            
            logger.info(f"📤 API Request: {json.dumps(request_info, indent=2)}")
        except Exception as e:
            print(f"Failed to log request to ReportPortal: {e}")
    
    @staticmethod
    def log_response(test_name: str, status_code: int, response_body: Any, response_time_ms: float = None):
        """
        Logs API response details to ReportPortal.
        
        Args:
            test_name: Name of the test
            status_code: HTTP status code
            response_body: Response body
            response_time_ms: Response time in milliseconds
        """
        if not ReportPortalHelper.is_enabled():
            return
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            response_info = {
                "test": test_name,
                "status_code": status_code,
                "timestamp": datetime.now().isoformat()
            }
            
            if response_time_ms:
                response_info["response_time_ms"] = response_time_ms
            
            if response_body:
                response_info["body"] = response_body
            
            logger.info(f"📥 API Response: {json.dumps(response_info, indent=2)}")
        except Exception as e:
            print(f"Failed to log response to ReportPortal: {e}")
    
    @staticmethod
    def log_bug(bug_id: str, description: str, severity: str = "HIGH"):
        """
        Logs a bug to ReportPortal with AI-powered categorization.
        
        Args:
            bug_id: Bug identifier
            description: Bug description
            severity: Bug severity (LOW, MEDIUM, HIGH, CRITICAL)
        """
        if not ReportPortalHelper.is_enabled():
            return
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            bug_info = {
                "bug_id": bug_id,
                "description": description,
                "severity": severity,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.error(f"🐛 Bug Found: {json.dumps(bug_info, indent=2)}")
        except Exception as e:
            print(f"Failed to log bug to ReportPortal: {e}")
    
    @staticmethod
    def add_screenshot(screenshot_path: str, description: str = "Screenshot"):
        """
        Adds a screenshot attachment to ReportPortal.
        
        Args:
            screenshot_path: Path to screenshot file
            description: Screenshot description
        """
        if not ReportPortalHelper.is_enabled():
            return
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            with open(screenshot_path, 'rb') as image_file:
                logger.info(
                    description,
                    extra={"attachment": {
                        "name": description,
                        "data": image_file.read(),
                        "mime": "image/png"
                    }}
                )
        except Exception as e:
            print(f"Failed to add screenshot to ReportPortal: {e}")
    
    @staticmethod
    def add_json_attachment(data: Dict, name: str = "API Response"):
        """
        Adds JSON data as attachment to ReportPortal.
        
        Args:
            data: Dictionary to attach
            name: Attachment name
        """
        if not ReportPortalHelper.is_enabled():
            return
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            json_data = json.dumps(data, indent=2)
            logger.info(
                name,
                extra={"attachment": {
                    "name": name,
                    "data": json_data,
                    "mime": "application/json"
                }}
            )
        except Exception as e:
            print(f"Failed to add JSON attachment to ReportPortal: {e}")
    
    @staticmethod
    def set_test_description(description: str):
        """
        Sets description for current test in ReportPortal.
        
        Args:
            description: Test description
        """
        if not ReportPortalHelper.is_enabled():
            return
        
        try:
            from reportportal_client import RPLogger
            logger = logging.getLogger(__name__)
            logger.info(f"Test Description: {description}")
        except Exception as e:
            pass
    
    @staticmethod
    def add_attributes(**kwargs):
        """
        Adds custom attributes to current test in ReportPortal.
        
        Args:
            **kwargs: Key-value pairs for attributes
        """
        if not ReportPortalHelper.is_enabled():
            return
        
        try:
            import logging
            logger = logging.getLogger(__name__)
            
            for key, value in kwargs.items():
                logger.info(f"Attribute: {key} = {value}")
        except Exception as e:
            pass


# Pytest fixtures for ReportPortal integration

def pytest_configure(config):
    """Configure ReportPortal integration."""
    if ReportPortalHelper.is_enabled():
        print("\n" + "="*50)
        print("🚀 ReportPortal Integration ENABLED")
        print("="*50)
        rp_endpoint = os.getenv("RP_ENDPOINT")
        rp_project = os.getenv("RP_PROJECT")
        print(f"Endpoint: {rp_endpoint}")
        print(f"Project: {rp_project}")
        print("="*50 + "\n")


def pytest_collection_finish(session):
    """Called after test collection is completed."""
    if ReportPortalHelper.is_enabled():
        test_count = len(session.items)
        print(f"\n📊 Collected {test_count} tests for ReportPortal execution\n")
