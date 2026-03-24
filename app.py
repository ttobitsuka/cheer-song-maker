import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="応援歌エディタ", layout="centered")

st.title("⚾️ 応援歌エディタ")
st.write("マス目をタップして色をつけてから、下の「演奏」を押してください！")

# 1. 音階データ
NOTES = ["ド(高)", "シ", "ラ#", "ラ", "ソ#", "ソ", "ファ#", "ファ", "ミ", "レ#", "レ", "ド#", "ド"]
FREQS = [523.25, 493.88, 466.16, 440.00, 415.30, 392.00, 369.99, 349.23, 329.63, 311.13, 293.66, 277.18, 261.63]
IS_SHARP = [False, False, True, False, True, False, True, False, False, True, False, True, False]

# 2. メインのJavaScriptエディタ
# スマホでも押しやすいようにボタンを大きくし、横スクロールを強化しました
js_code = f"""
<div style="background: #222; padding: 10px; border-radius: 8px; color: white; font-size: 12px; margin-bottom: 10px;">
    🎨 <b>タップで切替:</b> なし → <span style="color:red">●8分</span> → <span style="color:cyan">●4分</span> → <span style="color:yellow">●16分</span>
</div>

<div id="container" style="overflow-x: auto; -webkit-overflow-scrolling: touch; background: #111; padding: 5px; border-radius: 5px;">
    <div id="grid-root" style="display: inline-grid; grid-template-columns: 60px repeat(16, 45px); gap: 2px;">
    </div>
</div>

<button id="playBtn" style="margin-top: 20px; width: 100%; padding: 20px; background: #28a745; color: white; border: none; border-radius: 10px; font-size: 20px; font-weight: bold; cursor: pointer;">
    🎶 曲を再生する
</button>

<script>
const notes = {NOTES};
const freqs = {FREQS};
const isSharp = {IS_SHARP};
const steps = 16;
const grid = Array.from({{ length: notes.length }}, () => Array(steps).fill(0));

const root = document.getElementById('grid-root');

// グリッド作成
for (let i = 0; i < notes.length; i++) {{
    const label = document.createElement('div');
    label.innerText = notes[i];
    label.style = `color:white; background:${{isSharp[i]?'#333':'#555'}}; padding:10px 2px; text-align:center; font-size:10px; font-weight:bold;`;
    root.appendChild(label);

    for (let j = 0; j < steps; j++) {{
        const cell = document.createElement('div');
        cell.id = `cell-${{i}}-${{j}}`;
        cell.style = "background:#eee; height:35px; width:45px; cursor:pointer; border-radius:2px;";
        cell.onclick = () => {{
            // 同一列をリセット
            for(let r=0; r<notes.length; r++) {{
                if(r !== i) {{
                    grid[r][j] = 0;
                    document.getElementById(`cell-${{r}}-${{j}}`).style.background = isSharp[r]?'#ccc':'#eee';
                }}
            }}
            // 状態切り替え
            grid[i][j] = (grid[i][j] + 1) % 4;
            const colors = ['#eee', '#ff4b4b', '#007bff', '#ffca28'];
            if(isSharp[i] && grid[i][j]===0) cell.style.background = '#ccc';
            else cell.style.background = colors[grid[i][j]];
        }};
        root.appendChild(cell);
    }}
}}

// 再生ロジック
let audioCtx = null;
document.getElementById('playBtn').onclick = () => {{
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const tempo = 135;
    const baseTime = 60 / tempo;
    const startTime = audioCtx.currentTime;

    for (let j = 0; j < steps; j++) {{
        for (let i = 0; i < notes.length; i++) {{
            const val = grid[i][j];
            if (val > 0) {{
                let duration = [0, baseTime*0.5, baseTime, baseTime*0.25][val];
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'square';
                osc.frequency.setValueAtTime(freqs[i], startTime + (j * baseTime * 0.5));
                gain.gain.setValueAtTime(0.1, startTime + (j * baseTime * 0.5));
                gain.gain.exponentialRampToValueAtTime(0.001, startTime + (j * baseTime * 0.5) + duration - 0.02);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start(startTime + (j * baseTime * 0.5));
                osc.stop(startTime + (j * baseTime * 0.5) + duration);
            }}
        }}
    }}
}};
</script>
"""

components.html(js_code, height=750, scrolling=True)

st.warning("⚠️ 音が出ない時は、iPhoneの左横にあるスイッチ（マナーモード）をOFFにしてください。")
