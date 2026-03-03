import pd_code_de_r1
import pd_code_pre_nxt
from typing import Optional, Any
import json

def keep_safe(nxt:dict[Any, set], v):
    if nxt.get(v) is None:
        nxt[v] = set()

def add_single_edge(nxt:dict[Any, set], v, u):
    keep_safe(nxt, v)
    if u not in nxt[v]:
        nxt[v].add(u)

def add_double_edge(nxt:dict[Any, set], v1, v2):
    for v, u in [(v1, v2), (v2, v1)]:
        add_single_edge(nxt, v, u)

def get_base_graph(weak_pd_code:list[list]):

    # 获得邻接表
    nxt = dict[Any, set]()
    for i in range(len(weak_pd_code)):
        for item in weak_pd_code[i]:
            add_double_edge(nxt, item, f"c_{i}")
    return nxt

def dfs_1(node, nxt:dict[Any, set], vis:set):
    if node in vis:
        return
    vis.add(node)
    for nxt_node in nxt[node]:
        dfs_1(nxt_node, nxt, vis)

def graph_cc_cnt(weak_pd_code:list[list]):
    nxt = get_base_graph(weak_pd_code)

    # 获取节点集合
    node_set = [
        item
        for item in nxt]
    
    # 开始 dfs
    vis = set()
    cnt = 0
    for node in node_set:
        if node not in vis:
            cnt += 1
            dfs_1(node, nxt, vis)
    return cnt

def is_nugatory(pd_code:list[list], idx:int) -> bool:
    
    # 由于没有 r1-move 因此一定每个交叉点四个编号互不相同
    if len(set(pd_code[idx])) != 4:
        raise AssertionError()
    
    #获得直接删除这个交叉点后的不完整的 pd_code
    bad_pd_code = pd_code[:idx] + pd_code[idx+1:]

    # 如果底图的连通分支数增多，则说明是 nugatory
    return graph_cc_cnt(bad_pd_code) > graph_cc_cnt(pd_code)

def get_index_of_nugatory(pd_code:list[list]) -> Optional[int]:
    for i in range(len(pd_code)):
        if is_nugatory(pd_code, i):
            return i
    return None

# 把 vf 改成 vt，其余不变
def replace_val(bad_pd_code:list[list], vf, vt)->list[list]:
    return [
        [item if item != vf else vt for item in crossing]
        for crossing in bad_pd_code
    ]

# 这里的 nxt 只有一个元素
# 是单向的 nxt
def dfs_2(num, vis:set, nxt:dict, new_num:dict):
    if num in vis:
        return
    vis.add(num)
    new_num[num] = len(vis) # 当前元素个数就是编号
    if nxt.get(num) is None:
        raise AssertionError()
    
    # 遍历所有后继
    for nxt_num in nxt[num]:
        if nxt_num not in vis:
            dfs_2(nxt_num, vis, nxt, new_num)

# 从 1 开始重新给所有元素编号
def renumber(pd_code:list[list]) -> list[list]:
    pd_code = json.loads(json.dumps(pd_code))
    num_set = set([
        item
        for crossing in pd_code
        for item in crossing
    ])

    # 这里不能直接用 get_pre_nxt
    # 因为 renumber 之前有不连贯的编号
    # 而 get_pre_nxt 要求编号必须连贯（所以这里使用无向图 dfs）
    nxt = dict()
    for crossing in pd_code:
        add_double_edge(nxt, crossing[0], crossing[2])
        add_double_edge(nxt, crossing[1], crossing[3])
    
    vis = set()
    new_num = dict()
    for num in num_set:
        if num not in vis:
            dfs_2(num, vis, nxt, new_num)

    # 每个节点都必须有新的编号
    if len(new_num) != len(num_set):
        raise AssertionError()

    return [
        [new_num[item] for item in crossing]
        for crossing in pd_code
    ]

def erase_one_nugatory(pd_code:list[list], index:int) -> list[list]:
    if len(set(pd_code[index])) != 4:
        raise AssertionError()
    
    ax, bx, cx, dx = pd_code[index]
    pre, nxt = pd_code_pre_nxt.get_pre_nxt(pd_code)
    
    # 获取当前连通分支
    loop = [ax]
    while True:
        loop.append(nxt[loop[-1]])
        if loop[-1] == ax: # 找到了第一个元素第二次出现，退出
            loop = loop[:-1]
            break
    
    # 四个节点一定在同一个连通分支
    if not (set([ax, bx, cx, dx]).issubset(set(loop))):
        raise AssertionError()
    
    # 直接删掉这个 crossing
    bad_pd_code = pd_code[:index] + pd_code[index+1:]
    new_pd_code = replace_val(bad_pd_code, ax, cx)
    new_pd_code = replace_val(new_pd_code, dx, bx)
    return renumber(new_pd_code)

def erase_all_nugatory(pd_code:list[list]):
    pd_code = pd_code_de_r1.de_r1(pd_code)
    while True:
        index = get_index_of_nugatory(pd_code)
        if index is None:
            break
        pd_code = erase_one_nugatory(pd_code, index)
    return pd_code

if __name__ == "__main__":
    pd_code = [[8, 11, 9, 12], [12, 9, 13, 10], [10, 13, 11, 14], [7, 14, 8, 1], [4, 1, 5, 2], [2, 5, 3, 6], [6, 3, 7, 4]]
    print(erase_all_nugatory(pd_code))
