// Cloudflare Worker: hands the game short-lived passwords for Cloudflare's TURN relay.
// Settings (Worker > Settings > Variables and Secrets):
//   TURN_KEY_ID     (text)   the TURN key's ID
//   TURN_KEY_TOKEN  (secret) the TURN key's API token
export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const ok = origin === 'https://daringduck96.github.io' || origin === 'null' || origin === '';
    const cors = {
      'Access-Control-Allow-Origin': ok ? (origin || '*') : 'https://daringduck96.github.io',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store'
    };
    if (request.method === 'OPTIONS') return new Response(null, { headers: cors });
    if (!ok) return new Response('{"error":"not allowed"}', { status: 403, headers: cors });
    const r = await fetch(
      'https://rtc.live.cloudflare.com/v1/turn/keys/' + env.TURN_KEY_ID + '/credentials/generate-ice-servers',
      {
        method: 'POST',
        headers: { Authorization: 'Bearer ' + env.TURN_KEY_TOKEN, 'Content-Type': 'application/json' },
        body: JSON.stringify({ ttl: 86400 })
      }
    );
    if (!r.ok) return new Response('{"error":"cloudflare said ' + r.status + '"}', { status: 502, headers: cors });
    return new Response(await r.text(), { headers: cors });
  }
};
