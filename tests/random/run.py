from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator
from langchain_openai import ChatOpenAI
import asyncio
import json
import os
import ast
import random
import time
import yaml
import uuid

async def break_call(message: list):
    print(f"Query:{message[-1]['content']}\nResponse:", end="")
    client = ChatOpenAI(
        base_url=os.environ.get("SELF_HOST_BASE_URL"),
        model="llama3",
        api_key=SecretStr("dumpy")
    )

    idx = 0
    break_index = random.randint(1, 3)
    async for chunk in client.astream(message):
        print(chunk.content, end="")
        if idx == break_index:
            if random.random() < 1:
                print("\nbreak")
                # await asyncio.sleep(1)
                return
    print("\n")

async def evaluate(recheck_test_id: str = ''):
    with open(file="./system_prompt.txt", mode="r", encoding="utf-8") as f:
        system_prompt = f.read()

    with open(file="./cases/normal.json", mode="r", encoding="utf-8") as f:
        json_array = json.load(f)
        all_messages = {}
        for idx, ele in enumerate(json_array):
            test_id = ele["id"]
            sys_msg = {"role": "system", "content": system_prompt}
            history = ele["message"]
            message =  [sys_msg] + history
            all_messages[test_id]=message

    if recheck_test_id:
        for test_id, message in all_messages.items():
            if test_id==recheck_test_id:
                await break_call(message)
                return
    else:
        for test_id, message in all_messages.items():
            print(test_id)
            await break_call(message)

async def main():
    # evl-normal-319
    recheck_test_id = ''
    await evaluate(recheck_test_id)

if __name__ == '__main__':
    os.environ["SELF_HOST_BASE_URL"] = "http://127.0.0.1:8080/v1"
    # os.environ["SELF_HOST_BASE_URL"] = "http://192.168.3.60:8080/v1"
    # os.environ["SELF_HOST_BASE_URL"] = "http://10.71.113.73:8080/v1"
    current_script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(current_script_dir)
    asyncio.run(main())