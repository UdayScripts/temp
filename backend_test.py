#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Temporary Email System
Tests all critical API endpoints and functionality
"""

import requests
import json
import time
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Configuration
BASE_URL = "https://d89c1895-fe9f-400d-bf96-4a56ef864fdc.preview.emergentagent.com/api"
TIMEOUT = 30

class TemporaryEmailTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.timeout = TIMEOUT
        self.created_emails = []  # Track created emails for cleanup
        
    def log(self, message: str, level: str = "INFO"):
        """Log test messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
    def test_api_health(self) -> bool:
        """Test if the API is accessible"""
        try:
            self.log("Testing API health check...")
            response = self.session.get(f"{self.base_url}/")
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ API Health Check: {data}")
                return True
            else:
                self.log(f"❌ API Health Check failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ API Health Check exception: {str(e)}", "ERROR")
            return False
    
    def test_create_temporary_email(self, expiration_minutes: int = 60) -> Optional[Dict]:
        """Test POST /api/email/create endpoint"""
        try:
            self.log(f"Testing email creation with {expiration_minutes} minutes expiration...")
            
            payload = {"expiration_minutes": expiration_minutes}
            response = self.session.post(
                f"{self.base_url}/email/create",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Email created successfully: {data['email']}")
                self.log(f"   Password: {data['password']}")
                self.log(f"   Expires at: {data['expires_at']}")
                self.log(f"   Remaining time: {data['remaining_time']} seconds")
                
                # Validate response structure
                required_fields = ['email', 'password', 'expires_at', 'remaining_time']
                for field in required_fields:
                    if field not in data:
                        self.log(f"❌ Missing field in response: {field}", "ERROR")
                        return None
                
                # Validate email format
                if '@udayscripts.in' not in data['email']:
                    self.log(f"❌ Invalid email domain: {data['email']}", "ERROR")
                    return None
                
                # Track for cleanup
                self.created_emails.append(data['email'])
                return data
                
            else:
                self.log(f"❌ Email creation failed: {response.status_code} - {response.text}", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"❌ Email creation exception: {str(e)}", "ERROR")
            return None
    
    def test_get_email_info(self, email_address: str) -> Optional[Dict]:
        """Test GET /api/email/{email_address}/info endpoint"""
        try:
            self.log(f"Testing email info retrieval for: {email_address}")
            
            response = self.session.get(f"{self.base_url}/email/{email_address}/info")
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Email info retrieved successfully")
                self.log(f"   Email: {data['email']}")
                self.log(f"   Created at: {data['created_at']}")
                self.log(f"   Expires at: {data['expires_at']}")
                self.log(f"   Remaining time: {data['remaining_time']} seconds")
                self.log(f"   Active: {data['active']}")
                self.log(f"   Last checked: {data.get('last_checked', 'Never')}")
                
                # Validate response structure
                required_fields = ['email', 'created_at', 'expires_at', 'remaining_time', 'active']
                for field in required_fields:
                    if field not in data:
                        self.log(f"❌ Missing field in response: {field}", "ERROR")
                        return None
                
                return data
                
            elif response.status_code == 404:
                self.log(f"❌ Email account not found: {email_address}", "ERROR")
                return None
            elif response.status_code == 410:
                self.log(f"❌ Email account expired: {email_address}", "ERROR")
                return None
            else:
                self.log(f"❌ Email info retrieval failed: {response.status_code} - {response.text}", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"❌ Email info retrieval exception: {str(e)}", "ERROR")
            return None
    
    def test_get_emails(self, email_address: str) -> Optional[List]:
        """Test GET /api/email/{email_address}/messages endpoint"""
        try:
            self.log(f"Testing email messages retrieval for: {email_address}")
            
            response = self.session.get(f"{self.base_url}/email/{email_address}/messages")
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Email messages retrieved successfully: {len(data)} messages")
                
                # Log details of each email
                for i, email in enumerate(data):
                    self.log(f"   Email {i+1}:")
                    self.log(f"     From: {email.get('sender', 'Unknown')}")
                    self.log(f"     Subject: {email.get('subject', 'No Subject')}")
                    self.log(f"     Date: {email.get('date', 'Unknown')}")
                    self.log(f"     UID: {email.get('uid', 'Unknown')}")
                    self.log(f"     Read: {email.get('read', False)}")
                
                # Validate email structure if emails exist
                if data:
                    required_fields = ['id', 'account_email', 'uid', 'sender', 'subject', 'date', 'body_text', 'body_html']
                    for field in required_fields:
                        if field not in data[0]:
                            self.log(f"❌ Missing field in email response: {field}", "ERROR")
                            return None
                
                return data
                
            elif response.status_code == 404:
                self.log(f"❌ Email account not found: {email_address}", "ERROR")
                return None
            else:
                self.log(f"❌ Email messages retrieval failed: {response.status_code} - {response.text}", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"❌ Email messages retrieval exception: {str(e)}", "ERROR")
            return None
    
    def test_delete_email_account(self, email_address: str) -> bool:
        """Test DELETE /api/email/{email_address} endpoint"""
        try:
            self.log(f"Testing email account deletion for: {email_address}")
            
            response = self.session.delete(f"{self.base_url}/email/{email_address}")
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✅ Email account deleted successfully: {data['message']}")
                
                # Remove from tracking list
                if email_address in self.created_emails:
                    self.created_emails.remove(email_address)
                
                return True
                
            elif response.status_code == 404:
                self.log(f"❌ Email account not found for deletion: {email_address}", "ERROR")
                return False
            else:
                self.log(f"❌ Email account deletion failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Email account deletion exception: {str(e)}", "ERROR")
            return False
    
    def test_invalid_email_handling(self) -> bool:
        """Test error handling for invalid email addresses"""
        try:
            self.log("Testing invalid email address handling...")
            
            invalid_emails = [
                "nonexistent@udayscripts.in",
                "invalid-email",
                "test@wrongdomain.com",
                ""
            ]
            
            all_passed = True
            
            for invalid_email in invalid_emails:
                self.log(f"  Testing invalid email: '{invalid_email}'")
                
                # Test info endpoint
                response = self.session.get(f"{self.base_url}/email/{invalid_email}/info")
                if response.status_code not in [404, 400, 422]:
                    self.log(f"❌ Expected 404/400/422 for invalid email info, got: {response.status_code}", "ERROR")
                    all_passed = False
                else:
                    self.log(f"✅ Correctly handled invalid email info: {response.status_code}")
                
                # Test messages endpoint
                response = self.session.get(f"{self.base_url}/email/{invalid_email}/messages")
                if response.status_code not in [404, 400, 422]:
                    self.log(f"❌ Expected 404/400/422 for invalid email messages, got: {response.status_code}", "ERROR")
                    all_passed = False
                else:
                    self.log(f"✅ Correctly handled invalid email messages: {response.status_code}")
            
            return all_passed
            
        except Exception as e:
            self.log(f"❌ Invalid email handling test exception: {str(e)}", "ERROR")
            return False
    
    def test_expiration_handling(self) -> bool:
        """Test email account expiration handling"""
        try:
            self.log("Testing email account expiration handling...")
            
            # Create email with very short expiration (1 minute)
            email_data = self.test_create_temporary_email(expiration_minutes=1)
            if not email_data:
                self.log("❌ Failed to create email for expiration test", "ERROR")
                return False
            
            email_address = email_data['email']
            
            # Wait for expiration (65 seconds to be safe)
            self.log("Waiting 65 seconds for email to expire...")
            time.sleep(65)
            
            # Try to access expired email
            info_response = self.session.get(f"{self.base_url}/email/{email_address}/info")
            if info_response.status_code == 410:
                self.log("✅ Correctly handled expired email account (410 Gone)")
                return True
            elif info_response.status_code == 404:
                self.log("✅ Expired email account not found (404) - acceptable")
                return True
            else:
                self.log(f"❌ Unexpected response for expired email: {info_response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Expiration handling test exception: {str(e)}", "ERROR")
            return False
    
    def cleanup_created_emails(self):
        """Clean up any emails created during testing"""
        self.log("Cleaning up created email accounts...")
        
        for email_address in self.created_emails.copy():
            try:
                self.test_delete_email_account(email_address)
            except Exception as e:
                self.log(f"Warning: Failed to cleanup {email_address}: {str(e)}", "WARN")
    
    def run_comprehensive_test(self) -> Dict[str, bool]:
        """Run all tests and return results"""
        results = {}
        
        self.log("=" * 60)
        self.log("STARTING COMPREHENSIVE BACKEND API TESTING")
        self.log("=" * 60)
        
        try:
            # Test 1: API Health Check
            results['api_health'] = self.test_api_health()
            
            if not results['api_health']:
                self.log("❌ API is not accessible. Stopping tests.", "ERROR")
                return results
            
            # Test 2: Create Temporary Email
            results['email_creation'] = False
            email_data = self.test_create_temporary_email()
            if email_data:
                results['email_creation'] = True
                test_email = email_data['email']
                
                # Test 3: Get Email Info
                results['email_info'] = self.test_get_email_info(test_email) is not None
                
                # Test 4: Get Email Messages
                results['email_messages'] = self.test_get_emails(test_email) is not None
                
                # Test 5: Delete Email Account
                results['email_deletion'] = self.test_delete_email_account(test_email)
            else:
                results['email_info'] = False
                results['email_messages'] = False
                results['email_deletion'] = False
            
            # Test 6: Invalid Email Handling
            results['invalid_email_handling'] = self.test_invalid_email_handling()
            
            # Test 7: Expiration Handling (optional - takes time)
            # Uncomment if you want to test expiration
            # results['expiration_handling'] = self.test_expiration_handling()
            
        except Exception as e:
            self.log(f"❌ Critical error during testing: {str(e)}", "ERROR")
        
        finally:
            # Cleanup
            self.cleanup_created_emails()
        
        return results
    
    def print_test_summary(self, results: Dict[str, bool]):
        """Print a summary of test results"""
        self.log("=" * 60)
        self.log("TEST RESULTS SUMMARY")
        self.log("=" * 60)
        
        total_tests = len(results)
        passed_tests = sum(1 for result in results.values() if result)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log(f"{test_name.replace('_', ' ').title()}: {status}")
        
        self.log("-" * 60)
        self.log(f"OVERALL: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            self.log("🎉 ALL TESTS PASSED!")
        else:
            self.log(f"⚠️  {total_tests - passed_tests} tests failed")
        
        return passed_tests == total_tests

def main():
    """Main test execution"""
    tester = TemporaryEmailTester()
    
    try:
        results = tester.run_comprehensive_test()
        all_passed = tester.print_test_summary(results)
        
        # Exit with appropriate code
        sys.exit(0 if all_passed else 1)
        
    except KeyboardInterrupt:
        tester.log("Testing interrupted by user", "WARN")
        tester.cleanup_created_emails()
        sys.exit(1)
    except Exception as e:
        tester.log(f"Critical error: {str(e)}", "ERROR")
        tester.cleanup_created_emails()
        sys.exit(1)

if __name__ == "__main__":
    main()