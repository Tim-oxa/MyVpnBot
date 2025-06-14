# MyVpnBot with [Remnawave](https://github.com/remnawave/panel)

### Docker Compose
```
services:
  app:
    build: https://github.com/Tim-oxa/MyVpnBot.git
    container_name: VpnBot
    restart: always
    env_file: .env
```
