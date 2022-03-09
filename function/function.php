<?php

//アップロードされたファイル名の拡張子が許可されているか確認
function check_ext($filename){
  //許可する拡張子
	$cfg['ALLOW_EXTS'] = array('jpg', 'jpeg', 'png' , 'gif' , 'JPG' , 'JPEG' , 'PNG' , 'GIF');
	$ext = strtolower(pathinfo($filename, PATHINFO_EXTENSION));
	return in_array($ext, $cfg['ALLOW_EXTS']);
}

?>