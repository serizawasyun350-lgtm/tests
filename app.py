import os
from flask import Flask, render_template_string, redirect

app = Flask(__name__)

# 提供されたHTMLを読み込むか、直接保持
HTML_CONTENT = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>コグトレ オンライン風 トレーニング 完全版</title>
    <link href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-sky: #eaf6ff;
            --bg-grass: #b5e2a8;
            --main-border: #2c221e;
            --card-bg: #fdfbf7;
            --blue-category: #7bc0e3;
            --green-category: #6bc296;
            --purple-category: #d6b4d6;
            --orange-category: #e59a58;
            --yellow-category: #ded071;
            --pink-category: #efa6a2;
            --gold-accent: #f5ab35;
            --mission-yellow: #f8c325;
        }

        * {
            box-sizing: border-box;
            user-select: none;
            -webkit-user-select: none;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'M PLUS Rounded 1c', sans-serif;
            background-color: var(--bg-grass);
            color: #333;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            position: relative;
        }

        .sky-bg {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 75vh;
            background: linear-gradient(to bottom, #ffffff 0%, var(--bg-sky) 100%);
            z-index: 0;
        }
        .grass-bg {
            position: absolute;
            bottom: 0; left: 0; width: 100%; height: 25vh;
            background-color: var(--bg-grass);
            border-top: 4px solid #82b875;
            z-index: 0;
        }

        .bg-element { position: absolute; z-index: 1; opacity: 0.7; pointer-events: none; }
        .bg-bird { top: 12%; left: 10%; font-size: 28px; }
        .bg-bird2 { top: 18%; right: 12%; font-size: 24px; }
        .bg-tree { bottom: 22vh; left: 4%; font-size: 40px; }
        .bg-tree2 { bottom: 22vh; right: 5%; font-size: 45px; }

        .app-container {
            position: relative;
            z-index: 10;
            width: 96vw;
            max-width: 1040px;
            height: 94vh;
            max-height: 680px;
            background: rgba(255, 255, 255, 0.45);
            border-radius: 28px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 12px 18px;
            box-shadow: 0 12px 36px rgba(0,0,0,0.12);
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 52px;
        }
        .header-left, .header-right {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .icon-btn {
            width: 44px; height: 44px;
            background-color: #3a3f47;
            color: #fff;
            border: 3px solid var(--main-border);
            border-radius: 14px;
            display: flex; justify-content: center; align-items: center;
            font-size: 20px; cursor: pointer;
            box-shadow: 0 4px 0 var(--main-border);
            transition: transform 0.1s;
        }
        .icon-btn:active { transform: translateY(4px); box-shadow: 0 0 0 var(--main-border); }

        .user-id-badge {
            background-color: #fff;
            border: 2px solid #ccc;
            border-radius: 20px;
            padding: 4px 12px;
            font-weight: 800; font-size: 14px;
            display: flex; align-items: center; gap: 6px;
            cursor: pointer;
            box-shadow: 0 2px 0 rgba(0,0,0,0.1);
        }
        .user-id-badge:active { transform: translateY(1px); }
        .user-id-badge span.id-tag {
            background-color: #f77d67;
            color: white;
            padding: 2px 6px; border-radius: 10px; font-size: 11px;
        }

        .title-logo {
            font-size: 26px; font-weight: 900; color: #4a4a4a;
            display: flex; align-items: center; gap: 8px; letter-spacing: 2px;
        }

        .main-stage {
            flex: 1;
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            position: relative; margin: 6px 0;
        }

        .window-panel {
            width: 100%; height: 100%;
            background-color: #ebdcd0;
            border: 4px solid var(--main-border);
            border-radius: 24px;
            display: flex; flex-direction: column;
            overflow: hidden;
            box-shadow: inset 0 0 0 4px #fff, 0 8px 0 rgba(0,0,0,0.15);
            position: relative;
        }

        .panel-header {
            height: 48px;
            display: flex; justify-content: center; align-items: center;
            font-size: 20px; font-weight: 800; color: #333;
            border-bottom: 4px solid var(--main-border);
            background-color: var(--blue-category);
            gap: 8px; position: relative;
        }

        .close-header-btn {
            position: absolute; right: 12px; top: 50%;
            transform: translateY(-50%);
            background-color: #f77d67; color: #fff;
            border: 2px solid var(--main-border);
            border-radius: 14px; padding: 4px 12px;
            font-size: 14px; font-weight: 800; cursor: pointer;
            box-shadow: 0 3px 0 var(--main-border);
            display: flex; align-items: center; gap: 4px;
        }

        .panel-body {
            flex: 1; padding: 16px;
            display: flex; justify-content: center; align-items: center;
            gap: 16px; position: relative;
        }

        ruby { ruby-position: over; }
        rt { font-size: 10px; font-weight: 700; color: #555; }

        .top-outer-wrapper {
            display: flex; flex-direction: column;
            align-items: center; justify-content: space-between;
            width: 100%; height: 100%;
        }

        .top-container { display: flex; width: 100%; height: 82%; gap: 16px; }
        .top-menu-grid {
            flex: 1;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            grid-template-rows: repeat(2, 1fr);
            gap: 14px;
        }

        .cat-btn {
            background-color: #fff;
            border: 4px solid var(--main-border);
            border-radius: 28px;
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            cursor: pointer; box-shadow: 0 8px 0 var(--main-border);
            transition: all 0.15s ease; position: relative;
        }
        .cat-btn:hover { transform: translateY(-2px); }
        .cat-btn:active { transform: translateY(6px); box-shadow: 0 2px 0 var(--main-border); }

        .cat-btn .icon { font-size: 30px; margin-bottom: 2px; }
        .cat-btn .title { font-size: 20px; font-weight: 900; color: #2c221e; }

        .cat-btn.blue { background-color: var(--blue-category); }
        .cat-btn.green { background-color: var(--green-category); }
        .cat-btn.purple { background-color: var(--purple-category); }
        .cat-btn.orange { background-color: var(--orange-category); }
        .cat-btn.yellow { background-color: var(--yellow-category); }
        .cat-btn.pink { background-color: var(--pink-category); }

        .side-btn-group { display: flex; flex-direction: column; gap: 12px; }

        .mission-tab-btn {
            width: 140px;
            background-color: var(--mission-yellow);
            border: 4px solid var(--main-border);
            border-radius: 28px;
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            cursor: pointer; box-shadow: 0 8px 0 var(--main-border);
            padding: 10px; transition: all 0.15s ease;
        }

        .notice-bar {
            width: 90%; height: 48px;
            background-color: #dbece2; border: 3px solid #aacab3;
            border-radius: 24px; display: flex; justify-content: center;
            align-items: center; font-size: 16px; font-weight: 800;
            color: #333; gap: 10px; box-shadow: 0 3px 0 rgba(0,0,0,0.06);
        }
        .notice-icon {
            background-color: #f77d67; color: #fff;
            width: 24px; height: 24px; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            font-size: 14px; font-weight: bold;
        }

        .sub-card-container { display: flex; justify-content: center; align-items: stretch; gap: 16px; width: 100%; height: 100%; }
        .sub-card {
            flex: 1; background-color: var(--card-bg);
            border: 3px solid var(--main-border); border-radius: 20px;
            display: flex; flex-direction: column; justify-content: space-between; align-items: center;
            padding: 12px; box-shadow: 0 4px 0 rgba(0,0,0,0.1);
        }

        .sub-card-title { font-size: 18px; font-weight: 800; text-align: center; }
        .sub-card-preview {
            flex: 1; width: 100%; display: flex; justify-content: center; align-items: center;
            background: #fff; border: 2px dashed #ccc; border-radius: 12px; margin: 8px 0;
        }

        .level-select-group { width: 100%; display: flex; flex-direction: column; align-items: center; gap: 4px; }
        .star-btns { display: flex; gap: 6px; width: 100%; justify-content: center; }

        .star-btn {
            background-color: #fff; border: 3px solid var(--main-border); border-radius: 16px;
            padding: 6px 10px; cursor: pointer; box-shadow: 0 4px 0 var(--main-border); font-size: 14px;
        }
        .star-btn .stars { color: #ff5252; font-size: 16px; }

        .stage-num-grid {
            display: grid; grid-template-columns: repeat(5, 1fr); grid-template-rows: repeat(2, 1fr);
            gap: 16px; width: 90%; height: 75%;
        }

        .stage-num-card {
            border: 4px solid var(--main-border); border-radius: 24px;
            display: flex; justify-content: center; align-items: center;
            font-size: 44px; font-weight: 900; color: #2c221e; cursor: pointer; position: relative;
            box-shadow: 0 6px 0 var(--main-border);
        }

        .stage-c1 { background-color: #fffde7; }
        .stage-c2 { background-color: #fce4ec; }
        .stage-c3 { background-color: #e8eaf6; }
        .stage-c4 { background-color: #e8f5e9; }
        .stage-c5 { background-color: #e0f7fa; }

        .hanamaru-mark { position: absolute; top: -12px; left: -12px; font-size: 32px; line-height: 1; }
        .check-mark {
            position: absolute; bottom: -6px; right: -6px;
            background-color: #2e7d32; color: #fff; width: 28px; height: 28px;
            border: 2px solid #fff; border-radius: 50%;
            display: flex; justify-content: center; align-items: center; font-size: 16px; font-weight: bold;
        }

        .game-screen {
            width: 100%; height: 100%; background-color: #fff; border-radius: 16px;
            display: flex; flex-direction: column; align-items: center; padding: 16px; position: relative;
        }

        .game-header {
            width: 100%; display: flex; justify-content: space-between; align-items: center;
            padding-bottom: 8px; border-bottom: 2px solid #eee; margin-bottom: 12px;
        }

        .game-question-text { font-size: 20px; font-weight: 800; color: #333; }
        .game-canvas-area { flex: 1; width: 100%; display: flex; justify-content: center; align-items: center; position: relative; }

        .action-btn {
            background-color: var(--gold-accent); color: #fff;
            border: 3px solid var(--main-border); border-radius: 16px;
            padding: 10px 24px; font-size: 18px; font-weight: 800; cursor: pointer;
            box-shadow: 0 4px 0 var(--main-border);
        }

        .home-back-btn {
            position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%);
            background-color: #f77d67; color: #fff;
            border: 3px solid var(--main-border); border-radius: 20px;
            padding: 6px 24px; font-weight: 800; font-size: 16px; cursor: pointer;
            box-shadow: 0 4px 0 var(--main-border); display: flex; align-items: center; gap: 6px; z-index: 5;
        }

        footer { height: 24px; display: flex; justify-content: center; align-items: center; font-size: 12px; color: #555; font-weight: 700; }

        .modal-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0, 0, 0, 0.5); display: flex; justify-content: center; align-items: center;
            z-index: 100; opacity: 0; pointer-events: none; transition: opacity 0.2s;
        }
        .modal-overlay.active { opacity: 1; pointer-events: auto; }

        .notebook-modal {
            background: #fff; border: 4px solid var(--main-border); border-radius: 24px;
            width: 80%; max-width: 500px; padding: 24px; box-shadow: 0 10px 0 rgba(0,0,0,0.2); text-align: center;
        }

        canvas.drawing-board { border: 2px solid #ccc; border-radius: 12px; background-color: #fcfcfc; cursor: crosshair; }
        .symbol-grid { display: grid; gap: 10px; }
        .symbol-item {
            display: flex; justify-content: center; align-items: center;
            background: #f0f4f8; border: 2px solid #ccc; border-radius: 12px;
            font-size: 28px; font-weight: bold; cursor: pointer;
        }

        .login-input {
            width: 100%; padding: 12px 16px; font-size: 18px;
            border: 3px solid var(--main-border); border-radius: 16px;
            margin: 12px 0 20px; outline: none; font-family: inherit; text-align: center;
        }

        .loading-overlay {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 9999;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            opacity: 0; pointer-events: none; transition: opacity 0.3s ease;
            background: repeating-linear-gradient(
                -45deg, #f8a5c2, #f8a5c2 40px, #fcf4dd 40px, #fcf4dd 80px,
                #74b9ff 80px, #74b9ff 120px, #55efc4 120px, #55efc4 160px
            );
        }
        .loading-overlay.active { opacity: 1; pointer-events: auto; }

        .loading-card {
            background: #ffffff; border: 6px solid var(--main-border); border-radius: 32px;
            padding: 30px 50px; display: flex; flex-direction: column; align-items: center;
            box-shadow: 0 12px 0 rgba(0,0,0,0.2); animation: bounceIn 0.4s ease;
        }
        @keyframes bounceIn { 0% { transform: scale(0.7); } 70% { transform: scale(1.05); } 100% { transform: scale(1); } }
        .loading-logo { font-size: 38px; font-weight: 900; color: #4a4a4a; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
        .spinner {
            width: 50px; height: 50px; border: 6px solid #e0e0e0; border-top: 6px solid #ff7675;
            border-radius: 50%; animation: spin 0.8s linear infinite; margin-bottom: 16px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .loading-text { font-size: 22px; font-weight: 800; color: #333; }

        .grid-matrix {
            display: grid; gap: 8px; border: 4px solid var(--main-border);
            border-radius: 16px; padding: 12px; background: #fff;
        }
        .grid-cell {
            width: 60px; height: 60px; border: 2px solid #ddd; border-radius: 10px;
            display: flex; justify-content: center; align-items: center;
            font-size: 24px; font-weight: bold; background: #fafafa; cursor: pointer;
        }
        .grid-cell.active-dot { background: #333; border-radius: 50%; }
        .grid-cell.selected { background: #7bc0e3; color: #fff; }
    </style>
</head>
<body>

    <div class="loading-overlay" id="loading-screen">
        <div class="loading-card">
            <div class="loading-logo">
                <span style="color:#e65b46;">コグトレ</span> オンライン
            </div>
            <div class="spinner"></div>
            <div class="loading-text">
                <ruby>読み込み中<rt>よみこみちゅう</rt></ruby>
            </div>
        </div>
    </div>

    <div class="sky-bg"></div>
    <div class="grass-bg"></div>
    <div class="bg-element bg-bird">🕊️</div>
    <div class="bg-element bg-bird2">🐤</div>
    <div class="bg-element bg-tree">🌳</div>
    <div class="bg-element bg-tree2">🌲</div>

    <div class="app-container">
        <header>
            <div class="header-left">
                <button class="icon-btn" id="btn-back" title="戻る">◀</button>
                <div class="user-id-badge" onclick="openLoginModal()" title="ユーザー切り替え">
                    <span class="id-tag">ID</span>
                    <span id="user-id-display">guDr6ElT</span>
                </div>
            </div>

            <div class="title-logo" id="header-title">
                💡 <ruby>トレーニング<rt>ちょうせん</rt></ruby>を選ぶ
            </div>

            <div class="header-right">
                <button class="icon-btn" id="btn-home" title="ホーム">🏠</button>
                <button class="icon-btn" id="btn-notebook" title="がんばりノート">📖</button>
            </div>
        </header>

        <main class="main-stage" id="stage">
            <div class="top-outer-wrapper">
                <div class="top-container">
                    <div class="top-menu-grid" id="top-menu">
                        <div class="cat-btn blue" onclick="navigateTo('see_remember')">
                            <div class="icon">👁️</div>
                            <div class="title"><ruby>見て覚える<rt>み おぼ</rt></ruby></div>
                        </div>
                        <div class="cat-btn green" onclick="navigateTo('hear_remember')">
                            <div class="icon">👂</div>
                            <div class="title"><ruby>聞いて覚える<rt>き おぼ</rt></ruby></div>
                        </div>
                        <div class="cat-btn purple" onclick="navigateTo('count')">
                            <div class="icon">🔢</div>
                            <div class="title"><ruby>数える<rt>かぞ</rt></ruby></div>
                        </div>
                        <div class="cat-btn orange" onclick="navigateTo('copy')">
                            <div class="icon">📝</div>
                            <div class="title"><ruby>写す<rt>うつ</rt></ruby></div>
                        </div>
                        <div class="cat-btn yellow" onclick="navigateTo('find')">
                            <div class="icon">🔍</div>
                            <div class="title"><ruby>見つける<rt>み</rt></ruby></div>
                        </div>
                        <div class="cat-btn pink" onclick="navigateTo('imagine')">
                            <div class="icon">💭</div>
                            <div class="title"><ruby>想像する<rt>そうぞう</rt></ruby></div>
                        </div>
                    </div>

                    <div class="side-btn-group">
                        <div class="mission-tab-btn" onclick="openMissionModal()" style="flex:1;">
                            <div style="font-size: 36px; margin-bottom: 4px;">❗</div>
                            <div style="font-size: 16px; font-weight: 900; text-align: center; color: #2c221e;">
                                コグトレ<br>ミッション
                            </div>
                        </div>
                    </div>
                </div>

                <div class="notice-bar">
                    <div class="notice-icon">！</div>
                    <div><ruby>今週<rt>こんしゅう</rt></ruby>のコグトレは、ありません。</div>
                </div>
            </div>
        </main>

        <footer>
            © TOKYO SHOSEKI CO., LTD. All rights reserved.
        </footer>
    </div>

    <div class="modal-overlay" id="login-modal">
        <div class="notebook-modal">
            <h2>👤 ユーザー ログイン</h2>
            <p style="margin-top: 8px; font-size: 14px; color: #666;">名前（ID）を入力してログインしてください</p>
            <input type="text" id="login-username-input" class="login-input" placeholder="なまえ（例: 太郎）" maxlength="12">
            
            <div style="display: flex; gap: 10px; justify-content: center;">
                <button class="action-btn" style="background: var(--blue-category);" onclick="performLogin()">ログイン</button>
                <button class="action-btn" style="background: #e65b46;" onclick="performLogout()">ログアウト</button>
                <button class="action-btn" style="background: #94a3b8;" onclick="closeModal('login-modal')">とじる</button>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="notebook-modal">
        <div class="notebook-modal">
            <h2>📖 がんばりノート</h2>
            <p style="margin: 16px 0; font-size: 18px;">ユーザー: <strong id="notebook-user-name">guDr6ElT</strong></p>
            <div id="stamp-container" style="display: flex; justify-content: center; gap: 12px; font-size: 36px; min-height: 50px;">
                💮 💮 💮 💮 💮
            </div>
            <br>
            <button class="action-btn" onclick="closeModal('notebook-modal')">閉じる</button>
        </div>
    </div>

    <div class="modal-overlay" id="mission-modal">
        <div class="notebook-modal" style="background:#fffbe6;">
            <h2 style="color:#d97706;">❗ 今日のコグトレミッション</h2>
            <p style="margin: 16px 0; font-size: 18px; font-weight:bold;">「形さがし ★1」をクリアしよう！</p>
            <button class="action-btn" style="background:#22c55e;" onclick="closeModal('mission-modal'); navigateTo('shape_find_lvl1');">ミッションに挑戦！</button>
            <button class="action-btn" style="background:#94a3b8; margin-left:10px;" onclick="closeModal('mission-modal')">とじる</button>
        </div>
    </div>

    <script>
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        function playSound(type) {
            if (audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.connect(gain); gain.connect(audioCtx.destination);

            if (type === 'correct') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(587.33, audioCtx.currentTime);
                osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.1);
                gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
                osc.start(); osc.stop(audioCtx.currentTime + 0.3);
            } else if (type === 'wrong') {
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(220, audioCtx.currentTime);
                osc.frequency.setValueAtTime(164.81, audioCtx.currentTime + 0.15);
                gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
                osc.start(); osc.stop(audioCtx.currentTime + 0.4);
            } else if (type === 'pop') {
                osc.type = 'sine';
                osc.frequency.setValueAtTime(400, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(800, audioCtx.currentTime + 0.08);
                gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
                osc.start(); osc.stop(audioCtx.currentTime + 0.08);
            }
        }

        function speakText(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const uttr = new SpeechSynthesisUtterance(text);
                uttr.lang = 'ja-JP'; uttr.rate = 0.9;
                window.speechSynthesis.speak(uttr);
            }
        }

        let currentUser = localStorage.getItem('cog_current_user') || 'guDr6ElT';

        function updateUserIdDisplay() {
            document.getElementById('user-id-display').innerText = currentUser;
            document.getElementById('notebook-user-name').innerText = currentUser;
        }

        function getUserProgressKey() { return `cog_progress_${currentUser}`; }
        function getProgressData() { return JSON.parse(localStorage.getItem(getUserProgressKey()) || '{}'); }
        function saveProgress(key) {
            const data = getProgressData();
            data[key] = true;
            localStorage.setItem(getUserProgressKey(), JSON.stringify(data));
        }

        function openLoginModal() {
            playSound('pop');
            document.getElementById('login-username-input').value = currentUser;
            document.getElementById('login-modal').classList.add('active');
        }

        function performLogin() {
            const name = document.getElementById('login-username-input').value.trim();
            if (!name) return alert('名前を入力してください！');
            currentUser = name;
            localStorage.setItem('cog_current_user', currentUser);
            updateUserIdDisplay();
            closeModal('login-modal');
            navigateTo('top');
        }

        function performLogout() {
            currentUser = 'guDr6ElT';
            localStorage.setItem('cog_current_user', currentUser);
            updateUserIdDisplay();
            closeModal('login-modal');
            navigateTo('top');
        }

        function transitionTo(callback) {
            playSound('pop');
            const loading = document.getElementById('loading-screen');
            loading.classList.add('active');
            setTimeout(() => {
                callback();
                setTimeout(() => loading.classList.remove('active'), 400);
            }, 800);
        }

        let currentCategory = null;
        let currentSubTask = null;
        let currentLevel = 1;

        const categoryData = {
            see_remember: {
                title: '見て覚える', color: 'var(--blue-category)',
                sub: [
                    { id: 'what_was', title: '何があった？', ruby: 'なに' },
                    { id: 'where_what', title: 'どこに何があった？', ruby: 'なに' },
                    { id: 'dot_where', title: '●はどこ？', ruby: '' }
                ]
            },
            hear_remember: {
                title: '聞いて覚える', color: 'var(--green-category)',
                sub: [
                    { id: 'first_pon', title: '最初とポン', ruby: 'さいしょ' },
                    { id: 'last_pon', title: '最後とポン', ruby: 'さいご' },
                    { id: 'what_order', title: '何が何番？', ruby: 'なに なんばん' }
                ]
            },
            count: {
                title: '数える', color: 'var(--purple-category)',
                sub: [
                    { id: 'symbol_find', title: '記号さがし', ruby: 'きごう' },
                    { id: 'add_find', title: 'さがし算', ruby: 'ざん' },
                    { id: 'add_challenge', title: 'さがし算チャレンジ', ruby: 'ざん' }
                ]
            },
            copy: {
                title: '写す', color: 'var(--orange-category)',
                sub: [ { id: 'dot_connect', title: '点つなぎ', ruby: 'てん' } ]
            },
            find: {
                title: '見つける', color: 'var(--yellow-category)',
                sub: [ { id: 'shape_find', title: '形さがし', ruby: 'かたち' } ]
            },
            imagine: {
                title: '想像する', color: 'var(--pink-category)',
                sub: [
                    { id: 'ranking', title: '順位決定戦', ruby: 'じゅんいけっていせん' },
                    { id: 'stamp', title: 'スタンプ', ruby: '' }
                ]
            }
        };

        const stage = document.getElementById('stage');
        const topMenuHTML = stage.innerHTML;

        function navigateTo(targetHash) {
            window.location.hash = targetHash;
        }

        window.addEventListener('hashchange', handleRoute);
        window.addEventListener('load', () => {
            // パス指定(例: /top など)をハッシュ指定に自動同期
            const pathRoute = window.location.pathname.replace('/', '');
            if (pathRoute && pathRoute !== 'index.html' && !window.location.hash) {
                window.location.hash = pathRoute;
            }
            handleRoute();
        });

        function handleRoute() {
            const rawHash = window.location.hash.replace('#', '') || 'top';
            transitionTo(() => renderRoute(rawHash));
        }

        function renderRoute(route) {
            if (route === 'top' || route === '') {
                goHomeDirect();
            } else if (categoryData[route]) {
                openSubMenuDirect(route);
            } else if (route.includes('_lvl') && route.includes('_stg')) {
                const parts = route.split('_');
                const stgIndex = parts.indexOf('stg');
                const stageNum = parseInt(parts[stgIndex + 1]);
                const lvlIndex = parts.indexOf('lvl');
                const level = parseInt(parts[lvlIndex + 1]);
                const taskId = parts.slice(0, lvlIndex).join('_');
                startSpecificGameDirect(taskId, level, stageNum);
            } else if (route.includes('_lvl')) {
                const parts = route.split('_lvl');
                const taskId = parts[0];
                const level = parseInt(parts[1]);
                openStageSelectDirect(taskId, level);
            } else {
                goHomeDirect();
            }
        }

        function goHomeDirect() {
            currentCategory = null;
            currentSubTask = null;
            stage.innerHTML = topMenuHTML;
            document.getElementById('header-title').innerHTML = `💡 <ruby>トレーニング<rt>ちょうせん</rt></ruby>を選ぶ`;
            updateUserIdDisplay();
        }

        document.getElementById('btn-home').addEventListener('click', () => navigateTo('top'));
        document.getElementById('btn-back').addEventListener('click', () => {
            if (currentSubTask) navigateTo(currentCategory);
            else navigateTo('top');
        });

        function openSubMenuDirect(catKey) {
            currentCategory = catKey;
            currentSubTask = null;
            const cat = categoryData[catKey];

            let cardsHTML = cat.sub.map(sub => `
                <div class="sub-card">
                    <div class="sub-card-title">
                        ${sub.ruby ? `<ruby>${sub.title}<rt>${sub.ruby}</rt></ruby>` : sub.title}
                    </div>
                    <div class="sub-card-preview">${getPreviewGraphic(sub.id)}</div>
                    <div class="level-select-group">
                        <div class="level-label">レベル</div>
                        <div class="star-btns">
                            <button class="star-btn" onclick="navigateTo('${sub.id}_lvl1')"><span class="stars">★</span></button>
                            <button class="star-btn" onclick="navigateTo('${sub.id}_lvl2')"><span class="stars">★★</span></button>
                            <button class="star-btn" onclick="navigateTo('${sub.id}_lvl3')"><span class="stars">★★★</span></button>
                        </div>
                    </div>
                </div>
            `).join('');

            stage.innerHTML = `
                <div class="window-panel">
                    <div class="panel-header" style="background-color: ${cat.color};">${cat.title}</div>
                    <div class="panel-body">
                        <div class="sub-card-container">${cardsHTML}</div>
                        <button class="home-back-btn" onclick="navigateTo('top')">🏠 ホーム</button>
                    </div>
                </div>
            `;
        }

        function getPreviewGraphic(id) {
            switch(id) {
                case 'what_was': return '<span style="font-size:40px;">📐 ◯ 🔲</span>';
                case 'where_what': return '<span style="font-size:32px;">田 (7, 2, り)</span>';
                case 'dot_where': return '<span style="font-size:36px;">⁙ ● ⁙</span>';
                case 'first_pon': return '<span style="font-size:36px;">🔘 ⚪ ⚪ [ポン]</span>';
                case 'last_pon': return '<span style="font-size:36px;">⚪ ⚪ 🔘 [ポン]</span>';
                case 'what_order': return '<span style="font-size:36px;">🐱 🐶 🐖</span>';
                case 'symbol_find': return '<span style="font-size:36px;">🍎 ⭐ ⭕ 🐒</span>';
                case 'add_find': return '<span style="font-size:28px; font-weight:bold; color:#d9534f;">7 + 3 = 10</span>';
                case 'add_challenge': return '<button style="padding:6px 12px; background:#f77d67; color:#fff; border-radius:10px; border:none; font-weight:bold;">⏱️ 60秒</button>';
                case 'dot_connect': return '<span style="font-size:36px;">▫️➡️▫️ (描画)</span>';
                case 'shape_find': return '<span style="font-size:36px;">✨ 🔲 ✨</span>';
                case 'ranking': return '<span style="font-size:36px;">🥇 🥈 🥉</span>';
                case 'stamp': return '<span style="font-size:36px;">💮 🍒</span>';
                default: return '🧩';
            }
        }

        function openStageSelectDirect(taskId, level) {
            currentSubTask = taskId;
            currentLevel = level;
            const stars = '★'.repeat(level);
            let stageCardsHTML = '';
            const userProgress = getProgressData();

            for (let i = 1; i <= 10; i++) {
                const colorClass = `stage-c${((i - 1) % 5) + 1}`;
                const key = `${taskId}_lvl${level}_stg${i}`;
                const isDone = userProgress[key];

                stageCardsHTML += `
                    <div class="stage-num-card ${colorClass}" onclick="navigateTo('${taskId}_lvl${level}_stg${i}')">
                        ${isDone ? '<div class="hanamaru-mark">💮</div>' : ''}
                        <span>${i}</span>
                        ${isDone ? '<div class="check-mark">✓</div>' : ''}
                    </div>
                `;
            }

            stage.innerHTML = `
                <div class="window-panel">
                    <div class="panel-header" style="background-color: var(--yellow-category);">
                        🔍 ${taskId} <span style="color:#ff5252; margin-left:6px;">${stars}</span>
                        <button class="close-header-btn" onclick="navigateTo('${currentCategory || 'top'}')">✖ とじる</button>
                    </div>
                    <div class="panel-body">
                        <div class="stage-num-grid">${stageCardsHTML}</div>
                        <button class="home-back-btn" onclick="navigateTo('${currentCategory || 'top'}')">✖ とじる</button>
                    </div>
                </div>
            `;
        }

        let currentQuestionIndex = 0; // 各ステージ内での問題カウント（5問連続）

        function startSpecificGameDirect(taskId, level, stageNum) {
            currentSubTask = taskId;
            currentLevel = level;
            currentQuestionIndex = 0;
            runSubQuestion(taskId, level, stageNum);
        }

        // 各ステージ内の5問連続処理の制御ルーチン
        function runSubQuestion(taskId, level, stageNum) {
            if (currentQuestionIndex >= 5) {
                markGameCleared(taskId, level, stageNum);
                return;
            }

            if (taskId === 'what_was') renderWhatWasGame(level, stageNum);
            else if (taskId === 'where_what') renderWhereWhatGame(level, stageNum);
            else if (taskId === 'dot_where') renderDotWhereGame(level, stageNum);
            else if (taskId === 'first_pon' || taskId === 'last_pon') renderPonGame(taskId, level, stageNum);
            else if (taskId === 'what_order') renderWhatOrderGame(level, stageNum);
            else if (taskId === 'symbol_find') renderSymbolFindGame(level, stageNum);
            else if (taskId === 'add_find' || taskId === 'add_challenge') renderAddFindGame(taskId, level, stageNum);
            else if (taskId === 'dot_connect') renderDotConnectGame(level, stageNum);
            else if (taskId === 'shape_find') renderShapeFindGame(level, stageNum);
            else if (taskId === 'ranking') renderRankingGame(level, stageNum);
            else if (taskId === 'stamp') renderStampGame(level, stageNum);
        }

        function advanceQuestion(taskId, level, stageNum) {
            playSound('correct');
            currentQuestionIndex++;
            if (currentQuestionIndex < 5) {
                runSubQuestion(taskId, level, stageNum);
            } else {
                markGameCleared(taskId, level, stageNum);
            }
        }

        function markGameCleared(taskId, level, stageNum) {
            saveProgress(`${taskId}_lvl${level}_stg${stageNum}`);
            playSound('correct');
            alert(`🎉 ステージ ${stageNum} (全5問) クリア！おめでとう！`);
            navigateTo(`${taskId}_lvl${level}`);
        }

        // ================= 各問題（5問ループ対応） =================

        // 1. 何があった？
        function renderWhatWasGame(level, stageNum) {
            const allItems = ['🍎', '⭐', '🚗', '🐱', '🍌', '🎁', '🔔', '⚽', '💎', '🚀'];
            const targetCount = level + 2;
            const chosen = [...allItems].sort(() => Math.random() - 0.5).slice(0, targetCount);

            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text" id="mem-title">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】3秒間で図形を覚えてね！</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="game-canvas-area" id="mem-display">
                        <div style="font-size:60px; display:flex; gap:20px;">
                            ${chosen.join(' ')}
                        </div>
                    </div>
                </div>
            `;

            setTimeout(() => {
                const titleEl = document.getElementById('mem-title');
                if (!titleEl) return;
                titleEl.innerText = `【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】何がありましたか？すべて選ぼう！`;
                const shuffled = [...allItems].sort(() => Math.random() - 0.5);
                let selected = [];

                document.getElementById('mem-display').innerHTML = `
                    <div style="display:flex; flex-direction:column; align-items:center; gap:20px;">
                        <div style="display:flex; gap:16px; flex-wrap:wrap; justify-content:center; max-width:500px;">
                            ${shuffled.map(item => `
                                <button class="star-btn" style="font-size:36px; padding:12px 18px;" onclick="toggleMemoryChoice('${item}', this)">${item}</button>
                            `).join('')}
                        </div>
                        <button class="action-btn" onclick="checkWhatWasAnswer()">答え合わせ</button>
                    </div>
                `;

                window.toggleMemoryChoice = function(item, btn) {
                    playSound('pop');
                    if (selected.includes(item)) {
                        selected = selected.filter(i => i !== item);
                        btn.style.background = '#fff';
                    } else {
                        selected.push(item);
                        btn.style.background = '#ffd166';
                    }
                };

                window.checkWhatWasAnswer = function() {
                    const isCorrect = chosen.length === selected.length && chosen.every(i => selected.includes(i));
                    if (isCorrect) advanceQuestion('what_was', level, stageNum);
                    else { playSound('wrong'); alert('惜しい！もう一度チャレンジしてみよう。'); }
                };
            }, 3000);
        }

        // 2. どこに何があった？
        function renderWhereWhatGame(level, stageNum) {
            const items = ['7', 'り', 'ま', '2', 'き', 'ね', 'A', '★', '🍎'];
            const target = items[Math.floor(Math.random() * items.length)];
            const targetRow = Math.floor(Math.random() * 3);
            const targetCol = Math.floor(Math.random() * 3);

            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text" id="where-title">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】「${target}」の位置を覚えてね！</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="game-canvas-area" id="where-display">
                        <div class="grid-matrix" style="grid-template-columns: repeat(3, 1fr);">
                            ${[0,1,2].map(r => [0,1,2].map(c => `
                                <div class="grid-cell">${(r === targetRow && c === targetCol) ? target : ''}</div>
                            `).join('')).join('')}
                        </div>
                    </div>
                </div>
            `;

            setTimeout(() => {
                const titleEl = document.getElementById('where-title');
                if (!titleEl) return;
                titleEl.innerText = `【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】「${target}」があった場所をタッチしよう！`;

                document.getElementById('where-display').innerHTML = `
                    <div class="grid-matrix" style="grid-template-columns: repeat(3, 1fr);">
                        ${[0,1,2].map(r => [0,1,2].map(c => `
                            <div class="grid-cell" onclick="checkWhereWhatAnswer(${r}, ${c}, ${targetRow}, ${targetCol})"></div>
                        `).join('')).join('')}
                    </div>
                `;

                window.checkWhereWhatAnswer = function(r, c, tr, tc) {
                    if (r === tr && c === tc) advanceQuestion('where_what', level, stageNum);
                    else { playSound('wrong'); alert('ちがう場所だよ！'); }
                };
            }, 2500);
        }

        // 3. ●はどこ？
        function renderDotWhereGame(level, stageNum) {
            const dotCount = level + 1;
            const matrixSize = 4;
            let dotPositions = [];
            while (dotPositions.length < dotCount) {
                const pos = Math.floor(Math.random() * (matrixSize * matrixSize));
                if (!dotPositions.includes(pos)) dotPositions.push(pos);
            }

            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text" id="dot-title">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】●の位置を覚えてね！</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="game-canvas-area" id="dot-display">
                        <div class="grid-matrix" style="grid-template-columns: repeat(${matrixSize}, 1fr);">
                            ${Array.from({length: matrixSize * matrixSize}).map((_, idx) => `
                                <div class="grid-cell ${dotPositions.includes(idx) ? 'active-dot' : ''}"></div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;

            setTimeout(() => {
                const titleEl = document.getElementById('dot-title');
                if (!titleEl) return;
                titleEl.innerText = `【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】●があった場所を ${dotCount} 箇所タッチしよう！`;
                let userSelected = [];

                document.getElementById('dot-display').innerHTML = `
                    <div style="display:flex; flex-direction:column; align-items:center; gap:16px;">
                        <div class="grid-matrix" style="grid-template-columns: repeat(${matrixSize}, 1fr);">
                            ${Array.from({length: matrixSize * matrixSize}).map((_, idx) => `
                                <div class="grid-cell" id="dot-cell-${idx}" onclick="toggleDotSelect(${idx})"></div>
                            `).join('')}
                        </div>
                        <button class="action-btn" onclick="checkDotWhereAnswer()">決定</button>
                    </div>
                `;

                window.toggleDotSelect = function(idx) {
                    playSound('pop');
                    const cell = document.getElementById(`dot-cell-${idx}`);
                    if (userSelected.includes(idx)) {
                        userSelected = userSelected.filter(i => i !== idx);
                        cell.classList.remove('selected');
                    } else {
                        userSelected.push(idx);
                        cell.classList.add('selected');
                    }
                };

                window.checkDotWhereAnswer = function() {
                    const isCorrect = dotPositions.length === userSelected.length && dotPositions.every(i => userSelected.includes(i));
                    if (isCorrect) advanceQuestion('dot_where', level, stageNum);
                    else { playSound('wrong'); alert('位置がちがうよ！'); }
                };
            }, 2500);
        }

        // 4. 最初とポン / 最後とポン
        function renderPonGame(taskId, level, stageNum) {
            const isFirst = taskId === 'first_pon';
            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】${isFirst ? '最初の音が鳴ったら「ポン」を押そう！' : '最後の音が鳴ったら「ポン」を押そう！'}</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="game-canvas-area" style="flex-direction:column; gap:30px;">
                        <button class="action-btn" style="background:#5bc0de;" onclick="startAudioSequence()">🔊 音を聴く</button>
                        <button class="cat-btn orange" style="width:160px; height:160px; border-radius:50%; border-width:6px;" onclick="handlePonClick()">
                            <span style="font-size:32px; font-weight:900;">ポン！</span>
                        </button>
                    </div>
                </div>
            `;

            let startTime = 0;
            window.startAudioSequence = function() {
                speakText('さん、に、いち');
                setTimeout(() => {
                    playSound('pop');
                    startTime = Date.now();
                }, 2200);
            };

            window.handlePonClick = function() {
                if (!startTime) return alert('まず音を再生してください');
                const diff = Date.now() - startTime;
                if (diff < 2500) advanceQuestion(taskId, level, stageNum);
                else { playSound('wrong'); alert('タイミングが合わなかったよ！もう一度！'); }
            };
        }

        // 5. 何が何番？
        function renderWhatOrderGame(level, stageNum) {
            const animals = ['🐱 ネコ', '🐶 イヌ', '🐖 ブタ', '🐰 ウサギ', '🐵 サル'];
            const chosen = [...animals].sort(() => Math.random() - 0.5).slice(0, 3);

            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text" id="order-title">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】音声を聞いてね！</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="game-canvas-area" style="flex-direction:column; gap:20px;">
                        <button class="action-btn" style="background:#5bc0de;" onclick="playOrderAudio()">🔊 音声をもう一度聴く</button>
                        <div id="order-options" style="display:flex; gap:16px; margin-top:20px;"></div>
                    </div>
                </div>
            `;

            window.playOrderAudio = function() {
                speakText(`１番は ${chosen[0]}、２番は ${chosen[1]}、３番は ${chosen[2]}`);
            };

            playOrderAudio();

            setTimeout(() => {
                document.getElementById('order-title').innerText = `【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】２番目の動物はどれでしたか？`;
                const shuffled = [...chosen].sort(() => Math.random() - 0.5);

                document.getElementById('order-options').innerHTML = shuffled.map(item => `
                    <button class="action-btn" onclick="checkWhatOrderAnswer('${item}', '${chosen[1]}')">${item}</button>
                `).join('');

                window.checkWhatOrderAnswer = function(selected, target) {
                    if (selected === target) advanceQuestion('what_order', level, stageNum);
                    else { playSound('wrong'); alert('ちがう動物だよ！'); }
                };
            }, 2000);
        }

        // 6. 記号さがし
        function renderSymbolFindGame(level, stageNum) {
            const symbols = ['🍎', '⭐', '🍌', '🚗', '🐱', '⚽', '💎'];
            const target = symbols[Math.floor(Math.random() * symbols.length)];
            const totalCount = 2 + level;

            let list = [];
            for (let i = 0; i < totalCount; i++) list.push(target);
            while (list.length < 18) {
                const randomSym = symbols[Math.floor(Math.random() * symbols.length)];
                if (randomSym !== target) list.push(randomSym);
            }
            list.sort(() => Math.random() - 0.5);

            let found = 0;

            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】「${target}」を全部見つけよう！ (残り ${totalCount - found} 個)</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="symbol-grid" style="grid-template-columns: repeat(6, 1fr); width: 100%; height: 80%;">
                        ${list.map((item, idx) => `
                            <div class="symbol-item" id="item-${idx}" onclick="checkSymbol('${item}', '${target}', 'item-${idx}', ${totalCount}, ${stageNum})">${item}</div>
                        `).join('')}
                    </div>
                </div>
            `;

            window.checkSymbol = function(selected, targetSym, elementId, totalTarget, stg) {
                const el = document.getElementById(elementId);
                if (el.style.opacity === '0.3') return;

                if (selected === targetSym) {
                    playSound('correct');
                    el.style.background = '#a8d59d';
                    el.style.opacity = '0.3';
                    found++;
                    document.querySelector('.game-question-text').innerText = `【ステージ ${stg} - 第${currentQuestionIndex + 1}/5問】「${target}」を全部見つけよう！ (残り ${totalTarget - found} 個)`;
                    if (found >= totalTarget) setTimeout(() => advanceQuestion('symbol_find', level, stg), 300);
                } else playSound('wrong');
            };
        }

        // 7. さがし算
        function renderAddFindGame(taskId, level, stageNum) {
            const targetSum = 8 + Math.floor(Math.random() * 10);
            const nums = [1, 2, 3, 4, 5, 6, 7, 8, 9];
            const n1 = nums[Math.floor(Math.random() * (nums.length / 2))];
            const n2 = targetSum - n1;

            const options = [n2, n2 + 1, n2 - 1, n2 + 2].sort(() => Math.random() - 0.5);

            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】足して ${targetSum} になる数を選ぼう！</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="game-canvas-area" style="flex-direction:column; gap:24px;">
                        <div style="font-size:48px; font-weight:bold; color:var(--main-border);">
                            ${n1} + ❓ = ${targetSum}
                        </div>
                        <div style="display:flex; gap:16px;">
                            ${options.map(opt => `
                                <button class="action-btn" style="font-size:28px; min-width:80px;" onclick="checkAddAnswer(${opt}, ${n2})">${opt}</button>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;

            window.checkAddAnswer = function(selected, correct) {
                if (selected === correct) advanceQuestion(taskId, level, stageNum);
                else { playSound('wrong'); alert('計算がちがうよ！'); }
            };
        }

        // 8. 点つなぎ
        function renderDotConnectGame(level, stageNum) {
            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】お手本と同じように点をつなごう！</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="game-canvas-area" style="gap: 20px;">
                        <div>
                            <div style="text-align:center; font-weight:bold; margin-bottom:4px;">お手本</div>
                            <canvas id="canvas-ref" width="220" height="220" style="border:2px solid #333; border-radius:12px; background:#fff;"></canvas>
                        </div>
                        <div>
                            <div style="text-align:center; font-weight:bold; margin-bottom:4px;">あなたの入力</div>
                            <canvas id="canvas-user" class="drawing-board" width="220" height="220"></canvas>
                        </div>
                    </div>
                    <button class="action-btn" style="margin-top:10px;" onclick="advanceQuestion('dot_connect', ${level}, ${stageNum})">できた！</button>
                </div>
            `;

            const refCanvas = document.getElementById('canvas-ref');
            const refCtx = refCanvas.getContext('2d');
            const userCanvas = document.getElementById('canvas-user');
            const userCtx = userCanvas.getContext('2d');

            function drawGrid(ctx) {
                ctx.fillStyle = '#333';
                for (let x = 40; x <= 180; x += 70) {
                    for (let y = 40; y <= 180; y += 70) {
                        ctx.beginPath(); ctx.arc(x, y, 6, 0, Math.PI * 2); ctx.fill();
                    }
                }
            }

            drawGrid(refCtx); drawGrid(userCtx);

            refCtx.strokeStyle = '#e65b46'; refCtx.lineWidth = 4; refCtx.beginPath();
            if (currentQuestionIndex % 2 === 0) {
                refCtx.moveTo(40, 40); refCtx.lineTo(180, 40); refCtx.lineTo(180, 180); refCtx.lineTo(40, 180); refCtx.closePath();
            } else {
                refCtx.moveTo(110, 40); refCtx.lineTo(180, 180); refCtx.lineTo(40, 180); refCtx.closePath();
            }
            refCtx.stroke();

            let isDrawing = false;
            userCtx.strokeStyle = '#2b7bc0'; userCtx.lineWidth = 4;

            userCanvas.addEventListener('mousedown', (e) => {
                isDrawing = true; userCtx.beginPath();
                const rect = userCanvas.getBoundingClientRect();
                userCtx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
            });
            userCanvas.addEventListener('mousemove', (e) => {
                if (!isDrawing) return;
                const rect = userCanvas.getBoundingClientRect();
                userCtx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
                userCtx.stroke();
            });
            window.addEventListener('mouseup', () => isDrawing = false);
        }

        // 9. 形さがし
        function renderShapeFindGame(level, stageNum) {
            const isSquare = (currentQuestionIndex % 2 === 0);
            const targetShape = isSquare ? '正方形' : '三角形';

            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】「${targetShape}」を選ぼう！</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="game-canvas-area" style="gap:24px;">
                        <button class="star-btn" style="font-size:50px; padding:20px;" onclick="checkShapeAnswer(true)">
                            ${isSquare ? '🔲' : '🔺'}
                        </button>
                        <button class="star-btn" style="font-size:50px; padding:20px;" onclick="checkShapeAnswer(false)">
                            ${isSquare ? '⭕' : '⭐'}
                        </button>
                    </div>
                </div>
            `;

            window.checkShapeAnswer = function(isCorrect) {
                if (isCorrect) advanceQuestion('shape_find', level, stageNum);
                else { playSound('wrong'); alert('形がちがうよ！'); }
            };
        }

        // 10. 順位決定戦
        function renderRankingGame(level, stageNum) {
            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】1位の動物はどれ？（イヌはネコより速い）</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="game-canvas-area" style="gap:20px;">
                        <button class="action-btn" onclick="checkRankingAnswer(true)">🐶 イヌ</button>
                        <button class="action-btn" onclick="checkRankingAnswer(false)">🐱 ネコ</button>
                    </div>
                </div>
            `;

            window.checkRankingAnswer = function(isCorrect) {
                if (isCorrect) advanceQuestion('ranking', level, stageNum);
                else { playSound('wrong'); alert('順位をもう一度考えてみよう！'); }
            };
        }

        // 11. スタンプ
        function renderStampGame(level, stageNum) {
            stage.innerHTML = `
                <div class="game-screen">
                    <div class="game-header">
                        <div class="game-question-text">【ステージ ${stageNum} - 第${currentQuestionIndex + 1}/5問】スタンプと同じ形を選ぼう！</div>
                        <button class="action-btn" onclick="navigateTo('${currentSubTask}_lvl${level}')">とじる</button>
                    </div>
                    <div class="game-canvas-area" style="flex-direction:column; gap:24px;">
                        <div style="font-size:40px; border:2px dashed #999; padding:12px; border-radius:12px;">お手本: 💮</div>
                        <div style="display:flex; gap:16px;">
                            <button class="action-btn" style="font-size:32px;" onclick="checkStampAnswer(true)">💮</button>
                            <button class="action-btn" style="font-size:32px;" onclick="checkStampAnswer(false)">🌸</button>
                        </div>
                    </div>
                </div>
            `;

            window.checkStampAnswer = function(isCorrect) {
                if (isCorrect) advanceQuestion('stamp', level, stageNum);
                else { playSound('wrong'); alert('形がちがうよ！'); }
            };
        }

        function openMissionModal() { playSound('pop'); document.getElementById('mission-modal').classList.add('active'); }
        document.getElementById('btn-notebook').addEventListener('click', () => {
            playSound('pop'); updateUserIdDisplay(); document.getElementById('notebook-modal').classList.add('active');
        });
        function closeModal(id) { playSound('pop'); document.getElementById(id).classList.remove('active'); }

        updateUserIdDisplay();
    </script>
</body>
</html>"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # 各URLパス（例: localhost:3030/top）に対応
    return render_template_string(HTML_CONTENT)

if __name__ == '__main__':
    # Discloud環境のPORT変数またはデフォルト3030で起動
    port = int(os.environ.get('PORT', 3030))
    app.run(host='0.0.0.0', port=port)
