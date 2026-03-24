import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="応援歌メーカー", layout="centered")

st.title("🎺 簡易・応援歌メーカー")
st.write("パワプロ風に、ドレミでメロディを作ってみよう！")

# 1. メロディ入力エリア
st.subheader("📝 メロディ入力")
col1, col2 = st.columns([3, 1])

with col1:
    # ユーザーが「ドレミ」を入力する
    melody_input = st.text_area(
        "ドレミを入力（例: ドレミド レミファレ）",
        value="ドレミド レミファレ ミファソミ ファソラファ",
        help="ひらがなで『ド・レ・ミ・ファ・ソ・ラ・シ』を入力してください。スペースで休み（休符）になります。"
    )

with col2:
    tempo = st.slider("テンポ", 60, 200, 120)

# 2. 再生機能（JavaScriptを利用してブラウザで音を鳴らす）
st.subheader("🎵 再生")

# ドレミを周波数に変換するマッピング
notes_map = {
    "ド": 261.63, "レ": 293.66, "ミ": 329.63, "ファ": 349.23,
    "ソ": 392.00, "ラ": 440.00, "シ": 493.88, "ド（高）": 523.25
}

# 再生用のJavaScriptコード
js_code = f"""
<script>
const context = new (window.AudioContext || window.webkitAudioContext)();
const notes = {list(notes_map.keys())};
const freqs = {list(notes_map.values())};
const input = "{melody_input}";
const tempo = {tempo};

function playSong() {{
    let currentTime = context.currentTime;
    const noteDuration = 60 / tempo * 0.5; // 8分音符くらいの長さ

    // 文字列を1文字ずつ（または2文字ずつ）解析
    const melody = input.split(/[\s,、]+/); 

    melody.forEach(symbol => {{
        const index = notes.indexOf(symbol);
        if (index !== -1) {{
            const osc = context.createOscillator();
            const gain = context.createGain();
            
            osc.type = 'square'; // パワプロ風のピコピコ音（矩形波）
            osc.frequency.setValueAtTime(freqs[index], currentTime);
            
            gain.gain.setValueAtTime(0.1, currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, currentTime + noteDuration - 0.05);
            
            osc.connect(gain);
            gain.connect(context.destination);
            
            osc.start(currentTime);
            osc.stop(currentTime + noteDuration);
        }}
        currentTime += noteDuration;
    }});
}}
</script>
<button onclick="playSong()" style="
    background-color: #ff4b4b;
    color: white;
    padding: 15px 32px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    width: 100%;
">▶ 曲を再生する</button>
"""

# HTML/JSを表示
components.html(js_code, height=100)

# 3. 歌詞などのメモ
st.divider()
st.subheader("💬 歌詞・設定メモ")
player_name = st.text_input("選手名", "パワプロくん")
lyrics = st.text_area("歌詞", "かっ飛ばせー！ パワプロくん！")

if st.button("応援歌設定を保存"):
    st.success(f"【{player_name}】の応援歌を仮保存しました（ブラウザを閉じると消えます）")
