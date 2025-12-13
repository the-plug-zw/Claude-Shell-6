#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    COMPREHENSIVE FUNCTION TEST SUITE
    Tests all functions and classes across all Python modules
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import inspect
import traceback
from pathlib import Path

# Add workspace to path
sys.path.insert(0, os.path.dirname(__file__))

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}")
    print(f"{text}")
    print(f"{'='*80}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

class TestRunner:
    def __init__(self):
        self.results = {}
        self.total_passed = 0
        self.total_failed = 0
        self.total_skipped = 0
        self.modules = [
            'master_umbrella_setup',
            'agent_registry',
            'api_bridge',
            'communication_managers',
            'command_executor',
            'rest_api_server',
            'rat_executable_builder',
            'rat_server_fixed',
        ]

    def test_module(self, module_name):
        """Test all functions in a module"""
        print_info(f"Testing module: {module_name}")
        self.results[module_name] = {'passed': 0, 'failed': 0, 'skipped': 0, 'details': []}
        
        try:
            module = __import__(module_name)
            
            # Get all public classes and functions
            members = inspect.getmembers(module, lambda x: inspect.isclass(x) or inspect.isfunction(x))
            
            for name, obj in members:
                # Skip private/magic methods
                if name.startswith('_'):
                    continue
                
                # Skip imported items from other modules
                if inspect.getmodule(obj) != module:
                    continue
                
                if inspect.isclass(obj):
                    self.test_class(module_name, name, obj)
                elif inspect.isfunction(obj):
                    self.test_function(module_name, name, obj)
                    
        except Exception as e:
            print_error(f"Failed to import {module_name}: {str(e)}")
            self.results[module_name]['failed'] += 1
            self.total_failed += 1

    def test_class(self, module_name, class_name, class_obj):
        """Test a class by checking if it can be instantiated"""
        try:
            # Try to instantiate with no arguments
            sig = inspect.signature(class_obj.__init__)
            params = list(sig.parameters.items())
            
            # Skip 'self' parameter
            params = params[1:]
            
            # Check if __init__ requires arguments
            required_args = [p for p in params if p[1].default == inspect.Parameter.empty]
            
            if required_args:
                # Has required arguments, mark as skipped
                print_warning(f"  {class_name}: Skipped (requires constructor args: {[p[0] for p in required_args]})")
                self.results[module_name]['skipped'] += 1
                self.total_skipped += 1
                self.results[module_name]['details'].append({
                    'type': 'class',
                    'name': class_name,
                    'status': 'skipped',
                    'reason': 'Requires constructor arguments'
                })
            else:
                # Try to instantiate
                try:
                    instance = class_obj()
                    print_success(f"  {class_name}: OK (instantiated successfully)")
                    self.results[module_name]['passed'] += 1
                    self.total_passed += 1
                    self.results[module_name]['details'].append({
                        'type': 'class',
                        'name': class_name,
                        'status': 'passed'
                    })
                except Exception as e:
                    print_error(f"  {class_name}: FAILED - {str(e)}")
                    self.results[module_name]['failed'] += 1
                    self.total_failed += 1
                    self.results[module_name]['details'].append({
                        'type': 'class',
                        'name': class_name,
                        'status': 'failed',
                        'error': str(e)
                    })
        except Exception as e:
            print_error(f"  {class_name}: ERROR - {str(e)}")
            self.results[module_name]['failed'] += 1
            self.total_failed += 1

    def test_function(self, module_name, func_name, func_obj):
        """Test a function by checking its signature"""
        try:
            sig = inspect.signature(func_obj)
            params = list(sig.parameters.values())
            
            # Check if function has required arguments
            required_args = [p for p in params if p.default == inspect.Parameter.empty]
            
            # Skip main() functions and Flask route handlers
            if func_name == 'main' or hasattr(func_obj, '__self__') or 'request' in [p.name for p in params]:
                print_warning(f"  {func_name}(): Skipped (main entry point or Flask route)")
                self.results[module_name]['skipped'] += 1
                self.total_skipped += 1
                return
            
            if required_args:
                # Has required arguments, mark as skipped
                print_warning(f"  {func_name}(): Skipped (requires args: {[p.name for p in required_args]})")
                self.results[module_name]['skipped'] += 1
                self.total_skipped += 1
                self.results[module_name]['details'].append({
                    'type': 'function',
                    'name': func_name,
                    'status': 'skipped',
                    'reason': f'Requires arguments: {[p.name for p in required_args]}'
                })
            else:
                # Try to call with no arguments
                try:
                    result = func_obj()
                    print_success(f"  {func_name}(): OK")
                    self.results[module_name]['passed'] += 1
                    self.total_passed += 1
                    self.results[module_name]['details'].append({
                        'type': 'function',
                        'name': func_name,
                        'status': 'passed'
                    })
                except (RuntimeError, SystemExit) as e:
                    # Skip functions that require runtime context or exit
                    if 'request context' in str(e) or 'application context' in str(e) or 'arguments are required' in str(e):
                        print_warning(f"  {func_name}(): Skipped (requires runtime context)")
                        self.results[module_name]['skipped'] += 1
                        self.total_skipped += 1
                    else:
                        print_error(f"  {func_name}(): FAILED - {str(e)}")
                        self.results[module_name]['failed'] += 1
                        self.total_failed += 1
                        self.results[module_name]['details'].append({
                            'type': 'function',
                            'name': func_name,
                            'status': 'failed',
                            'error': str(e)
                        })
                except Exception as e:
                    print_error(f"  {func_name}(): FAILED - {str(e)}")
                    self.results[module_name]['failed'] += 1
                    self.total_failed += 1
                    self.results[module_name]['details'].append({
                        'type': 'function',
                        'name': func_name,
                        'status': 'failed',
                        'error': str(e)
                    })
        except Exception as e:
            print_error(f"  {func_name}: ERROR - {str(e)}")
            self.results[module_name]['failed'] += 1
            self.total_failed += 1

    def run_all_tests(self):
        """Run tests on all modules"""
        print_header("🧪 COMPREHENSIVE PYTHON FUNCTION TEST SUITE")
        print(f"Testing {len(self.modules)} modules...\n")
        
        for module in self.modules:
            print_header(f"Module: {module}")
            self.test_module(module)
        
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print_header("📊 TEST SUMMARY")
        
        for module_name, results in self.results.items():
            print(f"\n{Colors.BOLD}{module_name}{Colors.RESET}")
            print(f"  Passed:  {Colors.GREEN}{results['passed']}{Colors.RESET}")
            print(f"  Failed:  {Colors.RED}{results['failed']}{Colors.RESET}")
            print(f"  Skipped: {Colors.YELLOW}{results['skipped']}{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}OVERALL RESULTS{Colors.RESET}")
        print(f"  Total Passed:  {Colors.GREEN}{self.total_passed}{Colors.RESET}")
        print(f"  Total Failed:  {Colors.RED}{self.total_failed}{Colors.RESET}")
        print(f"  Total Skipped: {Colors.YELLOW}{self.total_skipped}{Colors.RESET}")
        print(f"  Total Tests:   {self.total_passed + self.total_failed + self.total_skipped}")
        
        success_rate = 0
        if (self.total_passed + self.total_failed) > 0:
            success_rate = (self.total_passed / (self.total_passed + self.total_failed)) * 100
        
        if self.total_failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ ALL TESTS PASSED!{Colors.RESET}")
            print(f"Success Rate: {Colors.GREEN}{success_rate:.1f}%{Colors.RESET}\n")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ SOME TESTS FAILED{Colors.RESET}")
            print(f"Success Rate: {Colors.RED}{success_rate:.1f}%{Colors.RESET}\n")

def main():
    runner = TestRunner()
    runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if runner.total_failed == 0 else 1)

if __name__ == '__main__':
    main()
