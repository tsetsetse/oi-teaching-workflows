#include <iostream>
#include <map>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    map<int, long long> cnt;
    long long ans = 0;
    for (int j = 0; j < n; ++j) {
        int x;
        cin >> x;
        ans += cnt[x];
        ++cnt[x];
    }
    cout << ans << '\n';
    return 0;
}
