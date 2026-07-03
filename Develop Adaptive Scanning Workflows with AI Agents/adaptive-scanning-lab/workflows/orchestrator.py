import asyncio
import json
import time
from agents.scanning_agent import AdaptiveScanningAgent

class WorkflowOrchestrator:
    def __init__(self):
        self.agents = {}
        self.workflows = {}
        self.results = []
        
    def register_agent(self, agent_name, agent):
        self.agents[agent_name] = agent
        
    def create_adaptive_workflow(self, workflow_name, targets):
        """Create an adaptive scanning workflow"""
        workflow = {
            'name': workflow_name,
            'targets': targets,
            'status': 'created',
            'steps': [],
            'results': {}
        }
        self.workflows[workflow_name] = workflow
        return workflow
    
    async def execute_workflow(self, workflow_name):
        """Execute adaptive workflow with AI decision making"""
        workflow = self.workflows[workflow_name]
        workflow['status'] = 'running'
        
        scan_agent = self.agents.get('scanner')
        if not scan_agent:
            return {'error': 'No scanning agent registered'}
        
        for target in workflow['targets']:
            print(f"Processing target: {target}")
            
            # Initialize target data
            target_data = {
                'target': target,
                'previous_scans': [],
                'open_ports': [],
                'services': []
            }
            
            # Adaptive scanning loop
            for iteration in range(3):  # Max 3 adaptive iterations
                print(f"  Iteration {iteration + 1}")
                
                # AI analysis
                analysis = scan_agent.analyze(target_data)
                print(f"    Analysis: {analysis}")
                
                # AI decision
                decision = scan_agent.decide(analysis)
                print(f"    Decision: {decision}")
                
                # Execute scan
                scan_result = scan_agent.execute_scan(target, decision)
                
                # Update target data for next iteration
                if 'results' in scan_result and scan_result['results']:
                    host_data = scan_result['results']
                    if 'tcp' in host_data:
                        target_data['open_ports'].extend(
                            [port for port, data in host_data['tcp'].items() 
                             if data['state'] == 'open']
                        )
                    target_data['previous_scans'].append(scan_result)
                
                # Store results
                workflow['results'][f"{target}_iteration_{iteration}"] = scan_result
                
                # Adaptive delay
                await asyncio.sleep(2)
            
        workflow['status'] = 'completed'
        return workflow
