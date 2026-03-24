import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="パワプロ風・音長エディタ", layout="wide")

st.title("⚾️ 応援歌エディタ（音の長さ打ち分けVer.）")
st.write("同じマスをタップすると、音の長さが切り替わります！")

# 音階データ
SOUND_DATA = [
    {"name": "ド(高)", "freq": 523.25, "sharp": False}, {"name": "シ", "freq": 493.88, "sharp": False},
    {"name": "ラ#", "freq": 466.16, "sharp": True}, {"name": "ラ", "freq": 440.00, "sharp": False},
    {"name": "ソ#", "freq": 415.30, "sharp": True}, {"name": "ソ", "freq": 392.00, "sharp": False},
    {"name": "ファ#", "freq": 369.99, "sharp": True}, {"name": "ファ", "freq": 349.23, "sharp": False},
    {"name": "ミ", "freq": 329.63, "sharp": False}, {"name": "レ#", "freq": 311.13, "sharp": True},
    {"name": "レ", "freq": 293.66, "sharp": False}, {"name": "ド#", "freq": 277.18, "sharp": True},
    {"name": "ド", "freq": 261.63, "sharp": False},
]

STEPS = 16 

js_notes = [d["name"] for d in SOUND_DATA]
js_freqs = [d["freq"] for d in SOUND_DATA]
js_sharps = [d["sharp"] for d in SOUND_DATA]

js_code = f"""
<div style="background: #333; padding: 10px; border-radius: 8px; margin-bottom: 10px; display: flex; gap: 20px; color: white; font-size: 13px;">
    <span>🎨 <b>色と長さ:</b></span>
    <span><span style="background:red; padding:2px 8px; border-radius:3px;"></span> 8分(通常)</span>
    <span><span style="background:blue; padding:2px 8px; border-radius:3px;"></span> 4分(長)</span>
    <span><span style="background:yellow; padding:2px 8px; border-radius:3px; color:black;"></span> 16分(短)</span>
</div>

<div id="editor-container" style="overflow-x: auto;">
    <div id="editor" style="display: grid; grid-template-columns: 80px repeat({STEPS}, 1fr); gap: 2px; background: #222; padding: 5px; min-width: 800px;">
        <script>
        const notes = {js_notes};
        const freqs = {js_freqs};
        const isSharps = {js_sharps};
        const steps = {STEPS};
        // gridには 0:なし, 1:8分, 2:4分, 3:16分 を入れる
        const grid = Array.from({{ length: notes.length }}, () => Array(steps).fill(0));

        for (let i = 0; i < notes.length; i++) {{
            const labelBg = isSharps[i] ? '#333' : '#555';
            document.write(`<div style="color:white; background:${{labelBg}}; padding:10px 5px; text-align:center; font-size:11px; font-weight:bold;">${{notes[i]}}</div>`);
            
            for (let j = 0; j < steps; j++) {{
                const id = `cell-${{i}}-${{j}}`;
                document.write(`<div id="${{id}}" onclick="cycleNote(${{i}}, ${{j}})" style="background:#eee; height:35px; cursor:pointer;"></div>`);
            }}
        }}

        function cycleNote(row, col) {{
            // 他の音程をリセット
            for (let i = 0; i < notes.length; i++) {{
                if (i !== row) {{
                    grid[i][col] = 0;
                    updateStyle(i, col);
                }}
            }}

            grid[row][col] = (grid[row][col] + 1) % 4;
            updateStyle(row, col);
        }}

        function updateStyle(r, c) {{
            const cell = document.getElementById(`cell-${{r}}-${{c}}`);
            const val = grid[r][c];
            if (val === 1) cell.style.background = 'red';    // 8分
            else if (val === 2) cell.style.background = 'blue';  // 4分
            else if (val === 3) cell.style.background = 'yellow'; // 16分
            else cell.style.background = isSharps[r] ? '#ccc' : '#eee';
        }}

        let audioCtx = null;
        function play() {{
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();

            let tempo = 130;
            let baseTime = 60 / tempo; // 4分音符の秒数
            let startTime = audioCtx.currentTime;

            for (let j = 0; j < steps; j++) {{
                for (let i = 0; i < notes.length; i++) {{
                    const val = grid[i][j];
                    if (val > 0) {{
                        let duration = 0;
                        if (val === 1) duration = baseTime * 0.5; // 8分
                        else if (val === 2) duration = baseTime;     // 4分
                        else if (val === 3) duration = baseTime * 0.25; // 16分

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
        }}
        </script>
    </div>
</div>
<br>
<button onclick="play()" style="width:100%; padding:20px; background:#28a745; color:white; border:none; border-radius:10px; font-size:20px; font-weight:bold; cursor:pointer;">
    🎶 オリジナル応援歌を演奏！
</button>
"""

components.html(js_code, height=650)
