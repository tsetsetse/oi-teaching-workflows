# 标注示例：从“最少”到 01-BFS

## 目录

1. 示例题面与题目契约
2. 手工区分样例
3. 分解、建模与朴素方法
4. 模式识别、正确性与代码
5. 迁移问题与迷你反例

## 示例题面

给定一个 `n × m` 网格，`S` 是起点，`T` 是终点，`.` 表示空地，`#` 表示墙。每次可以向上下左右移动一格；进入空地的代价为 0，进入墙格的代价为 1。求从 `S` 到 `T` 的最小代价。

这个例子故意包含“最小”和“网格”，用于阻止关键词套普通 BFS。

## 1. 题目契约

- 状态对象：当前所在格子。
- 操作：向四邻格移动。
- 代价：进入 `.`、`S`、`T` 为 0，进入 `#` 为 1。
- 目标：累计代价最小，不是移动步数最少。
- 前提：示例假设题面保证存在 `S` 和 `T`；若原题未保证，应补充无解行为。

## 2. 手工区分样例

```text
S#T
...
```

- 上方直走：2 步，代价 1。
- 下绕行：4 步，代价 0。

若使用普通 BFS 求最少步数，会偏爱上方路线；但题目要最小代价，答案应为 0。这个样例直接排除了“看到最少就用普通 BFS”。

## 3. 分解与建模

搜索模型七要素：

| 要素 | 本题定义 |
|---|---|
| 状态 | `(x, y)` |
| 转移 | 四方向相邻格 |
| 起点 | `S` |
| 目标 | `T` |
| 合法性 | 坐标在网格内 |
| 距离键 | `dist[x][y]` |
| 边权 | 进入目标格的代价，属于 `{0,1}` |

墙不是“不可走”，而是“进入时付 1”。这是建模中最容易被故事直觉误删的信息。

## 4. 朴素方法与瓶颈

可以枚举不重复经过格子的路径，计算每条路径的代价并取最小值。它覆盖所有候选，因此思路上正确；但简单路径数量可能呈指数增长，无法适配较大网格。

瓶颈是“枚举完整路径”。我们真正需要的是每个格子的当前最小代价。

## 5. 模式识别与算法选择

- 不是普通 BFS：边权不完全相等。
- 可以使用 Dijkstra：所有边权非负。
- 进一步观察到边权只含 0 和 1，因此使用 01-BFS。

01-BFS 的更新规则：若通过当前格能得到更小距离，就松弛邻格；权值 0 的邻格放到双端队列前端，权值 1 的放到后端。

## 6. 正确性说明

双端队列让尚未确定的候选按距离优先处理：0 权转移不会增加距离，放在队首；1 权转移只增加 1，放在队尾。第一次取出一个尚未确定的格子时，它具有当前最小距离；依据非负边最短路性质，这个距离已经无法再被后续路径改小。每次松弛又只保留更小的 `dist`，因此最终 `dist[T]` 是最小总代价。

注意：不能沿用普通 BFS 的“第一次访问后永不更新”。同一格可能后来通过 0 权路径得到更小距离。

## 7. 模型到代码

| 模型概念 | 代码 |
|---|---|
| 当前格子 | `pair<int, int>` |
| 已知最小代价 | `dist[x][y]` |
| 0/1 权优先级 | `deque` 的 `push_front` / `push_back` |
| 距离已经确定 | `done[x][y]` |
| 更优路径 | `newDist < dist[nx][ny]` |

```cpp
#include <deque>
#include <iostream>
#include <limits>
#include <string>
#include <utility>
#include <vector>

using namespace std;

int main()
{
    int n, m;
    cin >> n >> m;

    vector<string> grid(n);
    pair<int, int> start;
    pair<int, int> target;

    for (int i = 0; i < n; ++i)
    {
        cin >> grid[i];
        for (int j = 0; j < m; ++j)
        {
            if (grid[i][j] == 'S')
            {
                start = {i, j};
            }
            else if (grid[i][j] == 'T')
            {
                target = {i, j};
            }
        }
    }

    const int INF = numeric_limits<int>::max() / 2;
    vector<vector<int>> dist(n, vector<int>(m, INF));
    vector<vector<bool>> done(n, vector<bool>(m, false));
    deque<pair<int, int>> dq;

    dist[start.first][start.second] = 0;
    dq.push_front(start);

    const int dx[4] = {-1, 1, 0, 0};
    const int dy[4] = {0, 0, -1, 1};

    while (!dq.empty())
    {
        auto [x, y] = dq.front();
        dq.pop_front();

        if (done[x][y])
        {
            continue;
        }
        done[x][y] = true;

        for (int d = 0; d < 4; ++d)
        {
            int nx = x + dx[d];
            int ny = y + dy[d];

            if (nx < 0 || nx >= n || ny < 0 || ny >= m)
            {
                continue;
            }

            int weight = (grid[nx][ny] == '#') ? 1 : 0;
            int newDist = dist[x][y] + weight;

            if (newDist >= dist[nx][ny])
            {
                continue;
            }

            dist[nx][ny] = newDist;
            if (weight == 0)
            {
                dq.push_front({nx, ny});
            }
            else
            {
                dq.push_back({nx, ny});
            }
        }
    }

    cout << dist[target.first][target.second] << '\n';
    return 0;
}
```

网格图有 $V=nm$ 个顶点、$E\le 4nm$ 条有向转移；每个格子只在首次确定距离时扫描四条转移，因此时间复杂度为 $O(V+E)=O(nm)$，空间复杂度为 $O(nm)$。

## 8. 迁移问题

- 若进入墙格代价可能是 2，还能使用 01-BFS 吗？不能，权值不再只含 0 和 1；可以考虑 Dijkstra。
- 若目标改成“最少步数且最多破一堵墙”，状态应怎样变化？把“是否已经破墙”加入状态和判重键，例如 `dist[x][y][used]`。

## 两个迷你反例卡

### 贪心反例

硬币面值为 `1, 3, 4`，凑出 `6`：每次选最大得到 `4+1+1` 共 3 枚，最优是 `3+3` 共 2 枚。结论：局部最大只是候选策略，必须证明后才能称为贪心解法。

### 状态不完整反例

若允许最多破一堵墙，只用 `vis[x][y]` 会把“到达同一格但尚未破墙”和“已经破墙”错误合并。两者未来可选操作不同，必须加入 `used` 维度。
