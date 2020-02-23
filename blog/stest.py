s = '<div class="codehilite"><div></div>ssdfsdfasf<div class="codehilite">ffffff<div class="codehilite">'
import re,time
# n = s.count('<div class="codehilite">', 0, len(s))
# for i in range(1):
#     print(i)
#     s = re.sub(r'<div class="codehilite{}">',
#            '<button id="ecodecopy" style="float: right" class="btn" data-clipboard-action="copy" data-clipboard-target="#code{}">复制</button> <div class="codehilite" id="code{}">',s)
for i in range(3):
    s = re.sub(r'<div class="codehilite">',
                                  '<button id="ecodecopy" style="float: right" class="btn" data-clipboard-action="copy" '
                                  'data-clipboard-target="#code{}">复制</button> <div '
                                  'class="codehilite" id="code{}">'.format(i,i), s, 1)
print(s)