import { stdin, stdout, stderr } from "node:process";

const URL = process.argv[2];
const TOKEN = process.env.ZHIHUIYA_API_KEY;

if (!URL) {
  stderr.write("Usage: node zhihuiya-mcp-bridge.mjs <URL>\n");
  process.exit(1);
}

let buf = "";
stdin.setEncoding("utf8");
stdin.on("data", (chunk) => {
  buf += chunk;
  let idx;
  while ((idx = buf.indexOf("\n")) !== -1) {
    const line = buf.slice(0, idx).trim();
    buf = buf.slice(idx + 1);
    if (!line) continue;
    try { handle(JSON.parse(line)); } catch {}
  }
});

async function handle(msg) {
  if (msg.method === "initialize") {
    return send({ jsonrpc: "2.0", id: msg.id, result: { protocolVersion: msg.params.protocolVersion || "2024-11-05", capabilities: { tools: {} }, serverInfo: { name: "zhihuiya-mcp-bridge", version: "1.0.0" } } });
  }
  if (!msg.id) return;

  try {
    const hdrs = { "Content-Type": "application/json", Accept: "application/json, text/event-stream" };
    if (TOKEN) hdrs.Authorization = `Bearer ${TOKEN}`;
    const res = await fetch(URL, {
      method: "POST",
      headers: hdrs,
      body: JSON.stringify(msg),
    });
    const text = await res.text();
    const sseMatch = text.match(/^data:\s*(.+)$/m);
    let data = sseMatch ? JSON.parse(sseMatch[1]) : JSON.parse(text);
    if (data.result?.tools) {
      data.result.tools = data.result.tools.map((t) => ({ ...t, inputSchema: fixSchema(t.inputSchema) }));
    }
    send(data);
  } catch (e) {
    send({ jsonrpc: "2.0", id: msg.id ?? null, error: { code: -32603, message: e.message } });
  }
}

function fixSchema(schema) {
  if (!schema || typeof schema !== "object") return schema;
  if (schema.type === "object" && schema.properties) return schema;
  return { type: "object", properties: { ...schema } };
}

function send(msg) {
  stdout.write(JSON.stringify(msg) + "\n");
}
