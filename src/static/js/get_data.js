// JSONデータを非同期に読み込む処理
window.onload = function() {
    fetch('../static/js/guitars.json')
        .then(response => response.json()) // JSONをパース
        .then(jsonData => {
            const outputDiv = document.getElementById('output');
            jsonData.forEach(guitar => {
                // ギター情報をHTMLに出力
                const guitarInfo = `
                    <div>
                        <h2>${guitar.種類} - ${guitar.ブランド} ${guitar.モデル}</h2>
                        <p><strong>特徴:</strong></p>
                        <ul>
                            ${guitar.特徴.map(feature => `<li>${feature}</li>`).join('')}
                        </ul>
                    </div>
                `;
                outputDiv.innerHTML += guitarInfo;
            });
        })
        .catch(error => {
            console.error('JSON読み込みエラー:', error);
        });
};