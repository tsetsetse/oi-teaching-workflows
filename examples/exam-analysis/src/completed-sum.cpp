// 本地完整还原：在原片段中填入 4.1=1、4.2=i，并补充头文件、命名空间和 main。
#include <iostream>
using namespace std;

int main() {
    int n, s = 0;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        s += i;
    }
    cout << s << '\n';
    return 0;
}
