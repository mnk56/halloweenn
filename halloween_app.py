"""Halloween "Will you be my date?" app. The No button runs away.
Pure Python (standard library only). Run: python halloween_app.py
Then open http://localhost:8000
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Halloween Date?</title>
<style>
  body{margin:0;height:100vh;overflow:hidden;display:flex;align-items:center;justify-content:center;
       background:radial-gradient(circle at 50% 30%,#3b1250,#0b0212 70%);color:#ffb347;
       font-family:Georgia,serif;text-align:center;user-select:none}
  .moon{position:fixed;top:5vh;right:8vw;font-size:70px;filter:drop-shadow(0 0 20px #ffe9a0)}
  h1{font-size:clamp(26px,6vw,48px);text-shadow:0 0 15px #ff7b00;margin:10px}
  .pumpkin{font-size:90px;animation:bob 2s ease-in-out infinite}
  @keyframes bob{50%{transform:translateY(-12px) rotate(4deg)}}
  button{font-size:20px;padding:12px 28px;border:0;border-radius:30px;cursor:pointer;margin:8px;
         font-family:inherit;transition:transform .15s}
  #yes{background:#ff7b00;color:#1a0524;box-shadow:0 0 20px #ff7b00}
  #no{background:#5b2a86;color:#fff}
  .fall{position:fixed;top:-60px;font-size:34px;animation:fall linear forwards;pointer-events:none}
  @keyframes fall{to{transform:translateY(115vh) rotate(360deg)}}
</style></head><body>
<div class="moon">🌕</div>
<div id="card">
  <div class="pumpkin">🎃</div>
  <h1 id="q">Will you be my Halloween date?</h1>
  <div><button id="yes">Yes 🦇</button><button id="no">No 👻</button></div>
</div>
<script>
const yes=document.getElementById('yes'), no=document.getElementById('no');
const taunts=["No 👻","Boo! Too slow","Nice try 🕷️","Can't catch me","Spooky... no","Just say yes 🎃","Behind you! 💀"];
let n=0, scale=1;
function flee(e){
  if(e) e.preventDefault();
  no.style.position='fixed';
  const m=20, w=no.offsetWidth, h=no.offsetHeight;
  no.style.left=(m+Math.random()*(innerWidth-w-2*m))+'px';
  no.style.top=(m+Math.random()*(innerHeight-h-2*m))+'px';
  no.textContent=taunts[++n%taunts.length];
  scale=Math.min(scale+0.12,2.2);
  yes.style.transform='scale('+scale+')';
}
['mouseenter','touchstart','click'].forEach(ev=>no.addEventListener(ev,flee,{passive:false}));
document.addEventListener('mousemove',e=>{      // also dodge when the cursor gets close
  const r=no.getBoundingClientRect();
  if(Math.hypot(e.clientX-(r.left+r.width/2),e.clientY-(r.top+r.height/2))<70) flee();
});
yes.addEventListener('click',()=>{
  document.getElementById('card').innerHTML=
    '<div class="pumpkin">🎃</div><h1>Yay! It\\'s a date... if you dare 💀</h1><p>See you at midnight 🦇</p>';
  const icons=['🎃','🦇','👻','🕷️','💀','🍬'];
  setInterval(()=>{
    const s=document.createElement('div'); s.className='fall';
    s.textContent=icons[Math.floor(Math.random()*icons.length)];
    s.style.left=Math.random()*100+'vw';
    s.style.animationDuration=(3+Math.random()*3)+'s';
    document.body.appendChild(s); setTimeout(()=>s.remove(),6500);
  },150);
});
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print("🎃 Running at http://localhost:8000  (Ctrl+C to stop)")
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
