#!/usr/bin/env python3
"""
Test cPanel API connectivity and credentials
"""

import requests
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent / "backend"
load_dotenv(ROOT_DIR / '.env')

def test_cpanel_connectivity():
    """Test basic cPanel API connectivity"""
    try:
        print("Testing cPanel API connectivity...")
        print(f"Host: {os.environ['CPANEL_HOST']}")
        print(f"User: {os.environ['CPANEL_USER']}")
        print(f"Domain: {os.environ['DOMAIN']}")
        
        # Test basic API endpoint
        url = f"{os.environ['CPANEL_HOST']}/execute/Features/list_features"
        headers = {
            "Authorization": f"cpanel {os.environ['CPANEL_USER']}:{os.environ['CPANEL_TOKEN']}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        print(f"Testing URL: {url}")
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("✅ cPanel API is accessible")
            return True
        else:
            print("❌ cPanel API access failed")
            return False
            
    except Exception as e:
        print(f"❌ cPanel API test failed: {str(e)}")
        return False

def test_email_list():
    """Test listing existing email accounts"""
    try:
        print("\nTesting email account listing...")
        
        url = f"{os.environ['CPANEL_HOST']}/execute/Email/list_pops"
        headers = {
            "Authorization": f"cpanel {os.environ['CPANEL_USER']}:{os.environ['CPANEL_TOKEN']}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            print("✅ Email listing works")
            return True
        else:
            print("❌ Email listing failed")
            return False
            
    except Exception as e:
        print(f"❌ Email listing test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("CPANEL API CONNECTIVITY TEST")
    print("=" * 60)
    
    test_cpanel_connectivity()
    test_email_list()