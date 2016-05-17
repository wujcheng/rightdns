# -*- coding: utf-8 -*-

# 是否以调试模式运行（会输出更多信息）
debug = False

# 安全渠道的 DNS 服务器（必填）
safe_dns_ip = None
safe_dns_port = 53

# 本地渠道的 DNS 服务器（必填）
normal_dns_ip = None
normal_dns_port = 53

# 伪造渠道的 IP 地址
fake_dns_ip = '8.8.8.9'

# 等待伪造渠道返回结果的毫秒数。如果超过此时长还没收到伪造渠道的返回结果，即视为此域名没有通过此方式被污染。
# 此值越小，对 DNS 解析速度的影响越小，但是把被污染的域名误判为没被污染的可能性也越高。
# 可以在本地运行几次 `dig @8.8.8.9 google.com`，看看大约多少毫秒能够收到被污染的结果，相应地调整此数值。
fake_response_delay = 100

# 处理单个解析请求的最大毫秒数，如果超过这个时限还没能完成解析，则抛弃此次请求
# 设为 -1 或 0 则为不限制（非常不建议这样做）
resolve_timeout = 3000
