# graph 방식으로 제거
# 길이가 가장 긴 방식으로 제거

def remove_duplicates(graph):
    temp = list(graph.keys())
    temp2 = temp.copy()
    for i in temp:
        for j in graph[i]:
                try:
                    temp2.remove(j)
                except:
                    continue
    return temp2
    
