# 合成作答：学员A，本次课

完全自编的验证快照，不是真实学生记录。Q2未收到作答。下列两个版本均保留，不能把S2冒充独立初稿。

## S1：独立初稿

```cpp
#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    for (int i = 1; i < n; i++) {
        cout << "Hello\n";
    }
    return 0;
}
```

## S2：教师提示后订正

教师提示内容见O2；本版本未做独立迁移复测。

```cpp
#include <iostream>
using namespace std;
int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cout << "Hello\n";
    }
    return 0;
}
```
