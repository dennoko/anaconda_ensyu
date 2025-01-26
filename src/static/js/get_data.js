window.onload = function() {
    fetch('../static/js/guitars.json')  // JSONファイルのパス
        .then(response => response.json())  // JSONをパース
        .then(jsonData => {
            const outputDiv = document.getElementById('output');
            jsonData.forEach(guitar => {
                // ギター情報をHTMLに出力
                const guitarInfo = `
                    <div class="guitar">
                        <div class="guitar-info">
                            <h2>${guitar["ギター名"]}</h2>
                            <h2>${guitar["メーカー"]}</h2>
                            <h2>(${guitar["メーカーの国"]})</h2>
                        </div>
                        <div class="guitar-details">
                            <h3>音のバランスの評価</h3>
                            <p>${guitar["音のバランスの評価"]}</p>
                        </div>
                        <div class="guitar-details">
                            <h3>サステインの評価</h3>
                            <p>${guitar["サステインの評価"]}</p>
                        </div>
                        <div class="guitar-details">
                            <h3>レスポンスの評価</h3>
                            <p>${guitar["レスポンスの評価"]}</p>
                        </div>
                        <div class="guitar-details">
                            <h3>倍音の評価</h3>
                            <p>${guitar["倍音の評価"]}</p>
                        </div>
                        <div class="guitar-details">
                            <h3>トーンの評価</h3>
                            <p>${guitar["トーンの評価"]}</p>
                        </div>
                        <div class="guitar-details">
                            <h3>総合評価</h3>
                            <p>${guitar["総合評価"]}</p>
                        </div>
                    </div>
                `;
                outputDiv.innerHTML += guitarInfo;
            });
        })
        .catch(error => {
            console.error('JSON読み込みエラー:', error);
        });
};