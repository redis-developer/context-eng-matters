#!/usr/bin/env python3
"""
Test script to diagnose OpenAI API connection issues.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent / ".env"
print(f"Loading .env from: {env_path}")
load_dotenv(env_path)

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key prefix: {api_key[:20]}...")

print("\n" + "="*80)
print("Test 1: Direct socket connection")
print("="*80)

import socket
import ssl

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    print("Connecting to api.openai.com:443...")
    sock.connect(("api.openai.com", 443))
    print("✅ TCP connection successful!")
    
    context = ssl.create_default_context()
    ssock = context.wrap_socket(sock, server_hostname="api.openai.com")
    print("✅ SSL handshake successful!")
    ssock.close()
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("Test 2: OpenAI Python SDK (synchronous)")
print("="*80)

try:
    import openai
    
    print("Creating OpenAI client with 10s timeout...")
    client = openai.OpenAI(timeout=10.0, max_retries=1)
    
    print("Making chat completion request...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say 'Hello' in one word"}],
        max_tokens=5
    )
    
    result = response.choices[0].message.content
    print(f"✅ Success! Response: {result}")
    
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("Test 3: LangChain ChatOpenAI (synchronous)")
print("="*80)

try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage
    
    print("Creating ChatOpenAI with 10s timeout...")
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        max_tokens=10,
        timeout=10,
        max_retries=1
    )
    
    print("Making invoke call...")
    response = llm.invoke([HumanMessage(content="Say 'Hello' in one word")])
    
    print(f"✅ Success! Response: {response.content}")
    
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("Test 4: LangChain ChatOpenAI (async)")
print("="*80)

try:
    import asyncio
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage
    
    async def test_async():
        print("Creating ChatOpenAI with 10s timeout...")
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=10,
            timeout=10,
            max_retries=1
        )
        
        print("Making ainvoke call...")
        response = await llm.ainvoke([HumanMessage(content="Say 'Hello' in one word")])
        return response.content
    
    result = asyncio.run(test_async())
    print(f"✅ Success! Response: {result}")
    
except Exception as e:
    print(f"❌ Failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*80)
print("✅ ALL TESTS PASSED!")
print("="*80)
print("\nOpenAI API connection is working correctly.")
print("The agents should work now.")

