const dropArea = document.getElementById('drop_area');

function createFormData(files) {
    const formData = new FormData();
    Array.from(files).forEach((file) => {
        formData.append('files[]', file); // サーバー側が期待するキー名を使用
    });
    return formData;
}
function fileUpload(formData) {
    fetch('/uploads', {
        method: 'POST',
        body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('アップロード成功:', data);
    })
    .catch((error) => {
        console.error('アップロード失敗:', error);
    });
}
// ドラッグした状態で要素内に入ったとき
dropArea.addEventListener('dragover', function(e) {
    // デフォルトの動作を止めて、要素のスタイルを変える
    e.stopPropagation();
    e.preventDefault();
    dropArea.style.background = '#cccccc';
});

// ドラッグした状態で要素から出たとき
dropArea.addEventListener('dragleave', function(e) {
    // 要素のスタイルを元に戻す
    dropArea.style.background = '#ffffff';
});

// ファイルが要素内でドロップされたとき
dropArea.addEventListener('drop', function(e) {
    // デフォルトの動作を止めて、要素のスタイルを元に戻す
    e.preventDefault();
    dropArea.style.background = '#ffffff';
    // dataTrasnferプロパティからドロップされたファイルのFileListオブジェクトが取得できる
    const files = e.dataTransfer.files;
    // 前述の関数を使ってFormDataの作成およびAjax送信
    const formData = createFormData(files);
    fileUpload(formData);
});
dropArea.addEventListener('drop', function(e) {
    // デフォルトの動作を無効化
    e.preventDefault();
    dropArea.style.background = '#ffffff';

    // ドロップされたファイルを取得
    const files = e.dataTransfer.files;

    // FormData オブジェクトを作成
    const formData = new FormData();
    Array.from(files).forEach((file) => {
        formData.append('files[]', file);
    });

    // アップロード処理を呼び出す
    fileUpload(formData);
});
// JavaScriptのドラッグ＆ドロップ実装
// const dropArea = document.getElementById('drop_area');
const fileList = document.getElementById('file_list');

dropArea.addEventListener('drop', (event) => {
    event.preventDefault(); // デフォルトの動作を無効化
    dropArea.classList.remove('hover');
  
    // ドロップされたファイルを取得
    const files = event.dataTransfer.files;
  
    // ファイル名をリストに表示
    // fileList.innerHTML = '<h3>ファイル一覧:</h3>';
    Array.from(files).forEach((file) => {
        const listItem = document.createElement('div');
        listItem.textContent = file.name;
        fileList.appendChild(listItem);
    });
    fetch('/upload', {
      method: 'POST',
      body: formData,
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('アップロード成功:', data);
    })
    .catch((error) => {
        console.error('アップロード失敗:', error);
    });
});