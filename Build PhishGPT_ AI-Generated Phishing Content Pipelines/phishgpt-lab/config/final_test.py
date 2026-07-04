#!/usr/bin/env python3
from phishing_pipeline import PhishingPipeline
import json

def final_comprehensive_test():
    print("=== Final PhishGPT Pipeline Test ===")
    
    pipeline = PhishingPipeline()
    
    # Comprehensive target list
    targets = [
        {'name': 'Test User 1', 'email': 'test1@example.com', 'phone': '+1555000001'},
        {'name': 'Test User 2', 'email': 'test2@example.com', 'phone': '+1555000002'},
        {'name': 'Test User 3', 'email': 'test3@example.com', 'phone': '+1555000003'}
    ]
    
    # Test all content types and scenarios
    test_configs = [
        {
            'name': 'Banking Campaign',
            'config': {
                'content_types': ['email', 'sms', 'form'],
                'email_type': 'banking',
                'sms_type': 'banking',
                'form_type': 'login'
            }
        },
        {
            'name': 'Social Media Campaign',
            'config': {
                'content_types': ['email', 'form'],
                'email_type': 'social',
                'form_type': 'survey'
            }
        },
        {
            'name': 'Corporate Campaign',
            'config': {
                'content_types': ['email', 'sms', 'form'],
                'email_type': 'corporate',
                'sms_type': 'delivery',
                'form_type': 'support'
            }
        }
    ]
    
    results = []
    for test in test_configs:
        print(f"\nRunning {test['name']}...")
        try:
            result = pipeline.run_campaign(targets, test['config'])
            results.append({
                'name': test['name'],
                'status': 'SUCCESS',
                'emails': len(result['results']['emails']),
                'sms': len(result['results']['sms']),
                'forms': len(result['results']['forms'])
            })
            print(f"✓ {test['name']} completed successfully")
        except Exception as e:
            results.append({
                'name': test['name'],
                'status': 'FAILED',
                'error': str(e)
            })
            print(f"✗ {test['name']} failed: {e}")
    
    # Summary
    print("\n=== Test Summary ===")
    for result in results:
        if result['status'] == 'SUCCESS':
            print(f"✓ {result['name']}: {result['emails']} emails, {result['sms']} SMS, {result['forms']} forms")
        else:
            print(f"✗ {result['name']}: {result['error']}")
    
    return results

if __name__ == "__main__":
    final_comprehensive_test()
