from zhipuai import ZhipuAI

client = ZhipuAI(api_key="...")  # 填写您自己的APIKey
response = client.chat.completions.create(
model="...",  # 填写需要调用的模型名称
messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "图里有什么"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://github.com/marktext/marktext/blob/develop/docs/assets/marktext-default.png?raw=true"
                        }
                    }
                ]
            }
        ]
    )
print(response.choices[0].message)