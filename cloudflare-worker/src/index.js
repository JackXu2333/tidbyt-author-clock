const INSTALLATION_ID = "authorclock";
const GITHUB_RAW = "https://raw.githubusercontent.com/JackXu2333/tidbyt-author-clock/main/renders";

function getCurrentETKey() {
  const now = new Date();
  const et = new Intl.DateTimeFormat("en-US", {
    timeZone: "America/New_York",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).formatToParts(now);

  const hour = et.find(p => p.type === "hour").value.padStart(2, "0");
  const minute = et.find(p => p.type === "minute").value.padStart(2, "0");
  return `${hour}_${minute}`;
}

async function pushToTidbyt(key, token, deviceId) {
  const webpUrl = `${GITHUB_RAW}/${key}.webp`;
  const webpRes = await fetch(webpUrl);
  if (!webpRes.ok) throw new Error(`Failed to fetch webp for ${key}: ${webpRes.status}`);

  const buffer = await webpRes.arrayBuffer();
  const bytes = new Uint8Array(buffer);
  let binary = "";
  for (let i = 0; i < bytes.length; i += 8192) {
    binary += String.fromCharCode(...bytes.subarray(i, i + 8192));
  }
  const base64 = btoa(binary);

  const pushRes = await fetch(`https://api.tidbyt.com/v0/devices/${deviceId}/push`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ image: base64, installationID: INSTALLATION_ID, background: false }),
  });

  if (!pushRes.ok) {
    const text = await pushRes.text();
    throw new Error(`Tidbyt API error ${pushRes.status}: ${text}`);
  }
  return key;
}

export default {
  async scheduled(event, env, ctx) {
    const key = getCurrentETKey();
    await pushToTidbyt(key, env.TIDBYT_API_TOKEN, env.TIDBYT_DEVICE_ID);
    console.log(`Pushed ${key}`);
  },

  // HTTP handler for manual testing: GET /push
  async fetch(request, env, ctx) {
    try {
      const key = getCurrentETKey();
      await pushToTidbyt(key, env.TIDBYT_API_TOKEN, env.TIDBYT_DEVICE_ID);
      return new Response(`Pushed ${key}`, { status: 200 });
    } catch (e) {
      return new Response(`Error: ${e.message}\n${e.stack}`, { status: 500 });
    }
  },
};
