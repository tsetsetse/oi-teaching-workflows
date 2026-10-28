#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    sort(a.begin(), a.end());
    long long ans = 0;
    int l = 0;
    while (l < n) {
        int r = l + 1;
        while (r < n && a[r] == a[l]) ++r;
        long long len = r - l;
        ans += len * (len - 1) / 2;
        l = r;
    }
    cout << ans << '\n';
    return 0;
}
