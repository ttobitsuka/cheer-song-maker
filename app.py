import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="パワプロ風応援歌作成", layout="wide")

st.title("⚾️ パワプロ風・応援歌エディタ")
st.write("マス目をタップして音を置いてみよう！")

# 音程の定義（高い順）
NOTES = ["ド(高)", "シ", "ラ", "ソ", "ファ", "ミ", "レ", "ド"]
FREQS = [523.25, 493.88, 440.00, 392.00, 349.23, 329.63, 293.66, 261.63]
# 小節数（とりあえず4拍子×4小節＝16マス）
STEPS = 16

# JavaScriptとHTMLでグリッドを作成
js_code = f"""
<div id="editor" style="display: grid; grid-template-columns: 80px repeat({STEPS}, 1fr); gap: 2px; background: #333; padding: 5px; border-radius: 5px;">
    <script>
    const notes = {NOTES};
    const freqs = {FREQS};
    const steps = {STEPS};
    const grid = [];

    // グリッドの初期化
    for (let i = 0; i < notes.length; i++) {{
        document.write(`<div style="color: white; background: #444; padding: 10px; text-align: center; font-size: 12px;">${{notes[i]}}</div>`);
        grid[i] = [];
        for (let j = 0; j < steps; j++) {{
            const id = `cell-${{i}}-${{j}}`;
            document.write(`<div id="${{id}}" onclick="toggleCell(${{i}}, ${{j}})" style="background: #eee; height: 40px; cursor: pointer; border-radius: 2px;"></div>`);
        }}
    }}

    function toggleCell(row, col) {{
        const cell = document.getElementById(`cell-${{row}}-${{col}}`);
        // 同じ列の他のセルをリセット（単音のみ）
        for (let i = 0; i < notes.length; i++) {{
            if (i !== row) {{
                grid[i][col] = false;
                document.getElementById(`cell-${{i}}-${{col}}`).style.background = '#eee';
            }}
        }}
        
        grid[row][col] = !grid[row][col];
        cell.style.background = grid[row][col] ? '#ff4b4b' : '#eee';
    }}

    let audioCtx = null;
    function play() {{
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();

        let tempo = 120;
        let noteTime = 60 / tempo * 0.5;
        let startTime = audioCtx.currentTime;

        for (let j = 0; j < steps; j++) {{
            for (let i = 0; i < notes.length; i++) {{
                if (grid[i][j]) {{
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = 'square';
                    osc.frequency.setValueAtTime(freqs[i], startTime + (j * noteTime));
                    gain.gain.setValueAtTime(0.1, startTime + (j * noteTime));
                    gain.gain.exponentialRampToValueAtTime(0.001, startTime + (j * noteTime) + noteTime - 0.05);
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start(startTime + (j * noteTime));
                    osc.stop(startTime + (j * noteTime) + noteTime);
                }}
            }}
        }}
    }}
    </script>
</div>
<br>
<button onclick="play()" style="width: 100%; padding: 15px; background: #008cba; color: white; border: none; border-radius: 5px; font-size: 18px; cursor: pointer;">
    ▶ 曲を再生する
</button>
"""

components.html(js_code, height=500)

st.info("💡 縦軸が音の高さ、横軸が時間です。マス目をタップして赤い色をつけてから再生してください。")
