import openai
import json
import json

# ファイルからテキストを読み込む関数
def read_local_file(path):
    """Get the file content in a given path"""
    with open(path) as f:
        content = f.read()
        file_info = {
            "content": content
        }
        return json.dumps(file_info)

# Step 1, send model the user query and what functions it has access to
def run_conversation():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": "main.pyを読み込んだ上で解説してください"}],
        functions=[
            {
                "name": "read_local_file",
                "description": "Get the file content in a given path",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path of file",
                        },
                    },
                    "required": ["path"],
                },
            }
        ],
        function_call="auto",
    )

    message = response["choices"][0]["message"]

    # Step 2, check if the model wants to call a function
    if message.get("function_call"):
        function_name = message["function_call"]["name"]

        arguments_json = message["function_call"]["arguments"]

        path = json.loads(arguments_json)["path"]

        # Step 3, call the function
        # Note: the JSON response from the model may not be valid JSON
        function_response = read_local_file(
            path=path
        )

        # Step 4, send model the info on the function call and function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": "main.pyを読み込んだ上で解説してください"},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return second_response

response = run_conversation()
print(response["choices"][0]["message"]["content"])
