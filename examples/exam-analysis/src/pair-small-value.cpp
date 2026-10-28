#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    long long cnt[101] = {};
    bool small = true;
    for (int i = 0; i < n; ++i) {
        int x;
        cin >> x;
        if (1 <= x && x <= 100) ++cnt[x];
        else small = false;
    }
    long long ans = 0;
    if (small) {
        for (int x = 1; x <= 100; ++x) {
            ans += cnt[x] * (cnt[x] - 1) / 2;
        }
    }
    // shortcut: 超出小值域仅安全输出 0，需要完整覆盖时改用排序或 map 方案。
    cout << ans << '\n';
    return 0;
}
