import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="パワプロ風・半音対応エディタ", layout="wide")

st.title("⚾️ 応援歌エディタ（半音/シャープ対応版）")
st.write("黒いラベルの行が半音（#）です。ポチポチして名曲を作ろう！")

# 音名、周波数、背景色の定義（高い順）
SOUND_DATA = [
    {"name": "ド(高)", "freq": 523.25, "is_sharp": False},
    {"name": "シ", "freq": 493.88, "is_sharp": False},
    {"name": "ラ#", "freq": 466.16, "is_sharp": True},
    {"name": "ラ", "freq": 440.00, "is_sharp": False},
    {"name": "ソ#", "freq": 415.30, "is_sharp": True},
    {"name": "ソ", "freq": 392.00, "is_sharp": False},
    {"name": "ファ#", "freq": 369.99, "is_sharp": True},
    {"name": "ファ", "freq": 349.23, "is_sharp": False},
    {"name": "ミ", "freq": 329.63, "is_sharp": False},
    {"name": "レ#", "freq": 311.13, "is_sharp": True},
    {"name": "レ", "freq": 293.66, "is_sharp": False},
    {"name": "ド#", "freq": 277.18, "is_sharp": True},
    {"name": "ド", "freq": 261.63, "is_sharp": False},
]

STEPS = 16 # 横のマス目数

# JavaScriptのデータに変換
js_notes = [d["name"] for d in SOUND_DATA]
js_freqs = [d["freq"] for d in SOUND_DATA]
js_sharps = [d["is_sharp"] for d in SOUND_DATA]

js_code = f"""
<div id="editor-container" style="overflow-x: auto;">
    <div id="editor" style="display: grid; grid-template-columns: 80px repeat({STEPS}, 1fr); gap: 2px; background: #222; padding: 5px; min-width: 800px;">
        <script>
        const notes = {js_notes};
        const freqs = {js_freqs};
        const isSharps = {js_sharps};
        const steps = {STEPS};
        const grid = Array.from({{ length: notes.length }}, () => Array(steps).fill(false));

        // グリッド生成
        for (let i = 0; i < notes.length; i++) {{
            // 音階ラベル（半音は黒っぽく）
            const labelBg = isSharps[i] ? '#333' : '#555';
            const labelColor = isSharps[i] ? '#ffca28' : 'white';
            document.write(`<div style="color: ${{labelColor}}; background: ${{labelBg}}; padding: 10px 5px; text-align: center; font-size: 11px; font-weight: bold; border-right: 2px solid #222;">${{notes[i]}}</div>`);
            
            for (let j = 0; j < steps; j++) {{
                const id = `cell-${{i}}-${{j}}`;
                const cellBg = isSharps[i] ? '#ddd' : '#eee'; // 半音の行は少し色を変える
                document.write(`<div id="${{id}}" onclick="toggleCell(${{i}}, ${{j}})" style="background: ${{cellBg}}; height: 35px; cursor: pointer; border-radius: 1px;"></div>`);
            }}
        }}

        function toggleCell(row, col) {{
            // 同じ列をリセット（単音制限）
            for (let i = 0; i < notes.length; i++) {{
                if (i !== row) {{
                    grid[i][col] = false;
                    document.getElementById(`cell-${{i}}-${{col}}`).style.background = isSharps[i] ? '#ddd' : '#eee';
                }}
            }}
            
            grid[row][col] = !grid[row][col];
            const cell = document.getElementById(`cell-${{row}}-${{col}}`);
            cell.style.background = grid[row][col] ? '#ff4b4b' : (isSharps[row] ? '#ddd' : '#eee');
        }}

        let audioCtx = null;
        function play() {{
            if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            if (audioCtx.state === 'suspended') audioCtx.resume();

            let tempo = 130;
            let noteTime = 60 / tempo * 0.5;
            let startTime = audioCtx.currentTime;

            for (let j = 0; j < steps; j++) {{
                for (let i = 0; i < notes.length; i++) {{
                    if (grid[i][j]) {{
                        const osc = audioCtx.createOscillator();
                        const gain = audioCtx.createGain();
                        osc.type = 'square'; // パワプロサウンド
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
</div>
<br>
<button onclick="play()" style="width: 100%; padding: 20px; background: #28a745; color: white; border: none; border-radius: 10px; font-size: 20px; font-weight: bold; cursor: pointer; box-shadow: 0 4px #1e7e34;">
    🎵 演奏を聴く
</button>
"""

components.html(js_code, height=600)

st.markdown("""
### ✍️ 作曲のコツ
- **メジャー（明るい）:** ド・ミ・ソを基本に使う
- **マイナー（悲しい/かっこいい）:** 「レ#」や「ソ#」など半音を混ぜる
- **スピード:** テンポを上げると攻撃開始、下げるとチャンス風になります
""")
