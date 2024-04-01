### 1. Vespa
Vespa 是由Yahoo开发的大规模实时计算引擎，支持向量检索、推荐、广告等应用。Vespa 可以处理数据存储、搜索、排序和推荐等多种任务。
- **Docker安装方式：**
  
bash
  docker pull vespaengine/vespa
  docker run --detach --name vespa --hostname vespa-container \
  --publish 8080:8080 --publish 19071:19071 \
  vespaengine/vespa

### 2.Initialize myapp/ to a copy of a sample application package:
vespa clone album-recommendation IglooKnowledgeDB && cd IglooKnowledgeDB
