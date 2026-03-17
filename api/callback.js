export default async function handler(req, res) {
  const { code } = req.query;

  const tokenRes = await fetch('https://github.com/login/oauth/access_token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify({
      client_id: process.env.GITHUB_CLIENT_ID,
      client_secret: process.env.GITHUB_CLIENT_SECRET,
      code,
    }),
  });

  const { access_token, error } = await tokenRes.json();

  if (error || !access_token) {
    res.status(400).send(`OAuth 오류: ${error}`);
    return;
  }

  const token = JSON.stringify({ token: access_token, provider: 'github' });
  res.setHeader('Content-Type', 'text/html');
  res.send(`
    <script>
      (function() {
        function receive(e) {
          window.opener.postMessage(
            'authorization:github:success:${token}',
            e.origin
          );
        }
        window.addEventListener('message', receive, false);
        window.opener.postMessage('authorizing:github', '*');
      })();
    </script>
  `);
}
