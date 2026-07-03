import asyncio
import json
from workflows.orchestrator import WorkflowOrchestrator
from agents.scanning_agent import AdaptiveScanningAgent

class EnhancedScanningAgent(AdaptiveScanningAgent):
    def __init__(self, name="EnhancedScanAgent"):
        super().__init__(name)
        self.threat_score = 0
        self.scan_history = {}
    
    def analyze(self, target_data):
        """Enhanced analysis with threat scoring"""
        target = target_data['target']
        
        # Initialize history for new targets
        if target not in self.scan_history:
            self.scan_history[target] = {'scans': 0, 'findings': 0}
        
        history = self.scan_history[target]
        open_ports = target_data.get('open_ports', [])
        
        # Calculate threat score
        threat_score = len(open_ports) * 10
        if any(port in [21, 23, 135, 139, 445] for port in open_ports):
            threat_score += 50  # High-risk ports
        
        self.threat_score = threat_score
        history['scans'] += 1
        
        # Adaptive recommendations based on threat score and history
        if threat_score > 100:
            return {'recommendation': 'aggressive_scan', 'confidence': 0.9, 'threat_score': threat_score}
        elif threat_score > 50:
            return {'recommendation': 'thorough_scan', 'confidence': 0.8, 'threat_score': threat_score}
        elif history['scans'] == 1:
            return {'recommendation': 'initial_scan', 'confidence': 0.7, 'threat_score': threat_score}
        else:
            return {'recommendation': 'maintenance_scan', 'confidence': 0.6, 'threat_score': threat_score}

async def test_enhanced_adaptation():
    print("=== Enhanced Adaptive Scanning Test ===")
    
    # Create multiple test scenarios
    targets = ['127.0.0.1', '127.0.0.1']  # Same target, different iterations
    
    orchestrator = WorkflowOrchestrator()
    enhanced_agent = EnhancedScanningAgent()
    orchestrator.register_agent('scanner', enhanced_agent)
    
    # Create and execute workflow
    workflow = orchestrator.create_adaptive_workflow('enhanced_test', targets)
    result = await orchestrator.execute_workflow('enhanced_test')
    
    print(f"\nFinal threat score: {enhanced_agent.threat_score}")
    print(f"Scan history: {enhanced_agent.scan_history}")
    
    # Save enhanced results
    with open('logs/enhanced_results.json', 'w') as f:
        json.dump({
            'workflow_result': result,
            'threat_score': enhanced_agent.threat_score,
            'scan_history': enhanced_agent.scan_history
        }, f, indent=2)
    
    print("Enhanced test completed. Results saved to logs/enhanced_results.json")

if __name__ == "__main__":
    asyncio.run(test_enhanced_adaptation())
