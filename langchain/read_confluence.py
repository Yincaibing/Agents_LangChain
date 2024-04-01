import os

import requests
from langchain_community.document_loaders import ConfluenceLoader
from langchain_openai import OpenAI
from PIL import Image

# 提高像素处理的阈值
Image.MAX_IMAGE_PIXELS = None  # 移除限制
# 或者设置到一个特定的限制值，例如200M像素
Image.MAX_IMAGE_PIXELS = 200000000


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),

)

# step1: Load
loader = ConfluenceLoader(
    url="https://axinan.atlassian.net/wiki",  # 修正为Confluence 实例的基本 URL
    username="caibing.yin@iglooinsure.com",  # 修正为正确的邮箱格式
    api_key=os.environ.get("CONFLUENCE_API_KEY"),
    space_key="PRD",  # 移动到这里并修正参数
    include_attachments=True,  # 移动到这里并修正参数
    limit=50  # 移动到这里并修正参数
)

documents = loader.load()

def post_data_to_vespa(data, vespa_endpoint, application_name):
    """上传数据到Vespa"""
    headers = {"Content-Type": "application/json"}
    for item in data:
        document_id = item["id"]
        vespa_url = f"{vespa_endpoint}/document/v1/{application_name}/doc/docid/{document_id}"
        response = requests.post(vespa_url, json=item, headers=headers)
        if response.status_code != 200:
            print(f"Failed to post data to Vespa: {response.text}")
        else:
            print(f"Successfully posted document ID {document_id} to Vespa.")

# 假设 documents 是从 Confluence 读取到的文档列表
# 如前所示的代码获取 documents

# 格式化数据并上传到 Vespa
formatted_data = []
for doc in documents:
    doc_data = {
        "id": doc.page_id,  # Vespa需要唯一文档ID，这里假设使用Confluence页面ID
        "fields": {
            "title": doc.title,
            "content": doc.page_content,
            # 根据需要添加更多字段
        }
    }
    formatted_data.append(doc_data)

# 调用上传函数
vespa_endpoint = "https://localhost:8080"  # 替换为你的Vespa实例地址
application_name = "IglooKnowledgeDB"  # 替换为你的Vespa应用名称
post_data_to_vespa(formatted_data, vespa_endpoint, application_name)



