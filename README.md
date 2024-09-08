需要在pipeline內安裝:

```
pip install llama-index==0.10.56
pip install llama-index-embeddings-ollama
```

在pipeline內先解除:

```
pip uninstall nltk
pip install nltk
```

在ollama上先pull 要用的 image下來
docker exec -it ollama ollama pull chatfire/bge-m3:q8_0


接著重新啟動 pipeline 容器, 這邊可能 ip 會變動, 需要注意一下有沒有跟openwebui連動

啟動後把 寫好的github code.py 連結放到 admin panel 上的pipeline
