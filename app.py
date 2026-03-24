import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="応援歌エディタ", layout="wide")

st.title("⚾️ 応援歌グリッドエディタ")
st.write("マス目をタップして音を置いてください。横にスライドすると続きがあります。")

# 音階データ（半音あり・フルスケール）
SOUND_DATA = [
    {"name": "ド(高)", "freq": 523.25, "s": False}, {"name": "シ", "freq": 493.88, "s": False},
    {"name": "ラ#", "freq": 466.16, "s": True}, {"name": "ラ", "freq": 440.00, "s": False},
    {"name": "ソ#", "freq": 415.30, "s": True}, {"name": "ソ", "freq": 392.00, "s": False},
    {"name": "ファ#", "freq": 369.99, "s": True}, {"name": "ファ", "freq": 349.23, "s": False},
    {"name": "ミ", "freq": 329.63, "s": False}, {"name": "レ#", "freq": 311.13, "s": True},
    {"name": "レ", "freq": 293.66, "s": False}, {"name": "ド#", "freq": 277.18, "s": True},
    {"name": "ド", "freq": 261.63, "s": False},
]
STEPS = 16 

js_notes = [d["name"] for d in SOUND_DATA]
js_freqs = [d["freq"] for d in SOUND_DATA]
js_sharps = [d["s"] for d in SOUND_DATA]

js_code = f"""
<div style="background: #333; padding: 10px; border-radius: 8px; color: white; font-size: 13px; margin-bottom: 10px; display: flex; gap: 15px;">
    <span>🎨 <b>タップ:</b> なし→<span style="color:red">●8分</span>→<span style="color:blue">●4分</span>→<span style="color:orange">●16分</span></span>
</div>

<div id="wrapper" style="width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch; background: #111; border-radius: 5px;">
    <div id="grid-root" style="display: grid; grid-template-columns: 70px repeat({STEPS}, 50px); gap: 2px; padding: 5px; width: max-content;">
        <script>
        const notes = {js_notes};
        const freqs = {js_freqs};
        const isSharps = {js_sharps};
        const steps = {STEPS};
        const grid = Array.from({{ length: notes.length }}, () => Array(steps).fill(0));

        const root = document.getElementById('grid-root');

        for (let i = 0; i < notes.length; i++) {{
            const label = document.createElement('div');
            label.innerText = notes[i];
            label.style = `color:white; background:${{isSharps[i]?'#333':'#555'}}; padding:12px 0; text-align:center; font-size:11px; font-weight:bold; position:sticky; left:0; z-index:10; border-right:1px solid #222;`;
            root.appendChild(label);
            
            for (let j = 0; j < steps; j++) {{
                const cell = document.createElement('div');
                cell.id = `cell-${{i}}-${{j}}`;
                const defBg = isSharps[i] ? '#bbb' : '#eee';
                cell.style = `background:${{defBg}}; height:40px; width:50px; cursor:pointer; border-radius:2px;`;
                
                cell.onclick = () => {{
                    for(let r=0; r<notes.length; r++) {{
                        if(r !== i) {{
                            grid[r][j] = 0;
                            document.getElementById(`cell-${{r}}-${{j}}`).style.background = isSharps[r]?'#bbb':'#eee';
                        }}
                    }}
                    grid[i][j] = (grid[i][j] + 1) % 4;
                    const colors = [defBg, 'red', '#007bff', 'orange'];
                    cell.style.background = colors[grid[i][j]];
                }};
                root.appendChild(cell);
            }}
        }}

        let audioCtx = null;
        function play() {{
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();

            const tempo = 135;
            const baseTime = 60 / tempo;
            let startTime = audioCtx.currentTime;

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
        }}
        </script>
    </div>
</div>

<button onclick="play()" style="margin-top: 20px; width: 100%; padding: 25px; background: #28a745; color: white; border: none; border-radius: 12px; font-size: 20px; font-weight: bold; cursor: pointer;">
    🎶 オリジナル応援歌を演奏！
</button>
"""

components.html(js_code, height=700)
