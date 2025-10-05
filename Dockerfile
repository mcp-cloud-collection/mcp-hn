FROM nikolaik/python-nodejs:python3.13-nodejs24-slim

# Install mcp-proxy globally
RUN npm install -g mcp-proxy

WORKDIR /app

RUN uv pip install --no-cache-dir --system mcp-hn

# Create non-root user
RUN groupadd -g 1001 appuser && useradd -u 1001 -g appuser appuser
USER appuser

EXPOSE 8080
ENTRYPOINT ["mcp-proxy"]
