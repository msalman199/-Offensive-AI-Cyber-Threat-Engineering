import subprocess
import time

def setup_test_targets():
    """Set up local test services for scanning"""
    print("Setting up test environment...")
    
    # Start a simple HTTP server
    try:
        subprocess.Popen(['python3', '-m', 'http.server', '8080'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Started HTTP server on port 8080")
    except:
        print("Could not start HTTP server")
    
    # Start SSH service if available
    try:
        subprocess.run(['sudo', 'systemctl', 'start', 'ssh'], 
                      capture_output=True)
        print("SSH service started")
    except:
        print("SSH service not available")
    
    time.sleep(2)
    return ['127.0.0.1']

if __name__ == "__main__":
    targets = setup_test_targets()
    print(f"Test targets ready: {targets}")
