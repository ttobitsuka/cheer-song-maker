import streamlit as st
import streamlit.components.v1 as components

# ページを広く使う設定
st.set_page_config(page_title="応援歌エディタ", layout="wide")

st.title("⚾️ 応援歌エディタ")
st.write("もしマス目が見えない場合は、画面を下に引っ張って更新してください。")

# 音階データ
NOTES = ["ド(高)", "シ", "ラ#", "ラ", "ソ#", "ソ", "ファ#", "ファ", "ミ", "レ#", "レ", "ド#", "ド"]
FREQS = [523.25, 493.88, 466.16, 440.00, 415.30, 392.00, 369.99, 349.23, 329.63, 311.13, 293.66, 277.18, 261.63]
IS_SHARP = [False, False, True, False, True, False, True, False, False, True, False, True, False]

js_code = f"""
<div style="background: #333; padding: 10px; border-radius: 8px; color: white; font-size: 13px; margin-bottom: 10px;">
    🎨 <b>タップ:</b> なし → <span style="color:#ff4b4b">●8分</span> → <span style="color:#007bff">●4分</span> → <span style="color:#ffca28">●16分</span>
</div>

<div id="scroll-wrapper" style="width: 100%; height: 500px; overflow: auto; -webkit-overflow-scrolling: touch; background: #111; border: 1px solid #444;">
    <div id="grid-root" style="display: grid; grid-template-columns: 70px repeat(16, 55px); gap: 2px; padding: 5px; width: max-content;">
        </div>
</div>

<button id="playBtn" style="margin-top: 20px; width: 100%; padding: 25px; background: #28a745; color: white; border: none; border-radius: 12px; font-size: 22px; font-weight: bold; cursor: pointer;">
    🎶 曲を再生する
</button>

<script>
const notes = {NOTES};
const freqs = {FREQS};
const isSharp = {IS_SHARP};
const steps = 16;
const grid = Array.from({{ length: notes.length }}, () => Array(steps).fill(0));
const root = document.getElementById('grid-root');

for (let i = 0; i < notes.length; i++) {{
    const label = document.createElement('div');
    label.innerText = notes[i];
    label.style = `color:white; background:${{isSharp[i]?'#333':'#555'}}; padding:15px 2px; text-align:center; font-size:12px; font-weight:bold; position:sticky; left:0; z-index:10;`;
    root.appendChild(label);

    for (let j = 0; j < steps; j++) {{
        const cell = document.createElement('div');
        cell.id = `cell-${{i}}-${{j}}`;
        const defaultBg = isSharp[i] ? '#bbb' : '#eee';
        cell.style = `background:${{defaultBg}}; height:45px; width:55px; cursor:pointer; border-radius:2px;`;
        
        cell.onclick = () => {{
            for(let r=0; r<notes.length; r++) {{
                if(r !== i) {{
                    grid[r][j] = 0;
                    document.getElementById(`cell-${{r}}-${{j}}`).style.background = isSharp[r]?'#bbb':'#eee';
                }}
            }}
            grid[i][j] = (grid[i][j] + 1) % 4;
            const colors = [defaultBg, '#ff4b4b', '#007bff', '#ffca28'];
            cell.style.background = colors[grid[i][j]];
        }};
        root.appendChild(cell);
    }}
}}

let audioCtx = null;
document.getElementById('playBtn').onclick = () => {{
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
    const tempo = 140;
    const baseTime = 60 / tempo;
    const startTime = audioCtx.currentTime;

    for (let j = 0; j < steps; j++) {{
        for (let i = 0; i < notes.length; i++) {{
            const val = grid[i][j];
            if (val > 0) {{
                let d = [0, baseTime*0.5, baseTime, baseTime*0.25][val];
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'square';
                osc.frequency.setValueAtTime(freqs[i], startTime + (j * baseTime * 0.5));
                gain.gain.setValueAtTime(0.1, startTime + (j * baseTime * 0.5));
                gain.gain.exponentialRampToValueAtTime(0.001, startTime + (j * baseTime * 0.5) + d - 0.02);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start(startTime + (j * baseTime * 0.5));
                osc.stop(startTime + (j * baseTime * 0.5) + d);
            }}
        }}
    }}
}};
</script>
"""

# heightを600に広げて確実に表示させる
components.html(js_code, height=700)
