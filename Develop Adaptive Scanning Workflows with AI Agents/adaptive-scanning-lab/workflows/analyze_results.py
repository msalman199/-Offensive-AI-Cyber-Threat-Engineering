import json

def analyze_workflow_results():
    """Analyze the adaptive behavior of the scanning workflow"""
    
    try:
        with open('logs/workflow_results.json', 'r') as f:
            results = json.load(f)
        
        with open('logs/agent_state.json', 'r') as f:
            agent_state = json.load(f)
    except FileNotFoundError:
        print("Results files not found. Run the test first.")
        return
    
    print("=== Adaptive Scanning Analysis ===")
    print(f"Workflow Status: {results['status']}")
    print(f"Total Targets: {len(results.get('targets', []))}")
    print(f"Total Scan Iterations: {len(results['results'])}")
    
    print("\n=== Agent Learning Analysis ===")
    learning_data = agent_state['learning_data']
    print(f"Total Actions Logged: {len(learning_data)}")
    
    # Analyze scan progression
    scan_actions = [action for action in learning_data if action['action'] == 'scan_executed']
    
    if scan_actions:
        print("\n=== Scan Progression ===")
        for i, action in enumerate(scan_actions):
            result = action['result']
            print(f"Scan {i+1}:")
            print(f"  Technique: {result['scan_params']['technique']}")
            print(f"  Ports: {result['scan_params']['ports']}")
            print(f"  Timing: {result['scan_params']['timing']}")
    
    # Check for adaptive behavior
    techniques_used = set()
    for action in scan_actions:
        techniques_used.add(action['result']['scan_params']['technique'])
    
    print(f"\n=== Adaptation Evidence ===")
    print(f"Different techniques used: {len(techniques_used)}")
    print(f"Techniques: {list(techniques_used)}")
    
    if len(techniques_used) > 1:
        print("✓ Adaptive behavior detected - multiple techniques used")
    else:
        print("⚠ Limited adaptation - consider enhancing AI logic")

if __name__ == "__main__":
    analyze_workflow_results()
