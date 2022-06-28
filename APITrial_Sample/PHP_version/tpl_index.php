<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <form action="index.php" method="post" enctype="multipart/form-data">
    ファイル:
    <input type="file" name="upfile" size="30" /><br />
    <br />
    <input type="submit" name="submit" value="アップロード" />
  </form>
  <?php if(!empty($result)): ?>
    <h1><?php echo round($result[0]['results'] * 100); ?>%の確率で<?php echo $result[0]['labels']; ?>やんけ！<h1>  
  <?php endif; ?>
  <?php  if(!empty($exif)): ?><p>撮影日(アップロード時間)は<?php echo date("Y/m/d H:i:s" , $exif['FileDateTime']) ?></p><?php endif; ?>
  <?php if(!empty($error)) var_dump($error) ?>
</body>
</html>