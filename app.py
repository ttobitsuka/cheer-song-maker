import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="応援歌メーカーV2", layout="centered")

st.title("🎺 応援歌メーカー（文字入力・音長対応版）")

st.markdown("""
### ✍️ 入力のルール
音名のあとに記号をつけて長さを変えられます！
- **ド** （そのまま） → **8分音符** (普通)
- **ド-** （マイナス） → **4分音符** (長い)
- **ド.** （ドット） → **16分音符** (短い)
- **休** または **スペース** → **休み**
""")

# 1. メロディ入力
melody_input = st.text_area(
    "メロディを入力",
    value="ド ド レ ミ- ド. レ. ミ-",
    help="例: ド- (長) ド (普) ド. (短)",
    height=150
)

tempo = st.slider("テンポ", 60, 200, 135)

# 2. 再生ロジック (JavaScript)
js_code = f"""
<div id="status" style="color: #888; font-size: 14px; margin-bottom: 5px;">準備完了</div>
<button id="playBtn" style="
    background-color: #28a745;
    color: white;
    padding: 20px;
    border: none;
    border-radius: 12px;
    cursor: pointer;
    font-size: 18px;
    font-weight: bold;
    width: 100%;
    box-shadow: 0 4px #1e7e34;
">🎶 このメロディを再生する</button>

<script>
let audioCtx = null;

const notesMap = {{
    "ド": 261.63, "ド#": 277.18, "レ": 293.66, "レ#": 311.13,
    "ミ": 329.63, "ファ": 349.23, "ファ#": 369.99, "ソ": 392.00,
    "ソ#": 415.30, "ラ": 440.00, "ラ#": 466.16, "シ": 493.88, "ド（高）": 523.25
}};

document.getElementById('playBtn').addEventListener('click', function() {{
    if (!audioCtx) {{
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }}
    if (audioCtx.state === 'suspended') {{
        audioCtx.resume();
    }}

    const input = "{melody_input}";
    const tempo = {tempo};
    const baseUnit = 60 / tempo * 0.5; // 8分音符を基準(0.5拍)
    let currentTime = audioCtx.currentTime;

    // スペースや改行で分割
    const tokens = input.split(/[\\s\\n]+/);

    tokens.forEach(token => {{
        if (!token) return;

        let noteName = token.replace(/[-.]/g, ""); // 記号を取り除いた名前
        let durationMultiplier = 1.0; // デフォルトは8分

        if (token.includes("-")) durationMultiplier = 2.0; // 4分
        if (token.includes(".")) durationMultiplier = 0.5; // 16分

        const duration = baseUnit * durationMultiplier;

        if (notesMap[noteName]) {{
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            
            osc.type = 'square';
            osc.frequency.setValueAtTime(notesMap[noteName], currentTime);
            
            gain.gain.setValueAtTime(0.1, currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, currentTime + duration - 0.02);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.start(currentTime);
            osc.stop(currentTime + duration);
        }}
        // 鳴っていてもいなくても、時間は進める
        currentTime += duration;
    }});
    
    document.getElementById('status').innerText = "再生中...";
    setTimeout(() => {{
        document.getElementById('status').innerText = "準備完了";
    }}, (currentTime - audioCtx.currentTime) * 1000);
}});
</script>
"""

components.html(js_code, height=150)

st.info("💡 半音は『ド#』のように入力してください。")
