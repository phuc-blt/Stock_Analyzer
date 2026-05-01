#!/usr/bin/env python3
"""
Vietnam Stock Analyzer - Ollama Setup Script
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
            print(f"✅ Success: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False

def check_ollama_installation():
    """Check if Ollama is installed"""
    print("🔍 Checking Ollama installation...")
    
    if run_command("ollama --version", "Check Ollama version"):
        return True
    else:
        print("\n❌ Ollama is not installed!")
        print("Please install Ollama first:")
        print("1. Download from: https://ollama.com/download")
        print("2. Run the installer")
        print("3. Restart your terminal")
        return False

def check_ollama_service():
    """Check if Ollama service is running"""
    print("\n🔍 Checking Ollama service...")
    
    if run_command("curl -s http://localhost:11434/api/tags", "Check Ollama API"):
        return True
    else:
        print("\n❌ Ollama service is not running!")
        print("Please start Ollama service:")
        print("Run: ollama serve")
        return False

def check_available_models():
    """Check available models"""
    print("\n🔍 Checking available models...")
    
    success, output = run_command_with_output("ollama list", "List available models")
    if success and output.strip():
        print("✅ Available models:")
        print(output)
        return True
    else:
        print("\n❌ No models found!")
        return False

def run_command_with_output(command, description):
    """Run command and return both success and output"""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success")
            return True, result.stdout
        else:
            print(f"❌ Error: {result.stderr.strip()}")
            return False, result.stderr
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False, str(e)

def install_recommended_model():
    """Install a recommended model"""
    models = [
        ("llama3:8b", "Lightweight Llama3 (4.7GB)"),
        ("qwen:7b", "Qwen model (4.1GB)"),
        ("phi3", "Microsoft Phi3 (2.2GB)")
    ]
    
    print("\n📦 Available models to install:")
    for i, (model, desc) in enumerate(models, 1):
        print(f"{i}. {model} - {desc}")
    
    try:
        choice = input("\nSelect model to install (1-3) or press Enter for default (1): ").strip()
        if not choice:
            choice = "1"
        
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(models):
            selected_model, description = models[choice_idx]
            print(f"\n📦 Installing {selected_model} - {description}")
            
            if run_command(f"ollama pull {selected_model}", f"Pull {selected_model}"):
                print(f"✅ {selected_model} installed successfully!")
                return True
            else:
                print(f"❌ Failed to install {selected_model}")
                return False
        else:
            print("❌ Invalid choice")
            return False
    except ValueError:
        print("❌ Invalid input")
        return False

def main():
    """Main setup function"""
    print("🚀 Vietnam Stock Analyzer - Ollama Setup")
    print("=" * 50)
    
    # Step 1: Check Ollama installation
    if not check_ollama_installation():
        print("\n❌ Please install Ollama first and run this script again.")
        sys.exit(1)
    
    # Step 2: Check Ollama service
    if not check_ollama_service():
        print("\n❌ Please start Ollama service with 'ollama serve' and run this script again.")
        sys.exit(1)
    
    # Step 3: Check available models
    if not check_available_models():
        print("\n📦 No models found. Installing recommended model...")
        if not install_recommended_model():
            print("\n❌ Failed to install model. Please run 'ollama pull llama3:8b' manually.")
            sys.exit(1)
    
    # Step 4: Final verification
    print("\n🎉 Setup complete!")
    print("You can now:")
    print("1. Start the backend: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("2. Start the frontend: cd frontend && npm run dev")
    print("3. Open http://localhost:3000 in your browser")

if __name__ == "__main__":
    main()
