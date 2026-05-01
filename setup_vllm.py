#!/usr/bin/env python3
"""
Vietnam Stock Analyzer - vLLM Setup Script
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success")
            return True
        else:
            print(f"❌ Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def install_vllm():
    """Install vLLM"""
    print("🚀 Installing vLLM...")
    
    if run_command("pip install vllm", "Install vLLM"):
        print("✅ vLLM installed successfully!")
        return True
    else:
        print("❌ Failed to install vLLM")
        return False

def test_vllm_import():
    """Test vLLM import"""
    print("\n🔍 Testing vLLM import...")
    
    try:
        from vllm import LLM
        print("✅ vLLM import successful!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {str(e)}")
        return False

def test_vllm_basic():
    """Test basic vLLM functionality"""
    print("\n🔍 Testing vLLM basic functionality...")
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
        from app.services.llm import llm_router
        
        # Test vLLM connection
        print("1. Testing vLLM connection...")
        llm = llm_router.get_vllm()
        print("✅ vLLM connection successful!")
        
        # Test simple response
        print("2. Testing simple response...")
        response = llm_router.invoke("Say hello")
        print(f"✅ Response: {response}")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def check_gpu_support():
    """Check GPU support for vLLM"""
    print("\n🔍 Checking GPU support...")
    
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name()}")
            print(f"📊 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
            return True
        else:
            print("⚠️  CUDA not available - vLLM will use CPU (slower)")
            print("💡 For better performance, consider GPU acceleration")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed - cannot check GPU")
        return False

def main():
    """Main setup function"""
    print("🚀 Vietnam Stock Analyzer - vLLM Setup")
    print("=" * 50)
    
    # Step 1: Check GPU support
    gpu_available = check_gpu_support()
    
    # Step 2: Install vLLM
    if not install_vllm():
        print("\n❌ vLLM installation failed")
        sys.exit(1)
    
    # Step 3: Test import
    if not test_vllm_import():
        print("\n❌ vLLM import test failed")
        sys.exit(1)
    
    # Step 4: Test basic functionality
    if not test_vllm_basic():
        print("\n❌ vLLM functionality test failed")
        print("💡 This might be normal if no model is available")
        print("📋 Next steps:")
        print("   1. Start the backend server")
        print("   2. Test with frontend")
        print("   3. vLLM will be prioritized over Ollama")
        return
    
    print("\n🎉 vLLM setup completed successfully!")
    
    print("\n📋 vLLM Benefits:")
    print("• 🚀 Much faster inference than Ollama")
    print("• 🔧 Better resource utilization")
    print("• 📈 Improved multi-agent performance")
    print("• ⚡ Optimized for production use")
    
    if gpu_available:
        print("• 🎮 GPU acceleration available")
    else:
        print("• 💻 CPU mode (consider GPU for better performance)")
    
    print("\n🔧 Usage:")
    print("• vLLM is now prioritized in LLM router")
    print("• Multi-agent analysis will be much faster")
    print("• Falls back to Ollama if vLLM fails")

if __name__ == "__main__":
    main()
