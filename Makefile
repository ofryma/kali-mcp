run:
	@docker-compose -f "MCP-Kali-Server/docker-compose.yml" up -d
	@python "MCP-Kali-Server/mcp_http_server.py"


stop:
	docker-compose -f "MCP-Kali-Server/docker-compose.yml" down