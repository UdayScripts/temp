#!/usr/bin/env python3
"""
Test IMAP server connectivity
"""

import ssl
import socket
from imapclient import IMAPClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent / "backend"
load_dotenv(ROOT_DIR / '.env')

def test_imap_connectivity():
    """Test IMAP server connectivity"""
    try:
        print("Testing IMAP server connectivity...")
        print(f"Host: {os.environ['IMAP_HOST']}")
        print(f"Port: {os.environ['IMAP_PORT']}")
        
        # Test basic socket connection first
        print("Testing socket connection...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((os.environ['IMAP_HOST'], int(os.environ['IMAP_PORT'])))
        sock.close()
        
        if result == 0:
            print("✅ Socket connection successful")
        else:
            print(f"❌ Socket connection failed: {result}")
            return False
        
        # Test IMAP connection
        print("Testing IMAP SSL connection...")
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with IMAPClient(host=os.environ['IMAP_HOST'], port=int(os.environ['IMAP_PORT']), ssl=True, ssl_context=context) as imap_client:
            print("✅ IMAP connection successful")
            
            # Test with dummy credentials (should fail but connection works)
            try:
                imap_client.login("test@udayscripts.in", "dummy")
                print("✅ Login successful (unexpected)")
            except Exception as e:
                print(f"✅ Login failed as expected: {str(e)[:100]}...")
            
            return True
            
    except Exception as e:
        print(f"❌ IMAP test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("IMAP SERVER CONNECTIVITY TEST")
    print("=" * 60)
    
    test_imap_connectivity()