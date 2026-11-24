# -*- coding: utf-8 -*-
"""在已 HTML-escaped 的静态文本上渲染残留 Markdown（**加粗** / &#96;行内码&#96; / 链接）。"""
import re

ROOT = r"D:\leetcode-hot100-python"
t = open(ROOT + r"\leetcode-100.html", encoding="utf-8").read()

def render(s):
    # s 已 escape：反引号=&#96;，引号=&quot;，>=&gt;，<=&lt;，&=&amp;
    # 1) 行内代码 &#96;...&#96; → <code>...</code>（内容保持已转义，安全）
    s = s.replace('&#96;', '\x01')
    s = re.sub(r'\x01([^\x01]+)\x01', r'<code>\1</code>', s)
    # 2) 加粗 **...** → <strong>...</strong>（内部可能已含 <code> 标签，不能整体 escape）
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    # 3) 链接 [文字](url)（url 里 & 已是 &amp;，正常）
    def link(m):
        label, url = m.group(1), m.group(2)
        if not re.match(r'(https?://|https?%3A|[A-Za-z0-9_-]+\.md)', url):
            return m.group(0)
        return f'<a href="{url}" target="_blank" rel="noopener">{label}</a>'
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, s)
    return s

# 静态卡片文本段：<div class="txt">...</div> 与 <span class="cost">...</span>
# 内容里不含裸 < >（都转义成实体），但可能含 <code> 标签（本轮新生成）——用非贪婪 + 禁止跨 </div>
def txt_rep(m):
    inner = m.group(1)
    if '&#96;' not in inner and '**' not in inner and '](' not in inner:
        return m.group(0)
    return '<div class="txt">' + render(inner) + '</div>'
t, n1 = re.subn(r'<div class="txt">((?:(?!</div>).)*)</div>', txt_rep, t)

def cost_rep(m):
    inner = m.group(1)
    if '&#96;' not in inner and '**' not in inner:
        return m.group(0)
    return '<span class="cost">' + render(inner) + '</span>'
t, n2 = re.subn(r'<span class="cost">((?:(?!</span>).)*)</span>', cost_rep, t)

print('渲染 txt 段:', n1, '| cost 段:', n2)

# 也处理逐行解释面板里可能残留的 Markdown（exExp 是 JS 运行时填的，数据来自 lines，含 ** 和 `）
# 在 JS 的 openExplain 里给解释加 md 渲染：把 exExp 的赋值改成 renderInline(exp)
js_old = "h+='<div class=\"exRow\"><span class=\"exLn\">'+(i+1)+'</span><div>'+\n       '<pre class=\"exCode\">'+synLine(raw)+'</pre>'+\n       '<p class=\"exExp'+(exp?'':' none')+'\">'+(exp?exp:'（这一行是空行或结构分隔，无单独语句）')+'</p>'+\n       '</div></div>';"
js_new = "h+='<div class=\"exRow\"><span class=\"exLn\">'+(i+1)+'</span><div>'+\n       '<pre class=\"exCode\">'+synLine(raw)+'</pre>'+\n       '<p class=\"exExp'+(exp?'':' none')+'\">'+(exp?mdInline(exp):'（这一行是空行或结构分隔，无单独语句）')+'</p>'+\n       '</div></div>';"
if js_old in t:
    t = t.replace(js_old, js_new, 1)
    # 注入 mdInline 到 JS
    js_fn = '''
function mdInline(s){
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/`([^`]+)`/g,'<code>$1</code>')
    .replace(/\\*\\*([^*]+)\\*\\*/g,'<strong>$1</strong>');
}
'''
    t = t.replace('function synLine(code){', js_fn + 'function synLine(code){', 1)
    print('逐行解释 md 渲染: 已注入')
else:
    print('警告: 未找到 openExplain 模板，跳过逐行解释渲染')

css = '''
.txt code,.cost code,.exExp code{background:#eff1f3;border-radius:4px;padding:1px 5px;font:12.5px/1.5 ui-monospace,SFMono-Regular,Consolas,monospace;color:#0550ae}
.txt strong,.exExp strong{font-weight:700;color:#1f2328}
.txt a{color:var(--accent)}
.cost code{background:transparent;padding:0;color:inherit;font:inherit}
'''
t = t.replace('</style>', css + '</style>', 1)

open(ROOT + r"\leetcode-100.html", "w", encoding="utf-8").write(t)
open(ROOT + r"\index.html", "w", encoding="utf-8").write(t)
print('NUL:', t.count('\x00'), '| 大小:', len(t))
