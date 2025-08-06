#!/usr/bin/env python3
"""
TCP Implementation Diagnostic Tool for Pyrofork
Deep analysis to identify specific issues in TCP transport
"""

import asyncio
import sys
import time
import traceback
import socket
import ssl
import os
from typing import Dict, Any, List, Tuple, Optional
import logging

# Setup path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '../../../../../'))
sys.path.insert(0, root_dir)

# Import TCP implementation
try:
    from pyrogram.connection.transport.tcp import TCP
    print("Successfully imported TCP from local source")
except ImportError as e:
    print(f"Failed to import TCP: {e}")
    sys.exit(1)

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

class TCPDiagnostics:
    """Diagnostic tools for TCP implementation analysis"""
    
    def __init__(self):
        self.telegram_servers = [
            ("149.154.175.50", 443, "DC1-Miami"),
            ("149.154.167.51", 443, "DC2-Amsterdam"),
            ("149.154.175.100", 443, "DC3-Miami"), 
            ("149.154.167.91", 443, "DC4-Amsterdam"),
            ("91.108.56.130", 443, "DC5-Singapore"),
        ]

    async def test_raw_socket_connection(self, host: str, port: int, name: str) -> Dict[str, Any]:
        """Test raw socket connection without Pyrofork TCP wrapper"""
        print(f"\n[RAW SOCKET] Testing {name} ({host}:{port})")
        
        start_time = time.time()
        sock = None
        
        try:
            # Create raw socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10.0)
            
            # Test connection
            sock.connect((host, port))
            connect_time = time.time() - start_time
            
            # Test basic send/receive
            test_data = b'GET / HTTP/1.1\r\nHost: ' + host.encode() + b'\r\n\r\n'
            sock.send(test_data)
            
            # Try to receive response
            try:
                response = sock.recv(1024)
                received_data = len(response) > 0
            except socket.timeout:
                received_data = False
            
            sock.close()
            sock = None
            
            result = {
                "success": True,
                "connect_time": connect_time,
                "received_data": received_data,
                "error": None
            }
            
            print(f"[RAW SOCKET] {name}: SUCCESS - {connect_time:.2f}s")
            return result
            
        except Exception as e:
            if sock:
                sock.close()
            
            error_time = time.time() - start_time
            print(f"[RAW SOCKET] {name}: FAILED - {str(e)} ({error_time:.2f}s)")
            
            return {
                "success": False,
                "connect_time": error_time,
                "received_data": False,
                "error": str(e)
            }

    async def test_tcp_implementation(self, host: str, port: int, name: str) -> Dict[str, Any]:
        """Test Pyrofork TCP implementation with detailed logging"""
        print(f"\n[PYROFORK TCP] Testing {name} ({host}:{port})")
        
        start_time = time.time()
        tcp = None
        
        try:
            # Initialize TCP transport
            print(f"[PYROFORK TCP] Initializing TCP transport...")
            tcp = TCP(ipv6=False, proxy=None)
            
            print(f"[PYROFORK TCP] TCP object created: {type(tcp)}")
            print(f"[PYROFORK TCP] TCP attributes: {dir(tcp)}")
            
            # Attempt connection
            print(f"[PYROFORK TCP] Attempting connection...")
            await asyncio.wait_for(tcp.connect((host, port)), timeout=10.0)
            
            connect_time = time.time() - start_time
            print(f"[PYROFORK TCP] Connection established in {connect_time:.2f}s")
            
            # Test send operation
            print(f"[PYROFORK TCP] Testing send operation...")
            test_data = b'\x00\x00\x00\x00\x00\x00\x00\x00'
            await tcp.send(test_data)
            print(f"[PYROFORK TCP] Send operation successful")
            
            # Test receive operation
            print(f"[PYROFORK TCP] Testing receive operation...")
            try:
                response = await asyncio.wait_for(tcp.recv(8), timeout=3.0)
                received_data = len(response) > 0 if response else False
                print(f"[PYROFORK TCP] Received {len(response) if response else 0} bytes")
            except asyncio.TimeoutError:
                received_data = False
                print(f"[PYROFORK TCP] Receive timeout (normal for test data)")
            
            # Clean close
            print(f"[PYROFORK TCP] Closing connection...")
            await tcp.close()
            tcp = None
            print(f"[PYROFORK TCP] Connection closed successfully")
            
            result = {
                "success": True,
                "connect_time": connect_time,
                "received_data": received_data,
                "error": None
            }
            
            print(f"[PYROFORK TCP] {name}: SUCCESS - {connect_time:.2f}s")
            return result
            
        except Exception as e:
            error_time = time.time() - start_time
            print(f"[PYROFORK TCP] {name}: FAILED - {str(e)}")
            print(f"[PYROFORK TCP] Exception details:")
            traceback.print_exc()
            
            # Cleanup
            if tcp:
                try:
                    await tcp.close()
                except:
                    pass
            
            return {
                "success": False,
                "connect_time": error_time,
                "received_data": False,
                "error": str(e)
            }

    async def inspect_tcp_implementation(self):
        """Inspect TCP class implementation details"""
        print(f"\n[INSPECTION] Analyzing TCP implementation...")
        
        try:
            tcp = TCP(ipv6=False, proxy=None)
            
            print(f"[INSPECTION] TCP class: {TCP}")
            print(f"[INSPECTION] TCP module: {TCP.__module__}")
            print(f"[INSPECTION] TCP file: {TCP.__module__.replace('.', os.sep)}.py")
            
            # Check methods
            methods = [attr for attr in dir(tcp) if not attr.startswith('_')]
            print(f"[INSPECTION] Available methods: {methods}")
            
            # Check for required methods
            required_methods = ['connect', 'send', 'recv', 'close']
            for method in required_methods:
                if hasattr(tcp, method):
                    method_obj = getattr(tcp, method)
                    print(f"[INSPECTION] {method}: {method_obj} (callable: {callable(method_obj)})")
                else:
                    print(f"[INSPECTION] MISSING METHOD: {method}")
            
            # Check initialization parameters
            print(f"[INSPECTION] TCP instance attributes:")
            for attr in dir(tcp):
                if not attr.startswith('__'):
                    try:
                        value = getattr(tcp, attr)
                        if not callable(value):
                            print(f"[INSPECTION]   {attr}: {value}")
                    except:
                        print(f"[INSPECTION]   {attr}: <unable to access>")
            
        except Exception as e:
            print(f"[INSPECTION] Error during inspection: {e}")
            traceback.print_exc()

    async def test_concurrent_simple(self, host: str, port: int, count: int = 3) -> Dict[str, Any]:
        """Simple concurrent connection test"""
        print(f"\n[CONCURRENT] Testing {count} concurrent connections to {host}:{port}")
        
        async def single_connect():
            try:
                tcp = TCP(ipv6=False, proxy=None)
                await asyncio.wait_for(tcp.connect((host, port)), timeout=5.0)
                await tcp.close()
                return True
            except Exception as e:
                print(f"[CONCURRENT] Connection failed: {str(e)[:50]}")
                return False
        
        start_time = time.time()
        tasks = [single_connect() for _ in range(count)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.time() - start_time
        
        successful = sum(1 for r in results if r is True)
        success_rate = (successful / count) * 100
        
        print(f"[CONCURRENT] Results: {successful}/{count} successful ({success_rate:.1f}%) in {total_time:.2f}s")
        
        return {
            "successful": successful,
            "total": count,
            "success_rate": success_rate,
            "total_time": total_time
        }

    async def run_diagnostic_suite(self):
        """Run comprehensive diagnostic tests"""
        print("="*80)
        print("TCP IMPLEMENTATION DIAGNOSTIC SUITE")
        print("="*80)
        
        # Phase 1: Inspect implementation
        await self.inspect_tcp_implementation()
        
        # Phase 2: Raw socket tests (baseline)
        print(f"\n" + "="*50)
        print("PHASE 1: RAW SOCKET BASELINE TESTS")
        print("="*50)
        
        raw_results = []
        for host, port, name in self.telegram_servers:
            result = await self.test_raw_socket_connection(host, port, name)
            raw_results.append((name, result))
            await asyncio.sleep(0.5)
        
        # Phase 3: Pyrofork TCP tests
        print(f"\n" + "="*50)
        print("PHASE 2: PYROFORK TCP IMPLEMENTATION TESTS")
        print("="*50)
        
        tcp_results = []
        for host, port, name in self.telegram_servers:
            result = await self.test_tcp_implementation(host, port, name)
            tcp_results.append((name, result))
            await asyncio.sleep(1.0)
        
        # Phase 4: Concurrent test
        print(f"\n" + "="*50)
        print("PHASE 3: CONCURRENT CONNECTION TEST")
        print("="*50)
        
        concurrent_result = await self.test_concurrent_simple(
            self.telegram_servers[0][0], 
            self.telegram_servers[0][1]
        )
        
        # Analysis and recommendations
        print(f"\n" + "="*50)
        print("DIAGNOSTIC ANALYSIS")
        print("="*50)
        
        raw_success = sum(1 for _, r in raw_results if r["success"])
        tcp_success = sum(1 for _, r in tcp_results if r["success"])
        
        print(f"\nResults Summary:")
        print(f"  Raw Socket Success: {raw_success}/{len(raw_results)} ({raw_success/len(raw_results)*100:.1f}%)")
        print(f"  Pyrofork TCP Success: {tcp_success}/{len(tcp_results)} ({tcp_success/len(tcp_results)*100:.1f}%)")
        print(f"  Concurrent Success: {concurrent_result['success_rate']:.1f}%")
        
        print(f"\nDiagnostic Findings:")
        
        if raw_success < len(raw_results) * 0.8:
            print("  - Network connectivity issues detected")
            print("  - Check firewall, DNS resolution, or internet connection")
        else:
            print("  - Network connectivity is good (raw sockets work)")
        
        if tcp_success < raw_success:
            print("  - Pyrofork TCP implementation has issues")
            print("  - TCP wrapper is failing where raw sockets succeed")
            print("  - Likely issues: async/await implementation, connection state management")
        elif tcp_success == raw_success:
            print("  - Pyrofork TCP implementation matches raw socket performance")
            print("  - Implementation appears correct")
        
        if concurrent_result['success_rate'] > tcp_success / len(tcp_results) * 100:
            print("  - Concurrent connections work better than sequential")
            print("  - Possible timing or state management issue in sequential testing")
        
        # Specific recommendations
        print(f"\nRecommendations:")
        
        if tcp_success < raw_success:
            print("  1. Review TCP.connect() implementation for async/await correctness")
            print("  2. Check socket state management and cleanup")
            print("  3. Verify timeout handling in async operations")
            print("  4. Test with simpler connection sequence")
        
        if raw_success < len(raw_results):
            print("  1. Check network connectivity to Telegram servers")
            print("  2. Verify DNS resolution")
            print("  3. Check for firewall blocking connections")
        
        return {
            "raw_results": raw_results,
            "tcp_results": tcp_results,
            "concurrent_result": concurrent_result
        }


async def main():
    """Main diagnostic execution"""
    try:
        diagnostics = TCPDiagnostics()
        results = await diagnostics.run_diagnostic_suite()
        
        # Determine if ready for debugging or needs environment fixes
        tcp_success_rate = sum(1 for _, r in results["tcp_results"] if r["success"]) / len(results["tcp_results"])
        raw_success_rate = sum(1 for _, r in results["raw_results"] if r["success"]) / len(results["raw_results"])
        
        if raw_success_rate < 0.8:
            print(f"\nStatus: Environment issues detected - fix network connectivity first")
            sys.exit(2)
        elif tcp_success_rate < 0.5:
            print(f"\nStatus: TCP implementation issues detected - needs code review")
            sys.exit(1)
        else:
            print(f"\nStatus: Implementation appears functional - investigate edge cases")
            sys.exit(0)
        
    except KeyboardInterrupt:
        print("\nDiagnostic interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nUnexpected error in diagnostic: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("TCP Implementation Diagnostic Tool")
    print("Deep analysis of Pyrofork TCP transport issues")
    print("-" * 60)
    
    asyncio.run(main())