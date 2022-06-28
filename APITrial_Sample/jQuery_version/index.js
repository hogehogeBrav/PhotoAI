$(function(){
  $("#upload_file").on('change', function () {　//画像情報が入って(changeしたら)きたら
    $('h1').empty();
    var fd = new FormData();  //画像データ送信に必要なFromDataインスタンス作成
    fd.append('image', $(this).prop('files')[0]); //取得した画像データを追加

    $.ajax({
      headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content'),
      },
      url: 'http://127.0.0.1:8081/predict',
      type: 'POST',
      data: fd,
      processData: false,
      contentType: false, 
      dataType: 'text'
    })
      .done(function (data) {
        result = JSON.parse(data);
        console.log(result[0])
        $('h1').append(Math.round(result[0].results * 100) + '％の確率で' + result[0].labels + 'やんけ！');
      })
      .fail(function (data) {
        alert('通信に失敗しました');
      })
  });
});