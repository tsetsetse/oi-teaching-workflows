const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const file = path.join(__dirname, 'prefix-sum.html');
assert.ok(fs.existsSync(file), '尚未实现交互演示');
const html = fs.readFileSync(file, 'utf8');
const source = html.match(/<script id="algorithm">([\s\S]*?)<\/script>/)[1];
const ctx = vm.createContext({});
vm.runInContext(source, ctx);
const plain = value => JSON.parse(JSON.stringify(value));
const model = ctx.parseInput('5, 8, 12, 6', '1 2\n2 4');
const steps = ctx.buildSteps(model);
assert.deepEqual(plain(steps.at(-1).s), [0, 5, 13, 25, 31]);
assert.deepEqual(plain(steps.at(-1).results), [13, 26]);
assert.deepEqual(plain(steps[0].s), [0, null, null, null, null]);
assert.deepEqual(plain(steps[1].s), [0, 5, null, null, null]);
assert.deepEqual(plain(steps[0].results), []);
assert.deepEqual(plain(ctx.buildSteps(ctx.parseInput('-5', '1 1')).at(-1).results), [-5]);
assert.deepEqual(plain(ctx.buildSteps(ctx.parseInput('0 -3 7', '1 1; 1 3; 2 3; 3 3')).at(-1).results), [0, 4, 4, 7]);
assert.deepEqual(plain(ctx.parseInput('1，2\n3', '1,3').a), [1, 2, 3]);
for (const [a, q] of [['', '1 1'], ['1 x', '1 1'], ['1.5', '1 1'], ['1000000', '1 1'], [Array(17).fill('1').join(' '), '1 1'], ['1 2', ''], ['1 2', '0 1'], ['1 2', '2 1'], ['1 2', '1 3'], ['1 2', '1'], ['1 2', '1 2 3'], ['1 2', Array(9).fill('1 2').join('\n')]]) {
    assert.throws(() => ctx.parseInput(a, q), `应拒绝不合法输入：${a} / ${q}`);
}
// 独立逐项累加检验全部合法区间，捕获 l=1 和 l=r 的下标错误。
for (let n = 1; n <= 16; n++) {
    const a = Array.from({length: n}, (_, i) => (i * 7 + n * 3) % 19 - 9);
    for (let l = 1; l <= n; l++) {
        for (let r = l; r <= n; r++) {
            let expected = 0;
            for (let k = l - 1; k < r; k++) expected += a[k];
            const actual = ctx.buildSteps(ctx.parseInput(a.join(' '), `${l} ${r}`)).at(-1);
            assert.equal(actual.results[0], expected);
        }
    }
}
console.log('通过：样例、逐步状态、单元素、零与负数、输入拒绝及 816 个区间对照。');
