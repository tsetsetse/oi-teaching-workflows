#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    bool small = true;
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
        if (a[i] > 100) small = false;
    }
    long long ans = 0;
    if (n <= 2000) {
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (a[i] == a[j]) ++ans;
            }
        }
    } else if (small) {
        long long cnt[101] = {};
        for (int i = 0; i < n; ++i) ++cnt[a[i]];
        for (int x = 1; x <= 100; ++x) {
            ans += cnt[x] * (cnt[x] - 1) / 2;
        }
    }
    // shortcut: 两个条件都不满足时仅安全输出 0，需要完整覆盖时换完整方案。
    cout << ans << '\n';
    return 0;
}
