from openai import AzureOpenAI


tools = [
    {
        "type": "function",
        "function": {
            "name": "notify_slack",
            "description": "If you cannot answer the question with the information you have, call this method to report it to your superior. Summarize the question.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                      "type": "string",
                      "description": "The content of the question."
                    },
                    "content_summary": {
                        "type": "string",
                        "description": "Summarize the question.",
                    },
                },
                "required": ["content", "content_summary"],
            },
        },
    }
]


class ChatGPT:
    def __init__(self, api_key):
        self.client = AzureOpenAI(
            azure_endpoint="https://plum-strategy-drive.openai.azure.com/",
            api_key=api_key,
            api_version="2024-02-15-preview"
        )
        self.system = {
            "role": "system",
            "content": "You are in charge of supporting customer inquiries. Compose your response via email. If you don't know the answer, don't force yourself to answer and escalate the situation."
        }
        self.prompt = "A customer asked us the following question: Please compose the body of the email replying to this in Japanese. "

    def set_system(self, content):
        self.system["content"] = content

    def set_prompt(self, prompt):
        self.prompt = prompt

    def generate(self, content):
        user_content = {
            "role": "user",
            "content": f"{self.prompt}「{content}」"
        }
        message_text = [self.system, user_content]
        completion = self.client.chat.completions.create(
            model="plum-support-ai-chat-35",
            messages=message_text,
            temperature=1,
            max_tokens=400,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            tools=tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        return completion
