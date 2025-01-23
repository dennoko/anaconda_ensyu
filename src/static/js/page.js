// DOMContentLoaded イベントを使って、ページが読み込まれた後に実行する
document.addEventListener('DOMContentLoaded', async () => {
  try {
      // ヘッダーとフッター，画像の内容を読み込み、挿入 (flaskなら)
      const headerResponse = await fetch("/static/component/header.html");
      // ローカルならパスはこっち
      // const headerResponse = await fetch("/src/static/component/header.html");
    
      const headerHTML = await headerResponse.text();
      document.getElementById('header').innerHTML = headerHTML;

      // const footerResponse = await fetch('./footer.html');
      // const footerHTML = await footerResponse.text();
      // document.getElementById('footer').innerHTML = footerHTML;

      // flask
      const imageResponse = await fetch('/static/component/guitarImage.html');
      // ローカル
      // const imageResponse = await fetch('/src/static/component/guitarImage.html');
      const imageHTML = await imageResponse.text();
      document.getElementById('guitarImage').innerHTML = imageHTML;
      // 現在のページのパスを取得
      const currentPath = window.location.pathname;
      const guitarImageContentDiv = document.getElementById('pageContent');
  } catch (error) {
      console.error('Error loading common parts:', error);
  }
});