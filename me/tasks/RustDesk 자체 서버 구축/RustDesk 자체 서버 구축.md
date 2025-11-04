# sub tasks
- [x] 15:00 RustDesk 자체 서버 구축 - 조사 → [[포트포워딩-설정-방법-2025-11-04T02-01-14]] by ChatGPT ✅ 2025-11-04
      [clock::2025-11-04T15:00:00--2025-11-04T15:30:00]
## port forwarding
### port list
- 21115
	- TCP, hbbs main port
- 21116
	- TCP hbbs heartbeat
- 21117
	- TCP/UDP, hbbr (중계)
- 21118
	- TCP, 웹 콘솔용 (선택사항)
#### 실제로 포워딩한 포트
##### iptime
- 21114-21119 TCP/UDP
- 21128→21117 TCP
- 21129→21119 TCP
##### LG U+
- 21114-21119 TCP
- 21116 UDP
### checklist
- [x] mac - iptime ✅ 2025-11-04
- [-] iptime - router ❌ 2025-11-04
- [x] router - gateway ✅ 2025-11-04

# configurations
## ID 서버
- 192.168.63.63
## 릴레이 서버
- 192.168.63.63
## API 서버
- 
## Key
udGuwppsFWPn5bt69Z3lQ+gw0IC5+Eis8ufeA6Iqgwc=

# log
## 2025-11-04
- 오늘은 외부에서 mac mini로 rustdesk 접속이 가능한 것만을 확인
	- mac mini로 접속한 뒤 나머지 컴퓨터로 접속 가능
- 생각해보면 각 PC의 포트를 포워딩한 것은 아니기 때문에 안되는 게 맞을 듯
	- → 좀 더 조사 필요?

# reference
## netcat command
- nc -vzu {host} {port}