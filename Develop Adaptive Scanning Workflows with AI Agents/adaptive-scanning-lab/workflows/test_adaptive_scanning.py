import asyncio
import json
from workflows.orchestrator import WorkflowOrchestrator
from agents.scanning_agent import AdaptiveScanningAgent
from setup_test_environment import setup_test_targets

async def main():
    print("=== Adaptive Scanning Workflow Test ===")
    
    # Setup test environment
    targets = setup_test_targets()
    
    # Initialize orchestrator and agents
    orchestrator = WorkflowOrchestrator()
    scan_agent = AdaptiveScanningAgent()
    
    # Register agents
    orchestrator.register_agent('scanner', scan_agent)
    
    # Create adaptive workflow
    workflow = orchestrator.create_adaptive_workflow('test_workflow', targets)
    print(f"Created workflow: {workflow['name']}")
    
    # Execute workflow
    print("\nExecuting adaptive scanning workflow...")
    result = await orchestrator.execute_workflow('test_workflow')
    
    # Display results
    print("\n=== Workflow Results ===")
    print(f"Status: {result['status']}")
    
    for key, scan_result in result['results'].items():
        print(f"\n{key}:")
        if 'error' in scan_result:
            print(f"  Error: {scan_result['error']}")
        else:
            print(f"  Target: {scan_result['target']}")
            print(f"  Scan params: {scan_result['scan_params']}")
            if scan_result['results']:
                print(f"  Results available: Yes")
            else:
                print(f"  Results available: No")
    
    # Save results
    with open('logs/workflow_results.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    # Save agent learning data
    scan_agent.save_state('logs/agent_state.json')
    
    print(f"\nResults saved to logs/")
    print(f"Agent logged {len(scan_agent.learning_data)} actions")

if __name__ == "__main__":
    asyncio.run(main())
